from flask import Flask, render_template, request
import pandas as pd
import random

app = Flask(__name__)

# Загружаем Excel-файл
df = pd.read_excel("tzi_questions.xlsx")

@app.route("/", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        score = 0
        results = []

        for i in range(50):
            user_answer = request.form.get(f"q_{i}")
            qid = int(request.form.get(f"qid_{i}"))
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
        selected = df.sample(n=50).reset_index()
        return render_template("quiz.html", questions=selected.iterrows(), done=False)

if __name__ == "__main__":
    app.run(debug=True)
