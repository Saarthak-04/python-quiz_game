import streamlit as st
from quiz import get_questions

st.set_page_config(page_title="Quiz Game", page_icon="🎯", layout="centered")

st.title("🎯 Quiz Game")
st.write("Welcome to the Quiz Game! Test your knowledge and have fun!")

if st.button("Start Quiz"):
    try:
        question = get_questions()
        st.session_state.questions = question
        st.session_state.started = True
        st.success("Quiz started! Good luck!")
    except Exception as e:
        st.error(f"Unable to fetch questions. {e}")

if st.session_state.get("started", False):

    if "index" not in st.session_state:
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.finished = False

    if not st.session_state.get("finished", False):

        q = st.session_state.questions[st.session_state.index]

        st.subheader(f"Question {st.session_state.index + 1} of {len(st.session_state.questions)}")
        progress = (st.session_state.index + 1) / len(st.session_state.questions)
        st.progress(progress)

        st.metric("Current Score", st.session_state.score)

        st.write(q["question"])

        answer = st.radio(
            "Choose your answer:",
            q["options"],
            key=f"answer_{st.session_state.index}"
        )

        if st.button("Submit Answer"):
            if answer == q["answer"]:
                st.session_state.score += 1
                st.success("Correct answer! 🎉")
            else:
                st.error(f"Incorrect! The correct answer is: {q['answer']}")

            st.session_state.index += 1

            if st.session_state.index >= len(st.session_state.questions):
                st.session_state.finished = True

            st.rerun()

    else:
        total = len(st.session_state.questions)
        score = st.session_state.score
        percentage = (score / total) * 100

        st.title("🏆 Quiz Completed!")

        col1, col2 = st.columns(2)

        col1.metric("Final Score", f"{score}/{total}")
        col2.metric("Percentage", f"{percentage:.1f}%")

        if percentage >= 80:
            st.success("Excellent work! 🌟")
        elif percentage >= 60:
            st.info("Good job! Keep practicing. 👍")
        elif percentage >= 40:
            st.warning("Not bad! A little more practice will help. 💪")
        else:
            st.error("Keep learning. You'll improve with practice! 📚")

        if st.button("Play Again"):
            for key in ["started", "questions", "index", "score", "finished"]:
                st.session_state.pop(key, None)
            st.rerun()