from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from decimal import *

from controllers import menu, order, ingredient, journal
from schemas.staff import Credentials, Staff
from services.staff import get_staff_by_pin
from database import Base, engine, get_db, Session

# Create database schema
Base.metadata.create_all(bind=engine)

app = FastAPI(title='Weird Salads API', docs_url="/api/docs", openapi_url="/api")
app.include_router(menu.router, prefix="/api")
app.include_router(order.router, prefix="/api")
app.include_router(ingredient.router, prefix="/api")
app.include_router(journal.router, prefix="/api")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/api/login', response_model=Staff)
def login(
        credentials: Credentials,
        db: Session = Depends(get_db)
    ):
    staff = get_staff_by_pin(db, credentials.pin)
    if staff:
        return staff
    raise HTTPException(status_code=401, detail='Invalid PIN')


