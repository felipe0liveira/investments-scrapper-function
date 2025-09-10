import uvicorn
from fastapi import FastAPI
from src.core.settings import Settings
from src.usecases.search import SearchUseCase

app = FastAPI(title="Investment Scrapper API", version="1.0.0")

Settings()

@app.get("/")
async def root():
    return {"message": "Investment Scrapper API is running"}


@app.post("/search")
async def search():
    usecase = SearchUseCase(query="investment")
    return usecase.execute()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
