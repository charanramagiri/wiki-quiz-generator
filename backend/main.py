from fastapi import FastAPI, HTTPException
from services.scraper import scrape_wikipedia

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
