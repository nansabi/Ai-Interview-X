# questions.py

# Each role has multiple questions
# Each question has a "type": "definition" or "programming"

questions = {
    "Software Developer": [
        {"question": "What is object-oriented programming?", "type": "definition"},
        {"question": "Write a Python function to reverse a string.", "type": "programming"},
        {"question": "Explain what a class is in Python.", "type": "definition"},
        {"question": "Write a program to find factorial of a number.", "type": "programming"},
        {"question": "What is inheritance in OOP?", "type": "definition"},
        {"question": "Write a Python function to check if a number is prime.", "type": "programming"}
    ],
    "Data Analyst": [
        {"question": "What is the difference between mean, median, and mode?", "type": "definition"},
        {"question": "Write a Python code to calculate the average of a list of numbers.", "type": "programming"},
        {"question": "What is data normalization and why is it important?", "type": "definition"},
        {"question": "Write a Python code to count the number of missing values in a dataset.", "type": "programming"},
        {"question": "Explain the concept of standard deviation.", "type": "definition"}
    ],
    "AI / ML Beginner": [
        {"question": "What is machine learning?", "type": "definition"},
        {"question": "Write a Python snippet to create a list of numbers from 1 to 10.", "type": "programming"},
        {"question": "What is supervised learning?", "type": "definition"},
        {"question": "Write a Python snippet to calculate the sum of squares from 1 to 10.", "type": "programming"},
        {"question": "Explain the difference between AI, ML, and Deep Learning.", "type": "definition"}
    ]
}

# -------------------------
# Example usage (for testing)
# -------------------------
if __name__ == "__main__":
    role = "Software Developer"
    for q in questions[role]:
        print(f"{q['type'].capitalize()}: {q['question']}")
