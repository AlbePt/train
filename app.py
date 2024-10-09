import json
import streamlit as st

class TrainingApp:
    def __init__(self, json_file):
        self.json_file = json_file
        self.questions = self.load_questions()
        self.current_question_index = 0
        self.correct_answers = 0
        self.total_questions = len(self.questions)

    def load_questions(self):
        with open(self.json_file, 'r', encoding='utf-8') as file:
            questions = json.load(file)
        return questions

    def start_training(self, selected_topic):
        self.questions = [q for q in self.questions if q['topic'] == selected_topic]
        self.total_questions = len(self.questions)
        self.current_question_index = 0
        self.correct_answers = 0

    def get_current_question(self):
        if self.current_question_index < self.total_questions:
            return self.questions[self.current_question_index]
        else:
            return None

    def submit_answer(self, user_answer):
        correct_answer = self.questions[self.current_question_index]['correct_answer']
        is_correct = user_answer == correct_answer
        if is_correct:
            self.correct_answers += 1
        self.current_question_index += 1
        return correct_answer, is_correct

    def get_results(self):
        return f"Вы ответили правильно на {self.correct_answers} из {self.total_questions} вопросов."

# Streamlit app
st.set_page_config(page_title="Training App", page_icon="📘")
st.title("Тренировка для экзамена")

if 'app_state' not in st.session_state:
    st.session_state.app_state = TrainingApp('questions_85_complete.json')

app = st.session_state.app_state

# Выбор темы
topics = list(set(q['topic'] for q in app.questions))
selected_topic = st.selectbox("Выберите тему для тренировки", topics)

if selected_topic and st.button("Начать тренировку"):
    app.start_training(selected_topic)

question_data = app.get_current_question()
if question_data:
    st.write(f"### Вопрос: {question_data['question']}")
    user_answer = st.radio("Выберите ответ:", question_data['options'], key=f"q_{app.current_question_index}")
    if st.button("Ответить", key=f"submit_{app.current_question_index}"):
        correct_answer, is_correct = app.submit_answer(user_answer)
        if is_correct:
            st.write(f"✅ Правильно! Правильный ответ: {correct_answer}")
        else:
            st.write(f"❌ Неправильно. Правильный ответ: {correct_answer}")
        if app.current_question_index < app.total_questions:
            if  st.button("Следующий вопрос"):
                st.experimental_rerun()()
        else:
            st.write(app.get_results())
else:
    if app.current_question_index >= app.total_questions:
        st.write(app.get_results())
    else:
        st.write("Выберите тему и нажмите 'Начать тренировку', чтобы начать.")