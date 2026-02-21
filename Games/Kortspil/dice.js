// dice.js — Delt terningemodul til 10.000 og varianter
// Inkludér med <script src="dice.js"></script>

// ─── Kast ────────────────────────────────────────────────────────────────────

/**
 * Kaster n terninger og returnerer array af tilfældige værdier (1-6).
 * Holdte terninger sendes med og returneres uændrede.
 * @param {number} n          - Antal terninger der kastes
 * @param {Array}  heldDice   - Array af allerede holdte {value, id} objekter (bevares)
 * @returns {Array}           - Fuldt array af {id, value, held} for alle 6 terninger
 */
function rollDice(heldDice = []) {
  const held = new Map(heldDice.map(d => [d.id, d]));
  const result = [];

  for (let id = 0; id < 6; id++) {
    if (held.has(id)) {
      result.push({ id, value: held.get(id).value, held: true });
    } else {
      result.push({ id, value: Math.floor(Math.random() * 6) + 1, held: false });
    }
  }

  return result;
}

// ─── Scoring: Mini 10.000 ────────────────────────────────────────────────────

/**
 * Beregner point for et kast i Mini 10.000 (kun 1'ere og 5'ere tæller).
 * @param {Array} dice - Array af {value} objekter
 * @returns {number}   - Point for dette kast
 */
function scoreRollMini(dice) {
  let points = 0;
  for (const die of dice) {
    if (die.value === 1) points += 100;
    if (die.value === 5) points += 50;
  }
  return points;
}

/**
 * Returnerer hvilke terninger der er pointgivende i Mini-varianten.
 * @param {Array} dice - Array af {id, value, held} objekter
 * @returns {Set}      - Set af id'er der giver point
 */
function scoringDiceIdsMini(dice) {
  const ids = new Set();
  for (const die of dice) {
    if (die.value === 1 || die.value === 5) ids.add(die.id);
  }
  return ids;
}

// ─── Scoring: Klassisk 10.000 ────────────────────────────────────────────────

/**
 * Beregner point for et kast i klassisk 10.000.
 * Håndterer: enkelt 1/5, tre ens, fire/fem/seks ens, sekvens, tre par.
 * @param {Array} dice - Array af {value} objekter
 * @returns {number}   - Point for dette kast
 */
function scoreRollClassic(dice) {
  const values = dice.map(d => d.value).sort((a, b) => a - b);
  const counts = {};
  for (const v of values) counts[v] = (counts[v] || 0) + 1;

  // Sekvens 1-2-3-4-5-6
  if (values.join('') === '123456') return 1500;

  // Tre par
  const pairCounts = Object.values(counts).filter(c => c === 2).length;
  if (pairCounts === 3) return 750;

  let points = 0;

  for (const [valStr, count] of Object.entries(counts)) {
    const val = parseInt(valStr);

    if (count >= 3) {
      // Basispoint for tre ens
      const base = val === 1 ? 1000 : val * 100;
      // Dobling for hver ekstra terning over tre
      const multiplier = Math.pow(2, count - 3);
      points += base * multiplier;
    } else {
      // Enkelt 1'er og 5'er
      if (val === 1) points += count * 100;
      if (val === 5) points += count * 50;
    }
  }

  return points;
}

// ─── Rendering ───────────────────────────────────────────────────────────────

/**
 * Returnerer et SVG-baseret DOM-element for én terning.
 * @param {number}  value   - Terningens øjne (1-6)
 * @param {boolean} held    - Om terningen er holdt (markeret)
 * @param {boolean} scoring - Om terningen er pointgivende (grøn glød)
 * @param {boolean} rolling - Om terningen animeres (ruller)
 * @returns {HTMLElement}
 */
function renderDie(value, held = false, scoring = false, rolling = false) {
  const el = document.createElement('div');
  el.classList.add('die');
  if (held)    el.classList.add('die--held');
  if (scoring) el.classList.add('die--scoring');
  if (rolling) el.classList.add('die--rolling');

  el.appendChild(_buildDieFace(value));
  return el;
}

// ─── Intern: terningeflade med prikker ───────────────────────────────────────

// Prik-positioner for 1-6 (række, kolonne) i et 3×3 grid
const _DOT_POSITIONS = {
  1: [[1,1]],
  2: [[0,0],[2,2]],
  3: [[0,0],[1,1],[2,2]],
  4: [[0,0],[0,2],[2,0],[2,2]],
  5: [[0,0],[0,2],[1,1],[2,0],[2,2]],
  6: [[0,0],[0,2],[1,0],[1,2],[2,0],[2,2]],
};

function _buildDieFace(value) {
  const face = document.createElement('div');
  face.classList.add('die__face');

  const positions = _DOT_POSITIONS[value] || [];
  for (const [row, col] of positions) {
    const dot = document.createElement('div');
    dot.classList.add('die__dot');
    dot.style.gridRow    = row + 1;
    dot.style.gridColumn = col + 1;
    face.appendChild(dot);
  }

  return face;
}

// ─── Eksponeret API ───────────────────────────────────────────────────────────
// rollDice(heldDice)       → kast, bevar holdte
// scoreRollMini(dice)      → point til Mini 10.000
// scoreRollClassic(dice)   → point til Klassisk 10.000
// scoringDiceIdsMini(dice) → hvilke terninger giver point (Mini)
// renderDie(value, held, scoring, rolling) → DOM-element
