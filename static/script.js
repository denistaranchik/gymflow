document.addEventListener("DOMContentLoaded", function() {
    const suggestion = document.getElementById("next-suggestion");
    const confirmBtn = document.getElementById("confirm-button");
    const returnBtn = document.getElementById("return-button");
    const returnInput = document.getElementById("return-input");
    let state = [];
    let suggestedIndex = null;

    function updateGrid() {
        fetch('/get_state')
            .then(response => response.json())
            .then(data => {
                state = data.cells;
                suggestedIndex = data.suggested;
                suggestion.textContent = suggestedIndex !== null ? (suggestedIndex + 1) : 'Немає';

                ['col-1', 'col-2', 'col-3', 'col-4'].forEach(col => {
                    document.getElementById(col).innerHTML = '';
                });

                const columns = [
                    Array.from({length: 15}, (_, i) => i),
                    Array.from({length: 15}, (_, i) => i + 15),
                    Array.from({length: 15}, (_, i) => i + 30),
                    Array.from({length: 15}, (_, i) => i + 45)
                ];

                columns.forEach((arr, idx) => {
                    const colDiv = document.getElementById(`col-${idx + 1}`);
                    arr.slice().reverse().forEach(index => {
                        const cell = state[index];
                        const div = document.createElement("div");
                        div.className = "cell " + cell.color;
                        div.textContent = index + 1;
                        div.onclick = () => clickCell(index);
                        colDiv.appendChild(div);
                    });
                });
            });
    }

    function clickCell(index) {
        fetch('/click/' + index, {method: 'POST'})
            .then(() => updateGrid());
    }

    confirmBtn.onclick = function() {
        if (suggestedIndex !== null) {
            clickCell(suggestedIndex);
        }
    };

    returnBtn.onclick = function() {
        const num = parseInt(returnInput.value);
        if (!isNaN(num) && num >= 1 && num <= 60) {
            fetch('/return/' + (num - 1), {method: 'POST'})
                .then(() => {
                    returnInput.value = '';
                    updateGrid();
                });
        } else {
            alert('Введіть коректний номер від 1 до 60');
        }
    };

    updateGrid();
    setInterval(updateGrid, 5000);
});

