from flask import Flask, render_template, request
import pandas as pd
import random

app = Flask(__name__)

# Загрузка всех вопросов из CSV
df = pd.read_csv("tzi_questions.csv")

@app.route("/", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        answers = request.form
        score = 0
        results = []
        for i in range(50):
            qid = int(answers[f"qid_{i}"])
            user_answer = answers.get(f"q_{i}")
            correct_answer = df.iloc[qid]["Answer"]
            is_correct = user_answer == correct_answer
            if is_correct:
                score += 1
            results.append({
                "question": df.iloc[qid]["Question"],
                "options": [df.iloc[qid][opt] for opt in ['A', 'B', 'C', 'D', 'E']],
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct
            })
        return render_template("quiz.html", results=results, score=score, done=True)

    # GET: создаём 50 случайных вопросов
    selected = df.sample(50).reset_index()
    return render_template("quiz.html", questions=selected.iterrows(), done=False)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
