from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Connect to the database
conn = psycopg2.connect(
    dbname="mydb", user="user", password="pass", host="database"
)
cur = conn.cursor()

# Route to add a user
@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.get_json()
    name = data.get("name")

    cur.execute("INSERT INTO users (name) VALUES (%s) RETURNING id;", (name,))
    conn.commit()
    
    return jsonify({"message": "User added!", "id": cur.fetchone()[0]})

# Route to get all users
@app.route("/users", methods=["GET"])
def get_users():
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    
    return jsonify(users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

