const grid = document.getElementById("grid");
const suggestion = document.getElementById("suggestion");

function render(data) {
    const cells = data.cells;
    const suggested = data.suggested;

    grid.innerHTML = "";
    cells.forEach((cell, i) => {
        const div = document.createElement("div");
        div.classList.add("cell", cell.color);
        div.innerText = i + 1;
        div.addEventListener("click", () => {
            fetch(`/click/${i}`, { method: "POST" })
                .then(() => update());
        });
        grid.appendChild(div);
    });

    if (suggested !== null) {
        suggestion.innerText = `Підказка: обери комірку № ${suggested}`;
    } else {
        suggestion.innerText = "Всі комірки вже обрані.";
    }
}

function update() {
    fetch("/get_state")
        .then(res => res.json())
        .then(data => render(data));
}

setInterval(update, 1000);
update();
