import streamlit as st
import time
import openai

openai.api_key = st.secrets["api_key"]

st.set_page_config(layout="wide")

init_name = '홍길동'

# init_fact_gathering = """
# -산학 협력 과제 3건 달성
#  + 반도체 수요예측 과제
#  + 물류 최저화 과제
#  + Vision 품질 검사 모델 개발 과제
# -기술 내재화 1건 : Vision 품질 검사 모델 특허 출원
# -서울대학교 교수진 및 사내 과제를 매칭하고 과제를 추진하는 전체 과정을 리드하였음
# -3개 과제를 선정하여 산학협력을 추진하였음
# -Vision 품질 검사 모델은 특허 출원하여 사내 AI 역량을 내재화 하였음"""

# # feedback grade 셋팅값
# grade_set = {
#     'Highly Exceeds' : 5,
#     'Exceeds' : 4,
#     'Meets' : 3,
#     'Marginally Meets' : 2,
#     'Does not Meet' : 1
# }
# grade_list = list(grade_set.keys())

# overall, biz
eval_set = {
    'EX' : "우수",
    'GD' : "보통",
    'NI' : "저조"
}
eval_list = list(eval_set.keys())

# personal
rating_set = {
    'S' : "매우 우수",
    'A' : "우수",
    'B' : "보통",
    'C' : "저조",
    'D' : "매우 저조"
}
rating_list = list(rating_set.keys())

# Temperature 셋팅값
temperature_set = {
    '일관적' : 0.5,
    '보통' : 1,
    '창의적' : 1.5
}
temperature_list = list(temperature_set.keys())  

# 글자수 셋팅값
min_length_of_result = 100
init_length_of_result = 300

# GPT 모델 셋팅값
model_list = [
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301"
]

# Session History
if 'gen' not in st.session_state:
    st.session_state.gen = []

class Gen_set():
    name = None
    # fact_gathering = None
    # grade = None
    overall_y1 = None
    overall_y2 = None
    overall_y3 = None
    person_y1 = None
    person_y2 = None
    person_y3 = None
    biz_y1 = None
    biz_y2 = None
    biz_y3 = None
    temperature = None
    length = None
    model = None
    output = None

    def set_result(self, input_name,
                    input_overall_y1, input_overall_y2, input_overall_y3,
                    input_person_y1, input_person_y2, input_person_y3,
                    input_biz_y1, input_biz_y2, input_biz_y3,
                    input_temperature, input_length, p_model, p_output):
        
        self.name = input_name
        # self.fact_gathering = input_fact_gathering
        # self.grade = input_grade
        self.overall_y1 = input_overall_y1
        self.overall_y2 = input_overall_y2
        self.overall_y3 = input_overall_y3
        self.person_y1 = input_person_y1
        self.person_y2 = input_person_y2
        self.person_y3 = input_person_y3
        self.biz_y1 = input_biz_y1
        self.biz_y2 = input_biz_y2
        self.biz_y3 = input_biz_y3
        self.temperature = input_temperature
        self.length = input_length
        self.model = p_model
        self.output = p_output

