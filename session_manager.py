# session_manager.py

import json
import os
from datetime import datetime

SESSION_DIR = "sessions"

# Ensure session directory exists
if not os.path.exists(SESSION_DIR):
    os.makedirs(SESSION_DIR)

class SessionManager:
    """
    Manages an interview session:
    - Stores each question, answer, score, and camera feedback
    - Can save session to JSON file
    """

    def __init__(self, role):
        self.role = role
        self.start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.questions = []  # List of dicts: {question, answer, score, camera_feedback}

    def add_question(self, question_text, answer_text, score, camera_feedback):
        """
        Add a answered question to the session
        """
        self.questions.append({
            "question": question_text,
            "answer": answer_text,
            "score": score,
            "camera_feedback": camera_feedback
        })

    def total_score(self):
        """
        Return total session score
        """
        return sum(q["score"] for q in self.questions)

    def save_session(self):
        """
        Save the session as a JSON file with timestamp
        """
        session_data = {
            "role": self.role,
            "start_time": self.start_time,
            "total_score": self.total_score(),
            "questions_answered": len(self.questions),
            "questions": self.questions
        }

        filename = f"{SESSION_DIR}/session_{self.start_time}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=4)

        return filename

    def summary(self):
        """
        Return a summary string of the session
        """
        summary_lines = [f"Role: {self.role}", f"Started: {self.start_time}", f"Total Score: {self.total_score()}", ""]
        for idx, q in enumerate(self.questions, start=1):
            summary_lines.append(f"Q{idx}: {q['question']}")
            summary_lines.append(f"Your Answer: {q['answer']}")
            summary_lines.append(f"Score: {q['score']}, Camera: {q['camera_feedback']}\n")
        return "\n".join(summary_lines)


# -------------------------
# Example usage
# -------------------------
if __name__ == "__main__":
    session = SessionManager(role="Software Developer")
    session.add_question(
        question_text="What is Python?",
        answer_text="Python is a programming language.",
        score=8,
        camera_feedback="Confident"
    )
    session.add_question(
        question_text="Explain OOP concepts.",
        answer_text="OOP is Object-Oriented Programming.",
        score=7,
        camera_feedback="Neutral"
    )
    print(session.summary())
    saved_file = session.save_session()
    print(f"Session saved to: {saved_file}")
