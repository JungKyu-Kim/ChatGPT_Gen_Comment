import streamlit as st
import time
import openai

openai.api_key = st.secrets["api_key"]
system_content = st.secrets["system_content"]
user_prompt1 = st.secrets["user_prompt1"]
user_prompt2 = st.secrets["user_prompt2"]
user_prompt3 = st.secrets["user_prompt3"]
user_prompt4 = st.secrets["user_prompt4"]

st.set_page_config(layout="wide")

st.write(user_prompt1)
st.write(user_prompt2)
st.write(user_prompt3)
st.write(user_prompt4)

init_name = '홍길동'
init_fact_gathering = """
-산학 협력 과제 3건 달성
 + 반도체 수요예측 과제
 + 물류 최저화 과제
 + Vision 품질 검사 모델 개발 과제
-기술 내재화 1건 : Vision 품질 검사 모델 특허 출원
-서울대학교 교수진 및 사내 과제를 매칭하고 과제를 추진하는 전체 과정을 리드하였음
-3개 과제를 선정하여 산학협력을 추진하였음
-Vision 품질 검사 모델은 특허 출원하여 사내 AI 역량을 내재화 하였음"""

# feedback grade 셋팅값
grade_set = {
    'Highly Exceeds' : 5,
    'Exceeds' : 4,
    'Meets' : 3,
    'Marginally Meets' : 2,
    'Does not Meet' : 1
}
grade_list = list(grade_set.keys())  

# Temperature 셋팅값
temperature_set = {
    '일관적' : 0,
    '보통' : 1,
    '창의적' : 2
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
if 'inp' not in st.session_state:
    st.session_state.inp = []

class Input():
    name = None
    fact_gathering = None
    grade = None
    temperature = None
    length = None
    model = None

    def set_result(self, input_name, input_fact_gathering, input_grade, input_temperature, input_length, input_model):
        self.name = input_name
        self.fact_gathering = input_fact_gathering
        self.grade = input_grade
        self.temperature = input_temperature
        self.length = input_length
        self.model = input_model

def add_input():
    input_name = st.session_state.input_name
    input_fact_gathering = st.session_state.input_fact_gathering
    input_grade_text = st.session_state.input_grade_text
    input_grade = grade_set[input_grade_text]
    input_temperature_text = st.session_state.input_temperature_text
    input_temperature = temperature_set[input_temperature_text]
    input_length = st.session_state.input_length
    input_model = st.session_state.input_model

    ##################
    sys_prompt = system_content + input_name
    u_prompt = user_prompt1 + input_name + user_prompt2 + input_length + user_prompt3 + input_name + user_prompt4 + input_fact_gathering
    ##################

    # gpt_prompt = [{
    #     "role": "system",
    #     "content": sys_prompt
    # }, {
    #     "role": "user",
    #     "content": USER_CONTENT
    # }]

    # with st.spinner("Waiting for ChatGPT..."):
    #     gpt_response = openai.ChatCompletion.create(
    #         # model used here is ChatGPT
    #         # You can use all these models for this endpoint:
    #         # gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314,
    #         # gpt-3.5-turbo, gpt-3.5-turbo-0301
    #         model=input_model,
    #         messages=gpt_prompt,
    #         temperature=input_temperature,
    #         max_tokens=3000,
    #         top_p=1,
    #     )

    i = Input()
    i.set_result(input_name, input_fact_gathering, input_grade, input_temperature, input_length, input_model)

    inp = st.session_state.inp
    inp.append(i)
    st.session_state.inp = inp

def draw_result(input_name, input_fact_gathering, input_grade, input_temperature, input_length, input_model):
    st.write('---------------')
    st.write('이름 :', input_name)
    st.write('Fact Gathering :', input_fact_gathering)
    st.write('피드백 등급 :', input_grade)
    st.write('피드백 다양성 :', input_temperature)
    st.write('글자수 :', input_length)
    st.write('GPT모델 :', input_model)

# st.session_state.inp
# st.write(len(st.session_state.inp))

st.title("Peoply 📝FeedbackGPT🤖")
st.text("피평가자에 대한 MBO 내용을 입력하면, ChatGPT가 MBO 피드백을 생성합니다.")

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

        # fact_gathering text area
        st.text_area(
            "Fact Gathering",
            init_fact_gathering,
            height=280,
            key='input_fact_gathering'
            )

        # feedback grade
        st.selectbox(
            '피드백 등급',
            grade_list,
            index=2,
            key='input_grade_text'
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

        st.form_submit_button("Generate", on_click=add_input)

with col2:
    st.subheader("Result")

    # Result
    if(len(st.session_state.inp) > 0):
        for x in range(len(st.session_state.inp)):
            i = st.session_state.inp[x]
            draw_result(i.name, i.fact_gathering, i.grade, i.temperature, i.length, i.model)
