from flask import Flask, render_template, request

app = Flask(__name__)

# ==========================================
# TRANG CHỦ (MENU CHỌN BÀI TẬP)
# ==========================================
@app.route("/")
def home():
    return render_template("home.html")

# ==========================================
# BÀI 1: MÁY TÍNH CƠ BẢN
# ==========================================
def parse_calculator_number(val_str):
    if val_str is None or val_str.strip() == "":
        return None, "Vui lòng nhập một số."
    cleaned = val_str.strip().replace(",", ".")
    try:
        return float(cleaned), None
    except ValueError:
        return None, "Vui lòng nhập một số."

def format_calc_num(val):
    if val == int(val):
        return str(int(val))
    return str(val)

@app.route("/bai-1", methods=["GET", "POST"])
def bai1():
    errors = {}
    result = None
    a_raw, b_raw, op = "", "", "+"

    if request.method == "POST":
        a_raw = request.form.get("a", "")
        b_raw = request.form.get("b", "")
        op = request.form.get("op", "+")

        a_val, err_a = parse_calculator_number(a_raw)
        if err_a:
            errors["a"] = err_a

        valid_ops = ["+", "-", "*", "/"]
        if op not in valid_ops:
            errors["op"] = "Phép toán không hợp lệ."

        b_val, err_b = parse_calculator_number(b_raw)
        if err_b:
            errors["b"] = err_b
        elif op == "/" and b_val == 0:
            errors["b"] = "Không thể chia cho 0."

        if not errors:
            res_val = 0
            if op == "+":
                res_val = a_val + b_val
            elif op == "-":
                res_val = a_val - b_val
            elif op == "*":
                res_val = a_val * b_val
            elif op == "/":
                res_val = a_val / b_val

            result = f"{format_calc_num(a_val)} {op} {format_calc_num(b_val)} = {format_calc_num(res_val)}"

    return render_template("bai1.html", a=a_raw, b=b_raw, op=op, errors=errors, result=result)

# ==========================================
# BÀI 2: TÍNH ĐIỂM HỌC PHẦN
# ==========================================
# Hàm kiểm tra dùng chung cho cả 3 ô (CC, GK, CK)
def validate_score(val_str):
    if val_str is None or val_str.strip() == "":
        return None, "Vui lòng nhập một số."
    cleaned = val_str.strip().replace(",", ".")
    try:
        val = float(cleaned)
    except ValueError:
        return None, "Vui lòng nhập một số."

    if val < 0.0 or val > 10.0:
        return None, "Điểm phải từ 0 đến 10."

    return val, None

@app.route("/bai-2", methods=["GET", "POST"])
def bai2():
    errors = {}
    result = None
    cc_raw, gk_raw, ck_raw = "", "", ""

    if request.method == "POST":
        cc_raw = request.form.get("cc", "")
        gk_raw = request.form.get("gk", "")
        ck_raw = request.form.get("ck", "")

        # Kiểm tra dữ liệu từng ô qua hàm dùng chung
        cc_val, err_cc = validate_score(cc_raw)
        if err_cc:
            errors["cc"] = err_cc

        gk_val, err_gk = validate_score(gk_raw)
        if err_gk:
            errors["gk"] = err_gk

        ck_val, err_ck = validate_score(ck_raw)
        if err_ck:
            errors["ck"] = err_ck

        # Nếu không có lỗi, tiến hành tính điểm và xếp loại
        if not errors:
            # Chuyên cần 10%, Giữa kỳ 30%, Cuối kỳ 60%, làm tròn 1 chữ số
            score = round(cc_val * 0.1 + gk_val * 0.3 + ck_val * 0.6, 1)

            # Quy tắc điểm liệt: Cuối kỳ dưới 1 bị điểm F
            if ck_val < 1.0:
                grade = "F (điểm thi dưới 1)"
            else:
                if score >= 8.5:
                    grade = "A"
                elif score >= 7.0:
                    grade = "B"
                elif score >= 5.5:
                    grade = "C"
                elif score >= 4.0:
                    grade = "D"
                else:
                    grade = "F"

            result = f"{score} - {grade}"

    return render_template(
        "bai2.html",
        cc=cc_raw,
        gk=gk_raw,
        ck=ck_raw,
        errors=errors,
        result=result
    )


# ==========================================
# BÀI 3: TÍNH CHỈ SỐ BMI
# ==========================================
def validate_height(val_str):
    if val_str is None or val_str.strip() == "":
        return None, "Vui lòng nhập một số."
    cleaned = val_str.strip().replace(",", ".")
    try:
        val = float(cleaned)
    except ValueError:
        return None, "Vui lòng nhập một số."

    if val < 50 or val > 250:
        if 0 < val <= 3:
            return None, "Giá trị phải từ 50 đến 250. (nhập mét thay vì cm)"
        return None, "Giá trị phải từ 50 đến 250."

    return val, None

def validate_weight(val_str):
    if val_str is None or val_str.strip() == "":
        return None, "Vui lòng nhập một số."
    cleaned = val_str.strip().replace(",", ".")
    try:
        val = float(cleaned)
    except ValueError:
        return None, "Vui lòng nhập một số."

    if val < 10 or val > 300:
        return None, "Giá trị phải từ 10 đến 300."

    return val, None

@app.route("/bai-3", methods=["GET", "POST"])
def bai3():
    errors = {}
    result = None
    height_raw, weight_raw = "", ""

    if request.method == "POST":
        height_raw = request.form.get("height", "")
        weight_raw = request.form.get("weight", "")

        h_val, err_h = validate_height(height_raw)
        if err_h:
            errors["height"] = err_h

        w_val, err_w = validate_weight(weight_raw)
        if err_w:
            errors["weight"] = err_w

        if not errors:
            # Chiều cao chuyển từ cm sang m
            h_m = h_val / 100.0
            bmi = round(w_val / (h_m ** 2), 1)

            # Phân loại theo chuẩn châu Á và gán mã màu Bootstrap tương ứng
            if bmi < 18.5:
                category = "Thiếu cân"
                color = "warning"  # Vàng
            elif bmi < 23.0:
                category = "Bình thường"
                color = "success"  # Xanh
            elif bmi < 25.0:
                category = "Thừa cân"
                color = "warning"  # Vàng
            else:
                category = "Béo phì"
                color = "danger"   # Đỏ

            # Cân nặng nên có (BMI từ 18.5 đến 22.9)
            min_weight = round(18.5 * (h_m ** 2), 1)
            max_weight = round(22.9 * (h_m ** 2), 1)

            result = {
                "bmi": bmi,
                "category": category,
                "color": color,
                "min_weight": min_weight,
                "max_weight": max_weight
            }

    return render_template(
        "bai3.html",
        height=height_raw,
        weight=weight_raw,
        errors=errors,
        result=result
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)