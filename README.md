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
- 5 multiple-choice questions per article
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
