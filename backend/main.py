from fastapi import FastAPI, HTTPException
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

@app.post("/generate-quiz")
def generate_quiz_api(url: str):
    try:
        scraped = scrape_wikipedia(url)
        quiz_data = generate_quiz(scraped["title"], scraped["full_text"])
        return {
            "url": url,
            "title": scraped["title"],
            "summary": scraped["summary"],
            "sections": scraped["sections"],
            "quiz_data": quiz_data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
