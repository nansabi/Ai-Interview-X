# tests/test_engine.py
import pytest
from interview_engine import evaluate_answer

def test_definition_answer():
    answer = "Object-oriented programming uses classes and methods."
    result = evaluate_answer(answer, "definition")
    assert result["score"] > 0

def test_programming_answer():
    answer = "def reverse_string(s): return s[::-1]"
    result = evaluate_answer(answer, "programming")
    assert result["score"] > 0

def test_empty_answer():
    result = evaluate_answer("", "definition")
    assert result["score"] == 0
