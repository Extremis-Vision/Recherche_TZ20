import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI
from routes.Recherche import router as recherche_router
from routes.BDD import router as bdd_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "It works 😄"}

app.include_router(recherche_router)
app.include_router(bdd_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # � adapter selon tes besoins
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("website:app", host="0.0.0.0", port=8888, reload=True)