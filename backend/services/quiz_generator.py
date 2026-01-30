from services.llm import get_llm

def generate_quiz(article_title, article_text):
    llm = get_llm()

    prompt = f"""
You are an expert educator.

Using ONLY the information from the Wikipedia article titled "{article_title}",
generate a quiz of 5 to 10 multiple-choice questions.

Rules:
- Each question must have exactly 4 options labeled A, B, C, D
- Clearly mention the correct answer
- Provide a short explanation referencing the article
- Assign a difficulty level: easy, medium, or hard
- Do NOT invent facts outside the article

Return the output strictly in JSON format like this:

{{
  "quiz": [
    {{
      "question": "",
      "options": ["", "", "", ""],
      "answer": "",
      "difficulty": "",
      "explanation": ""
    }}
  ],
  "related_topics": []
}}

Article Content:
{article_text[:6000]}
"""

    response = llm.invoke(prompt)
    return response.content
