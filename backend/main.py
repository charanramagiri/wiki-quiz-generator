from fastapi import FastAPI

app = FastAPI(title="Wikipedia Quiz Generator")

@app.get("/")
def root():
    return {"message": "Backend is running successfully"}
