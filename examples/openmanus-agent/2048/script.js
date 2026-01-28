const gridSize = 4;
let grid = [];
let score = 0;

function initGrid() {
    grid = Array(gridSize).fill().map(() => Array(gridSize).fill(0));
    addRandomTile();
    addRandomTile();
    updateGrid();
}

function addRandomTile() {
    let emptyCells = [];
    for (let i = 0; i < gridSize; i++) {
        for (let j = 0; j < gridSize; j++) {
            if (grid[i][j] === 0) emptyCells.push({x: i, y: j});
        }
    }
    if (emptyCells.length > 0) {
        let cell = emptyCells[Math.floor(Math.random() * emptyCells.length)];
        grid[cell.x][cell.y] = Math.random() < 0.9 ? 2 : 4;
    }
}

function updateGrid() {
    const gridElement = document.getElementById('grid');
    gridElement.innerHTML = '';
    for (let i = 0; i < gridSize; i++) {
        for (let j = 0; j < gridSize; j++) {
            const tile = document.createElement('div');
            tile.className = 'tile';
            if (grid[i][j] !== 0) {
                tile.textContent = grid[i][j];
                tile.classList.add(`tile-${grid[i][j]}`);
            }
            gridElement.appendChild(tile);
        }
    }
    document.getElementById('score').textContent = score;
}

function move(direction) {
    let moved = false;
    if (direction === 'left') {
        for (let i = 0; i < gridSize; i++) {
            let row = grid[i].filter(val => val !== 0);
            for (let j = 0; j < row.length - 1; j++) {
                if (row[j] === row[j + 1]) {
                    row[j] *= 2;
                    score += row[j];
                    row.splice(j + 1, 1);
                }
            }
            while (row.length < gridSize) row.push(0);
            if (JSON.stringify(grid[i]) !== JSON.stringify(row)) moved = true;
            grid[i] = row;
        }
    } else if (direction === 'right') {
        for (let i = 0; i < gridSize; i++) {
            let row = grid[i].filter(val => val !== 0);
            for (let j = row.length - 1; j > 0; j--) {
                if (row[j] === row[j - 1]) {
                    row[j] *= 2;
                    score += row[j];
                    row.splice(j - 1, 1);
                }
            }
            while (row.length < gridSize) row.unshift(0);
            if (JSON.stringify(grid[i]) !== JSON.stringify(row)) moved = true;
            grid[i] = row;
        }
    } else if (direction === 'up') {
        for (let j = 0; j < gridSize; j++) {
            let col = grid.map(row => row[j]).filter(val => val !== 0);
            for (let i = 0; i < col.length - 1; i++) {
                if (col[i] === col[i + 1]) {
                    col[i] *= 2;
                    score += col[i];
                    col.splice(i + 1, 1);
                }
            }
            while (col.length < gridSize) col.push(0);
            let newCol = col;
            for (let i = 0; i < gridSize; i++) {
                if (grid[i][j] !== newCol[i]) moved = true;
                grid[i][j] = newCol[i];
            }
        }
    } else if (direction === 'down') {
        for (let j = 0; j < gridSize; j++) {
            let col = grid.map(row => row[j]).filter(val => val !== 0);
            for (let i = col.length - 1; i > 0; i--) {
                if (col[i] === col[i - 1]) {
                    col[i] *= 2;
                    score += col[i];
                    col.splice(i - 1, 1);
                }
            }
            while (col.length < gridSize) col.unshift(0);
            let newCol = col;
            for (let i = 0; i < gridSize; i++) {
                if (grid[i][j] !== newCol[i]) moved = true;
                grid[i][j] = newCol[i];
            }
        }
    }
    if (moved) {
        addRandomTile();
        updateGrid();
    }
}

document.addEventListener('keydown', (event) => {
    switch (event.key) {
        case 'ArrowLeft':
            move('left');
            break;
        case 'ArrowRight':
            move('right');
            break;
        case 'ArrowUp':
            move('up');
            break;
        case 'ArrowDown':
            move('down');
            break;
    }
});

document.getElementById('restart').addEventListener('click', () => {
    score = 0;
    initGrid();
});

initGrid();