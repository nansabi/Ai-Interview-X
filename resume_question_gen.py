def generate_questions(skills):
    questions = []

    for skill in skills:
        questions.append(
            f"Can you explain your experience working with {skill}?"
        )
        questions.append(
            f"What challenges did you face while using {skill}?"
        )

    return questions
