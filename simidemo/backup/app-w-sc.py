from flask import Flask, render_template, request, jsonify, redirect
import oracledb
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)


def get_connection():
    pw = os.getenv("DBPASSWORD")
    connection = oracledb.connect(user="sh", password=pw, dsn="23ai/freepdb1")
    return connection


def create_llm_cache_table():
    conn = get_connection()
    cursor = conn.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS llm_cache (
        cache_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        product_desc CLOB,
        llm_response CLOB,
        embedding VECTOR,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    try:
        cursor.execute(create_table_sql)
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

    cursor.close()
    conn.close()


def check_semantic_cache(product_desc, similarity_threshold):
    conn = get_connection()
    cursor = conn.cursor()

    # Generate embedding for the input product description
    embedding_query = """
    SELECT DBMS_VECTOR_CHAIN.UTL_TO_EMBEDDING(
        :product_desc, 
        JSON('{"provider":"database", "model":"demo_model"}')
    ) as embedding FROM DUAL
    """

    cursor.execute(embedding_query, product_desc=product_desc)
    input_embedding = cursor.fetchone()[0]

    # Search for semantically similar cached responses
    # Use TO_CHAR() to convert CLOB to VARCHAR2
    similarity_search = """
    SELECT cache_id, 
           TO_CHAR(product_desc) as product_desc_str, 
           TO_CHAR(llm_response) as llm_response_str, 
           vector_distance(embedding, :input_embedding, COSINE) as similarity
    FROM llm_cache
    WHERE vector_distance(embedding, :input_embedding, COSINE) < :threshold
    ORDER BY vector_distance(embedding, :input_embedding, COSINE)
    FETCH FIRST 1 ROWS ONLY
    """

    cursor.execute(similarity_search, {
        'input_embedding': input_embedding,
        'threshold': 1 - similarity_threshold  # Convert similarity to distance
    })

    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        return {
            'cache_id': result[0],
            'original_product_desc': result[1],  # Now it's already a string
            'llm_response': result[2],  # Now it's already a string
            'similarity_score': 1 - result[3],  # Convert distance back to similarity
            'cached': True
        }

    return None


def store_llm_response(product_desc, llm_response):
    conn = get_connection()
    cursor = conn.cursor()

    # Generate embedding for the product description
    embedding_query = """
    SELECT DBMS_VECTOR_CHAIN.UTL_TO_EMBEDDING(
        :product_desc, 
        JSON('{"provider":"database", "model":"demo_model"}')
    ) as embedding FROM DUAL
    """

    cursor.execute(embedding_query, product_desc=product_desc)
    embedding = cursor.fetchone()[0]

    # Insert the response and embedding into cache
    insert_sql = """
    INSERT INTO llm_cache (product_desc, llm_response, embedding)
    VALUES (:product_desc, :llm_response, :embedding)
    """

    cursor.execute(insert_sql, {
        'product_desc': product_desc,
        'llm_response': llm_response,
        'embedding': embedding
    })

    conn.commit()
    cursor.close()
    conn.close()


def create_llm(product_desc):
    try:
        payload = {
            "model": "llama3.2",
            "prompt": f"Which famous sports player could be a testimonial for this product. If possible name one male and one female person. I just want to have the names and the response should be: Testimonials: and then comma seprated the names. If the item is not a product, think who might be a fan or suggest famous fans: {product_desc}",
            "stream": False
        }

        response = requests.post(
            "http://ollama:11434/api/generate",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            return result.get("response", "No response generated")
        else:
            return f"Ollama API error: {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"Connection error: {str(e)}"


def get_llm_response(product_desc, similarity_threshold):
    # Here we check semantic cache
    cached_result = check_semantic_cache(product_desc, similarity_threshold)

    if cached_result:
        return {
            "response": cached_result['llm_response'],
            "cached": True,
            "cache_source": "semantic",
            "similarity_score": cached_result['similarity_score'],
            "original_query": cached_result['original_product_desc']
        }

    # Ok - we don't have it in the cache, so we need to create it
    llm_response = create_llm(product_desc)

    if not llm_response.startswith("Ollama API error") and not llm_response.startswith("Connection error"):
        # Store the new response in semantic cache
        store_llm_response(product_desc, llm_response)

    return {
        "response": llm_response,
        "cached": False,
        "cache_source": "fresh"
    }


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
            FETCH FIRST 8 ROWS ONLY
        """
        cursor.execute(query, search_value=search_query)
        products = cursor.fetchall()
        conn.close()

    return render_template("index.html", products=products, search_query=search_query)


@app.route("/get_product_info", methods=["POST"])
def get_product_info():
    data = request.get_json()
    product_desc = data.get("product_desc", "")
    similarity_threshold = 0.5

    if not product_desc:
        return jsonify({"error": "Product description is required"}), 400

    result = get_llm_response(product_desc, similarity_threshold)
    return jsonify(result)


@app.route("/cache_stats", methods=["GET"])
def cache_stats():
    """Get semantic cache statistics"""
    conn = get_connection()
    cursor = conn.cursor()

    stats_query = """
    SELECT 
        COUNT(*) as total_cached_responses,
        TO_CHAR(MIN(created_at), 'YYYY-MM-DD HH24:MI:SS') as oldest_cache,
        TO_CHAR(MAX(created_at), 'YYYY-MM-DD HH24:MI:SS') as newest_cache
    FROM llm_cache
    """

    cursor.execute(stats_query)
    stats = cursor.fetchone()
    cursor.close()
    conn.close()

    return jsonify({
        "total_cached_responses": stats[0],
        "oldest_cache": stats[1] if stats[1] else None,
        "newest_cache": stats[2] if stats[2] else None
    })


@app.route("/clear_cache", methods=["GET", "POST"])
def clear_cache():
    """Clear semantic cache (for testing purposes)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM llm_cache")
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect('/')

@app.route("/buy", methods=["POST"])
def buy():
    selected_products = request.form.getlist("selected_products")
    return render_template("confirmation.html", products=selected_products)


# Access the application here
print("http://" + os.getenv("PUBLIC_IP") + ":8088")

create_llm_cache_table()

if __name__ == "__main__":
    app.debug = True
    app.run(
        host="0.0.0.0",
        port=8088,
    )
