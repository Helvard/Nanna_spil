// deck.js — Delt kortdæk til alle kortspil
// Bruges ved at inkludere denne fil med <script src="deck.js"></script>

// ─── Kortdata ───────────────────────────────────────────────────────────────

function createDeck() {
  const suits = [
    { symbol: '♠', name: 'spar',   color: 'black' },
    { symbol: '♥', name: 'hjerter', color: 'red'   },
    { symbol: '♦', name: 'ruder',  color: 'red'   },
    { symbol: '♣', name: 'klør',   color: 'black' },
  ];

  const faces = {
    1:  'A',
    11: 'J',
    12: 'Q',
    13: 'K',
  };

  const deck = [];

  for (const suit of suits) {
    for (let value = 1; value <= 13; value++) {
      deck.push({
        suit:         suit.symbol,
        suitName:     suit.name,
        color:        suit.color,
        value:        value,
        displayValue: faces[value] ?? String(value),
      });
    }
  }

  return deck;
}

// ─── Shuffle ─────────────────────────────────────────────────────────────────

function shuffle(deck) {
  const d = [...deck];
  for (let i = d.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [d[i], d[j]] = [d[j], d[i]];
  }
  return d;
}

// ─── Kortrendering ───────────────────────────────────────────────────────────

/**
 * Returnerer et DOM-element der repræsenterer et kort.
 * @param {object} card      - Kortobj fra createDeck()
 * @param {boolean} faceDown - Vis bagsiden (harlequin-mønster)
 * @returns {HTMLElement}
 */
function renderCard(card, faceDown = false) {
  const el = document.createElement('div');
  el.classList.add('card');
  if (faceDown) {
    el.classList.add('card--back');
    el.appendChild(_buildCardBack());
  } else {
    el.classList.add('card--face', `card--${card.color}`);
    el.appendChild(_buildCardFace(card));
  }
  return el;
}

// ─── Intern: kortforside ──────────────────────────────────────────────────────

function _buildCardFace(card) {
  const face = document.createElement('div');
  face.classList.add('card__face');

  // Øverste venstre hjørne
  const topLeft = document.createElement('div');
  topLeft.classList.add('card__corner', 'card__corner--tl');
  topLeft.innerHTML = `<span class="card__value">${card.displayValue}</span><span class="card__suit">${card.suit}</span>`;

  // Nederste højre hjørne (roteret 180°)
  const botRight = document.createElement('div');
  botRight.classList.add('card__corner', 'card__corner--br');
  botRight.innerHTML = `<span class="card__value">${card.displayValue}</span><span class="card__suit">${card.suit}</span>`;

  // Midterste symbol
  const center = document.createElement('div');
  center.classList.add('card__center');
  center.textContent = card.suit;

  face.appendChild(topLeft);
  face.appendChild(center);
  face.appendChild(botRight);

  return face;
}

// ─── Intern: kortbagside (harlequin) ─────────────────────────────────────────

function _buildCardBack() {
  const COLS = 6;
  const ROWS = 9;

  // Harlequin-palette: dybe klassiske farver
  const COLORS = ['#c0392b', '#2980b9', '#f39c12', '#27ae60', '#8e44ad', '#e74c3c'];

  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', `0 0 ${COLS} ${ROWS}`);
  svg.setAttribute('preserveAspectRatio', 'none');
  svg.classList.add('card__back-svg');

  // Diamantmønster: hver celle er en rombe der er roteret 45°
  // Vi tegner to trekanter per celle så farverne skifter skakbræt-agtigt
  for (let row = 0; row < ROWS; row++) {
    for (let col = 0; col < COLS; col++) {
      const colorIndex = (row + col) % COLORS.length;
      const altIndex   = (row + col + 1) % COLORS.length;

      const x = col;
      const y = row;
      const cx = x + 0.5;
      const cy = y + 0.5;

      // Øvre trekant af cellen
      const top = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
      top.setAttribute('points', `${x},${y} ${x+1},${y} ${cx},${cy}`);
      top.setAttribute('fill', COLORS[colorIndex]);

      // Nedre trekant
      const bot = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
      bot.setAttribute('points', `${x},${y+1} ${x+1},${y+1} ${cx},${cy}`);
      bot.setAttribute('fill', COLORS[altIndex]);

      // Venstre trekant
      const left = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
      left.setAttribute('points', `${x},${y} ${x},${y+1} ${cx},${cy}`);
      left.setAttribute('fill', COLORS[(colorIndex + 2) % COLORS.length]);

      // Højre trekant
      const right = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
      right.setAttribute('points', `${x+1},${y} ${x+1},${y+1} ${cx},${cy}`);
      right.setAttribute('fill', COLORS[(colorIndex + 3) % COLORS.length]);

      svg.appendChild(top);
      svg.appendChild(bot);
      svg.appendChild(left);
      svg.appendChild(right);
    }
  }

  return svg;
}

// ─── Eksponeret API ───────────────────────────────────────────────────────────

// Tilgængeligt globalt når filen inkluderes via <script>
// Bruges i spil-filer som:
//   const deck = shuffle(createDeck());
//   const cardEl = renderCard(deck[0], false);
