import sys
from pathlib import Path

# Ajoute le dossier parent au PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI

# Importe ton routeur (ou tous les routeurs que tu as)
from routes.Recherche import router as recherche_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(recherche_router)


import uvicorn

if __name__ == "__main__":
    uvicorn.run("site:app", host="0.0.0.0", port=8888, reload=True)