function loadGrid() {
    fetch('/get_state')
        .then(res => res.json())
        .then(data => {
            const grid = document.getElementById('grid');
            grid.innerHTML = '';
            data.cells.forEach((cell, i) => {
                const div = document.createElement('div');
                div.className = `cell ${cell.color}`;
                div.textContent = i + 1;
                div.onclick = () => {
                    fetch(`/click/${i}`, { method: 'POST' })
                        .then(() => loadGrid());
                };
                grid.appendChild(div);
            });
            const suggestion = data.suggested !== null ? data.suggested + 1 : 'Всі зайняті';
            document.getElementById('suggestion').textContent = suggestion;
        });
}

document.getElementById('issue').onclick = () => {
    fetch('/get_state')
        .then(res => res.json())
        .then(data => {
            const suggested = data.suggested;
            if (suggested !== null) {
                fetch(`/click/${suggested}`, { method: 'POST' })
                    .then(() => loadGrid());
            }
        });
};

document.getElementById('return-form').onsubmit = (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    fetch('/return_number', {
        method: 'POST',
        body: formData
    }).then(() => {
        e.target.reset();
        loadGrid();
    });
};

loadGrid();
setInterval(loadGrid, 5000);

