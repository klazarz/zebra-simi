import oracledb
import json
import ollama
import os
import glob
from flask import Flask, jsonify, request, render_template, session
from pymongo import MongoClient
import requests
from flask_session import Session
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "super secret key"
Session(app)

session_folder = os.path.join(
    app.instance_path, "flask_session"
)  # Adjust path if needed
if not os.path.exists(session_folder):
    os.makedirs(session_folder)
for file in glob.glob(os.path.join(session_folder, "*")):
    os.remove(file)

STATIC_DIR = os.path.abspath("static")


def get_connection():
    pw = os.getenv("DBPASSWORD")
    connection = oracledb.connect(user="ora23ai", password=pw, dsn="23ai/freepdb1")
    return connection


cursor = get_connection().cursor()

ip = os.getenv("PUBLIC_IP")

def mongo_connect():
    pw = os.getenv("DBPASSWORD")
    client = MongoClient(
        f"mongodb://ora23ai:{pw}@{ip}:27017/ora23ai?authMechanism=PLAIN&authSource=$external&ssl=true&retryWrites=false&loadBalanced=true&tlsAllowInvalidCertificates=true"
    )
    db = client["ora23ai"]
    return db


def get_schema_tables():
    cursor.execute("""SELECT table_name FROM user_tables""")
    title = [i[0] for i in cursor.description]
    data = cursor.fetchall()
    return data, title


def get_employees():
    cursor.execute(
        """SELECT ID, PRODUCT_ID, ORDER_DATE, CUSTOMER_ID, TOTAL_VALUE, ORDER_SHIPPED FROM ORDERS
                """
    )
    title = [i[0] for i in cursor.description]
    data = cursor.fetchall()
    return data, title


def get_locations():
    cursor.execute(
        """SELECT * FROM COUNTRY_LIST
                """
    )
    title = [i[0] for i in cursor.description]
    data = cursor.fetchall()
    return data, title


def get_dept():
    cursor.execute(
        """SELECT * FROM CUSTOMERS
                """
    )
    title = [i[0] for i in cursor.description]
    data = cursor.fetchall()
    return data, title


# def get_vector_search():
#     cursor.execute(
#         """select dbms_vector_chain.utl_to_embedding('cat', json('{"provider":"database", "model":"demo_model"}') )
#                    """
#     )
#     title = [i[0] for i in cursor.description]
#     data = cursor.fetchall()
#     return data, title


def get_country_borders():
    cursor.execute(
        """select from_country,
        to_country
        from graph_table ( countries_graph match
            ( v1 is country )
(-[e is related where e.relationship = 'neighbour']- >( v2 is country where v2.name != 'Germany')) {1,5} where v1.cca3 = 'DEU'
    columns ( v1.id as from_country, listagg(v2.id,',') as to_country ) )
                """
    )
    title = [i[0] for i in cursor.description]
    data = cursor.fetchall()
    return data, title


def get_sql(query):
    if "select" in query:
        with get_connection().cursor() as cursor:
            cursor.execute("""{}""".format(query))
            title = [i[0] for i in cursor.description]
            data = cursor.fetchall()
    else:
        with get_connection().cursor() as cursor:
            cursor.execute("""{}""".format(query))
    return data, title


def get_dv():
    cursor.execute(
        """SELECT * FROM CUSTOMERS_DV c where json_exists(c.data, '$?(@.FirstName == "Michael")')"""
    )
    data = cursor.fetchall()
    data = json.dumps(data, default=str, indent=4, sort_keys=False)
    return data


def get_mongo():
    col = mongo_connect().CUSTOMERS_DV
    mongo_data = col.find_one({"FirstName": "Michael"})
    mongo_data = json.dumps(mongo_data, default=str, indent=4, sort_keys=False)
    return mongo_data


def update_mongo(new):
    col = mongo_connect().CUSTOMERS_DV
    col.update_one({"FirstName": "Michael"}, {"$set": {"Email": new}})
    return


def get_rest():
    response = requests.get(f"http://{ip}:8282/ords/ora23ai/customers_dv/100001")
    rest_data = json.dumps(response.json(), default=str, indent=4, sort_keys=False)
    return rest_data


