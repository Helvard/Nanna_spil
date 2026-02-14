#!/usr/bin/env python3
"""
Script der embedder Paw Patrol billeder som base64 i Kalaha HTML filen
"""

import base64
import os
from pathlib import Path

# Base directory
base_dir = Path(__file__).parent
paw_patrol_dir = base_dir / "paw_patrol"

# Image files
image_files = {
    'bg': 'Adventure_Bay_(S3).webp',
    'avatar1': 'images (1).jpeg',
    'avatar2': 'images (2).jpeg',
    'avatar5': 'images (5).jpeg',
    'avatar6': 'images (6).jpeg',
    'avatar8': 'images (8).jpeg',
}

def image_to_base64(filepath):
    """Convert image to base64 data URI"""
    try:
        with open(filepath, 'rb') as f:
            data = base64.b64encode(f.read()).decode('utf-8')
        
        # Determine mime type
        ext = filepath.suffix.lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.webp': 'image/webp'
        }
        mime = mime_types.get(ext, 'image/jpeg')
        
        return f"data:{mime};base64,{data}"
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return ""

# Load all images
print("Loading images...")
images_b64 = {}
for key, filename in image_files.items():
    filepath = paw_patrol_dir / filename
    print(f"  {key}: {filepath}")
    images_b64[key] = image_to_base64(filepath)

print(f"\nLoaded {len([v for v in images_b64.values() if v])} images successfully")

