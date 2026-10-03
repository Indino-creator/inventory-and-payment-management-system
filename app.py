from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
import qrcode

app = Flask(__name__)


# -----------------------------
# MySQL CONNECTION
# -----------------------------

def get_connection():
    conn =mysql.connector.connect(
        host="localhost",
        user="root",
        password="Armaan",       # Change this if your password is different
        database="inventory"
    )
    return conn

# -----------------------------
# HOME PAGE
# -----------------------------

@app.route("/")
def index():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM inventory ORDER BY product_id DESC")
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("index.html", products=products)


# -----------------------------
# ADD PRODUCT
# -----------------------------

@app.route("/add", methods=["POST"])
def add_product():

    product_name = request.form["name"]
    product_quantity = request.form["quantity"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO groceries (product_product_name, product_product_quantity)
        VALUES (%s, %s)
        """,
        (product_name, product_quantity)
    )

    conn.commit()

    product_id = cursor.lastrowid

    cursor.close()
    conn.close()

    # Generate QR code
    generate_qr(product_id)

    return redirect(url_for("product", product_id=product_id))


# -----------------------------
# PRODUCT PAGE
# -----------------------------

@app.route("/product/<int:product_id>")
def product(product_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM groceries WHERE id = %s",
        (product_id,)
    )

    product_data = cursor.fetchone()

    cursor.close()
    conn.close()

    if product_data is None:
        return "Product not found", 404

    return render_template(
        "product.html",
        product=product_data
    )


# -----------------------------
# UPDATE PRODUCT
# -----------------------------

@app.route("/update/<int:product_id>", methods=["POST"])
def update_product(product_id):

    product_name = request.form["product_name"]
    product_quantity = request.form["product_quantity"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE products
        SET product_name = %s,
            product_quantity = %s,
        WHERE id = %s
        """,
        (product_name, product_quantity, product_id)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("product", product_id=product_id))


# -----------------------------
# DELETE PRODUCT
# -----------------------------

@app.route("/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id = %s",
        (product_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    # Delete QR code
    qr_file = f"static/qr_codes/product_{product_id}.png"

    if os.path.exists(qr_file):
        os.remove(qr_file)

    return redirect(url_for("index"))


# -----------------------------
# GENERATE QR CODE
# -----------------------------

def generate_qr(product_id):

    url = f"http://127.0.0.1:5000/product/{product_id}"

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image()

    os.makedirs("static/qr_codes", exist_ok=True)

    filename = f"static/qr_codes/product_{product_id}.png"

    img.save(filename)

    print(f"QR code saved: {filename}")


# -----------------------------
# RUN SERVER
# -----------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )