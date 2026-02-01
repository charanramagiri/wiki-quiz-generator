# Wikipedia Quiz Generator

## Overview
This project is a full-stack application that generates quiz questions automatically from Wikipedia articles using a Large Language Model (LLM).

Users can enter a Wikipedia URL, and the system:
- Scrapes the article content
- Generates multiple-choice quiz questions
- Stores results in a PostgreSQL database
- Displays past quizzes with detailed views

---

## Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL
- **LLM**: LLaMA 3.1 (via Groq, free tier)
- **Scraping**: BeautifulSoup
- **ORM**: SQLAlchemy

---

## Features
- Generate quiz from Wikipedia URL
- 5 to 10 multiple-choice questions per article
- Each question includes:
  - 4 options (A–D)
  - Correct answer
  - Difficulty level
  - Short explanation
- Stores quiz history in PostgreSQL
- View past quizzes and quiz details
- Robust error handling for invalid URLs and LLM responses

---

## API Endpoints

### Generate Quiz
POST /generate-quiz?url=<wikipedia_url>


### Get History
GET /history


### Get Quiz Details
GET /quiz/{article_id}


---

## Prompt Design
The LLM prompt enforces:
- Exact number of questions
- Strict grounding to article content
- Structured JSON output
- Prevention of hallucinations

---

## Sample Data
Sample tested Wikipedia URLs and JSON outputs are available in the `sample_data/` folder.

---

## How to Run

## Environment Setup
Create a `.env` file and add:
GROQ_API_KEY=your_api_key_here


### Backend

cd backend
uvicorn main:app --reload

### Frontend
cd frontend
python -m http.server 5500
Open:

http://localhost:5500