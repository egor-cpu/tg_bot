document.addEventListener('DOMContentLoaded', () => {
    const gridSize = parseInt(localStorage.getItem('gridSize')) || 8;
    let score = 0;
    let scoreSent = false;
    let selected = null;
    const colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF'];
    
    const gameBoard = document.getElementById('game-board');
    const scoreElement = document.getElementById('score');

    function sendScoreToServer(score) {
        const userId = localStorage.getItem("userId") || 1; // пока жестко 1, позже можно сделать login
        fetch("/submit_score", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: userId,
                score: score,
                is_correct: true
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "ok") {
                console.log("Счёт отправлен успешно!");
            } else {
                console.error("Ошибка при отправке:", data.message);
            }
        })
        .catch(err => {
            console.error("Сетевая ошибка:", err);
        });
    }

    function initGame() {
        gameBoard.style.gridTemplateColumns = `repeat(${gridSize}, 50px)`;
        createGrid();
    }

    function createGrid() {
        gameBoard.innerHTML = '';
        for (let i = 0; i < gridSize * gridSize; i++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.style.backgroundColor = getRandomColor();
            cell.dataset.index = i;
            // Сброс бонусного статуса
            cell.dataset.bonus = 'false';
            cell.addEventListener('click', handleCellClick);
            gameBoard.appendChild(cell);
        }
    }

    function handleCellClick(e) {
        const cell = e.target;
        // Если ячейка является бонусом, активируем его
        if (cell.dataset.bonus === 'true') {
            activateBonus(cell);
            return;
        }
        if (!selected) {
            selected = cell;
            cell.classList.add('selected');
        } else {
            const selectedIndex = parseInt(selected.dataset.index);
            const clickedIndex = parseInt(cell.dataset.index);
            
            if (isAdjacent(selectedIndex, clickedIndex)) {
                swapCells(selected, cell);
                animateSwap(selected, cell);
                selected.classList.remove('selected');
                selected = null;
                setTimeout(() => {
                    checkMatches();
                }, 300);
            } else {
                selected.classList.remove('selected');
                selected = cell;
                cell.classList.add('selected');
            }
        }
    }

    function isAdjacent(index1, index2) {
        const diff = Math.abs(index1 - index2);
        return diff === 1 || diff === gridSize;
    }

    function swapCells(cell1, cell2) {
        const tempColor = cell1.style.backgroundColor;
        cell1.style.backgroundColor = cell2.style.backgroundColor;
        cell2.style.backgroundColor = tempColor;
        // Передаем бонусный статус и тип, если он был
        const tempBonus = cell1.dataset.bonus;
        const tempType = cell1.dataset.bonusType;
        cell1.dataset.bonus = cell2.dataset.bonus;
        cell1.dataset.bonusType = cell2.dataset.bonusType;
        cell2.dataset.bonus = tempBonus;
        cell2.dataset.bonusType = tempType;
    }

    function animateSwap(cell1, cell2) {
        cell1.classList.add('swap-animation');
        cell2.classList.add('swap-animation');
        setTimeout(() => {
            cell1.classList.remove('swap-animation');
            cell2.classList.remove('swap-animation');
        }, 300);
    }

    // Проверка совпадений с учетом горизонтальных и вертикальных последовательностей
    function checkMatches() {
        let matchesFound = false;
        const cells = Array.from(gameBoard.children);
        
        // Проверка горизонтальных последовательностей
        for (let row = 0; row < gridSize; row++) {
            let sequence = [];
            for (let col = 0; col < gridSize; col++) {
                const index = row * gridSize + col;
                const cell = cells[index];
                if (sequence.length === 0) {
                    sequence.push(cell);
                } else {
                    const baseColor = sequence[0].style.backgroundColor;
                    if (cell.style.backgroundColor === baseColor && baseColor !== 'transparent') {
                        sequence.push(cell);
                    } else {
                        if (sequence.length >= 3) markMatch(sequence);
                        sequence = [cell];
                    }
                }
            }
            if (sequence.length >= 3) markMatch(sequence);
        }

        // Проверка вертикальных последовательностей
        for (let col = 0; col < gridSize; col++) {
            let sequence = [];
            for (let row = 0; row < gridSize; row++) {
                const index = row * gridSize + col;
                const cell = cells[index];
                if (sequence.length === 0) {
                    sequence.push(cell);
                } else {
                    const baseColor = sequence[0].style.backgroundColor;
                    if (cell.style.backgroundColor === baseColor && baseColor !== 'transparent') {
                        sequence.push(cell);
                    } else {
                        if (sequence.length >= 3) markMatch(sequence);
                        sequence = [cell];
                    }
                }
            }
            if (sequence.length >= 3) markMatch(sequence);
        }

        function markMatch(sequence) {
            matchesFound = true;
            // Если последовательность достаточно длинная, назначаем бонус
            if (sequence.length >= 4) {
                const bonusCell = sequence[Math.floor(sequence.length / 2)];
                bonusCell.dataset.bonus = 'true';
                bonusCell.dataset.bonusType = getBonusType(sequence.length);
                bonusCell.classList.add('bonus');
                // Добавляем класс для визуального обозначения типа бонуса
                bonusCell.classList.add(`bonus-${bonusCell.dataset.bonusType}`);
            }
            // Анимация исчезновения и начисление очков
            sequence.forEach(cell => {
                cell.classList.add('fade-out');
                setTimeout(() => {
                    cell.style.backgroundColor = 'transparent';
                    cell.classList.remove('fade-out');
                }, 300);
                // Если ячейка-бонус, начисляем больше очков
                score += cell.dataset.bonus === 'true' ? 300 : 100;
            });
            scoreElement.textContent = `Счёт: ${score}`;
            
            if (!scoreSent && score >= 1000) {
                sendScoreToServer(score);
                scoreSent = true;
            }
        }

        if (matchesFound) {
            setTimeout(() => {
                refillGrid();
                setTimeout(checkMatches, 300);
            }, 400);
        }
    }

    // Определяем тип бонуса в зависимости от длины последовательности
    function getBonusType(length) {
        if (length === 4) {
            return 'row';
        } else if (length === 5) {
            return 'column';
        } else {
            return 'bomb';
        }
    }

    // Активация бонуса по типу
    function activateBonus(cell) {
        const index = parseInt(cell.dataset.index);
        const bonusType = cell.dataset.bonusType;
        const cells = Array.from(gameBoard.children);
        if (bonusType === 'row') {
            const row = Math.floor(index / gridSize);
            for (let col = 0; col < gridSize; col++) {
                const current = cells[row * gridSize + col];
                current.classList.add('bonus-activate');
                setTimeout(() => {
                    current.style.backgroundColor = 'transparent';
                    current.classList.remove('bonus-activate');
                }, 300);
                score += 100;
            }
        } else if (bonusType === 'column') {
            const col = index % gridSize;
            for (let row = 0; row < gridSize; row++) {
                const current = cells[row * gridSize + col];
                current.classList.add('bonus-activate');
                setTimeout(() => {
                    current.style.backgroundColor = 'transparent';
                    current.classList.remove('bonus-activate');
                }, 300);
                score += 100;
            }
        } else if (bonusType === 'bomb') {
            // Очищаем соседние ячейки (8 направлений)
            const adjacentOffsets = [
                -gridSize - 1, -gridSize, -gridSize + 1,
                -1, 1,
                gridSize - 1, gridSize, gridSize + 1
            ];
            adjacentOffsets.forEach(offset => {
                const adjIndex = index + offset;
                if (adjIndex >= 0 && adjIndex < gridSize * gridSize) {
                    const current = cells[adjIndex];
                    current.classList.add('bonus-activate');
                    setTimeout(() => {
                        current.style.backgroundColor = 'transparent';
                        current.classList.remove('bonus-activate');
                    }, 300);
                    score += 100;
                }
            });
        }
        // Сбрасываем бонусный статус ячейки
        cell.dataset.bonus = 'false';
        cell.dataset.bonusType = '';
        cell.classList.remove('bonus');
        cell.classList.remove('bonus-row');
        cell.classList.remove('bonus-column');
        cell.classList.remove('bonus-bomb');
        scoreElement.textContent = `Счёт: ${score}`;
        setTimeout(() => {
            refillGrid();
            setTimeout(checkMatches, 300);
        }, 400);
    }

    function refillGrid() {
        const cells = Array.from(gameBoard.children);
        const grid = [];
        
        // Формируем матрицу текущих цветов
        for (let row = 0; row < gridSize; row++) {
            grid[row] = [];
            for (let col = 0; col < gridSize; col++) {
                const index = row * gridSize + col;
                grid[row][col] = cells[index].style.backgroundColor;
            }
        }

        // Симуляция "падения" ячеек
        for (let col = 0; col < gridSize; col++) {
            let columnColors = [];
            for (let row = 0; row < gridSize; row++) {
                columnColors.push(grid[row][col]);
            }
            
            const nonEmpty = columnColors.filter(color => color !== 'transparent');
            const emptyCount = gridSize - nonEmpty.length;
            const newColors = Array.from({ length: emptyCount }, () => getRandomColor());
            const newColumn = [...newColors, ...nonEmpty];
            
            for (let row = 0; row < gridSize; row++) {
                grid[row][col] = newColumn[row];
            }
        }

        // Обновляем цвета ячеек с анимацией заполнения и сбрасываем бонусные статусы
        for (let row = 0; row < gridSize; row++) {
            for (let col = 0; col < gridSize; col++) {
                const index = row * gridSize + col;
                cells[index].style.transition = 'background-color 0.3s';
                cells[index].style.backgroundColor = grid[row][col];
                cells[index].dataset.bonus = 'false';
                cells[index].dataset.bonusType = '';
                cells[index].classList.remove('bonus');
                cells[index].classList.remove('bonus-row');
                cells[index].classList.remove('bonus-column');
                cells[index].classList.remove('bonus-bomb');
            }
        }
    }

    function getRandomColor() {
        return colors[Math.floor(Math.random() * colors.length)];
    }

    initGame();
});
