# Receipt Processor API (Django + Docker)

This is a simple Django REST API that processes receipts and calculates reward points.  
All data is stored in memory. No database is used.

---

## Run the project using Docker

Build the image:

    docker build -t receipt-api .

Run the container:

    docker run -p 8000:8000 receipt-api

The API will be available at http://localhost:8000

---

## API Endpoints

### 1. Submit a receipt

POST /receipts/process

Example using curl with a JSON file:
curl.exe -X POST http://localhost:8000/receipts/process -H "Content-Type: application/json" --data "@example1.json"


Response:

    {
      "id": "generated-uuid"
    }

---

### 2. Get points for a receipt

GET /receipts/{id}/points

Example:

    curl http://localhost:8000/receipts/generated-uuid/points

Response:

    {
      "points": 28
    }

---

## Example JSON files

These files are included for testing:

- example1.json
- example2.json
- morning-receipt.json
- simple-receipt.json

You can test each using:
curl.exe -X POST http://localhost:8000/receipts/process -H "Content-Type: application/json" --data "@example2.json"

---

## Notes

- Data is stored in memory and will be lost when the container is stopped.
- This project does not use a database.
- The logic is implemented in views.py and tested using curl and example files.
