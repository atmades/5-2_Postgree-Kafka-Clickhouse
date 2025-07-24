# 📦 Kafka Postgres → ClickHouse Pipeline
A simple educational pipeline that streams data from PostgreSQL to Kafka and then to ClickHouse.

**Pipeline Overview**
   ```
PostgreSQL → Kafka → Python Consumer → ClickHouse
```
- producer.py reads unsent records from PostgreSQL and sends them to Kafka
- consumer.py reads messages from Kafka and inserts them into ClickHouse
- after sending, the producer updates each row with sent_to_kafka = TRUE

## 🛠 Requirements
- Docker & Docker Compose
- Python 3.8+
- ClickHouse running at localhost:8123 (user: user, password: strongpassword)


## 🚀 How to Run
**1. Start services:**

   ```
docker-compose up -d
   ```
**2.Start the producer:**
   ```
python producer_pg_to_kafka.py
   ```

**3.Start the consumer:**
   ```
consumer_to_clickhouse.py
   ```
## ✅ Result
Data flows from PostgreSQL → Kafka → ClickHouse

**Already-sent rows are skipped on next run**
