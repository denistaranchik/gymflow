from flask import Flask, render_template, jsonify, request
import time

app = Flask(__name__)
NUM_CELLS = 15

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

    suggested = suggest_next()
    if suggested is not None:
        suggested_number = suggested + 1
    else:
        suggested_number = None

    return jsonify({
        "cells": cells,
        "suggested": suggested_number
    })

@app.route('/click/<int:index>', methods=['POST'])
def click(index):
    global last_clicked

    if index < 0 or index >= NUM_CELLS:
        return jsonify({"error": "Invalid index"}), 400

    current = cells[index]

    if current["color"] == "red":
        current["color"] = "green"
        return jsonify(success=True)

    current["color"] = "red"

    if index > 0 and cells[index - 1]["color"] != "red":
        cells[index - 1]["color"] = "yellow"
        cells[index - 1]["timestamp"] = time.time()
    if index < NUM_CELLS - 1 and cells[index + 1]["color"] != "red":
        cells[index + 1]["color"] = "yellow"
        cells[index + 1]["timestamp"] = time.time()

    last_clicked = index
    return jsonify(success=True)

def suggest_next():
    if last_clicked is None:
        return 0
    # Вибираємо тільки зелені комірки
    distances = [
        (i, abs(i - last_clicked))
        for i, c in enumerate(cells)
        if c["color"] == "green"
    ]
    if not distances:
        return None
    distances.sort(key=lambda x: -x[1])  # Найдальша від останньої
    return distances[0][0]

if __name__ == '__main__':
    app.run(debug=True)
