# ========================
# app_ui.py - AI INTERVIEW X (Classy Styled Version)
# ========================

# -------------------------
# Standard & Third-Party Imports
# -------------------------
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import cv2
import pyttsx3
from PIL import Image, ImageTk, ImageDraw, ImageFont

# -------------------------
# Internal App Imports
# -------------------------
from styles import AppTheme
from speech_to_text import listen_to_user
from camera_analysis import (
    start_camera,
    stop_camera,
    get_live_camera_feedback,
    get_camera_frame
)
from utils import timer
from agent.interview_agent import InterviewAgent
from interview_engine import evaluate_answer

# Resume modules
from resume_parser import extract_resume_text
from resume_analyzer import extract_skills
from resume_question_gen import generate_questions

# -------------------------
# Global Application State
# -------------------------
current_q_type = "definition"
engine = pyttsx3.init()

session_score = 0
questions_answered = 0
total_questions = 5
time_per_question = 60

timer_id = None
agent = None
camera_preview = None
role_var = None

resume_uploaded = False
resume_questions = []

# -------------------------
# Styling Helpers
# -------------------------

def create_rounded_button(master, text, bg, fg, command=None, radius=12):
    """Classy rounded button with hover effect"""
    frame = tk.Frame(master, bg=AppTheme.BG_LIGHT)
    frame.pack(pady=4, fill="x")

    def on_enter(e):
        btn.config(bg=AppTheme.ACCENT_ORANGE if bg == AppTheme.PRIMARY_DARK else bg)

    def on_leave(e):
        btn.config(bg=bg)

    btn = tk.Button(
        frame,
        text=text,
        bg=bg,
        fg=fg,
        font=AppTheme.FONT_LABEL,
        relief="flat",
        bd=0,
        padx=16,
        pady=10,
        cursor="hand2",
        command=command
    )
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.pack(fill="x")

    return btn

def style_text(widget):
    widget.config(
        font=AppTheme.FONT_TEXT,
        bg=AppTheme.WHITE,
        fg=AppTheme.TEXT_DARK,
        wrap="word",
        relief="flat",
        bd=2,
        padx=12,
        pady=10,
        highlightthickness=1,
        highlightbackground=AppTheme.BORDER_SUBTLE,
        highlightcolor=AppTheme.ACCENT_ORANGE
    )

# -------------------------
# Camera Preview
# -------------------------

class CameraPreview:
    def __init__(self, parent):
        self.running = True

        self.frame = tk.Frame(parent, bg=AppTheme.BG_LIGHT, bd=1, relief="solid")
        self.frame.pack(pady=10)

        self.video = tk.Label(self.frame, bg=AppTheme.PRIMARY_DARK)
        self.video.pack(padx=5, pady=5)

        self.feedback = tk.Label(
            self.frame,
            text="Emotion: Analyzing...",
            font=AppTheme.FONT_SMALL,
            bg=AppTheme.ACCENT_ORANGE,
            fg=AppTheme.WHITE,
            height=2
        )
        self.feedback.pack(fill="x")

        threading.Thread(target=self.update, daemon=True).start()

    def update(self):
        while self.running:
            frame = get_camera_frame()
            cam = get_live_camera_feedback()

            if frame is not None:
                frame = cv2.resize(frame, (240, 180))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = ImageTk.PhotoImage(Image.fromarray(frame))
                self.video.imgtk = img
                self.video.config(image=img)

            self.feedback.config(text=f"💭 {cam['feedback']}")
            time.sleep(0.03)

    def stop(self):
        self.running = False

# -------------------------
# Resume Upload Logic
# -------------------------

def upload_resume():
    global resume_uploaded, resume_questions

    file_path = filedialog.askopenfilename(
        filetypes=[("Resume Files", "*.pdf *.docx")]
    )
    if not file_path:
        return

    try:
        text = extract_resume_text(file_path)
        skills = extract_skills(text)
        resume_questions = generate_questions(skills)
        resume_uploaded = True

        messagebox.showinfo(
            "Resume Processed",
            f"Skills Detected:\n{', '.join(skills) if skills else 'General'}"
        )
    except Exception as e:
        messagebox.showerror("Resume Error", str(e))

# -------------------------
# Main Application UI
# -------------------------

