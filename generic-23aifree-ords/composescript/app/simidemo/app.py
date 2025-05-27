from flask import Flask, render_template, request
import oracledb
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


def get_connection():
    pw = os.getenv("DBPASSWORD")
    connection = oracledb.connect(user="sh", password=pw, dsn="23ai/freepdb1")
    return connection


@app.route("/", methods=["GET", "POST"])
def index():
    search_query = request.form.get("search", "")
    products = []

    if search_query:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT p.PROD_ID, p.PROD_DESC, p.PROD_CATEGORY_DESC, p.PROD_LIST_PRICE
            FROM products_vector pv
            JOIN products p ON pv.PROD_ID = p.PROD_ID
            where vector_distance(
                pv.EMBEDDING,
                DBMS_VECTOR_CHAIN.UTL_TO_EMBEDDING(:search_value, JSON('{"provider":"database", "model":"demo_model"}') ),
                COSINE) < 0.7
            ORDER BY vector_distance(
                pv.EMBEDDING,
                DBMS_VECTOR_CHAIN.UTL_TO_EMBEDDING(:search_value, JSON('{"provider":"database", "model":"demo_model"}') ),
                COSINE)
            FETCH FIRST 4 ROWS ONLY
        """
        cursor.execute(query, search_value=search_query)
        products = cursor.fetchall()
        conn.close()

    return render_template("index.html", products=products, search_query=search_query)


@app.route("/buy", methods=["POST"])
def buy():
    selected_products = request.form.getlist("selected_products")
    return render_template("confirmation.html", products=selected_products)


# Access the application here
print("http://" + os.getenv("PUBLIC_IP") + ":8088")


if __name__ == "__main__":
    app.debug = True
    app.run(
        host="0.0.0.0",
        port=8181,
    )
