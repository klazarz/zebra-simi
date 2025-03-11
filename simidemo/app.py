from flask import Flask, render_template, request
import oracledb

app = Flask(__name__)


def get_connection():
    pw = "<password>"
    connection = oracledb.connect(user="sh", password=pw, dsn="23ai/freepdb1")
    return connection


cursor = get_connection().cursor()


@app.route("/", methods=["GET", "POST"])
def index():
    search_query = request.form.get("search", "")
    products = []

    if search_query:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT p.PROD_DESC, p.PROD_CATEGORY_DESC, p.PROD_LIST_PRICE
            FROM products_vector pv 
            JOIN products p ON pv.PROD_ID = p.PROD_ID
            ORDER BY vector_distance(
                pv.EMBEDDING, 
                DBMS_VECTOR_CHAIN.UTL_TO_EMBEDDING(:search_value, JSON('{"provider":"database", "model":"demo_model"}') ), 
                COSINE)
            FETCH FIRST 10 ROWS ONLY
        """
        cursor.execute(query, search_value=search_query)
        products = cursor.fetchall()
        conn.close()

    return render_template("index.html", products=products, search_query=search_query)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8181)