class InterviewCoachApp:
    def __init__(self, root):
        self.root = root
        root.title("AI INTERVIEW X")
        root.geometry("1000x900")
        root.configure(bg=AppTheme.BG_LIGHT)

        self.build_ui()
        root.protocol("WM_DELETE_WINDOW", self.on_close)

    def build_ui(self):
        self.build_header()

        body = tk.Frame(self.root, bg=AppTheme.BG_LIGHT)
        body.pack(fill="both", expand=True, padx=16, pady=16)

        self.build_sidebar(body)
        self.build_content(body)

    def build_header(self):
        header = tk.Frame(self.root, bg=AppTheme.PRIMARY_DARK, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🎯 AI INTERVIEW X",
            font=("Segoe UI", 22, "bold"),
            fg=AppTheme.ACCENT_ORANGE,
            bg=AppTheme.PRIMARY_DARK
        ).pack(expand=True)

    def build_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=AppTheme.BG_LIGHT)
        sidebar.pack(side="left", padx=10)

        global camera_preview
        camera_preview = CameraPreview(sidebar)

        global role_var
        role_var = tk.StringVar(value="Software Developer")

        ttk.Combobox(
            sidebar,
            values=["Software Developer", "Data Analyst", "AI / ML Beginner"],
            textvariable=role_var,
            state="readonly",
            width=25
        ).pack(pady=10)

        create_rounded_button(
            sidebar, "▶ Start Interview",
            bg=AppTheme.ACCENT_ORANGE,
            fg=AppTheme.WHITE,
            command=start_interview
        )

        create_rounded_button(
            sidebar, "📄 Upload Resume",
            bg=AppTheme.PRIMARY_DARK,
            fg=AppTheme.WHITE,
            command=upload_resume
        )

    def build_content(self, parent):
        content = tk.Frame(parent, bg=AppTheme.BG_LIGHT)
        content.pack(side="left", fill="both", expand=True)

        self.section(content, "Question", "question_text", 4)
        self.timer_bar()
        self.section(content, "Your Answer", "answer_text", 6)
        self.buttons(content)
        self.section(content, "Feedback", "feedback_text", 4)

    def section(self, parent, title, name, height):
        tk.Label(parent, text=title, font=AppTheme.FONT_SUBHEADER,
                 bg=AppTheme.BG_LIGHT).pack(anchor="w", pady=4)

        text = tk.Text(parent, height=height)
        style_text(text)
        text.pack(fill="both", expand=True)
        globals()[name] = text

    def timer_bar(self):
        global timer_label, progress_label
        bar = tk.Frame(self.root, bg=AppTheme.BG_LIGHT)
        bar.pack(fill="x", padx=16, pady=6)

        timer_label = tk.Label(bar, text="⏱ Time Left", fg=AppTheme.WARNING_RED, bg=AppTheme.BG_LIGHT)
        timer_label.pack(side="left")

        progress_label = tk.Label(bar, text="Question 0/5", fg=AppTheme.ACCENT_ORANGE, bg=AppTheme.BG_LIGHT)
        progress_label.pack(side="right")

    def buttons(self, parent):
        frame = tk.Frame(parent, bg=AppTheme.BG_LIGHT)
        frame.pack(pady=10)

        create_rounded_button(
            frame, "✓ Submit Answer",
            bg=AppTheme.PRIMARY_DARK,
            fg=AppTheme.ACCENT_ORANGE,
            command=submit_answer
        )

        create_rounded_button(
            frame, "🎤 Speak Answer",
            bg=AppTheme.ACCENT_ORANGE,
            fg=AppTheme.WHITE,
            command=speak_user_answer
        )

    def on_close(self):
        stop_camera()
        camera_preview.stop()
        self.root.destroy()

# -------------------------
# Interview Logic (UNCHANGED)
# -------------------------

def speak(text):
    engine.say(text)
    engine.runAndWait()

def start_interview():
    global agent, questions_answered
    questions_answered = 0
    agent = InterviewAgent(role_var.get(), total_questions)

    if resume_uploaded and resume_questions:
        agent.load_custom_questions(resume_questions)

    start_camera()
    next_question()

def next_question():
    global current_q_type, questions_answered, timer_id

    if not agent.has_more_questions():
        show_final_score()
        return

    q, q_type = agent.get_next_question()
    current_q_type = q_type

    question_text.delete("1.0", tk.END)
    question_text.insert(tk.END, q)

    questions_answered += 1
    progress_label.config(text=f"Question {questions_answered}/{total_questions}")

    speak(q)
    timer_id = timer.start_timer(time_per_question, timer_label, submit_answer)

def submit_answer():
    timer.stop_timer(timer_id)
    answer = answer_text.get("1.0", tk.END)

    result = evaluate_answer(answer, current_q_type)
    cam = get_live_camera_feedback()

    feedback_text.delete("1.0", tk.END)
    feedback_text.insert(
        "1.0",
        f"{result['feedback']}\n\n📹 Camera: {cam['feedback']}"
    )

    speak(result["feedback"])
    next_question()

def speak_user_answer():
    answer = listen_to_user()
    if answer:
        answer_text.delete("1.0", tk.END)
        answer_text.insert("1.0", answer)

def show_final_score():
    stop_camera()
    camera_preview.stop()
    messagebox.showinfo("Completed", "Interview Finished")

# -------------------------
# Entry Point
# -------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = InterviewCoachApp(root)
    root.mainloop()
