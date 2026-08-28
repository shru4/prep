import os
import json
import psycopg2
from flask import Flask, jsonify, request
from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient, ServiceBusMessage

app = Flask(__name__)


def db_connection():
    return psycopg2.connect(
        host=os.environ["DATABASE_HOST"],
        port=int(os.getenv("DATABASE_PORT", "5432")),
        dbname=os.environ["DATABASE_NAME"],
        user=os.environ["DATABASE_USER"],
        password=os.environ["DATABASE_PASSWORD"],
        sslmode=os.getenv("DATABASE_SSLMODE", "require"),
    )


def init_db():
    with db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """CREATE TABLE IF NOT EXISTS orders (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL
                )"""
            )
        conn.commit()


def send_event(order):
    namespace = os.environ.get("SERVICE_BUS_NAMESPACE")
    queue = os.environ.get("SERVICE_BUS_QUEUE", "orders")
    if not namespace:
        return

    credential = DefaultAzureCredential()
    client = ServiceBusClient(fully_qualified_namespace=namespace, credential=credential)
    with client:
        sender = client.get_queue_sender(queue_name=queue)
        with sender:
            sender.send_messages(ServiceBusMessage(json.dumps(order)))


@app.get("/health")
def health():
    return jsonify({"status": "healthy"})


@app.get("/ready")
def ready():
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return jsonify({"status": "ready"}), 200
    except Exception as exc:
        return jsonify({"status": "not-ready", "error": str(exc)}), 503


@app.post("/orders")
def create_order():
    body = request.get_json(silent=True) or {}
    name = body.get("name")
    if not name:
        return jsonify({"error": "name is required"}), 400

    with db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO orders (name) VALUES (%s) RETURNING id", (name,))
            order_id = cur.fetchone()[0]
        conn.commit()

    order = {"id": order_id, "name": name}
    send_event(order)
    return jsonify(order), 201


@app.get("/orders")
def get_orders():
    with db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM orders ORDER BY id")
            rows = cur.fetchall()
    return jsonify([{"id": row[0], "name": row[1]} for row in rows])


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080)
