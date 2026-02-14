#!/usr/bin/env python3
import base64
from pathlib import Path

# Paths
base_dir = Path(__file__).parent
paw_patrol = base_dir / "paw_patrol"

# Read and encode images
def img_to_b64(filename):
    path = paw_patrol / filename
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode()
    ext = path.suffix.lower()
    mime = {'jpg': 'jpeg', 'jpeg': 'jpeg', 'png': 'png', 'webp': 'webp'}
    return f"data:image/{mime.get(ext.strip('.'), 'jpeg')};base64,{data}"

print("Indlæser billeder...")
bg = img_to_b64("Adventure_Bay_%28S3%29.webp")
av1 = img_to_b64("images (1).jpeg")
av2 = img_to_b64("images (2).jpeg")
av5 = img_to_b64("images (5).jpeg")
av6 = img_to_b64("images (6).jpeg")
av8 = img_to_b64("images (8).jpeg")
print("✓ Alle billeder indlæst!")

# HTML template
html = f'''<!DOCTYPE html>
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
            background-image: url('{bg}');
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
            max-width: 1200px;
            width: 100%;
        }}

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
            grid-template-columns: 120px 1fr 120px;
            gap: 20px;
            margin: 30px 0;
            background: linear-gradient(135deg, #f4a460 0%, #daa520 50%, #f4a460 100%);
            padding: 40px 30px;
            border-radius: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
            border: 5px solid #cd853f;
        }}

        .kalaha {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: rgba(139, 69, 19, 0.3);
            border-radius: 25px;
            padding: 30px 20px;
            min-height: 400px;
            box-shadow: inset 0 4px 15px rgba(0, 0, 0, 0.3);
            border: 3px solid rgba(101, 67, 33, 0.5);
        }}

        .kalaha-label {{
            color: #654321;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.5);
        }}

        .kalaha-stones {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
            align-items: center;
            min-height: 200px;
            width: 80px;
        }}

        .stone {{
            width: 18px;
            height: 18px;
            background: #8B4513;
            border-radius: 50%;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
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

        .stone-highlight {{
            animation: stoneHighlight 0.6s ease-out;
        }}

        @keyframes stoneHighlight {{
            0% {{
                transform: scale(2);
                opacity: 0;
                background: #FFD700;
            }}
            50% {{
                transform: scale(1.5);
                opacity: 1;
            }}
            100% {{
                transform: scale(1);
                opacity: 1;
                background: #8B4513;
            }}
        }}

        .stone.new-stone {{
            animation: stoneDrop 0.5s ease-out;
        }}

        @keyframes stoneDrop {{
            0% {{
                transform: translateY(-30px) scale(1.5);
                opacity: 0;
            }}
            50% {{
                transform: translateY(0px) scale(1.2);
            }}
            100% {{
                transform: translateY(0px) scale(1);
                opacity: 1;
            }}
        }}

        .pits-container {{
            display: flex;
            flex-direction: column;
            gap: 20px;
            justify-content: center;
        }}

        .pits-row {{
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 15px;
        }}

        .pit {{
            background: rgba(139, 69, 19, 0.2);
            border: 3px solid rgba(101, 67, 33, 0.5);
            border-radius: 50%;
            aspect-ratio: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.2);
            position: relative;
            padding: 10px;
            min-height: 100px;
        }}

        .pit:hover:not(.disabled) {{
            transform: translateY(-5px);
            box-shadow: 0 6px 20px rgba(139, 69, 19, 0.5);
            background: rgba(139, 69, 19, 0.3);
        }}

        .pit.disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}

        .pit.active {{
            animation: pulseActive 0.5s ease-in-out;
            background: rgba(255, 215, 0, 0.5);
            border-color: #FFD700;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.8);
        }}

        @keyframes pulseActive {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); }}
        }}

        .pit.receiving {{
            animation: receiving 0.3s ease-out;
        }}

        @keyframes receiving {{
            0% {{ background: rgba(255, 215, 0, 0.8); }}
            100% {{ background: rgba(139, 69, 19, 0.2); }}
        }}

        .kalaha.receiving {{
            animation: kalahaReceiving 0.3s ease-out;
        }}

        @keyframes kalahaReceiving {{
            0% {{ background: rgba(255, 215, 0, 0.8); }}
            100% {{ background: rgba(139, 69, 19, 0.3); }}
        }}

        .kalaha.extra-turn {{
            animation: extraTurn 1s ease-in-out;
        }}

        @keyframes extraTurn {{
            0%, 100% {{ 
                background: rgba(139, 69, 19, 0.3);
                transform: scale(1);
            }}
            25% {{ 
                background: rgba(255, 215, 0, 0.9);
                transform: scale(1.05);
            }}
            50% {{ 
                background: rgba(50, 205, 50, 0.7);
                transform: scale(1.1);
            }}
            75% {{ 
                background: rgba(255, 215, 0, 0.9);
                transform: scale(1.05);
            }}
        }}

        .pit-index {{
            position: absolute;
            top: 5px;
            font-size: 14px;
            color: #654321;
            font-weight: bold;
            background: rgba(255, 255, 255, 0.7);
            padding: 2px 6px;
            border-radius: 8px;
        }}

        .pit-stones {{
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
            justify-content: center;
            align-items: center;
            width: 100%;
            height: 100%;
            padding: 5px;
        }}

        .pit .stone {{
            width: 14px;
            height: 14px;
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
        <div class="avatar-selection" id="avatarSelection">
            <h1>🐾 Paw Patrol Kalaha 🐾</h1>
            
            <h2>Vælg spiltype:</h2>
            <div class="mode-selector">
                <button class="mode-button" id="vsComputerBtn">Mod Computer</button>
                <button class="mode-button" id="twoPlayerBtn">2 Spillere</button>
            </div>
            
            <div id="nameSection" style="display: none; margin: 20px 0;">
                <div style="display: flex; gap: 20px; justify-content: center; align-items: center;">
                    <div>
                        <label for="player1Name" style="display: block; margin-bottom: 8px; font-weight: bold; color: #1a5490;">Spiller 1 navn:</label>
                        <input type="text" id="player1Name" placeholder="Indtast navn" maxlength="15" 
                               style="padding: 10px; font-size: 18px; border: 2px solid #1a5490; border-radius: 10px; width: 200px;">
                    </div>
                    <div id="player2NameDiv">
                        <label for="player2Name" style="display: block; margin-bottom: 8px; font-weight: bold; color: #1a5490;">Spiller 2 navn:</label>
                        <input type="text" id="player2Name" placeholder="Indtast navn" maxlength="15"
                               style="padding: 10px; font-size: 18px; border: 2px solid #1a5490; border-radius: 10px; width: 200px;">
                    </div>
                </div>
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
                <div class="kalaha">
                    <div class="kalaha-label">Computer</div>
                    <div class="kalaha-stones" id="kalaha2"></div>
                </div>

                <div class="pits-container">
                    <div class="pits-row" id="player2Pits"></div>
                    <div class="pits-row" id="player1Pits"></div>
                </div>

                <div class="kalaha">
                    <div class="kalaha-label">Dig</div>
                    <div class="kalaha-stones" id="kalaha1"></div>
                </div>
            </div>
        </div>

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
        const STONES_PER_PIT = 6;
        const avatarPaths = ['{av1}', '{av2}', '{av5}', '{av6}', '{av8}'];
        let gameState = {{pits: [], currentPlayer: 1, player1Avatar: null, player2Avatar: null, gameOver: false, gameMode: null, animating: false, player1Name: '', player2Name: ''}};
        let selectedPlayer1Avatar = null;
        let selectedPlayer2Avatar = null;

        function initAvatarSelection() {{
            const p1Grid = document.getElementById('player1AvatarGrid');
            const p2Grid = document.getElementById('player2AvatarGrid');
            document.getElementById('vsComputerBtn').onclick = () => selectGameMode('vsComputer');
            document.getElementById('twoPlayerBtn').onclick = () => selectGameMode('twoPlayer');

            avatarPaths.forEach(path => {{
                p1Grid.appendChild(createAvatarOption(path, () => {{
                    document.querySelectorAll('#player1AvatarGrid .avatar-option').forEach(o => o.classList.remove('selected'));
                    event.currentTarget.classList.add('selected');
                    selectedPlayer1Avatar = path;
                    checkStartButton();
                }}));
                p2Grid.appendChild(createAvatarOption(path, () => {{
                    document.querySelectorAll('#player2AvatarGrid .avatar-option').forEach(o => o.classList.remove('selected'));
                    event.currentTarget.classList.add('selected');
                    selectedPlayer2Avatar = path;
                    checkStartButton();
                }}));
            }});
        }}

        function selectGameMode(mode) {{
            gameState.gameMode = mode;
            document.querySelectorAll('.mode-button').forEach(b => b.classList.remove('selected'));
            document.getElementById(mode === 'vsComputer' ? 'vsComputerBtn' : 'twoPlayerBtn').classList.add('selected');
            document.getElementById('player2Label').textContent = mode === 'vsComputer' ? "Computer's avatar:" : "Spiller 2 - Vælg din avatar:";
            
            // Vis/skjul navne sektion
            document.getElementById('nameSection').style.display = 'block';
            document.getElementById('player2NameDiv').style.display = mode === 'vsComputer' ? 'none' : 'block';
            
            checkStartButton();
        }}

        function createAvatarOption(path, onClick) {{
            const opt = document.createElement('div');
            opt.className = 'avatar-option';
            opt.onclick = onClick;
            const img = document.createElement('img');
            img.src = path;
            opt.appendChild(img);
            return opt;
        }}

        function checkStartButton() {{
            const player1Name = document.getElementById('player1Name') ? document.getElementById('player1Name').value.trim() : '';
            const player2Name = gameState.gameMode === 'vsComputer' ? 'Computer' : (document.getElementById('player2Name') ? document.getElementById('player2Name').value.trim() : '');
            const hasNames = player1Name.length > 0 && player2Name.length > 0;
            document.getElementById('startButton').disabled = !(gameState.gameMode && selectedPlayer1Avatar && selectedPlayer2Avatar && hasNames);
        }}

        document.getElementById('startButton').onclick = startGame;
        
        // Lyt til navne input
        document.addEventListener('DOMContentLoaded', () => {{
            const p1Input = document.getElementById('player1Name');
            const p2Input = document.getElementById('player2Name');
            if (p1Input) p1Input.addEventListener('input', checkStartButton);
            if (p2Input) p2Input.addEventListener('input', checkStartButton);
        }});

        function startGame() {{
            gameState.player1Avatar = selectedPlayer1Avatar;
            gameState.player2Avatar = selectedPlayer2Avatar;
            gameState.player1Name = document.getElementById('player1Name').value.trim() || 'Spiller 1';
            gameState.player2Name = gameState.gameMode === 'vsComputer' ? 'Computer' : (document.getElementById('player2Name').value.trim() || 'Spiller 2');
            
            document.getElementById('avatarSelection').style.display = 'none';
            document.getElementById('gameBoard').classList.add('active');
            document.getElementById('player1Avatar').src = gameState.player1Avatar;
            document.getElementById('player2Avatar').src = gameState.player2Avatar;
            
            document.querySelector('#player2Info .player-name').textContent = gameState.player2Name;
            document.getElementById('player1Info').querySelector('.player-name').textContent = gameState.player1Name;
            
            // Opdater kalaha labels
            const kalahaLabels = document.querySelectorAll('.kalaha-label');
            if (kalahaLabels[0]) kalahaLabels[0].textContent = gameState.player2Name;
            if (kalahaLabels[1]) kalahaLabels[1].textContent = gameState.player1Name;
            
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
            const p1Pits = document.getElementById('player1Pits');
            p1Pits.innerHTML = '';
            for (let i = 0; i < 6; i++) p1Pits.appendChild(createPitElement(i, gameState.pits[i], 1));
            const p2Pits = document.getElementById('player2Pits');
            p2Pits.innerHTML = '';
            for (let i = 12; i >= 7; i--) p2Pits.appendChild(createPitElement(i, gameState.pits[i], 2));
            updateKalahaStones('kalaha1', gameState.pits[6]);
            updateKalahaStones('kalaha2', gameState.pits[13]);
        }}

        function updateKalahaStones(id, count, highlightLast = false) {{
            const el = document.getElementById(id);
            el.innerHTML = '';
            const display = Math.min(count, 40);
            for (let i = 0; i < display; i++) {{
                const s = document.createElement('div');
                s.className = 'stone';
                if (highlightLast && i === display - 1) {{
                    s.classList.add('new-stone');
                }}
                el.appendChild(s);
            }}
            if (count > 40) {{
                const c = document.createElement('div');
                c.style.cssText = 'color:#654321;font-size:24px;font-weight:bold;margin-top:10px;background:rgba(255,255,255,0.8);padding:5px 10px;border-radius:10px;';
                c.textContent = `×${{count}}`;
                el.appendChild(c);
            }}
        }}

        function createPitElement(index, stones, player, highlightLast = false) {{
            const pit = document.createElement('div');
            pit.className = 'pit';
            pit.dataset.index = index;
            const num = document.createElement('div');
            num.className = 'pit-index';
            num.textContent = player === 1 ? (index + 1) : (index - 6);
            pit.appendChild(num);
            const stonesDiv = document.createElement('div');
            stonesDiv.className = 'pit-stones';
            const display = Math.min(stones, 25);
            for (let i = 0; i < display; i++) {{
                const s = document.createElement('div');
                s.className = 'stone';
                if (highlightLast && i === display - 1) {{
                    s.classList.add('new-stone');
                }}
                stonesDiv.appendChild(s);
            }}
            if (stones > 25) {{
                const c = document.createElement('div');
                c.style.cssText = 'color:#654321;font-size:16px;font-weight:bold;background:rgba(255,255,255,0.9);padding:2px 6px;border-radius:8px;margin-top:5px;';
                c.textContent = `×${{stones}}`;
                stonesDiv.appendChild(c);
            }}
            pit.appendChild(stonesDiv);
            if (player === gameState.currentPlayer && !gameState.gameOver) {{
                pit.onclick = () => makeMove(index);
            }} else {{
                pit.classList.add('disabled');
            }}
            return pit;
        }}

        function makeMove(pitIndex) {{
            if (gameState.gameOver || gameState.animating || !isValidMove(pitIndex)) return;
            
            gameState.animating = true;
            
            // Highlight det valgte hul
            const selectedPit = document.querySelector(`.pit[data-index="${{pitIndex}}"]`);
            if (selectedPit) selectedPit.classList.add('active');
            
            let stones = gameState.pits[pitIndex];
            gameState.pits[pitIndex] = 0;
            
            // Fjern stenene visuelt fra det valgte hul
            if (selectedPit) {{
                const stonesDiv = selectedPit.querySelector('.pit-stones');
                if (stonesDiv) stonesDiv.innerHTML = '';
            }}
            
            let curr = pitIndex;
            
            // Animér sten-bevægelser step-by-step
            let step = 0;
            let lastPosition = -1;
            const animateStep = () => {{
                if (step >= stones) {{
                    // Alle sten fra hånden er placeret
                    const isKalaha = lastPosition === 6 || lastPosition === 13;
                    const landedInNonEmptyPit = !isKalaha && lastPosition >= 0 && gameState.pits[lastPosition] > 1;
                    
                    if (landedInNonEmptyPit) {{
                        // FORTSÆT! Tag alle stenene fra dette pit
                        setTimeout(() => {{
                            updateStatusMessage('💫 Fortsætter med stenene!');
                            stones = gameState.pits[lastPosition];
                            gameState.pits[lastPosition] = 0;
                            
                            // Fjern stenene visuelt
                            const pit = document.querySelector(`.pit[data-index="${{lastPosition}}"]`);
                            if (pit) {{
                                pit.classList.add('active');
                                const stonesDiv = pit.querySelector('.pit-stones');
                                if (stonesDiv) stonesDiv.innerHTML = '';
                                setTimeout(() => pit.classList.remove('active'), 600);
                            }}
                            
                            curr = lastPosition;
                            step = 0;
                            setTimeout(animateStep, 800);
                        }}, 600);
                        return;
                    }}
                    
                    // STOP - landede i tomt pit eller kalaha
                    setTimeout(() => {{
                        gameState.animating = false;
                        updateStatusMessage('');
                        if (isGameOver()) {{ endGame(); return; }}
                        
                        // Tjek om sidste sten landede i eget kalaha (ekstra tur)
                        const playerKalaha = gameState.currentPlayer === 1 ? 6 : 13;
                        const gotExtraTurn = lastPosition === playerKalaha;
                        
                        if (gotExtraTurn) {{
                            // Ekstra tur - samme spiller fortsætter
                            updateStatusMessage('🎉 Ekstra tur! 🎉');
                            
                            // Animér kalaha med ekstra tur effekt
                            const kalahaElement = document.querySelector(`#kalaha${{gameState.currentPlayer}}`);
                            if (kalahaElement && kalahaElement.parentElement) {{
                                kalahaElement.parentElement.classList.add('extra-turn');
                                setTimeout(() => {{
                                    kalahaElement.parentElement.classList.remove('extra-turn');
                                }}, 1000);
                            }}
                            
                            setTimeout(() => updateStatusMessage(''), 2000);
                            renderBoard();
                            updateTurnIndicator();
                        }} else {{
                            // Normal tur - skift spiller
                            gameState.currentPlayer = gameState.currentPlayer === 1 ? 2 : 1;
                            renderBoard();
                            updateTurnIndicator();
                            if (gameState.gameMode === 'vsComputer' && gameState.currentPlayer === 2 && !gameState.gameOver) {{
                                setTimeout(computerMove, 1000);
                            }}
                        }}
                    }}, 500);
                    return;
                }}
                
                // Find næste gyldige position
                curr = (curr + 1) % 14;
                if (gameState.currentPlayer === 1 && curr === 13) {{
                    curr = (curr + 1) % 14;
                }}
                if (gameState.currentPlayer === 2 && curr === 6) {{
                    curr = (curr + 1) % 14;
                }}
                
                lastPosition = curr; // Husk sidste position
                
                // Placer sten i game state
                gameState.pits[curr]++;
                
                // Tilføj sten visuelt
                if (curr === 6 || curr === 13) {{
                    // Det er en kalaha
                    const kalahaId = curr === 6 ? 'kalaha1' : 'kalaha2';
                    const kalaha = document.getElementById(kalahaId);
                    if (kalaha) {{
                        kalaha.parentElement.classList.add('receiving');
                        setTimeout(() => kalaha.parentElement.classList.remove('receiving'), 600);
                        
                        // Tilføj en ny sten
                        const newStone = document.createElement('div');
                        newStone.className = 'stone stone-highlight';
                        kalaha.appendChild(newStone);
                    }}
                }} else {{
                    // Det er et almindeligt pit
                    const pit = document.querySelector(`.pit[data-index="${{curr}}"]`);
                    if (pit) {{
                        pit.classList.add('receiving');
                        setTimeout(() => pit.classList.remove('receiving'), 600);
                        
                        const stonesDiv = pit.querySelector('.pit-stones');
                        if (stonesDiv) {{
                            // Tilføj en ny sten
                            const newStone = document.createElement('div');
                            newStone.className = 'stone stone-highlight';
                            stonesDiv.appendChild(newStone);
                            
                            // Opdater tæller hvis der er for mange sten
                            const stoneCount = gameState.pits[curr];
                            const existingCounter = stonesDiv.querySelector('div[style*="font-weight:bold"]');
                            if (existingCounter) existingCounter.remove();
                            
                            if (stoneCount > 25) {{
                                const counter = document.createElement('div');
                                counter.style.cssText = 'color:#654321;font-size:16px;font-weight:bold;background:rgba(255,255,255,0.9);padding:2px 6px;border-radius:8px;margin-top:5px;';
                                counter.textContent = `×${{stoneCount}}`;
                                stonesDiv.appendChild(counter);
                            }}
                        }}
                    }}
                }}
                
                step++;
                setTimeout(animateStep, 1000); // 1 sekund mellem hver sten
            }};
            
            animateStep();
        }}

        function computerMove() {{
            updateStatusMessage('Computer tænker...');
            const valid = [];
            for (let i = 7; i <= 12; i++) if (gameState.pits[i] > 0) valid.push(i);
            if (valid.length === 0) {{ endGame(); return; }}
            setTimeout(() => {{
                updateStatusMessage('Computer laver sit træk...');
                makeMove(valid[Math.floor(Math.random() * valid.length)]);
            }}, 800);
        }}

        function isValidMove(i) {{
            if (gameState.currentPlayer === 1 && (i < 0 || i > 5)) return false;
            if (gameState.currentPlayer === 2 && (i < 7 || i > 12)) return false;
            return gameState.pits[i] > 0;
        }}

        function isGameOver() {{
            return gameState.pits.slice(0, 6).every(s => s === 0) || gameState.pits.slice(7, 13).every(s => s === 0);
        }}

        function endGame() {{
            gameState.gameOver = true;
            gameState.pits[6] += gameState.pits.slice(0, 6).reduce((a, b) => a + b, 0);
            gameState.pits[13] += gameState.pits.slice(7, 13).reduce((a, b) => a + b, 0);
            for (let i = 0; i < 6; i++) {{ gameState.pits[i] = 0; gameState.pits[i + 7] = 0; }}
            renderBoard();
            const s1 = gameState.pits[6], s2 = gameState.pits[13];
            document.getElementById('winnerTitle').textContent = s1 > s2 ? `🎉 ${{gameState.player1Name}} vandt! 🎉` : (s2 > s1 ? `🎉 ${{gameState.player2Name}} vandt! 🎉` : 'Uafgjort!');
            document.getElementById('winnerAvatar').src = s1 > s2 ? gameState.player1Avatar : (s2 > s1 ? gameState.player2Avatar : gameState.player1Avatar);
            document.getElementById('winnerScore').textContent = s1 > s2 ? `${{s1}} - ${{s2}}` : (s2 > s1 ? `${{s2}} - ${{s1}}` : `${{s1}} - ${{s2}}`);
            document.getElementById('winnerOverlay').classList.add('active');
        }}

        function updateTurnIndicator() {{
            const p1 = document.getElementById('player1Turn'), p2 = document.getElementById('player2Turn');
            if (gameState.currentPlayer === 1) {{
                p1.textContent = `← ${{gameState.player1Name}}'s tur`; p1.style.opacity = '1';
                p2.textContent = ''; p2.style.opacity = '0.5';
            }} else {{
                p1.textContent = ''; p1.style.opacity = '0.5';
                p2.textContent = `${{gameState.player2Name}}'s tur →`; p2.style.opacity = '1';
            }}
        }}

        function updateStatusMessage(msg) {{
            document.getElementById('statusMessage').textContent = msg;
        }}

        initAvatarSelection();
    </script>
</body>
</html>'''

output = base_dir / "kalaha.html"
with open(output, 'w', encoding='utf-8') as f:
    f.write(html)

size_kb = output.stat().st_size / 1024
print(f"\n✓ Genereret: {output}")
print(f"  Størrelse: {size_kb:.0f} KB")
print("\nÅbn kalaha.html i din browser - alle billeder er nu embedded!")