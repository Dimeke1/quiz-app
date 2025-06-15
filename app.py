from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
import random

app = Flask(__name__)
app.secret_key = "тут_любой_секретный_ключ"

# Загружаем вопросы
df = pd.read_excel("tzi_questions.xlsx")

@app.route("/", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        score = 0
        results = []

        question_ids = session.get("question_ids", [])

        for i, qid in enumerate(question_ids):
            user_answer = request.form.get(f"q_{i}")
            row = df.loc[qid]
            correct_answer = row["Answer"]
            options = {opt: row[opt] for opt in ['A', 'B', 'C', 'D', 'E']}

            is_correct = (user_answer == correct_answer)

            results.append({
                "question": row["Question"],
                "options": [f"{opt}) {text}" for opt, text in options.items()],
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct
            })

            if is_correct:
                score += 1

        return render_template("quiz.html", done=True, score=score, results=results)

    else:
        selected = df.sample(n=50)
        session["question_ids"] = selected.index.tolist()
        selected = selected.reset_index()
        return render_template("quiz.html", questions=selected.iterrows(), done=False)

if __name__ == "__main__":
    app.run(debug=True)