def put_rest(customer_id, new_email):
    # URL for the customer record
    url = f"http://{ip}:8282/ords/ora23ai/customers_dv/{customer_id}"
    headers = {"Content-Type": "application/json"}

    # Step 1: Retrieve existing data
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return f"Failed to retrieve record. Status code: {response.status_code}, Response: {response.text}"

    # Parse the existing data
    record_data = response.json()

    # Step 2: Update the email in the retrieved data
    record_data["Email"] = new_email

    # Step 3: Send the updated data back
    response = requests.put(url, headers=headers, json=record_data)

    if response.status_code == 200:
        return get_rest()
    else:
        return f"Failed to update email. Status code: {response.status_code}, Response: {response.text}"


def get_world():
    cursor.execute("""SELECT * FROM COUNTRIES c""")
    data = cursor.fetchall()
    data = json.dumps(data, default=str, indent=4, sort_keys=False)
    return data


app = Flask(__name__, static_folder=STATIC_DIR)


@app.route("/")
def index():
    return render_template(
        "index.html",
        headers=get_schema_tables()[1],
        data=get_schema_tables()[0],
    )


@app.route("/employees")
def employees():
    return render_template(
        "employees.html",
        headers=get_employees()[1],
        data=get_employees()[0],
    )


@app.route("/locations")
def locations():
    return render_template(
        "locations.html",
        headers=get_locations()[1],
        data=get_locations()[0],
    )


@app.route("/dept")
def dept():
    return render_template(
        "dept.html",
        headers=get_dept()[1],
        data=get_dept()[0],
    )


@app.route("/sql", methods=["GET", "POST"])
def sql():
    if request.method == "POST":
        query = request.form["query"]
        get_sql(query)
        return render_template(
            "sql.html",
            headers=get_sql(query)[1],
            data=get_sql(query)[0],
        )
    return render_template("sql.html")


@app.route("/sql2")
def sql2():
    return render_template("sql2.html")


@app.route("/sql3")
def sql3():
    return render_template(
        "sql3.html",
        headers=get_country_borders()[1],
        data=get_country_borders()[0],
    )


@app.route("/dv")
def dv():
    return render_template("dv.html", dv_data=get_dv())


@app.route("/mongo", methods=["GET", "POST"])
def mongo():
    if request.method == "POST":
        query = request.form["email"]
        update_mongo(query)
        return render_template("mongo.html", mongo_data=get_mongo())

    return render_template("mongo.html", mongo_data=get_mongo())


@app.route("/rest", methods=["GET", "POST"])
def rest():
    return render_template("rest.html", rest_data=get_rest())


@app.route("/update_email", methods=["POST"])
def update_email():
    new_email = request.form["email"]
    customer_id = "100001"
    result = put_rest(customer_id, new_email)
    return render_template("rest.html", rest_data=result)


@app.route("/world")
def world():
    return render_template("world.html", world_data=get_world())


# @app.route("/vector")
# def get_vector():
#     return render_template(
#         "vector.html",
#         headers=get_vector_search()[1],
#         data=get_vector_search()[0],
#     )


@app.route("/vector", methods=["GET", "POST"])
def get_vector_search():
    word = "cat"  # Default word if no input is provided
    if request.method == "POST":
        word = request.form.get("word", "cat")  # Get the word from the form input

    # Replace 'cat' in the query with the user-provided word
    query = f"""SELECT DBMS_VECTOR_CHAIN.UTL_TO_EMBEDDING('{word}', JSON('{{"provider":"database", "model":"demo_model"}}') )"""
    cursor.execute(query)
    title = [i[0] for i in cursor.description]
    data = cursor.fetchall()

    # Pass the formatted query result to the template
    return render_template("vector.html", data=data, query_result=query)


