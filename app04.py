import streamlit as st

def draw_ui():
    # title and description
    st.title("Title")
    st.text("description text.")

    # Name
    name = st.text_input(
        '이름',
        '홍길동'
        )

    # fact_gathering text area
    text = st.text_area(
        "Fact Gathering",
        "-산학 협력 과제 3건 달성"
        " + 반도체 수요예측 과제 "
        " + 물류 최저화 과제"
        " + Vision 품질 검사 모델 개발 과제"
        "-기술 내재화 1건 : Vision 품질 검사 모델 특허 출원"
        "-서울대학교 교수진 및 사내 과제를 매칭하고 과제를 추진하는 전체 과정을 리드하였음"
        "-3개 과제를 선정하여 산학협력을 추진하였음"
        "-Vision 품질 검사 모델은 특허 출원하여 사내 AI 역량을 내재화 하였음"
        )

    # feedback grade
    grade = st.selectbox(
        '피드백 등급',
        (
            'Highly Exceeds',
            'Exceeds',
            'Meets',
            'Marginally Meets',
            'Does not Meet'
        ),
        index=2
        )

    # Temperature
    temperature = st.select_slider(
        '피드백 다양성',
        options=['일관적', '보통', '창의적']
        )

    # length of result
    length = st.number_input(
        '글자수',
        min_value=0,
        value=300,
        format="%d"
        )

draw_ui()