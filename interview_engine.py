import random
from questions import questions

# Mock evaluation for offline AI logic
def evaluate_answer(answer, q_type="definition"):
    answer = answer.strip().lower()
    
    if not answer:
        return {"score": 0, "feedback": "You did not answer the question."}

    # Simple scoring logic
    if q_type == "definition":
        # Check for key words (mock logic)
        keywords = ["object-oriented", "class", "method", "data", "learning", "program"]
        score = min(10, sum([1 for word in keywords if word in answer]))
        feedback = "Good attempt." if score > 5 else "Needs more detail."
    elif q_type == "programming":
        # Check if user typed "def" or basic code keywords
        keywords = ["def", "for", "while", "return", "print"]
        score = min(10, sum([1 for word in keywords if word in answer]))
        feedback = "Code structure looks good." if score > 5 else "Check your code logic."

    return {"score": score, "feedback": feedback}

# Pick a random question
def ask_question(role):
    role_questions = questions.get(role, [])
    if not role_questions:
        return {"question": "No questions available", "type": "definition"}
    
    q = random.choice(role_questions)
    return q["question"], q["type"]
