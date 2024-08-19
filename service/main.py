from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from fastapi.middleware.cors import CORSMiddleware

# Veritabanı tablosu oluşturma
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://fogodomehleanmbgnkkegnenaljbfkcn"],  # Uzantı ID'nizi buraya ekleyin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/comments/{classified_id}")
async def read_comments(classified_id: str, db: Session = Depends(get_db)):
    comments_with_usernames = db.query(
        models.Comment,
        models.User.username
    ).join(
        models.User, models.Comment.user_id == models.User.id
    ).filter(
        models.Comment.classifiedId == classified_id
    ).order_by(
        models.Comment.comment_date.asc()
    ).all()

    # Sonuçları JSON formatına dönüştür
    results = [
        {
            "ip": comment.ip,
            "id": comment.id,
            "comment": comment.comment,
            "classifiedId": comment.classifiedId,
            "username": username,  # Kullanıcı adı burada
            "comment_date": comment.comment_date.isoformat()
        }
        for comment, username in comments_with_usernames
    ]
    print(results)
    return results
