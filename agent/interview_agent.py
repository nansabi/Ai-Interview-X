# agent/interview_agent.py

import random
from pathlib import Path
import json

# -------------------------
# Load roles and questions
# -------------------------
def load_roles(file_path="data/roles.json"):
    """Load all roles and their questions from JSON"""
    if not Path(file_path).exists():
        raise FileNotFoundError(f"{file_path} not found.")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["roles"]

# -------------------------
# Interview Agent Class
# -------------------------
class InterviewAgent:
    """
    Handles adaptive question selection for the AI Smart Interview Coach
    Tracks answered questions and scores
    """

    def __init__(self, role_name, max_questions=5):
        self.roles = load_roles()
        if role_name not in self.roles:
            raise ValueError(f"Role '{role_name}' not found in roles.json")

        self.role_name = role_name
        self.all_questions = self.roles[role_name]["questions"]
        self.max_questions = min(max_questions, len(self.all_questions))
        self.answered_questions = []
        self.current_index = 0

        # ✅ NEW (does not affect old logic)
        self.custom_questions = []
        self.use_custom_questions = False

    def get_next_question(self):
        """
        Return the next question text and type.
        Handles both dict-based and string-based questions.
        """

        # ✅ NEW: Use resume-based questions if loaded
        question_pool = (
            self.custom_questions if self.use_custom_questions else self.all_questions
        )

        remaining_questions = [
            q for q in question_pool if q not in self.answered_questions
        ]

        if not remaining_questions or self.current_index >= self.max_questions:
            return None, None  # No more questions

        # Pick a random question
        question_obj = random.choice(remaining_questions)
        self.answered_questions.append(question_obj)
        self.current_index += 1

        # If question is a dict with "question" and "type"
        if isinstance(question_obj, dict):
            q_text = question_obj.get("question", str(question_obj))
            q_type = question_obj.get("type", "definition")
        else:
            q_text = str(question_obj)
            q_type = "definition"

        return q_text, q_type

    def has_more_questions(self):
        """Check if there are more questions left"""
        return self.current_index < self.max_questions

    def reset_session(self):
        """Reset the interview session"""
        self.answered_questions = []
        self.current_index = 0

    def summary(self):
        """Return a summary of the session"""
        return {
            "role": self.role_name,
            "total_questions": self.max_questions,
            "answered_count": self.current_index,
            "answered_questions": self.answered_questions,
        }

    # =====================================================
    # ✅ NEW METHODS (Resume-based interview support)
    # =====================================================
    def load_custom_questions(self, questions):
        """
        Load resume-based questions dynamically.
        This DOES NOT affect role-based logic.
        """
        if not questions:
            return

        self.custom_questions = questions
        self.use_custom_questions = True
        self.max_questions = min(self.max_questions, len(questions))
        self.reset_session()

    def disable_custom_questions(self):
        """Switch back to role-based questions"""
        self.use_custom_questions = False
        self.reset_session()


# -------------------------
# Example usage (for testing)
# -------------------------
if __name__ == "__main__":
    agent = InterviewAgent("Software Developer", max_questions=3)

    print("=== ROLE BASED ===")
    while agent.has_more_questions():
        q, q_type = agent.get_next_question()
        print(f"Q ({q_type}): {q}")

    # Test resume questions
    resume_qs = [
        {"question": "Explain your final year project.", "type": "project"},
        {"question": "What technologies did you use in your internship?", "type": "experience"},
        {"question": "Explain your strongest skill from your resume.", "type": "skill"},
    ]

    agent.load_custom_questions(resume_qs)

    print("\n=== RESUME BASED ===")
    while agent.has_more_questions():
        q, q_type = agent.get_next_question()
        print(f"Q ({q_type}): {q}")
