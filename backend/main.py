from fastapi import FastAPI, HTTPException
import re
import json

# 🔹 Database setup
from database import engine, SessionLocal
from models import Base, Article, Quiz

# 🔹 Create tables automatically at startup
Base.metadata.create_all(bind=engine)

# 🔹 Services
from services.scraper import scrape_wikipedia
from services.quiz_generator import generate_quiz

app = FastAPI(title="Wikipedia Quiz Generator")

def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in LLM response")
    return json.loads(match.group())

@app.get("/")
def root():
    return {"message": "Backend is running successfully"}


@app.post("/scrape")
def scrape_article(url: str):
    try:
        data = scrape_wikipedia(url)
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 🔹 UPDATED ENDPOINT (STEP 4.6)
@app.post("/generate-quiz")
def generate_quiz_api(url: str):
    db = SessionLocal()

    try:
        # Scrape article
        scraped = scrape_wikipedia(url)

        # Generate quiz (AI response)
        quiz_response = generate_quiz(scraped["title"], scraped["full_text"])
        quiz_json = extract_json(quiz_response)


        # Check if article already exists
        article = db.query(Article).filter(Article.url == url).first()

        if not article:
            article = Article(
                url=url,
                title=scraped["title"],
                summary=scraped["summary"],
                sections=", ".join(scraped["sections"])
            )
            db.add(article)
            db.commit()
            db.refresh(article)

        # Save quizzes
        for q in quiz_json["quiz"]:
            options_list = q["options"]

            options_map = {
                "A": options_list[0],
                "B": options_list[1],
                "C": options_list[2],
                "D": options_list[3]
            }

            quiz = Quiz(
                article_id=article.id,
                question=q["question"],
                options=json.dumps(options_map),
                answer=q["answer"],
                difficulty=q["difficulty"],
                explanation=q["explanation"]
            )
            db.add(quiz)

        db.commit()

        return {
            "article_id": article.id,
            "title": article.title,
            "quiz_count": len(quiz_json["quiz"]),
            "related_topics": quiz_json["related_topics"]
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        db.close()

@app.get("/history")
def get_history():
    db = SessionLocal()
    articles = db.query(Article).all()

    result = []
    for a in articles:
        result.append({
            "id": a.id,
            "url": a.url,
            "title": a.title
        })

    db.close()
    return result

@app.get("/quiz/{article_id}")
def get_quiz_details(article_id: int):
    db = SessionLocal()

    article = db.query(Article).filter(Article.id == article_id).first()
    quizzes = db.query(Quiz).filter(Quiz.article_id == article_id).all()

    db.close()

    return {
        "title": article.title,
        "summary": article.summary,
        "sections": article.sections.split(", "),
        "quiz": [
            {
                "question": q.question,
                "options": q.options.split(", "),
                "answer": q.answer,
                "difficulty": q.difficulty,
                "explanation": q.explanation
            }
            for q in quizzes
        ]
    }