@app.route("/vector_ollama", methods=["GET", "POST"])
def get_vector_search_ollama():
    word = "cat"  # Default word if no input is provided
    if request.method == "POST":
        word = request.form.get("word", "cat")  # Get the word from the form input

    # Replace 'cat' in the query with the user-provided word
    query = f"""SELECT DBMS_VECTOR_CHAIN.UTL_TO_EMBEDDING('{word}', JSON('{{"provider":"ollama", "host": "local","url": "http://ollama:11434/api/embeddings", "model":"nomic-embed-text:v1.5"}}') )"""
    cursor.execute(query)
    title = [i[0] for i in cursor.description]
    data = cursor.fetchall()

    # Pass the formatted query result to the template
    return render_template("vector_ollama.html", data=data, query_result=query)


@app.route("/simsearch", methods=["GET", "POST"])
def get_simsearch():
    # Check if "results" is already in the session, initialize it if not
    if "results" not in session:
        session["results"] = []  # Initialize results as an empty list

    if request.method == "POST":
        # Retrieve input words
        word1 = request.form.get("word1", "cat")
        word2 = request.form.get("word2", "dog")

        # Construct and execute query
        query = f"""SELECT VECTOR_DISTANCE(
                            DBMS_VECTOR_CHAIN.UTL_TO_EMBEDDING('{word1}', JSON('{{"provider":"database", "model":"demo_model"}}')), 
                            DBMS_VECTOR_CHAIN.UTL_TO_EMBEDDING('{word2}', JSON('{{"provider":"database", "model":"demo_model"}}')),
                            COSINE )"""
        cursor.execute(query)
        data = cursor.fetchall()
        distance = data[0][0] if data else "N/A"  # Assuming single result for distance

        # Append new result to session
        result_data = {"word1": word1, "word2": word2, "distance": distance}
        session["results"].append(result_data)
        session.modified = True  # Mark the session as modified

    return render_template("simsearch.html", results=session["results"])


@app.route("/simsearch_ollama", methods=["GET", "POST"])
def get_simsearch_ollama():
    # Check if "results" is already in the session, initialize it if not
    if "results" not in session:
        session["results"] = []  # Initialize results as an empty list

    if request.method == "POST":
        # Retrieve input words
        word1 = request.form.get("word1", "cat")
        word2 = request.form.get("word2", "dog")

        # Construct and execute query
        query = f"""SELECT VECTOR_DISTANCE(
                            DBMS_VECTOR_CHAIN.UTL_TO_EMBEDDING('{word1}', JSON('{{"provider":"ollama", "host": "local","url": "http://ollama:11434/api/embeddings",  "model":"nomic-embed-text:v1.5"}}')), 
                            DBMS_VECTOR_CHAIN.UTL_TO_EMBEDDING('{word2}', JSON('{{"provider":"ollama", "host": "local","url": "http://ollama:11434/api/embeddings",  "model":"nomic-embed-text:v1.5"}}')),
                            COSINE )"""
        cursor.execute(query)
        data = cursor.fetchall()
        distance = data[0][0] if data else "N/A"  # Assuming single result for distance

        # Append new result to session
        result_data = {"word1": word1, "word2": word2, "distance": distance}
        session["results"].append(result_data)
        session.modified = True  # Mark the session as modified

    return render_template("simsearch_ollama.html", results=session["results"])


OLLAMA_URL = "http://ollama:11434/api/generate"


@app.route("/ask_llm", methods=["GET", "POST"])
def ask_llm():
    response_text = ""
    if request.method == "POST":
        question = request.form.get("question")
        model = request.form.get("model")

        if question and model:
            payload = {"model": model, "prompt": question}
            response = requests.post(OLLAMA_URL, json=payload, stream=True)

            if response.status_code == 200:
                response_text = ""
                for line in response.iter_lines():
                    if line:
                        try:
                            json_data = json.loads(
                                line.decode("utf-8")
                            )  # Corrected JSON parsing
                            response_text += json_data.get("response", "")
                        except json.JSONDecodeError as e:
                            response_text = f"Error processing response: {e}"
                            break
            else:
                response_text = f"Error: {response.status_code} - {response.text}"

    return render_template(
        "ask_llm.html",
        response_text=response_text,
        models=["llama3.2", "gemma3:1b"],
    )


if __name__ == "__main__":
    app.debug = True
    app.config["SECRET_KEY"] = "super secret key"
    app.run(host="0.0.0.0", port=8085)
