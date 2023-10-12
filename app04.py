import streamlit as st
import time

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

min_length_of_result = 100
init_length_of_result = 300

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
    '일관적' : 0.5,
    '보통' : 1,
    '창의적' : 1.5
}
temperature_list = list(temperature_set.keys())  

if 'inp' not in st.session_state:
    st.session_state.inp = []

class Input():
    name = None
    fact_gathering = None
    grade = None
    temperature = None
    length = None

    def set_result(self, input_name, input_fact_gathering, input_grade, input_temperature, input_length):
        self.name = input_name
        self.fact_gathering = input_fact_gathering
        self.grade = input_grade
        self.temperature = input_temperature
        self.length = input_length

def add_form():
    input_name = st.session_state.input_name
    input_fact_gathering = st.session_state.input_fact_gathering
    input_grade_text = st.session_state.input_grade_text
    input_grade = grade_set[input_grade_text]
    input_temperature_text = st.session_state.input_temperature_text
    input_temperature = temperature_set[input_temperature_text]
    input_length = st.session_state.input_length

    i = Input()
    i.set_result(input_name, input_fact_gathering, input_grade, input_temperature, input_length)

    inp = st.session_state.inp
    inp.append(i)
    st.session_state.inp = inp

def draw_result(input_name, input_fact_gathering, input_grade, input_temperature, input_length):
    st.write('---------------')
    st.write('이름 :', input_name)
    st.write('Fact Gathering :', input_fact_gathering)
    st.write('피드백 등급 :', input_grade)
    st.write('피드백 다양성 :', input_temperature)
    st.write('글자수 :', input_length)

# st.session_state.inp
# st.write(len(st.session_state.inp))

st.title("Peoply FeedbackGPT")
st.text("피평가자에 대한 MBO 내용을 입력하면, ChatGPT가 MBO 피드백을 생성합니다.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input")
    # Form
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
            # value=2,
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

        st.form_submit_button("Generate", on_click=add_form)

with col2:
    st.subheader("Result")

    if(len(st.session_state.inp) > 0):
        for x in range(len(st.session_state.inp)):
            i = st.session_state.inp[x]
            draw_result(i.name, i.fact_gathering, i.grade, i.temperature, i.length)
