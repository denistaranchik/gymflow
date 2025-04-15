from flask import Flask, render_template, jsonify, request
import time
import logging

app = Flask(__name__)
NUM_CELLS = 153

# Налаштування логування
logging.basicConfig(filename="locker_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# Ініціалізація комірок
cells = [{"color": "green", "timestamp": 0} for _ in range(NUM_CELLS)]
last_clicked = None

def suggest_next():
    if last_clicked is None:
        for i, c in enumerate(cells):
            if c["color"] == "green":
                return i
        return None
    distances = [
        (i, abs(i - last_clicked))
        for i, c in enumerate(cells)
        if c["color"] == "green"
    ]
    if not distances:
        return None
    distances.sort(key=lambda x: -x[1])
    return distances[0][0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_state')
def get_state():
    now = time.time()
    for cell in cells:
        if cell["color"] == "yellow" and now - cell["timestamp"] > 600:
            cell["color"] = "green"
    return jsonify({"cells": cells, "suggested": suggest_next()})

@app.route('/click/<int:index>', methods=['POST'])
def click(index):
    global last_clicked
    if index < 0 or index >= NUM_CELLS:
        return jsonify({"error": "Invalid index"}), 400

    if cells[index]["color"] == "green":
        cells[index]["color"] = "red"
        last_clicked = index
        if index > 0 and cells[index - 1]["color"] == "green":
            cells[index - 1]["color"] = "yellow"
            cells[index - 1]["timestamp"] = time.time()
        if index < NUM_CELLS - 1 and cells[index + 1]["color"] == "green":
            cells[index + 1]["color"] = "yellow"
            cells[index + 1]["timestamp"] = time.time()
        logging.info(f"Видано номер: {index + 1}")
        return jsonify(success=True)
    return jsonify({"error": "Cell not available"}), 400

@app.route('/return_number', methods=['POST'])
def return_number():
    number = int(request.form.get('number', -1))
    if 1 <= number <= NUM_CELLS:
        idx = number - 1
        cells[idx]["color"] = "green"
        cells[idx]["timestamp"] = 0
        logging.info(f"Повернуто номер: {number}")
        return jsonify(success=True)
    return jsonify({"error": "Invalid number"}), 400

if __name__ == '__main__':
    app.run(debug=True)
