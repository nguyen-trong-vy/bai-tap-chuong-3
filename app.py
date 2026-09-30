from flask import Flask, render_template, request, jsonify, abort

app = Flask(__name__)

# 1. Danh sách BOOKS (>= 4 cuốn)
BOOKS = [
    {"id": 1, "title": "Lập trình Python cơ bản", "author": "Nguyễn Văn A", "year": 2022, "category": "Lập trình", "available": True},
    {"id": 2, "title": "Flask Web Development", "author": "Miguel Grinberg", "year": 2018, "category": "Lập trình", "available": False},
    {"id": 3, "title": "Cấu trúc dữ liệu & Giải thuật", "author": "Trần B", "year": 2021, "category": "Khoa học máy tính", "available": True},
    {"id": 4, "title": "Nhà giả kim", "author": "Paulo Coelho", "year": 1988, "category": "Văn học", "available": True},
    {"id": 5, "title": "Clean Code", "author": "Robert C. Martin", "year": 2008, "category": "Lập trình", "available": False},
]

# Hàm hỗ trợ tìm sách theo ID tránh lặp code
def find_book_by_id(book_id):
    return next((book for book in BOOKS if book["id"] == book_id), None)

# Route 1: Trang chủ /
@app.route("/")
def home():
    total_books = len(BOOKS)
    available_books = sum(1 for b in BOOKS if b["available"])
    return render_template("index.html", total_books=total_books, available_books=available_books)

# Route 2: Danh sách sách /books (có lọc theo category)
@app.route("/books")
def list_books():
    selected_category = request.args.get("category")
    # Lấy danh sách thể loại duy nhất để làm thanh liên kết
    categories = sorted(list(set(b["category"] for b in BOOKS)))
    
    if selected_category:
        filtered_books = [b for b in BOOKS if b["category"].lower() == selected_category.lower()]
    else:
        filtered_books = BOOKS
        
    return render_template(
        "books.html", 
        books=filtered_books, 
        categories=categories, 
        selected_category=selected_category
    )

# Route 3: Chi tiết sách /books/<int:book_id>
@app.route("/books/<int:book_id>")
def book_detail(book_id):
    book = find_book_by_id(book_id)
    if not book:
        abort(404, description=f"Không có sách với ID = {book_id}")
    return render_template("book_detail.html", book=book)

# Route 4: API lấy danh sách sách
@app.route("/api/books")
def api_books():
    return jsonify(BOOKS), 200

# Route 5: API chi tiết 1 cuốn sách
@app.route("/api/books/<int:book_id>")
def api_book_detail(book_id):
    book = find_book_by_id(book_id)
    if not book:
        abort(404, description=f"Không có sách với ID = {book_id}")
    return jsonify(book), 200

# Xử lý trang lỗi 404 cho cả HTML và API
@app.errorhandler(404)
def handle_404(e):
    # Nếu request gửi đến API (/api/...) thì trả về định dạng JSON
    if request.path.startswith("/api/"):
        return jsonify({"error": getattr(e, "description", "Không tìm thấy tài nguyên")}), 404
    # Nếu là trang web HTML thì render giao diện 404 tùy biến có menu chung
    return render_template("404.html", message=getattr(e, "description", "Trang không tồn tại")), 404

if __name__ == "__main__":
    app.run(debug=True)