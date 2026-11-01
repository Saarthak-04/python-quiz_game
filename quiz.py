import requests,html,random

def get_questions():
    url = "https://opentdb.com/api.php?amount=5&type=multiple"

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    questions = []

    for q in data['results']:
        question = html.unescape(q['question'])
        cans = html.unescape(q['correct_answer'])

        options = [
            html.unescape(option)
            for option in q['incorrect_answers']
        ]

        options.append(cans)
        random.shuffle(options)

        questions.append({
            "question": question,
            "answer": cans,
            "options": options
        })

    return questions