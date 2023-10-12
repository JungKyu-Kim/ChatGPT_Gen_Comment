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


with st.form("my_form"):
    # title and description
    st.title("Peoply FeedbackGPT")
    st.text("Peoply FeedbackGPT 입니다.")

    # Name
    input_name = st.text_input(
        '이름',
        init_name
        )

    # fact_gathering text area
    input_fact_gathering = st.text_area(
        "Fact Gathering",
        init_fact_gathering
        )

    # feedback grade
    input_grade_text = st.selectbox(
        '피드백 등급',
        grade_list,
        index=2
        )
    input_grade = grade_set[input_grade_text]

    # Temperature
    input_temperature_text = st.select_slider(
        '피드백 다양성',
        options=temperature_list
        )
    input_temperature = temperature_set[input_temperature_text]

    # length of result
    input_length = st.number_input(
        '글자수',
        min_value=min_length_of_result,
        value=init_length_of_result,
        format="%d"
        )

    submitted = st.form_submit_button("Submit")

def draw_result():
    st.write('---------------')
    st.write('이름 :', input_name)
    st.write('Fact Gathering :', input_fact_gathering)
    st.write('피드백 등급 :', input_grade)
    st.write('피드백 다양성 :', input_temperature)
    st.write('글자수 :', input_length)

if submitted:
    draw_result()
    with st.spinner('Wait for it...'):
        time.sleep(5)
    st.success('Done!')
