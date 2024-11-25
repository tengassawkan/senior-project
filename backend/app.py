# app.py
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__, template_folder="frontend")

# Configure your PostgreSQL database connection
db_config = {
    "dbname": "your_database_name",
    "user": "your_database_user",
    "password": "your_password",
    "host": "localhost",
    "port": "5432",
}


def get_db_connection():
    return psycopg2.connect(**db_config)


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/product")
def product():
    return render_template(
        "product_page/product.html"
    )  # Adjust path within frontend


@app.route("/insert", methods=["POST"])
def insert_data():
    # Retrieve form data
    category_name = request.form.get("category_name")
    brand_name = request.form.get("brand_name")
    product_name = request.form.get("product_name")
    description = request.form.get("description")
    price = request.form.get("price")

    # Insert data into the PostgreSQL database
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Category (category_name) VALUES (%s) RETURNING category_id",
            (category_name,),
        )
        category_id = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO Brand (brand_name) VALUES (%s) RETURNING brand_id",
            (brand_name,),
        )
        brand_id = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO Product (name, description, price, category_id, brand_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
            """,
            (product_name, description, price, category_id, brand_id),
        )

        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
