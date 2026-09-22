from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Simple hardcoded user for demo purposes
# (In a real app you'd check a database with hashed passwords)
USERS = {
    "rohith": "hackathon123"
}

# Sample test questions - each has correct answer index
QUESTIONS = [
    {
        "question": "What does HTTPS stand for?",
        "options": ["HyperText Transfer Protocol Secure", "High Transfer Text Protocol System", "Home Text Protocol Secure"],
        "answer": 0
    },
    {
        "question": "Which of these is a strong password?",
        "options": ["password123", "Xk9#mQ2$vL", "12345678"],
        "answer": 1
    },
    {
        "question": "What is phishing?",
        "options": ["A type of firewall", "Tricking users into giving sensitive info", "A programming language"],
        "answer": 1
    }
]


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')

    if username in USERS and USERS[username] == password:
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"}), 401


@app.route('/questions', methods=['GET'])
def get_questions():
    # Send questions WITHOUT the answer key, so it can't be cheated by reading network tab
    public_questions = [
        {"question": q["question"], "options": q["options"]} for q in QUESTIONS
    ]
    return jsonify(public_questions)


@app.route('/submit-test', methods=['POST'])
def submit_test():
    data = request.get_json()
    user_answers = data.get('answers', [])

    score = 0
    for i, question in enumerate(QUESTIONS):
        if i < len(user_answers) and user_answers[i] == question["answer"]:
            score += 1

    total = len(QUESTIONS)
    return jsonify({"score": score, "total": total})


if __name__ == '__main__':
    app.run(port=5000, debug=True)