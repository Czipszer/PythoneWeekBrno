from fastapi import FastAPI

import scraping

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/search')
def search(origin, destination, date):
    return {"journey": scraping.search_journey(origin, destination, date)}
