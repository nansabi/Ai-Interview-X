def extract_skills(resume_text):
    skills_db = [
        "python", "java", "sql", "machine learning",
        "deep learning", "react", "node", "tensorflow",
        "mysql", "mongodb", "data analysis"
    ]

    found = []
    text = resume_text.lower()

    for skill in skills_db:
        if skill in text:
            found.append(skill)

    return list(set(found))
