from fastapi import FastAPI, HTTPException
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
        quiz_json = json.loads(quiz_response)

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
            quiz = Quiz(
                article_id=article.id,
                question=q["question"],
                options=", ".join(q["options"]),
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