# Generate HTML with embedded images
html_content = f'''<!DOCTYPE html>
<html lang="da">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Paw Patrol Kalaha</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Comic Sans MS', 'Arial', sans-serif;
            background-image: url('{images_b64['bg']}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}

        .game-container {{
            max-width: 1000px;
            width: 100%;
        }}

        /* Avatar Selection Screen */
        .avatar-selection {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 30px;
            padding: 40px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            animation: slideIn 0.5s ease-out;
        }}

        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateY(-30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .avatar-selection h1 {{
            color: #1a5490;
            font-size: 48px;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }}

        .avatar-selection h2 {{
            color: #e63946;
            font-size: 28px;
            margin-top: 30px;
            margin-bottom: 15px;
        }}

        .mode-selector {{
            margin: 30px 0;
            display: flex;
            gap: 20px;
            justify-content: center;
        }}

        .mode-button {{
            background: linear-gradient(135deg, #1a5490 0%, #0d3a6b 100%);
            color: white;
            border: 3px solid transparent;
            padding: 15px 40px;
            font-size: 22px;
            font-weight: bold;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(26, 84, 144, 0.3);
        }}

        .mode-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(26, 84, 144, 0.5);
        }}

        .mode-button.selected {{
            border-color: #e63946;
            background: linear-gradient(135deg, #e63946 0%, #d62839 100%);
            transform: scale(1.05);
        }}

        .avatar-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}

        .avatar-option {{
            cursor: pointer;
            border: 4px solid transparent;
            border-radius: 20px;
            padding: 10px;
            transition: all 0.3s ease;
            background: white;
        }}

        .avatar-option:hover {{
            transform: scale(1.1);
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
        }}

        .avatar-option.selected {{
            border-color: #e63946;
            background: #fff3cd;
            transform: scale(1.05);
        }}

        .avatar-option img {{
            width: 100%;
            height: 120px;
            object-fit: contain;
            border-radius: 10px;
        }}

        .start-button {{
            background: linear-gradient(135deg, #e63946 0%, #d62839 100%);
            color: white;
            border: none;
            padding: 20px 60px;
            font-size: 28px;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            margin-top: 30px;
            box-shadow: 0 5px 15px rgba(230, 57, 70, 0.4);
            transition: all 0.3s ease;
        }}

        .start-button:hover:not(:disabled) {{
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(230, 57, 70, 0.6);
        }}

        .start-button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}

        /* Game Board */
        .game-board {{
            display: none;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 30px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }}

        .game-board.active {{
            display: block;
            animation: slideIn 0.5s ease-out;
        }}

        .player-info {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #1a5490 0%, #0d3a6b 100%);
            border-radius: 20px;
            color: white;
        }}

        .player {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        .player-avatar {{
            width: 60px;
            height: 60px;
            border-radius: 50%;
            border: 3px solid white;
            object-fit: cover;
        }}

        .player-name {{
            font-size: 24px;
            font-weight: bold;
        }}

        .turn-indicator {{
            font-size: 18px;
            padding: 8px 20px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
        }}

        .board {{
            display: grid;
            grid-template-columns: auto 1fr auto;
            gap: 20px;
            margin: 30px 0;
            background: linear-gradient(135deg, #f4a460 0%, #daa520 50%, #f4a460 100%);
            padding: 40px;
            border-radius: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
            border: 5px solid #cd853f;
        }}

        .kalaha {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: rgba(230, 57, 70, 0.9);
            border-radius: 25px;
            padding: 30px 25px;
            min-width: 120px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(5px);
        }}

        .kalaha-label {{
            color: white;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }}

        .kalaha-stones {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
            align-items: center;
            min-height: 100px;
            max-width: 100px;
        }}

        .stone {{
            width: 20px;
            height: 20px;
            background: #8B4513;
            border-radius: 50%;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            animation: stoneAppear 0.3s ease-out;
        }}

        @keyframes stoneAppear {{
            from {{
                transform: scale(0);
                opacity: 0;
            }}
            to {{
                transform: scale(1);
                opacity: 1;
            }}
        }}

        .pits-container {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}

        .pits-row {{
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 15px;
        }}

        .pit {{
            background: rgba(255, 217, 61, 0.8);
            border: 4px solid rgba(255, 190, 11, 0.9);
            border-radius: 20px;
            aspect-ratio: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            position: relative;
            backdrop-filter: blur(5px);
            padding: 10px;
        }}

        .pit:hover:not(.disabled) {{
            transform: translateY(-5px);
            box-shadow: 0 6px 20px rgba(255, 190, 11, 0.7);
            background: rgba(255, 217, 61, 0.95);
        }}

        .pit.disabled {{
            opacity: 0.6;
            cursor: not-allowed;
        }}

        .pit-index {{
            position: absolute;
            top: 5px;
            font-size: 16px;
            color: #1a5490;
            font-weight: bold;
            background: rgba(255, 255, 255, 0.8);
            padding: 2px 8px;
            border-radius: 10px;
        }}

        .pit-stones {{
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            justify-content: center;
            align-items: center;
            width: 100%;
            height: 100%;
            padding: 5px;
        }}

        .pit .stone {{
            width: 15px;
            height: 15px;
        }}

        .winner-overlay {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.8);
            justify-content: center;
            align-items: center;
            z-index: 1000;
            animation: fadeIn 0.5s ease-out;
        }}

        @keyframes fadeIn {{
            from {{
                opacity: 0;
            }}
            to {{
                opacity: 1;
            }}
        }}

        .winner-overlay.active {{
            display: flex;
        }}

        .winner-message {{
            background: white;
            border-radius: 30px;
            padding: 60px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            animation: bounceIn 0.6s ease-out;
        }}

        @keyframes bounceIn {{
            0% {{
                opacity: 0;
                transform: scale(0.3);
            }}
            50% {{
                transform: scale(1.05);
            }}
            100% {{
                opacity: 1;
                transform: scale(1);
            }}
        }}

        .winner-message h2 {{
            font-size: 48px;
            color: #1a5490;
            margin-bottom: 20px;
        }}

        .winner-avatar {{
            width: 150px;
            height: 150px;
            border-radius: 50%;
            border: 5px solid #e63946;
            margin: 20px auto;
            object-fit: cover;
        }}

        .winner-score {{
            font-size: 32px;
            color: #e63946;
            margin: 20px 0;
        }}

        .play-again-button {{
            background: linear-gradient(135deg, #1a5490 0%, #0d3a6b 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 24px;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            margin-top: 20px;
            box-shadow: 0 5px 15px rgba(26, 84, 144, 0.4);
            transition: all 0.3s ease;
        }}

        .play-again-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(26, 84, 144, 0.6);
        }}

        .status-message {{
            text-align: center;
            font-size: 20px;
            color: #1a5490;
            margin: 20px 0;
            font-weight: bold;
            min-height: 30px;
        }}
    </style>
</head>
<body>
    <div class="game-container">
        <!-- Avatar Selection Screen -->
        <div class="avatar-selection" id="avatarSelection">
            <h1>🐾 Paw Patrol Kalaha 🐾</h1>
            
            <h2>Vælg spiltype:</h2>
            <div class="mode-selector">
                <button class="mode-button" id="vsComputerBtn">Mod Computer</button>
                <button class="mode-button" id="twoPlayerBtn">2 Spillere</button>
            </div>
            
            <div id="player1Section">
                <h2 id="player1Label">Spiller 1 - Vælg din avatar:</h2>
                <div class="avatar-grid" id="player1AvatarGrid"></div>
            </div>
            
            <div id="player2Section">
                <h2 id="player2Label">Computer's avatar:</h2>
                <div class="avatar-grid" id="player2AvatarGrid"></div>
            </div>
            
            <button class="start-button" id="startButton" disabled>Start Spil!</button>
        </div>

        <!-- Game Board -->
        <div class="game-board" id="gameBoard">
            <div class="player-info">
                <div class="player" id="player1Info">
                    <img class="player-avatar" id="player1Avatar" src="" alt="Spiller 1">
                    <div>
                        <div class="player-name">Dig</div>
                        <div class="turn-indicator" id="player1Turn"></div>
                    </div>
                </div>
                <div class="player" id="player2Info">
                    <div style="text-align: right;">
                        <div class="player-name">Computer</div>
                        <div class="turn-indicator" id="player2Turn"></div>
                    </div>
                    <img class="player-avatar" id="player2Avatar" src="" alt="Spiller 2">
                </div>
            </div>

            <div class="status-message" id="statusMessage"></div>

            <div class="board">
                <!-- Player 2 (Computer) Kalaha -->
                <div class="kalaha">
                    <div class="kalaha-label">Computer</div>
                    <div class="kalaha-stones" id="kalaha2"></div>
                </div>

                <!-- Pits -->
                <div class="pits-container">
                    <!-- Player 2 pits (top row, reversed) -->
                    <div class="pits-row" id="player2Pits"></div>
                    <!-- Player 1 pits (bottom row) -->
                    <div class="pits-row" id="player1Pits"></div>
                </div>

                <!-- Player 1 Kalaha -->
                <div class="kalaha">
                    <div class="kalaha-label">Dig</div>
                    <div class="kalaha-stones" id="kalaha1"></div>
                </div>
            </div>
        </div>

        <!-- Winner Overlay -->
        <div class="winner-overlay" id="winnerOverlay">
            <div class="winner-message">
                <h2 id="winnerTitle"></h2>
                <img class="winner-avatar" id="winnerAvatar" src="" alt="Vinder">
                <div class="winner-score" id="winnerScore"></div>
                <button class="play-again-button" onclick="location.reload()">Spil Igen</button>
            </div>
        </div>
    </div>

    <script>
        // Game Configuration
        const STONES_PER_PIT = 6;
        const PITS_PER_PLAYER = 6;
        
        // Avatar paths (embedded as base64)
        const avatarPaths = [
            '{images_b64['avatar1']}',
            '{images_b64['avatar2']}',
            '{images_b64['avatar5']}',
            '{images_b64['avatar6']}',
            '{images_b64['avatar8']}'
        ];

        // Game State
        let gameState = {{
            pits: [],
            currentPlayer: 1,
            player1Avatar: null,
            player2Avatar: null,
            gameOver: false,
            gameMode: null,
        }};

        // Avatar Selection Logic
        let selectedPlayer1Avatar = null;
        let selectedPlayer2Avatar = null;

        function initAvatarSelection() {{
            const player1Grid = document.getElementById('player1AvatarGrid');
            const player2Grid = document.getElementById('player2AvatarGrid');

            // Game mode buttons
            document.getElementById('vsComputerBtn').addEventListener('click', () => selectGameMode('vsComputer'));
            document.getElementById('twoPlayerBtn').addEventListener('click', () => selectGameMode('twoPlayer'));

            avatarPaths.forEach((path, index) => {{
                // Player 1 avatar option
                const player1Option = createAvatarOption(path, () => {{
                    document.querySelectorAll('#player1AvatarGrid .avatar-option').forEach(opt => 
                        opt.classList.remove('selected')
                    );
                    player1Option.classList.add('selected');
                    selectedPlayer1Avatar = path;
                    checkStartButton();
                }});
                player1Grid.appendChild(player1Option);

                // Player 2 avatar option
                const player2Option = createAvatarOption(path, () => {{
                    document.querySelectorAll('#player2AvatarGrid .avatar-option').forEach(opt => 
                        opt.classList.remove('selected')
                    );
                    player2Option.classList.add('selected');
                    selectedPlayer2Avatar = path;
                    checkStartButton();
                }});
                player2Grid.appendChild(player2Option);
            }});
        }}

        function selectGameMode(mode) {{
            gameState.gameMode = mode;
            
            // Update button styles
            document.querySelectorAll('.mode-button').forEach(btn => btn.classList.remove('selected'));
            if (mode === 'vsComputer') {{
                document.getElementById('vsComputerBtn').classList.add('selected');
                document.getElementById('player2Label').textContent = "Computer's avatar:";
            }} else {{
                document.getElementById('twoPlayerBtn').classList.add('selected');
                document.getElementById('player2Label').textContent = "Spiller 2 - Vælg din avatar:";
            }}
            
            checkStartButton();
        }}

        function createAvatarOption(path, onClick) {{
            const option = document.createElement('div');
            option.className = 'avatar-option';
            option.onclick = onClick;
            
            const img = document.createElement('img');
            img.src = path;
            img.alt = 'Avatar';
            
            option.appendChild(img);
            return option;
        }}

        function checkStartButton() {{
            const startButton = document.getElementById('startButton');
            startButton.disabled = !(gameState.gameMode && selectedPlayer1Avatar && selectedPlayer2Avatar);
        }}

        document.getElementById('startButton').addEventListener('click', startGame);

        function startGame() {{
            gameState.player1Avatar = selectedPlayer1Avatar;
            gameState.player2Avatar = selectedPlayer2Avatar;
            
            document.getElementById('avatarSelection').style.display = 'none';
            document.getElementById('gameBoard').classList.add('active');
            
            document.getElementById('player1Avatar').src = gameState.player1Avatar;
            document.getElementById('player2Avatar').src = gameState.player2Avatar;
            
            // Update player names based on game mode
            const player2Name = gameState.gameMode === 'vsComputer' ? 'Computer' : 'Spiller 2';
            document.querySelector('#player2Info .player-name').textContent = player2Name;
            document.getElementById('player1Info').querySelector('.player-name').textContent = 
                gameState.gameMode === 'twoPlayer' ? 'Spiller 1' : 'Dig';
            
            initGame();
        }}

        function initGame() {{
            gameState.pits = new Array(14).fill(0);
            
            for (let i = 0; i < 6; i++) {{
                gameState.pits[i] = STONES_PER_PIT;
                gameState.pits[i + 7] = STONES_PER_PIT;
            }}
            
            gameState.currentPlayer = 1;
            gameState.gameOver = false;
            
            renderBoard();
            updateTurnIndicator();
        }}

        function renderBoard() {{
            const player1Pits = document.getElementById('player1Pits');
            player1Pits.innerHTML = '';
            for (let i = 0; i < 6; i++) {{
                const pit = createPitElement(i, gameState.pits[i], 1);
                player1Pits.appendChild(pit);
            }}

            const player2Pits = document.getElementById('player2Pits');
            player2Pits.innerHTML = '';
            for (let i = 12; i >= 7; i--) {{
                const pit = createPitElement(i, gameState.pits[i], 2);
                player2Pits.appendChild(pit);
            }}

            updateKalahaStones('kalaha1', gameState.pits[6]);
            updateKalahaStones('kalaha2', gameState.pits[13]);
        }}

        function updateKalahaStones(kalahaId, count) {{
            const kalahaElement = document.getElementById(kalahaId);
            kalahaElement.innerHTML = '';
            
            const displayCount = Math.min(count, 30);
            for (let i = 0; i < displayCount; i++) {{
                const stone = document.createElement('div');
                stone.className = 'stone';
                kalahaElement.appendChild(stone);
            }}
            
            if (count > 30) {{
                const counter = document.createElement('div');
                counter.style.cssText = 'color: white; font-size: 24px; font-weight: bold; margin-top: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);';
                counter.textContent = `×${{count}}`;
                kalahaElement.appendChild(counter);
            }}
        }}

        function createPitElement(index, stones, player) {{
            const pit = document.createElement('div');
            pit.className = 'pit';
            pit.dataset.index = index;

            const pitNumber = document.createElement('div');
            pitNumber.className = 'pit-index';
            pitNumber.textContent = player === 1 ? (index + 1) : (index - 6);
            pit.appendChild(pitNumber);

            const stonesDiv = document.createElement('div');
            stonesDiv.className = 'pit-stones';
            
            const displayCount = Math.min(stones, 20);
            for (let i = 0; i < displayCount; i++) {{
                const stone = document.createElement('div');
                stone.className = 'stone';
                stonesDiv.appendChild(stone);
            }}
            
            if (stones > 20) {{
                const counter = document.createElement('div');
                counter.style.cssText = 'color: #1a5490; font-size: 18px; font-weight: bold; background: rgba(255,255,255,0.9); padding: 3px 8px; border-radius: 10px; margin-top: 5px;';
                counter.textContent = `×${{stones}}`;
                stonesDiv.appendChild(counter);
            }}
            
            pit.appendChild(stonesDiv);

            if (player === gameState.currentPlayer && !gameState.gameOver) {{
                pit.addEventListener('click', () => makeMove(index));
            }} else {{
                pit.classList.add('disabled');
            }}

            return pit;
        }}

        function makeMove(pitIndex) {{
            if (gameState.gameOver) return;
            
            if (!isValidMove(pitIndex)) {{
                updateStatusMessage('Ugyldigt træk! Vælg en anden hul.');
                return;
            }}

            updateStatusMessage('');

            let stones = gameState.pits[pitIndex];
            gameState.pits[pitIndex] = 0;

            let currentIndex = pitIndex;
            while (stones > 0) {{
                currentIndex = (currentIndex + 1) % 14;
                
                if (gameState.currentPlayer === 1 && currentIndex === 13) continue;
                if (gameState.currentPlayer === 2 && currentIndex === 6) continue;
                
                gameState.pits[currentIndex]++;
                stones--;
            }}

            if (isGameOver()) {{
                endGame();
                return;
            }}

            gameState.currentPlayer = gameState.currentPlayer === 1 ? 2 : 1;
            
            renderBoard();
            updateTurnIndicator();

            if (gameState.gameMode === 'vsComputer' && gameState.currentPlayer === 2 && !gameState.gameOver) {{
                setTimeout(computerMove, 1000);
            }}
        }}

        function computerMove() {{
            updateStatusMessage('Computer tænker...');
            
            const validMoves = [];
            for (let i = 7; i <= 12; i++) {{
                if (gameState.pits[i] > 0) {{
                    validMoves.push(i);
                }}
            }}

            if (validMoves.length === 0) {{
                endGame();
                return;
            }}

            const randomMove = validMoves[Math.floor(Math.random() * validMoves.length)];
            
            setTimeout(() => {{
                updateStatusMessage('');
                makeMove(randomMove);
            }}, 500);
        }}

        function isValidMove(pitIndex) {{
            if (gameState.currentPlayer === 1 && (pitIndex < 0 || pitIndex > 5)) return false;
            if (gameState.currentPlayer === 2 && (pitIndex < 7 || pitIndex > 12)) return false;
            
            return gameState.pits[pitIndex] > 0;
        }}

        function isGameOver() {{
            const player1Empty = gameState.pits.slice(0, 6).every(stones => stones === 0);
            const player2Empty = gameState.pits.slice(7, 13).every(stones => stones === 0);
            
            return player1Empty || player2Empty;
        }}

        function endGame() {{
            gameState.gameOver = true;

            let player1Remaining = gameState.pits.slice(0, 6).reduce((a, b) => a + b, 0);
            let player2Remaining = gameState.pits.slice(7, 13).reduce((a, b) => a + b, 0);
            
            gameState.pits[6] += player1Remaining;
            gameState.pits[13] += player2Remaining;

            for (let i = 0; i < 6; i++) {{
                gameState.pits[i] = 0;
                gameState.pits[i + 7] = 0;
            }}

            renderBoard();

            const player1Score = gameState.pits[6];
            const player2Score = gameState.pits[13];
            const player1Name = gameState.gameMode === 'twoPlayer' ? 'Spiller 1' : 'Du';
            const player2Name = gameState.gameMode === 'vsComputer' ? 'Computer' : 'Spiller 2';

            const winnerOverlay = document.getElementById('winnerOverlay');
            const winnerTitle = document.getElementById('winnerTitle');
            const winnerAvatar = document.getElementById('winnerAvatar');
            const winnerScore = document.getElementById('winnerScore');

            if (player1Score > player2Score) {{
                winnerTitle.textContent = gameState.gameMode === 'twoPlayer' ? '🎉 Spiller 1 vandt! 🎉' : '🎉 Du vandt! 🎉';
                winnerAvatar.src = gameState.player1Avatar;
                winnerScore.textContent = `${{player1Score}} - ${{player2Score}}`;
            }} else if (player2Score > player1Score) {{
                winnerTitle.textContent = gameState.gameMode === 'twoPlayer' ? '🎉 Spiller 2 vandt! 🎉' : 'Computer vandt!';
                winnerAvatar.src = gameState.player2Avatar;
                winnerScore.textContent = `${{player2Score}} - ${{player1Score}}`;
            }} else {{
                winnerTitle.textContent = 'Uafgjort!';
                winnerAvatar.src = gameState.player1Avatar;
                winnerScore.textContent = `${{player1Score}} - ${{player2Score}}`;
            }}

            winnerOverlay.classList.add('active');
        }}

        function updateTurnIndicator() {{
            const player1Turn = document.getElementById('player1Turn');
            const player2Turn = document.getElementById('player2Turn');
            const player2Name = gameState.gameMode === 'vsComputer' ? 'Computer' : 'Spiller 2';

            if (gameState.currentPlayer === 1) {{
                player1Turn.textContent = '← Din tur';
                player1Turn.style.opacity = '1';
                player2Turn.textContent = '';
                player2Turn.style.opacity = '0.5';
            }} else {{
                player1Turn.textContent = '';
                player1Turn.style.opacity = '0.5';
                player2Turn.textContent = `${{player2Name}}'s tur →`;
                player2Turn.style.opacity = '1';
            }}
        }}

        function updateStatusMessage(message) {{
            document.getElementById('statusMessage').textContent = message;
        }}

        // Initialize avatar selection on page load
        initAvatarSelection();
    </script>
</body>
</html>'''

# Write output file
output_file = base_dir / "kalaha_embedded.html"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"\n✓ Generated: {output_file}")
print(f"  File size: {output_file.stat().st_size / 1024:.1f} KB")
print("\nÅbn kalaha_embedded.html i din browser!")