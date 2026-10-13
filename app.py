import os
import time

import psycopg2
from flask import Flask, jsonify
from psycopg2 import OperationalError

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable is not set")

    retries = 5

    while retries > 0:
        try:
            return psycopg2.connect(DATABASE_URL)
        except OperationalError:
            retries -= 1

            if retries == 0:
                raise

            time.sleep(2)


@app.route("/")
def index():
    conn = get_db_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS visits (
                    id SERIAL PRIMARY KEY,
                    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cur.execute("INSERT INTO visits DEFAULT VALUES")
            cur.execute("SELECT COUNT(*) FROM visits")

            total_visits = cur.fetchone()[0]

        conn.commit()

        return jsonify({
            "status": "success",
            "message": "Docker Day 10 Capstone Active",
            "total_visits": total_visits
        })

    finally:
        conn.close()


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
