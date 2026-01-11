### AI Smart Interview Coach 🤖🎤
📌 Project Overview

AI Smart Interview Coach is an intelligent and interactive application that simulates a real interview environment.
It asks interview questions, evaluates answers, provides real-time feedback, and generates dynamic questions based on the user’s resume skills.

### This project demonstrates:

Generative AI integration

Prompt engineering and evaluation logic

Resume parsing and skill-based question generation

Responsible AI and unbiased feedback

Modular AI system design with GUI and multi-threading

### 🎯 Key Features

Role-Based Interview: Questions tailored for roles like Software Developer, Data Analyst, AI/ML Beginner.

Resume-Based Interview: Upload a resume (PDF/DOCX) → AI extracts skills and generates personalized questions.

Answer Evaluation and Scoring: Evaluates textual answers and assigns scores.

Camera Feedback & Emotion Analysis: Detects user emotions during answers to provide holistic feedback.

Speech-to-Text Input: Users can speak answers, AI converts to text and evaluates.

Constructive Feedback: Provides actionable suggestions to improve responses.

Progress Tracking: Displays current question, total questions, timer, and scores.

Scalable Architecture: Designed for voice, camera, and resume input simultaneously.

### 🧠 AI Concepts Used

Generative AI (LLMs): For generating and evaluating answers.

Prompt Engineering: Guides AI behavior for feedback and scoring.

Natural Language Processing: Extract skills from resumes and understand user answers.

Decision Support Systems: Combines answer evaluation + emotion analysis.

Responsible AI Principles: Fair, unbiased, and transparent scoring.

### 🏗️ Project Structure

app_ui.py → Application entry point with GUI and interview flow

agent/interview_agent.py → Handles role-based and resume-based question logic

resume_parser.py → Extracts text from PDF/DOCX resumes

resume_analyzer.py → Extracts skills from resume text

resume_question_gen.py → Generates skill-based questions dynamically

interview_engine.py → Core AI logic for answer evaluation and scoring

camera_analysis.py → Captures video and evaluates facial expressions/emotions

speech_to_text.py → Converts spoken answers to text

utils/ → Timer, helper functions, and support scripts

data/roles.json → Predefined role-based questions

tests/ → Automated tests for AI evaluation and parsing

### 🚀 Future Enhancements

Advanced Analytics Dashboard: Visualize performance, emotions, and trends.

Multi-Language Resume Parsing: Support for resumes in multiple languages.

Voice-Only Interview Mode: Conduct interviews without GUI.

Enhanced AI Feedback: Include reasoning, example answers, and improvement suggestions.

### 🧑‍💻 Built For

Learning and demonstrating AI fundamentals

Resume-standard AI/ML project for interviews

Interactive interview preparation and self-assessment tool