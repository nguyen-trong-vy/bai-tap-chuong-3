import math
from flask import Flask, render_template, request, abort

app = Flask(__name__)

SHOP = {
    "name": "Cà phê Sông Hương",
    "address": "12 Lê Lợi, Huế",
    "phone": "0234 3888 999",
}

# Danh sách đúng 7 món theo các trường hợp kiểm thử
MENU = [
    {"id": 1, "name": "Cà phê đen", "price": 20000, "image": "ca-phe-den.jpg"},
    {"id": 2, "name": "Cà phê sữa", "price": 25000, "image": "ca-phe-sua.jpg"},
    {"id": 3, "name": "Bạc xỉu", "price": 30000, "image": "bac-xiu.jpg"},
    {"id": 4, "name": "Trà đào", "price": 35000, "image": "tra-dao.jpg"},
    {"id": 5, "name": "Trà sữa", "price": 35000, "image": "tra-sua.jpg"},
    {"id": 6, "name": "Nước cam", "price": 40000, "image": "nuoc-cam.jpg"},
    {"id": 7, "name": "Sinh tố bơ", "price": 45000, "image": "sinh-to-bo.jpg"},
]

ITEMS_PER_PAGE = 3

@app.context_processor
def inject_shop():
    return dict(shop=SHOP)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/menu")
def menu():
    total_pages = math.ceil(len(MENU) / ITEMS_PER_PAGE)
    raw_page = request.args.get("page")

    # Xử lý tham số page:
    if raw_page is None:
        page = 1
    else:
        try:
            page = int(raw_page)
        except ValueError:
            # /menu?page=abc -> xử lý như trang 1
            page = 1

    # Trang không tồn tại (page <= 0 hoặc page > tổng số trang) -> 404
    if page < 1 or page > total_pages:
        abort(404)

    # Cắt danh sách món cho trang hiện tại (mỗi trang 3 món)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    items_on_page = MENU[start:end]

    return render_template("menu.html", items=items_on_page, page=page, pages=total_pages)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True, port=8000)