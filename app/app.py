from flask import Flask, jsonify
from sqlalchemy import create_engine, text
import os
import time

app = Flask(__name__)

DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
DB_NAME = os.getenv("POSTGRES_DB", "appdb")
DB_HOST = os.getenv("DB_HOST", "db")  

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}")

def init_db():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL
            );
        """))
        conn.commit()

for i in range(10):
    try:
        init_db()
        print("✅ DB connected and initialized")
        break
    except Exception as e:
        print(f"DB not ready yet ({i+1}/10): {e}")
        time.sleep(2)

# Endpoint testowy DB
@app.route("/health/db")
def health_db():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).fetchone()
        if result and result[0] == 1:
            return jsonify({"status": "ok"}), 200
        else:
            return jsonify({"status": "fail"}), 500
    except Exception as e:
        return jsonify({"status": "fail", "error": str(e)}), 500

@app.route("/")
def hello():
    return "Dzień dobry) strona dziala!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
