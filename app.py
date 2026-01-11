from interview_engine import ask_question, evaluate_answer

def main():
    print("🤖 Welcome to AI Smart Interview Coach")
    print("-----------------------------------")

    # Choose role
    role = input("Enter interview role (Software Developer / Data Analyst / AI / ML Beginner): ")

    # Ask question
    question = ask_question(role)
    print("\n📌 Interview Question:")
    print(question)

    # Get user answer
    answer = input("\n📝 Your Answer: ")

    # Evaluate answer
    result = evaluate_answer(answer)

    print("\n📊 Evaluation Result:")
    print(f"Score: {result['score']} / 10")
    print(f"Feedback: {result['feedback']}")


if __name__ == "__main__":
    main()
