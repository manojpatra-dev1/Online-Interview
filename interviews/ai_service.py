import json
import random
import google.generativeai as genai
from django.conf import settings

# Configure Gemini API
if not settings.GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

genai.configure(api_key=settings.GEMINI_API_KEY)


# ---------------- HELPER FUNCTION ----------------
def clean_json_response(text):
    """Extract valid JSON safely from Gemini response"""
    text = text.strip()

    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    # Extract JSON part only
    start = text.find("[")
    end = text.rfind("]") + 1

    if start != -1 and end != -1:
        return text[start:end]

    return text


# ---------------- GENERATE QUESTIONS ----------------
def generate_questions(topic_name, difficulty, num_questions, experience_level='mid'):
    prompt = f"""
You are a senior technical interviewer.

Generate {num_questions} UNIQUE, NON-REPEATING interview questions.

Topic: {topic_name}
Difficulty: {difficulty}
Experience Level: {experience_level}

STRICT RULES:
- NO generic questions like "Explain {topic_name}"
- Each question MUST be different
- Use real-world, scenario-based questions
- Include coding, conceptual, and problem-solving types
- Make questions feel like real interviews

Return ONLY JSON:
[
  {{
    "question_text": "question",
    "question_type": "conceptual|coding|scenario",
    "expected_answer_points": "point1; point2; point3"
  }}
]
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 1.0,
                "top_p": 0.95,
                "top_k": 40,
            }
        )

        text = clean_json_response(response.text)
        questions = json.loads(text)

        #  Validate structure
        valid_questions = []
        for q in questions:
            if all(k in q for k in ["question_text", "question_type", "expected_answer_points"]):
                valid_questions.append(q)

        # If Gemini fails → fallback
        if len(valid_questions) < num_questions:
            raise ValueError("Incomplete questions")

        return valid_questions[:num_questions]

    except Exception as e:
        print("Gemini Question Error:", e)

        #  Strong fallback (randomized)
        fallback = []
        for i in range(num_questions):
            fallback.append({
                "question_text": f"Explain a real-world use case of {topic_name} ({i+1}).",
                "question_type": random.choice(["conceptual", "scenario"]),
                "expected_answer_points": "definition; real-world example; benefits"
            })
        return fallback


# ---------------- EVALUATE ANSWER ----------------
def evaluate_answer(question, question_type, expected_points, user_answer, topic, difficulty):
    prompt = f"""
You are an expert interviewer.

Evaluate the candidate answer.

Topic: {topic}
Difficulty: {difficulty}

Question: {question}
Expected Points: {expected_points}
Answer: {user_answer}

Return ONLY JSON:
{{
 "score": 0-10,
 "feedback": "short feedback",
 "strengths": "point1; point2",
 "improvements": "point1; point2"
}}
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.7}
        )

        text = clean_json_response(response.text)
        return json.loads(text)

    except Exception as e:
        print("Gemini Evaluation Error:", e)

        return {
            "score": 5,
            "feedback": "Basic evaluation fallback",
            "strengths": "Attempted the question",
            "improvements": "Add more clarity and examples"
        }


# ---------------- SESSION SUMMARY ----------------
def generate_session_summary(topic, difficulty, answers_data):
    prompt = f"""
You are a career coach.

Give overall interview feedback.

Topic: {topic}
Difficulty: {difficulty}

Return ONLY JSON:
{{
 "overall_feedback": "...",
 "top_strengths": "point1; point2",
 "key_improvements": "point1; point2",
 "readiness_level": "Beginner|Intermediate|Ready"
}}
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(prompt)

        text = clean_json_response(response.text)
        return json.loads(text)

    except Exception as e:
        print("Summary Error:", e)

        return {
            "overall_feedback": "Session completed.",
            "top_strengths": "Completed session",
            "key_improvements": "Practice more",
            "readiness_level": "Needs Work"
        }