from flask import Flask, render_template, jsonify, request
import time

app = Flask(__name__)
NUM_CELLS = 60
cells = [{"color": "green", "timestamp": 0} for _ in range(NUM_CELLS)]
last_clicked = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_state')
def get_state():
    now = time.time()
    for cell in cells:
        if cell["color"] == "yellow" and now - cell["timestamp"] > 600:
            cell["color"] = "green"

    # Підказка: обрати найдальшу від попередньої зелену комірку
    suggested = None
    global last_clicked
    green_indexes = [i for i, cell in enumerate(cells) if cell["color"] == "green"]

    if last_clicked is None and green_indexes:
        suggested = green_indexes[0]
    elif green_indexes:
        suggested = max(green_indexes, key=lambda x: abs(x - last_clicked))

    return jsonify({"cells": cells, "suggested": suggested})

@app.route('/click/<int:index>', methods=['POST'])
def click(index):
    global last_clicked

    if index < 0 or index >= NUM_CELLS:
        return jsonify({"error": "Invalid index"}), 400

    if cells[index]["color"] == "green":
        cells[index]["color"] = "red"
        if index > 0 and cells[index - 1]["color"] == "green":
            cells[index - 1]["color"] = "yellow"
            cells[index - 1]["timestamp"] = time.time()
        if index < NUM_CELLS - 1 and cells[index + 1]["color"] == "green":
            cells[index + 1]["color"] = "yellow"
            cells[index + 1]["timestamp"] = time.time()

        last_clicked = index

    return jsonify(success=True)

@app.route('/return/<int:index>', methods=['POST'])
def return_locker(index):
    if 0 <= index < NUM_CELLS:
        cells[index]["color"] = "green"
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
