import pytest
from fastapi.testclient import TestClient
from check01 import app, books

client = TestClient(app)


# 各テスト前にbooksリストを空にする
@pytest.fixture(autouse=True)
def reset_books():
    books.clear()
    yield
    books.clear()


# ===== GET / =====

def test_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


# ===== GET /books =====

def test_get_books_empty():
    """書籍が0件のとき空リストを返す"""
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == {"books": [], "count": 0}


def test_get_books_with_data():
    """書籍が追加された後、件数と内容が正しく返る"""
    book_data = {"title": "FastAPI入門", "author": "山田太郎", "pages": 300, "published": True}
    client.post("/books", json=book_data)

    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert data["books"][0]["title"] == "FastAPI入門"


# ===== POST /books =====

def test_add_book():
    """正常な書籍データを追加できる"""
    book_data = {"title": "Python実践", "author": "鈴木花子", "pages": 250, "published": False}
    response = client.post("/books", json=book_data)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "書籍を追加しました"
    assert data["book"]["title"] == "Python実践"
    assert data["book"]["author"] == "鈴木花子"
    assert data["book"]["pages"] == 250
    assert data["book"]["published"] is False


def test_add_book_missing_field():
    """必須フィールドが欠けているとバリデーションエラー"""
    response = client.post("/books", json={"title": "不完全な本"})
    assert response.status_code == 422


def test_add_book_wrong_type():
    """pagesに文字列を渡すとバリデーションエラー"""
    book_data = {"title": "型エラー本", "author": "著者A", "pages": "三百", "published": True}
    response = client.post("/books", json=book_data)
    assert response.status_code == 422


def test_add_multiple_books():
    """複数冊追加すると件数が正しく増える"""
    for i in range(3):
        client.post("/books", json={"title": f"本{i}", "author": "著者", "pages": 100, "published": True})

    response = client.get("/books")
    assert response.json()["count"] == 3


# ===== DELETE /books/{book_id} =====

def test_delete_book():
    """追加した書籍をインデックス指定で削除できる"""
    client.post("/books", json={"title": "削除対象", "author": "著者B", "pages": 200, "published": True})

    response = client.delete("/books/0")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "書籍を削除しました"
    assert data["book"]["title"] == "削除対象"

    # 削除後は0件になる
    get_response = client.get("/books")
    assert get_response.json()["count"] == 0


def test_delete_book_invalid_index():
    """存在しないインデックスを指定してもエラーにならない（現状の実装確認）"""
    response = client.delete("/books/99")
    # 現在の実装ではNoneが返る（HTTPExceptionなし）
    assert response.status_code == 200
    assert response.json() is None
