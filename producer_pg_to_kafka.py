import psycopg2
from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

conn = psycopg2.connect(
    dbname="test_db", user="admin", password="admin", host="localhost", port=5434
)
cursor = conn.cursor()

# 🔧 Добавление поля sent_to_kafka, если оно отсутствует
cursor.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.columns
            WHERE table_name='user_logins' AND column_name='sent_to_kafka'
        ) THEN
            ALTER TABLE user_logins ADD COLUMN sent_to_kafka BOOLEAN DEFAULT FALSE;
        END IF;
    END
    $$;
""")
conn.commit()

cursor.execute("""
    SELECT username, event_type, extract(epoch FROM event_time)
    FROM user_logins
    WHERE sent_to_kafka = FALSE
""")

rows = cursor.fetchall()

for row in rows:
    data = {
        "user": row[0],
        "event": row[1],
        "timestamp": float(row[2])  # преобразуем Decimal → float
    }
    producer.send("user_events", value=data)

    cursor.execute("""
        UPDATE user_logins
        SET sent_to_kafka = TRUE
        WHERE username = %s AND event_type = %s AND extract(epoch FROM event_time) = %s
    """, (row[0], row[1], row[2]))

    conn.commit()
    print("Sent:", data)
    time.sleep(0.5)