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
        "It was the best of times, it was the worst of times, it was the age of "
        "wisdom, it was the age of foolishness, it was the epoch of belief, it "
        "was the epoch of incredulity, it was the season of Light, it was the "
        "season of Darkness, it was the spring of hope, it was the winter of "
        "despair, (...)"
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