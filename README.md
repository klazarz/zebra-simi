# Oracle Database 23ai - Similarity Search Demo

This demo web app showcases similarity search in Oracle Database using an embedded LLM. Instead of sending data to an external model, it loads an ONNX-compatible embedding model directly into the database.

The model generates embeddings (vectors) for all available products. Users can search for products by entering their criteria. The search input is converted into a vector, and the system performs a similarity search to find the most relevant products. Results are displayed in a table.


# Why does this matter?

- Secure – Data stays within the database.
- Cost-efficient – No external LLM calls.
- Resource-efficient – Reduces energy waste.


# How to start the demo?

## Prerequisites:
- Podman & Podman Compose (Docker & Docker Compose works too)
- x86 architecture only


## Setup
Before starting, replace <password> in:

```
- compose.yml
- ./sql/startup/01-init.sql
- ./sql/startup/02-products.sql
- ./sql/startup/03_load_model_2_db.sh
- ./simidemo/app.py
- .simidemo/check_ora23ai.sh
```

A future version will simplify this step.

## Start
Run:

```podman-compose up -d```


After a fee minutes the app can be accessed on <IP:8183>