def add_set():
    input_name = st.session_state.input_name
    # input_fact_gathering = st.session_state.input_fact_gathering
    # input_grade_text = st.session_state.input_grade_text
    # input_grade = grade_set[input_grade_text]
    input_overall_y1_text = st.session_state.input_overall_y1
    input_overall_y1 = eval_set[input_overall_y1_text]
    input_overall_y2_text = st.session_state.input_overall_y2
    input_overall_y2 = eval_set[input_overall_y2_text]
    input_overall_y3_text = st.session_state.input_overall_y3
    input_overall_y3 = eval_set[input_overall_y3_text]

    input_person_y1_text = st.session_state.input_person_y1
    input_person_y1 = rating_set[input_person_y1_text]
    input_person_y2_text = st.session_state.input_person_y2
    input_person_y2 = rating_set[input_person_y2_text]
    input_person_y3_text = st.session_state.input_person_y3
    input_person_y3 = rating_set[input_person_y3_text]

    input_biz_y1_text = st.session_state.input_biz_y1
    input_biz_y1 = eval_set[input_biz_y1_text]
    input_biz_y2_text = st.session_state.input_biz_y2
    input_biz_y2 = eval_set[input_biz_y2_text]
    input_biz_y3_text = st.session_state.input_biz_y3
    input_biz_y3 = eval_set[input_biz_y3_text]

    input_temperature_text = st.session_state.input_temperature_text
    input_temperature = temperature_set[input_temperature_text]
    input_length = st.session_state.input_length
    input_model = st.session_state.input_model

    # system_content = f"{input_name}에 대한 요약 리포트를 작성해줘. 작성하는 리포트는 200글자 내로 작성해줘."
    system_content = f"""You are an analyst.
    You should provide a summary of people's profile and evaluate this person.
    Keep the following guidelines in mind as you write.
     - write in the report based on given information.
     - write in korean.
     - write it up to 300 words."""

    # 대학정보
    univ_name = "가천대학교"
    univ_start = "2017"
    univ_end = "2018"
    univ_major = "나노의약생명과학"
    univ_credit = "4.18"
    univ_credit_eval = "준수하게"   # 저조하게/보통으로/준수하게

    # 어학정보
    eng_get = "2016"
    eng_score = "980"
    eng_score_eval = "준수함" # 저조함/보통임/준수함

    # 입사정보
    rec_start = "2019"

    # 평가year
    y1_year = "2022"
    y2_year = "2021"
    y3_year = "2020"

    req_com = f" 아래에 기술하는 {input_name}에 대한 프로필 정보를 2줄로 요약해줘."
    # req_com = f" 아래에 기술되는 {input_name}에 대한 프로필 정보에서 학업은 어땠어?"

    univ_com = f" {univ_name}를 {univ_start}년 입학하여 {univ_end}년 졸업했으며, 전공은 {univ_major} 이며, 학점은 {univ_credit}점으로 {univ_credit_eval} 졸업함."
    lan_com = f" 영어점수인 토익점수는 {eng_get}년 획득했으며, {eng_score}점으로 {eng_score_eval}."
    recruit_com = f" 회사에는 {rec_start}년에 입사하였음."

    overall_com = f" 최근 3년동안 종합평가는 가장 최근인 {y1_year}년은 {input_overall_y1}을 받았고, {y2_year}년은 {input_overall_y2}, {y3_year}년은 {input_overall_y3}을 받았음."
    comp_com = f" 종합평가의 구성요소중 하나인 개인역량은 {y1_year}년은 {input_person_y1}을 받았고, {y2_year}년은 {input_person_y2}, {y3_year}년은 {input_person_y3}을 받았음."
    obj_com = f" 또다른 종합평가의 구성요소인 사업성과는 {y1_year}년은 {input_biz_y1}, {y2_year}년은 {input_biz_y2}, {y3_year}년은 {input_biz_y3}을 받았음."

    ##################
    sys_prompt = system_content
    usr_prompt = req_com + univ_com + lan_com + recruit_com + overall_com + comp_com + obj_com
    # usr_prompt = req_com + overall_com + comp_com + obj_com
    ##################

    gpt_prompt = [{
        "role": "system",
        "content": sys_prompt
    }, {
        "role": "user",
        "content": usr_prompt
    }]

    with st.spinner("Waiting for ChatGPT..."):
        gpt_response = openai.ChatCompletion.create(
            # model used here is ChatGPT
            # You can use all these models for this endpoint:
            # gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314,
            # gpt-3.5-turbo, gpt-3.5-turbo-0301
            model=input_model,
            messages=gpt_prompt,
            temperature=input_temperature,
            max_tokens=3000,
            top_p=1,
            stream=True
        )

    t = st.empty()
    content = ""
    counter = 0
    for completions in gpt_response:
        counter += 1
        if "content" in completions.choices[0].delta:
            content += completions.choices[0].delta.get("content")
        t.markdown(" %s " % content)

    # model = gpt_response.model
    output = content

    g = Gen_set()
    g.set_result(input_name,
                  input_overall_y1, input_overall_y2, input_overall_y3,
                  input_person_y1, input_person_y2, input_person_y3,
                  input_biz_y1, input_biz_y2, input_biz_y3,
                  input_temperature, input_length, input_model, output)

    gen = st.session_state.gen
    gen.append(g)
    st.session_state.gen = gen

