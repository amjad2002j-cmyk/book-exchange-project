from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("book_exchange.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/books")
def books():
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return render_template("books.html", books=books)

@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO books (title, author) VALUES (?, ?)",
            (title, author)
        )
        conn.commit()
        conn.close()
        return redirect("/books")

    return render_template("add_book.html")

# 🔍 SEARCH (لا يعرض شي إلا بعد الكتابة)
@app.route("/search")
def search():
    title = request.args.get("title")
    books = []

    if title:
        conn = get_db_connection()
        books = conn.execute(
            "SELECT * FROM books WHERE title LIKE ?",
            (f"%{title}%",)
        ).fetchall()
        conn.close()

    return render_template("search.html", books=books)

# 🎯 FILTER (حسب المؤلف فقط)
@app.route("/filter")
def filter_books():
    author = request.args.get("author")
    books = []

    if author:
        conn = get_db_connection()
        books = conn.execute(
            "SELECT * FROM books WHERE author LIKE ?",
            (f"%{author}%",)
        ).fetchall()
        conn.close()

    return render_template("filter.html", books=books)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)