let grid = [];
let score = 0;
const gridSize = 4;

function initGrid() {
    grid = Array(gridSize).fill().map(() => Array(gridSize).fill(0));
    addRandomTile();
    addRandomTile();
    renderGrid();
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

function renderGrid() {
    const gridElement = document.getElementById('grid');
    gridElement.innerHTML = '';
    for (let i = 0; i < gridSize; i++) {
        for (let j = 0; j < gridSize; j++) {
            let cell = document.createElement('div');
            cell.className = 'cell';
            cell.textContent = grid[i][j] === 0 ? '' : grid[i][j];
            gridElement.appendChild(cell);
        }
    }
    document.getElementById('score').textContent = score;
}

function move(direction) {
    // Simplified move logic for basic functionality
    let moved = false;
    // This is a placeholder; implement full 2048 logic as needed
    if (direction === 'up') {
        // Add actual move logic here
    }
    if (moved) {
        addRandomTile();
        renderGrid();
    }
}

function resetGame() {
    score = 0;
    initGrid();
}

// Initialize game
initGrid();
// Add keyboard controls
document.addEventListener('keydown', (e) => {
    switch(e.key) {
        case 'ArrowUp': move('up'); break;
        case 'ArrowDown': move('down'); break;
        case 'ArrowLeft': move('left'); break;
        case 'ArrowRight': move('right'); break;
    }
});