def draw_result(set):
    st.write('---------------')
    st.write('이름 :', set.name)
    # st.write('Fact Gathering')
    # st.write(set.fact_gathering)
    # st.write('피드백 등급 값 :', input_grade)
    st.write('2022 종합 :', set.overall_y1)
    st.write('2021 종합 :', set.overall_y2)
    st.write('2020 종합 :', set.overall_y3)
    st.write('2022 개인 :', set.person_y1)
    st.write('2021 개인 :', set.person_y2)
    st.write('2020 개인 :', set.person_y3)
    st.write('2022 사업 :', set.biz_y1)
    st.write('2021 사업 :', set.biz_y2)
    st.write('2020 사업 :', set.biz_y3)
    st.write('피드백 다양성 값 :', set.temperature)
    st.write('글자수 :', set.length)
    st.write('GPT모델 :', set.model)
    st.write('Output')
    st.write(set.output)

st.title("Peoply Insight")
st.text("요약정보 생성")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input")

    # Input Form
    with st.form(key="my_form"):
        # Name
        st.text_input(
            '이름',
            init_name,
            key='input_name'
            )

        # # fact_gathering text area
        # st.text_area(
        #     "Fact Gathering",
        #     init_fact_gathering,
        #     height=280,
        #     key='input_fact_gathering'
        #     )

        # # feedback grade
        # st.selectbox(
        #     '피드백 등급',
        #     grade_list,
        #     index=2,
        #     disabled=True,
        #     key='input_grade_text'
        #     )

        # y1 overall
        st.selectbox(
            '2022 종합',
            eval_list,
            index=1,
            key='input_overall_y1'
            )
        # y2 overall
        st.selectbox(
            '2021 종합',
            eval_list,
            index=0,
            key='input_overall_y2'
            )
        # y3 overall
        st.selectbox(
            '2020 종합',
            eval_list,
            index=2,
            key='input_overall_y3'
            )
        
        # y1 person
        st.selectbox(
            '2022 개인역량',
            rating_list,
            index=0,
            key='input_person_y1'
            )
        # y2 person
        st.selectbox(
            '2021 개인역량',
            rating_list,
            index=1,
            key='input_person_y2'
            )
        # y3 person
        st.selectbox(
            '2020 개인역량',
            rating_list,
            index=4,
            key='input_person_y3'
            )

        # y1 biz
        st.selectbox(
            '2022 사업성과',
            eval_list,
            index=0,
            key='input_biz_y1'
            )
        # y2 biz
        st.selectbox(
            '2021 사업성과',
            eval_list,
            index=2,
            key='input_biz_y2'
            )
        # y3 biz
        st.selectbox(
            '2020 사업성과',
            eval_list,
            index=1,
            key='input_biz_y3'
            )

        # Temperature
        st.select_slider(
            '피드백 다양성',
            options=temperature_list,
            key='input_temperature_text'
            )

        # length of result
        st.number_input(
            '글자수',
            min_value=min_length_of_result,
            value=init_length_of_result,
            format="%d",
            key='input_length'
            )

        # GPT model
        st.selectbox(
            "ChatGPT 모델",
            model_list,
            key='input_model'
        )

        st.form_submit_button("Generate", on_click=add_set)

with col2:
    st.subheader("Result")

    # Result
    if(len(st.session_state.gen) > 0):
        for i in range(len(st.session_state.gen)):
            set = st.session_state.gen[i]
            draw_result(set)
