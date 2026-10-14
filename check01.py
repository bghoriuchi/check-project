from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app=FastAPI(title="お試し", description="確認用です")

@app.get("/")
def hello():
    return {"message":"Hello World"}

# 書籍データ
class Book(BaseModel):
    title: str      #タイトル
    author: str     #著者
    pages: int      #ページ数
    published: bool #出版済みフラグ

books = []

### 参照 ###
@app.get("/books")
def get_books():
    """全ての書籍を取得"""
    return {"books":books, "count":len(books)}

### 追加 ###
@app.post("/books")
def add_book(book: Book):
    books.append(book)
    return {"message":"書籍を追加しました", "book":book}

### 削除 ###
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    """インデックスを指定して削除"""
    if book_id < len(books):
        deleted_book = books.pop(book_id)
        return {"message":"書籍を削除しました", "book":deleted_book}
