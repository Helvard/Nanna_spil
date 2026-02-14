#!/usr/bin/env python3
"""
Æggespil - Billede Embedder
Gem dette script i samme mappe som dine Paw Patrol billeder og kør det med: python3 generate_aeggespil.py
"""

import base64
import os

def image_to_data_url(filepath):
    """Konverter billede til data URL"""
    with open(filepath, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
        ext = filepath.split('.')[-1].lower()
        mime = 'image/webp' if ext == 'webp' else 'image/jpeg'
        return f'data:{mime};base64,{data}'

# Få stien til scriptet
script_dir = os.path.dirname(os.path.abspath(__file__))

# Billedmappen er i paw_patrol undermappe
image_dir = os.path.join(script_dir, 'paw_patrol')

# Definer alle billeder
images = {
    'CHICKALETTA': 'Chickaletta_Official_Vector_Art.webp',
    'BAGGRUND': 'Æggespil_baggrund.jpeg',
    'TALLERKEN1': 'tallerken_paw.jpeg',
    'TALLERKEN2': 'tallerken_2.jpeg',
    'TALLERKEN3': 'Tallerken_3.jpeg',
    'TALLERKEN4': 'Tallerken_4.jpeg',
    'TALLERKEN5': 'Tallerken_5.jpeg',
    'STEGEPANDE': 'Stegepande.jpeg',
    'CURSOR': 'cursor_badge.jpeg',
    'AVATAR1': 'download (1).jpeg',
    'AVATAR2': 'download (2).jpeg',
    'AVATAR3': 'download (3).jpeg',
    'AVATAR4': 'download (4).jpeg',
    'AVATAR5': 'images (1).jpeg',
    'AVATAR6': 'images (2).jpeg',
    'AVATAR7': 'images (3).jpeg',
    'AVATAR8': 'images (4).jpeg',
    'AVATAR9': 'images (5).jpeg'
}

# Læs og konverter alle billeder
print(f"Læser billeder fra: {image_dir}")
image_data = {}
for key, filename in images.items():
    filepath = os.path.join(image_dir, filename)
    try:
        image_data[key] = image_to_data_url(filepath)
        print(f'✓ {key} ({filename})')
    except Exception as e:
        print(f'✗ {key} ({filename}): {e}')
        exit(1)

print(f"\nAlle {len(image_data)} billeder læst successfully! (inkl. 9 avatars + cursor)")
print("Genererer HTML...")

# HTML template
html_template = '''<!DOCTYPE html>
<html lang="da">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Æggespillet - Paw Patrol</title>
    <style>
        * { 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box;
            cursor: url('{CURSOR}') 16 16, url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><circle cx="16" cy="16" r="15" fill="%23667eea" stroke="white" stroke-width="2"/><text x="16" y="22" text-anchor="middle" font-size="18" fill="white">🐾</text></svg>') 16 16, pointer;
        }
        body {
            font-family: 'Comic Sans MS', cursive, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .game-container { max-width: 1400px; width: 100%; }
        .start-screen {
            background: white;
            border-radius: 30px;
            padding: 60px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .start-screen h1 {
            font-size: 72px;
            color: #ff6b6b;
            text-shadow: 3px 3px 0 #ffd93d;
            margin-bottom: 40px;
        }
        .chickaletta {
            width: 200px;
            height: auto;
            margin: 30px 0;
            animation: bounce 2s infinite;
        }
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
        .player-selection { margin: 40px 0; }
        .player-selection h2 {
            font-size: 36px;
            color: #333;
            margin-bottom: 30px;
        }
        
        /* Avatar valg skærm */
        .avatar-selection {
            display: none;
            background: white;
            border-radius: 30px;
            padding: 60px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .avatar-selection h1 {
            font-size: 48px;
            color: #ff6b6b;
            margin-bottom: 20px;
        }
        .avatar-selection h2 {
            font-size: 32px;
            color: #333;
            margin-bottom: 30px;
        }
        .avatar-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 30px;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        .avatar-option {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            border: 5px solid #ddd;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            background: white;
            overflow: hidden;
            padding: 10px;
        }
        .avatar-option img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            pointer-events: none;
        }
        .avatar-option:hover {
            transform: scale(1.1);
            border-color: #667eea;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        .avatar-option.selected {
            border-color: #ff6b6b;
            box-shadow: 0 0 30px rgba(255, 107, 107, 0.6);
            transform: scale(1.15);
        }
        .player-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 10px;
            vertical-align: middle;
            border: 3px solid;
            overflow: hidden;
            object-fit: cover;
        }
        .player-buttons {
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
        }
        .player-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 30px 50px;
            font-size: 32px;
            border-radius: 20px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            font-weight: bold;
        }
        .player-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .game-screen { display: none; }
        .game-board {
            background: white;
            border-radius: 30px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            position: relative;
        }
        .background-image {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 30px;
            opacity: 0.75;
            pointer-events: none;
        }
        .game-content {
            position: relative;
            z-index: 1;
        }
        .players-info {
            display: flex;
            justify-content: space-around;
            margin-bottom: 30px;
            gap: 20px;
            flex-wrap: wrap;
        }
        .player-info {
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 15px;
            border: 4px solid #ddd;
            min-width: 200px;
        }
        .player-info.active {
            border-color: #ff6b6b;
            box-shadow: 0 0 20px rgba(255, 107, 107, 0.5);
            animation: pulse 1s infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        .player-info h3 {
            font-size: 24px;
            color: #333;
            margin-bottom: 15px;
        }
        .player-basket {
            display: grid;
            grid-template-columns: repeat(13, 1fr);
            gap: 8px;
            margin-top: 15px;
            padding: 15px;
            background: linear-gradient(145deg, #f9f9f9, #e8e8e8);
            border-radius: 12px;
            box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);
        }
        .basket-slot {
            width: 35px;
            height: 35px;
            background: linear-gradient(145deg, #fff, #f5f5f5);
            border: 3px solid #ddd;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .basket-slot.filled {
            background: linear-gradient(145deg, #ffd93d, #ffb700);
            border-color: #ff9800;
            box-shadow: 0 3px 8px rgba(255, 152, 0, 0.4);
            transform: scale(1.05);
        }
        .egg-mini {
            width: 25px;
            height: 30px;
            background: radial-gradient(circle at 35% 35%, #f4a460, #d2691e);
            border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
            box-shadow: inset -2px -2px 4px rgba(0,0,0,0.2), 0 2px 4px rgba(0,0,0,0.2);
        }
        .play-area {
            background: rgba(255, 255, 255, 0.85);
            padding: 40px;
            border-radius: 20px;
            margin: 30px 0;
            backdrop-filter: blur(5px);
        }
        .plates-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 30px;
            margin-bottom: 40px;
        }
        .plate-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
        }
        .plate-number {
            font-size: 48px;
            font-weight: bold;
            color: #333;
            text-shadow: 2px 2px 0 #ffd93d;
        }
        .plate {
            width: 150px;
            height: 150px;
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .plate:hover { transform: scale(1.1); }
        .egg-on-plate {
            width: 70px;
            height: 85px;
            background: radial-gradient(circle at 35% 35%, #f9d5a7, #f4a460, #d2691e);
            border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
            box-shadow: 
                inset -3px -3px 8px rgba(0,0,0,0.3),
                inset 3px 3px 8px rgba(255,255,255,0.5),
                0 8px 20px rgba(0,0,0,0.4);
            animation: eggWobble 2s infinite;
        }
        @keyframes eggWobble {
            0%, 100% { transform: rotate(-3deg); }
            50% { transform: rotate(3deg); }
        }
        .pan {
            grid-column: 2;
            width: 200px;
            height: 150px;
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
        }
        .controls {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 30px;
            flex-wrap: wrap;
        }
        .dice-area { text-align: center; }
        .dice {
            width: 140px;
            height: 140px;
            background: linear-gradient(145deg, #ffffff, #e6e6e6);
            border: 6px solid #2c3e50;
            border-radius: 25px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 80px;
            font-weight: bold;
            color: #2c3e50;
            margin: 0 auto 20px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.4), inset 0 2px 10px rgba(255,255,255,0.8);
            transition: transform 0.1s;
            position: relative;
            cursor: pointer;
        }
        .dice:hover {
            transform: scale(1.05);
        }
        .dice::before {
            content: '';
            position: absolute;
            top: 10px;
            left: 10px;
            right: 10px;
            bottom: 10px;
            border: 2px solid rgba(44, 62, 80, 0.1);
            border-radius: 15px;
            pointer-events: none;
        }
        .dice.rolling {
            animation: diceRoll 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }
        @keyframes diceRoll {
            0% { transform: rotate(0deg) scale(1); }
            25% { transform: rotate(180deg) scale(1.3) translateY(-20px); }
            50% { transform: rotate(360deg) scale(0.9) translateY(0px); }
            75% { transform: rotate(540deg) scale(1.2) translateY(-10px); }
            100% { transform: rotate(720deg) scale(1) translateY(0px); }
        }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 20px 40px;
            font-size: 28px;
            border-radius: 15px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            font-weight: bold;
        }
        .btn:hover:not(:disabled) {
            transform: scale(1.1);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .btn-end-turn {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        }
        .message {
            background: rgba(255, 235, 59, 0.92);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin: 20px 0;
            min-height: 70px;
            display: flex;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(3px);
        }
        .winner-screen {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        .winner-content {
            background: white;
            padding: 60px;
            border-radius: 30px;
            text-align: center;
            animation: winnerPop 0.5s;
        }
        @keyframes winnerPop {
            0% { transform: scale(0); }
            70% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        .winner-content h2 {
            font-size: 64px;
            color: #ff6b6b;
            margin-bottom: 30px;
            text-shadow: 3px 3px 0 #ffd93d;
        }
        .winner-content p {
            font-size: 36px;
            color: #333;
            margin-bottom: 40px;
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="start-screen" id="startScreen">
            <h1>🥚 Æggespillet 🥚</h1>
            <img src="{CHICKALETTA}" alt="Chickaletta" class="chickaletta">
            <div class="player-selection">
                <h2>Vælg antal spillere:</h2>
                <div class="player-buttons">
                    <button class="player-btn" onclick="showAvatarSelection(1)">1 Spiller<br>(vs Computer)</button>
                    <button class="player-btn" onclick="showAvatarSelection(2)">2 Spillere</button>
                    <button class="player-btn" onclick="showAvatarSelection(3)">3 Spillere</button>
                    <button class="player-btn" onclick="showAvatarSelection(4)">4 Spillere</button>
                </div>
            </div>
        </div>
        
        <div class="avatar-selection" id="avatarSelection">
            <h1>Vælg din avatar</h1>
            <h2 id="avatarPlayerName">Spiller 1</h2>
            <div class="avatar-grid">
                <div class="avatar-option" onclick="selectAvatar('{AVATAR1}', event)"><img src="{AVATAR1}"></div>
                <div class="avatar-option" onclick="selectAvatar('{AVATAR2}', event)"><img src="{AVATAR2}"></div>
                <div class="avatar-option" onclick="selectAvatar('{AVATAR3}', event)"><img src="{AVATAR3}"></div>
                <div class="avatar-option" onclick="selectAvatar('{AVATAR4}', event)"><img src="{AVATAR4}"></div>
                <div class="avatar-option" onclick="selectAvatar('{AVATAR5}', event)"><img src="{AVATAR5}"></div>
                <div class="avatar-option" onclick="selectAvatar('{AVATAR6}', event)"><img src="{AVATAR6}"></div>
                <div class="avatar-option" onclick="selectAvatar('{AVATAR7}', event)"><img src="{AVATAR7}"></div>
                <div class="avatar-option" onclick="selectAvatar('{AVATAR8}', event)"><img src="{AVATAR8}"></div>
                <div class="avatar-option" onclick="selectAvatar('{AVATAR9}', event)"><img src="{AVATAR9}"></div>
            </div>
        </div>
        <div class="game-screen" id="gameScreen">
            <div class="game-board">
                <img src="{BAGGRUND}" alt="Baggrund" class="background-image">
                <div class="game-content">
                    <div class="players-info" id="playersInfo"></div>
                    <div class="play-area">
                        <div class="plates-container">
                            <div class="plate-wrapper">
                                <div class="plate-number">1</div>
                                <div class="plate" id="plate1" style="background-image: url('{TALLERKEN1}')"></div>
                            </div>
                            <div class="plate-wrapper">
                                <div class="plate-number">2</div>
                                <div class="plate" id="plate2" style="background-image: url('{TALLERKEN2}')"></div>
                            </div>
                            <div class="plate-wrapper">
                                <div class="plate-number">3</div>
                                <div class="plate" id="plate3" style="background-image: url('{TALLERKEN3}')"></div>
                            </div>
                            <div class="plate-wrapper">
                                <div class="plate-number">4</div>
                                <div class="plate" id="plate4" style="background-image: url('{TALLERKEN4}')"></div>
                            </div>
                            <div class="plate-wrapper">
                                <div class="plate-number">6</div>
                                <div class="pan" id="plate6" style="background-image: url('{STEGEPANDE}')"></div>
                            </div>
                            <div class="plate-wrapper">
                                <div class="plate-number">5</div>
                                <div class="plate" id="plate5" style="background-image: url('{TALLERKEN5}')"></div>
                            </div>
                        </div>
                        <div class="message" id="message">Tryk på "Slå Terning" for at starte!</div>
                        <div class="controls">
                            <div class="dice-area">
                                <div class="dice" id="dice" onclick="rollDice()">?</div>
                                <button class="btn" id="rollBtn" onclick="rollDice()">Slå Terning</button>
                            </div>
                            <button class="btn btn-end-turn" id="endTurnBtn" onclick="endTurn()" disabled>Slut Tur</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="winner-screen" id="winnerScreen">
            <div class="winner-content">
                <h2>🎉 TILLYKKE! 🎉</h2>
                <p id="winnerText"></p>
                <button class="btn" onclick="location.reload()">Spil Igen</button>
            </div>
        </div>
    </div>
    <script>
        let gameState = {
            numPlayers: 0,
            players: [],
            currentPlayer: 0,
            plates: [false, false, false, false, false, false],
            lastRoll: 0,
            canRollAgain: true,
            canEndTurn: false,
            avatarSelectionMode: false,
            currentAvatarPlayer: 0,
            selectedAvatars: []
        };
        const playerColors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24'];
        const playerNames = ['Spiller 1', 'Spiller 2', 'Spiller 3', 'Spiller 4'];
        
        function showAvatarSelection(numPlayers) {
            gameState.numPlayers = numPlayers;
            gameState.selectedAvatars = [];
            gameState.currentAvatarPlayer = 0;
            gameState.avatarSelectionMode = true;
            
            // Hvis "1 Spiller" er valgt, betyder det 1 menneske + 1 computer = 2 spillere total
            const actualNumPlayers = numPlayers === 1 ? 2 : numPlayers;
            gameState.numPlayers = actualNumPlayers;
            
            document.getElementById('startScreen').style.display = 'none';
            document.getElementById('avatarSelection').style.display = 'block';
            
            updateAvatarSelectionTitle();
        }
        
        function updateAvatarSelectionTitle() {
            const playerNum = gameState.currentAvatarPlayer + 1;
            const isComputer = gameState.numPlayers === 2 && gameState.currentAvatarPlayer === 1;
            
            if (isComputer) {
                document.getElementById('avatarPlayerName').textContent = 'Computer';
            } else {
                document.getElementById('avatarPlayerName').textContent = 'Spiller ' + playerNum;
            }
        }
        
        function selectAvatar(avatar, event) {
            // Highlight selected
            document.querySelectorAll('.avatar-option').forEach(opt => opt.classList.remove('selected'));
            
            // Find the avatar-option div (parent of img)
            let target = event.target;
            if (target.tagName === 'IMG') {
                target = target.parentElement;
            }
            target.classList.add('selected');
            
            // Gem valg
            gameState.selectedAvatars[gameState.currentAvatarPlayer] = avatar;
            
            // Næste spiller eller start spil
            setTimeout(() => {
                gameState.currentAvatarPlayer++;
                
                if (gameState.currentAvatarPlayer >= gameState.numPlayers) {
                    // Alle har valgt - start spil
                    startGameWithAvatars();
                } else {
                    // Næste spillers tur til at vælge
                    document.querySelectorAll('.avatar-option').forEach(opt => opt.classList.remove('selected'));
                    updateAvatarSelectionTitle();
                }
            }, 300);
        }
        
        function startGameWithAvatars() {
            document.getElementById('avatarSelection').style.display = 'none';
            document.getElementById('gameScreen').style.display = 'block';
            
            // Opret spillere med avatars
            gameState.players = [];
            for (let i = 0; i < gameState.numPlayers; i++) {
                const isComputer = gameState.numPlayers === 2 && i === 1;
                gameState.players.push({
                    name: i === 0 ? 'Nanna' : (isComputer ? 'Computer' : playerNames[i]),
                    eggs: 7,
                    isComputer: isComputer,
                    avatar: gameState.selectedAvatars[i]
                });
            }
            
            console.log('Game started with avatars - Players:', gameState.players);
            
            renderPlayers();
            updateMessage(gameState.players[0].name + ' starter!');
        }
        
        function startGame(numPlayers) {
            gameState.numPlayers = numPlayers;
            gameState.players = [];
            
            // Hvis "1 Spiller" er valgt, betyder det 1 menneske + 1 computer = 2 spillere total
            const actualNumPlayers = numPlayers === 1 ? 2 : numPlayers;
            
            for (let i = 0; i < actualNumPlayers; i++) {
                gameState.players.push({
                    name: i === 0 ? 'Nanna' : (numPlayers === 1 ? 'Computer' : playerNames[i]),
                    eggs: 7,
                    isComputer: i > 0 && numPlayers === 1
                });
            }
            
            gameState.numPlayers = actualNumPlayers;
            
            console.log('Game started - Players:', gameState.players);
            
            document.getElementById('startScreen').style.display = 'none';
            document.getElementById('gameScreen').style.display = 'block';
            renderPlayers();
            updateMessage(gameState.players[0].name + ' starter!');
        }
        
        function renderPlayers() {
            const container = document.getElementById('playersInfo');
            container.innerHTML = '';
            gameState.players.forEach((player, index) => {
                const div = document.createElement('div');
                div.className = 'player-info' + (index === gameState.currentPlayer ? ' active' : '');
                div.id = 'player' + index;
                div.style.borderColor = playerColors[index];
                let basketHTML = '<div class="player-basket">';
                for (let i = 0; i < 13; i++) {
                    basketHTML += '<div class="basket-slot' + (i < player.eggs ? ' filled' : '') + '">';
                    if (i < player.eggs) basketHTML += '<div class="egg-mini"></div>';
                    basketHTML += '</div>';
                }
                basketHTML += '</div>';
                
                const avatarHTML = player.avatar ? 
                    `<img src="${player.avatar}" class="player-avatar" style="border-color: ${playerColors[index]}">` : '';
                
                div.innerHTML = `
                    <h3 style="color: ${playerColors[index]}">${avatarHTML}${player.name}${player.isComputer ? ' 🤖' : ''}</h3>
                    <p style="font-size: 20px; margin: 10px 0;">Æg: ${player.eggs}</p>
                    ${basketHTML}
                `;
                container.appendChild(div);
            });
        }
        
        function renderPlates() {
            for (let i = 0; i < 6; i++) {
                const plate = document.getElementById('plate' + (i + 1));
                if (gameState.plates[i]) {
                    if (!plate.querySelector('.egg-on-plate')) {
                        const egg = document.createElement('div');
                        egg.className = 'egg-on-plate';
                        plate.appendChild(egg);
                    }
                } else {
                    const egg = plate.querySelector('.egg-on-plate');
                    if (egg) egg.remove();
                }
            }
        }
        
        function updateMessage(text) {
            document.getElementById('message').textContent = text;
        }
        
        function rollDice() {
            if (!gameState.canRollAgain) return;
            
            const dice = document.getElementById('dice');
            const rollBtn = document.getElementById('rollBtn');
            
            rollBtn.disabled = true;
            document.getElementById('endTurnBtn').disabled = true;
            dice.classList.add('rolling');
            
            let rolls = 0;
            const rollInterval = setInterval(() => {
                dice.textContent = Math.floor(Math.random() * 6) + 1;
                rolls++;
                if (rolls >= 10) {
                    clearInterval(rollInterval);
                    const finalRoll = Math.floor(Math.random() * 6) + 1;
                    dice.textContent = finalRoll;
                    dice.classList.remove('rolling');
                    gameState.lastRoll = finalRoll;
                    handleRoll(finalRoll);
                }
            }, 100);
        }
        
        function handleRoll(roll) {
            const plateIndex = roll - 1;
            const currentPlayer = gameState.players[gameState.currentPlayer];
            
            if (!gameState.plates[plateIndex]) {
                // Tallerken er tom - placer æg
                if (currentPlayer.eggs > 0) {
                    gameState.plates[plateIndex] = true;
                    currentPlayer.eggs--;
                    renderPlates();
                    renderPlayers();
                    
                    if (roll === 6) {
                        // Stegepande - æg forsvinder permanent
                        gameState.plates[plateIndex] = false;
                        renderPlates();
                        updateMessage(currentPlayer.name + ' placerede et æg i stegepanden! Du kan vælge at slå igen eller slutte turen.');
                        gameState.canEndTurn = true;
                        gameState.canRollAgain = true;
                        if (!currentPlayer.isComputer) {
                            document.getElementById('endTurnBtn').disabled = false;
                            document.getElementById('rollBtn').disabled = false;
                        }
                    } else {
                        // Normal tallerken - kan vælge at fortsætte eller stoppe
                        updateMessage(currentPlayer.name + ' placerede et æg på tallerken ' + roll + '! Du kan vælge at slå igen eller slutte turen.');
                        gameState.canEndTurn = true;
                        gameState.canRollAgain = true;
                        if (!currentPlayer.isComputer) {
                            document.getElementById('endTurnBtn').disabled = false;
                            document.getElementById('rollBtn').disabled = false;
                        }
                    }
                    
                    // Tjek for sejr
                    if (currentPlayer.eggs === 0) {
                        showWinner(gameState.currentPlayer);
                        return;
                    }
                } else {
                    updateMessage(currentPlayer.name + ' har ingen æg tilbage!');
                    nextPlayer();
                }
            } else {
                // Tallerken har allerede et æg - tag det
                gameState.plates[plateIndex] = false;
                currentPlayer.eggs++;
                renderPlates();
                renderPlayers();
                updateMessage(currentPlayer.name + ' tog et æg fra tallerken ' + roll + '. Turen slutter.');
                gameState.canRollAgain = false;
                gameState.canEndTurn = false;
                
                setTimeout(() => nextPlayer(), 1500);
            }
        }
        
        function endTurn() {
            gameState.canRollAgain = false;
            gameState.canEndTurn = false;
            updateMessage(gameState.players[gameState.currentPlayer].name + ' slutter turen.');
            setTimeout(() => nextPlayer(), 1000);
        }
        
        function nextPlayer() {
            gameState.currentPlayer = (gameState.currentPlayer + 1) % gameState.numPlayers;
            gameState.canRollAgain = true;
            gameState.canEndTurn = false;
            document.getElementById('dice').textContent = '?';
            renderPlayers();
            
            const currentPlayer = gameState.players[gameState.currentPlayer];
            console.log('Next player:', currentPlayer.name, 'isComputer:', currentPlayer.isComputer);
            updateMessage(currentPlayer.name + 's tur!');
            
            // Hvis computer, disable knapper og start computer tur
            if (currentPlayer.isComputer) {
                console.log('Starting computer turn...');
                document.getElementById('rollBtn').disabled = true;
                document.getElementById('endTurnBtn').disabled = true;
                setTimeout(computerTurn, 2000);
            } else {
                // Menneske spiller - enable roll, disable end turn
                document.getElementById('rollBtn').disabled = false;
                document.getElementById('endTurnBtn').disabled = true;
            }
        }
        
        function computerTurn() {
            const currentPlayer = gameState.players[gameState.currentPlayer];
            console.log('computerTurn called, current player:', currentPlayer.name, 'isComputer:', currentPlayer.isComputer);
            
            if (!currentPlayer.isComputer) {
                console.log('ERROR: computerTurn called but player is not computer!');
                return;
            }
            
            console.log('Computer rolling dice...');
            rollDice();
            
            // Vent på at terning er færdig (ca 1.5 sek)
            setTimeout(() => {
                console.log('Computer evaluating result. canEndTurn:', gameState.canEndTurn, 'lastRoll:', gameState.lastRoll);
                
                // Tjek om vi kan fortsætte
                if (gameState.canEndTurn) {
                    // Vi har lige placeret et æg - skal vi fortsætte?
                    let shouldContinue = false;
                    
                    if (gameState.lastRoll === 6) {
                        // Stegepande - 70% chance for at fortsætte hvis > 2 æg
                        shouldContinue = Math.random() < 0.7 && currentPlayer.eggs > 2;
                        console.log('Stegepande decision. Eggs:', currentPlayer.eggs, 'Continue:', shouldContinue);
                    } else {
                        // Normal tallerken - 60% chance for at fortsætte hvis > 3 æg
                        shouldContinue = Math.random() < 0.6 && currentPlayer.eggs > 3;
                        console.log('Normal plate decision. Eggs:', currentPlayer.eggs, 'Continue:', shouldContinue);
                    }
                    
                    if (shouldContinue) {
                        console.log('Computer continues...');
                        setTimeout(computerTurn, 1500);
                    } else {
                        console.log('Computer ends turn');
                        setTimeout(endTurn, 1500);
                    }
                } else if (gameState.canRollAgain && currentPlayer.isComputer) {
                    // Kan stadig rulle (skulle ikke ske i denne version)
                    console.log('WARNING: Unexpected state - canRollAgain true but not canEndTurn');
                    setTimeout(computerTurn, 2000);
                }
            }, 1800);
        }
        
        function showWinner(playerIndex) {
            const winner = gameState.players[playerIndex];
            document.getElementById('winnerText').textContent = winner.name + ' har vundet!';
            document.getElementById('winnerScreen').style.display = 'flex';
        }
    </script>
</body>
</html>'''

# Indsæt billeder i template
final_html = html_template
for key, data_url in image_data.items():
    final_html = final_html.replace(f'{{{key}}}', data_url)

# Gem fil
output_file = os.path.join(script_dir, 'aeggespil_final.html')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f"\n✅ HTML fil genereret: {output_file}")
print(f"📊 Filstørrelse: {len(final_html) / 1024 / 1024:.1f} MB")
print("\nÅbn filen i din browser for at spille!")