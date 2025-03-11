#!/bin/bash

# Check if the `ora23ai` user can connect to the `sql` database
until echo "exit" | sqlplus sh/<password>@23ai:1521/freepdb1; do
  echo "Waiting for DB ready...."
  sleep 30
done


echo "DB container is ready. Starting Python application..."
exec python app.py  