// Simple drawing generator for testing the coloring game
// This creates basic SVG drawings for each theme

const fs = require('fs');
const path = require('path');

// Create directories
const themes = ['paw_patrol', 'disney', 'animals', 'vehicles'];
themes.forEach(theme => {
    const dir = path.join(__dirname, theme);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
});

// Paw Patrol drawings
const pawPatrolDrawings = {
    chase: `<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="80" r="40" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="85" cy="70" r="5" fill="black"/>
        <circle cx="115" cy="70" r="5" fill="black"/>
        <path d="M 90 90 Q 100 100 110 90" fill="none" stroke="black" stroke-width="2"/>
        <rect x="80" y="120" width="40" height="60" fill="none" stroke="black" stroke-width="2"/>
        <rect x="70" y="130" width="15" height="40" fill="none" stroke="black" stroke-width="2"/>
        <rect x="115" y="130" width="15" height="40" fill="none" stroke="black" stroke-width="2"/>
        <text x="100" y="190" text-anchor="middle" font-family="Arial" font-size="12">Chase</text>
    </svg>`,
    
    marshall: `<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="80" r="40" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="85" cy="70" r="5" fill="black"/>
        <circle cx="115" cy="70" r="5" fill="black"/>
        <path d="M 90 90 Q 100 100 110 90" fill="none" stroke="black" stroke-width="2"/>
        <rect x="80" y="120" width="40" height="60" fill="none" stroke="black" stroke-width="2"/>
        <rect x="70" y="130" width="15" height="40" fill="none" stroke="black" stroke-width="2"/>
        <rect x="115" y="130" width="15" height="40" fill="none" stroke="black" stroke-width="2"/>
        <ellipse cx="100" cy="50" rx="30" ry="20" fill="none" stroke="red" stroke-width="2"/>
        <text x="100" y="190" text-anchor="middle" font-family="Arial" font-size="12">Marshall</text>
    </svg>`,
    
    skye: `<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="80" r="40" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="85" cy="70" r="5" fill="black"/>
        <circle cx="115" cy="70" r="5" fill="black"/>
        <path d="M 90 90 Q 100 100 110 90" fill="none" stroke="black" stroke-width="2"/>
        <rect x="80" y="120" width="40" height="60" fill="none" stroke="black" stroke-width="2"/>
        <path d="M 60 60 Q 40 40 60 20 Q 80 30 100 20 Q 120 30 140 20 Q 160 40 140 60" fill="none" stroke="pink" stroke-width="2"/>
        <text x="100" y="190" text-anchor="middle" font-family="Arial" font-size="12">Skye</text>
    </svg>`,
    
    rubble: `<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="80" r="40" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="85" cy="70" r="5" fill="black"/>
        <circle cx="115" cy="70" r="5" fill="black"/>
        <path d="M 90 90 Q 100 100 110 90" fill="none" stroke="black" stroke-width="2"/>
        <rect x="80" y="120" width="40" height="60" fill="none" stroke="black" stroke-width="2"/>
        <rect x="70" y="130" width="15" height="40" fill="none" stroke="black" stroke-width="2"/>
        <rect x="115" y="130" width="15" height="40" fill="none" stroke="black" stroke-width="2"/>
        <rect x="60" y="50" width="80" height="20" fill="none" stroke="yellow" stroke-width="2"/>
        <text x="100" y="190" text-anchor="middle" font-family="Arial" font-size="12">Rubble</text>
    </svg>`,
    
    rocky: `<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="80" r="40" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="85" cy="70" r="5" fill="black"/>
        <circle cx="115" cy="70" r="5" fill="black"/>
        <path d="M 90 90 Q 100 100 110 90" fill="none" stroke="black" stroke-width="2"/>
        <rect x="80" y="120" width="40" height="60" fill="none" stroke="black" stroke-width="2"/>
        <rect x="70" y="130" width="15" height="40" fill="none" stroke="black" stroke-width="2"/>
        <rect x="115" y="130" width="15" height="40" fill="none" stroke="black" stroke-width="2"/>
        <path d="M 60 60 L 140 60 L 120 80 L 80 80 Z" fill="none" stroke="green" stroke-width="2"/>
        <text x="100" y="190" text-anchor="middle" font-family="Arial" font-size="12">Rocky</text>
    </svg>`,
    
    zuma: `<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="80" r="40" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="85" cy="70" r="5" fill="black"/>
        <circle cx="115" cy="70" r="5" fill="black"/>
        <path d="M 90 90 Q 100 100 110 90" fill="none" stroke="black" stroke-width="2"/>
        <rect x="80" y="120" width="40" height="60" fill="none" stroke="black" stroke-width="2"/>
        <rect x="70" y="130" width="15" height="40" fill="none" stroke="black" stroke-width="2"/>
        <rect x="115" y="130" width="15" height="40" fill="none" stroke="black" stroke-width="2"/>
        <ellipse cx="100" cy="50" rx="25" ry="15" fill="none" stroke="orange" stroke-width="2"/>
        <text x="100" y="190" text-anchor="middle" font-family="Arial" font-size="12">Zuma</text>
    </svg>`
};

// Disney drawings
const disneyDrawings = {
    mickey: `<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="100" r="50" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="70" cy="60" r="25" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="130" cy="60" r="25" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="85" cy="95" r="8" fill="black"/>
        <circle cx="115" cy="95" r="8" fill="black"/>
        <ellipse cx="100" cy="120" rx="15" ry="10" fill="none" stroke="black" stroke-width="2"/>
        <text x="100" y="190" text-anchor="middle" font-family="Arial" font-size="12">Mickey Mouse</text>
    </svg>`,
    
    minnie: `<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="100" r="50" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="70" cy="60" r="25" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="130" cy="60" r="25" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="85" cy="95" r="8" fill="black"/>
        <circle cx="115" cy="95" r="8" fill="black"/>
        <ellipse cx="100" cy="120" rx="15" ry="10" fill="none" stroke="black" stroke-width="2"/>
        <path d="M 60 50 Q 40 30 60 10 Q 80 20 100 10 Q 120 20 140 10 Q 160 30 140 50" fill="none" stroke="red" stroke-width="2"/>
        <text x="100" y="190" text-anchor="middle" font-family="Arial" font-size="12">Minnie Mouse</text>
    </svg>`,
    
    donald: `<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="100" cy="100" rx="40" ry="50" fill="none" stroke="black" stroke-width="2"/>
        <path d="M 60 80 Q 40 60 60 40 Q 80 50 100 40 Q 120 50 140 40 Q 160 60 140 80" fill="none" stroke="yellow" stroke-width="2"/>
        <circle cx="85" cy="95" r="8" fill="black"/>
        <circle cx="115" cy="95" r="8" fill="black"/>
        <path d="M 90 110 Q 100 120 110 110" fill="none" stroke="black" stroke-width="2"/>
        <text x="100" y="190" text-anchor="middle" font-family="Arial" font-size="12">Donald Duck</text>
    </svg>`,
    
    goofy: `<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="100" cy="100" rx="35" ry="45" fill="none" stroke="black" stroke-width="2"/>
        <ellipse cx="70" cy="70" rx="20" ry="30" fill="none" stroke="black" stroke-width="2"/>
        <ellipse cx="130" cy="70" rx="20" ry="30" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="90" cy="95" r="6" fill="black"/>
        <circle cx="110" cy="95" r="6" fill="black"/>
        <path d="M 95 110 Q 100 115 105 110" fill="none" stroke="black" stroke-width="2"/>
        <text x="100" y="190" text-anchor="middle" font-family="Arial" font-size="12">Goofy</text>
    </svg>`
};

// Animal drawings
const animalDrawings = {
    lion: `<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="100" r="40" fill="none" stroke="black" stroke-width="2"/>
        <path d="M 60 80 Q 40 60 60 40 Q 80 50 100 40 Q 120 50 140 40 Q 160 60 140 80" fill="none" stroke="orange" stroke-width="2"/>
        <circle cx="85" cy="90" r="5" fill="black"/>
        <circle cx="115" cy="90" r="5" fill="black"/>
        <path d="M 90 105 Q 100 115 110 105" fill="none" stroke="black" stroke-width="2"/>
        <ellipse cx="100" cy="140" rx="15" ry="8" fill="none" stroke="black" stroke-width="2"/>
        <text x="100" y="190" text-anchor="middle" font-family="Arial" font-size="12">Løve</text>
    </svg>`,
    
    elephant: `<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="100" cy="100" rx="50" ry="40" fill="none" stroke="black" stroke-width="2"/>
        <path d="M 60 80 Q 40 70 50 50 Q 60 60 70 50" fill="none" stroke="black" stroke-width="2"/>
        <path d="M 140 80 Q 160 70 150 50 Q 140 60 130 50" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="85" cy="90" r="5" fill="black"/>
        <circle cx="115" cy="90" r="5" fill="black"/>
        <path d="M 90 105 Q 100 110 110 105" fill="none" stroke="black" stroke-width="2"/>
        <path d="M 70 130 Q 60 150 70 170" fill="none" stroke="black" stroke-width="2"/>
        <path d="M 130 130 Q 140 150 130 170" fill="none" stroke="black" stroke-width="2"/>
        <text x="100" y="190" text-anchor="middle" font-family="Arial" font-size="12">Elefant</text>
    </svg>`,
    
    monkey: `<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="100" r="35" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="70" cy="70" r="20" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="130" cy="70" r="20" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="90" cy="95" r="4" fill="black"/>
        <circle cx="110" cy="95" r="4" fill="black"/>
        <path d="M 95 108 Q 100 112 105 108" fill="none" stroke="black" stroke-width="2"/>
        <path d="M 65 120 Q 50 140 65 160" fill="none" stroke="black" stroke-width="2"/>
        <path d="M 135 120 Q 150 140 135 160" fill="none" stroke="black" stroke-width="2"/>
        <text x="100" y="190" text-anchor="middle" font-family="Arial" font-size="12">Abe</text>
    </svg>`,
    
    giraffe: `<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="100" cy="120" rx="30" ry="40" fill="none" stroke="black" stroke-width="2"/>
        <rect x="90" y="60" width="20" height="60" fill="none" stroke="black" stroke-width="2"/>
        <ellipse cx="100" cy="50" rx="15" ry="20" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="95" cy="45" r="3" fill="black"/>
        <circle cx="105" cy="45" r="3" fill="black"/>
        <path d="M 98 52 Q 100 55 102 52" fill="none" stroke="black" stroke-width="2"/>
        <rect x="85" y="140" width="10" height="30" fill="none" stroke="black" stroke-width="2"/>
        <rect x="105" y="140" width="10" height="30" fill="none" stroke="black" stroke-width="2"/>
        <rect x="75" y="80" width="8" height="25" fill="none" stroke="black" stroke-width="2"/>
        <rect x="117" y="80" width="8" height="25" fill="none" stroke="black" stroke-width="2"/>
        <text x="100" y="190" text-anchor="middle" font-family="Arial" font-size="12">Giraf</text>
    </svg>`,
    
    zebra: `<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="100" cy="110" rx="35" ry="40" fill="none" stroke="black" stroke-width="2"/>
        <rect x="90" y="60" width="20" height="50" fill="none" stroke="black" stroke-width="2"/>
        <ellipse cx="100" cy="50" rx="15" ry="15" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="95" cy="45" r="3" fill="black"/>
        <circle cx="105" cy="45" r="3" fill="black"/>
        <path d="M 98 52 Q 100 55 102 52" fill="none" stroke="black" stroke-width="2"/>
        <rect x="85" y="140" width="10" height="30" fill="none" stroke="black" stroke-width="2"/>
        <rect x="105" y="140" width="10" height="30" fill="none" stroke="black" stroke-width="2"/>
        <path d="M 85 70 L 85 90 M 95 65 L 95 85 M 105 65 L 105 85 M 115 70 L 115 90" stroke="black" stroke-width="3"/>
        <text x="100" y="190" text-anchor="middle" font-family="Arial" font-size="12">Zebra</text>
    </svg>`,
    
    penguin: `<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="100" cy="110" rx="30" ry="40" fill="none" stroke="black" stroke-width="2"/>
        <ellipse cx="100" cy="60" rx="25" ry="30" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="90" cy="50" r="3" fill="black"/>
        <circle cx="110" cy="50" r="3" fill="black"/>
        <path d="M 95 60 Q 100 65 105 60" fill="none" stroke="orange" stroke-width="2"/>
        <ellipse cx="100" cy="100" rx="15" ry="25" fill="none" stroke="white" stroke-width="2"/>
        <path d="M 85 140 Q 80 160 85 180" fill="none" stroke="black" stroke-width="2"/>
        <path d="M 115 140 Q 120 160 115 180" fill="none" stroke="black" stroke-width="2"/>
        <path d="M 70 80 Q 50 70 60 50 Q 70 60 80 50" fill="none" stroke="black" stroke-width="2"/>
        <path d="M 130 80 Q 150 70 140 50 Q 130 60 120 50" fill="none" stroke="black" stroke-width="2"/>
        <text x="100" y="190" text-anchor="middle" font-family="Arial" font-size="12">Pingvin</text>
    </svg>`
};

// Vehicle drawings
const vehicleDrawings = {
    car: `<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <rect x="50" y="100" width="100" height="40" fill="none" stroke="black" stroke-width="2"/>
        <rect x="70" y="80" width="60" height="20" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="75" cy="150" r="15" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="125" cy="150" r="15" fill="none" stroke="black" stroke-width="2"/>
        <rect x="85" y="85" width="15" height="10" fill="none" stroke="lightblue" stroke-width="1"/>
        <rect x="100" y="85" width="15" height="10" fill="none" stroke="lightblue" stroke-width="1"/>
        <text x="100" y="190" text-anchor="middle" font-family="Arial" font-size="12">Bil</text>
    </svg>`,
    
    truck: `<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <rect x="40" y="90" width="80" height="50" fill="none" stroke="black" stroke-width="2"/>
        <rect x="120" y="100" width="40" height="40" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="70" cy="150" r="12" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="110" cy="150" r="12" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="145" cy="150" r="12" fill="none" stroke="black" stroke-width="2"/>
        <rect x="125" y="105" width="10" height="10" fill="none" stroke="lightblue" stroke-width="1"/>
        <text x="100" y="190" text-anchor="middle" font-family="Arial" font-size="12">Lastbil</text>
    </svg>`,
    
    airplane: `<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="100" cy="100" rx="60" ry="15" fill="none" stroke="black" stroke-width="2"/>
        <rect x="90" y="70" width="20" height="60" fill="none" stroke="black" stroke-width="2"/>
        <path d="M 70 100 L 30 85 L 30 95 Z" fill="none" stroke="black" stroke-width="2"/>
        <path d="M 130 100 L 170 85 L 170 95 Z" fill="none" stroke="black" stroke-width="2"/>
        <rect x="85" y="85" width="10" height="8" fill="none" stroke="lightblue" stroke-width="1"/>
        <text x="100" y="190" text-anchor="middle" font-family="Arial" font-size="12">Fly</text>
    </svg>`,
    
    boat: `<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <path d="M 50 120 L 150 120 L 130 150 L 70 150 Z" fill="none" stroke="black" stroke-width="2"/>
        <rect x="95" y="60" width="10" height="60" fill="none" stroke="black" stroke-width="2"/>
        <path d="M 105 70 L 140 90 L 105 90 Z" fill="none" stroke="red" stroke-width="2"/>
        <text x="100" y="190" text-anchor="middle" font-family="Arial" font-size="12">Båd</text>
    </svg>`,
    
    train: `<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <rect x="30" y="100" width="40" height="40" fill="none" stroke="black" stroke-width="2"/>
        <rect x="80" y="100" width="40" height="40" fill="none" stroke="black" stroke-width="2"/>
        <rect x="130" y="100" width="40" height="40" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="45" cy="150" r="8" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="55" cy="150" r="8" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="95" cy="150" r="8" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="105" cy="150" r="8" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="145" cy="150" r="8" fill="none" stroke="black" stroke-width="2"/>
        <circle cx="155" cy="150" r="8" fill="none" stroke="black" stroke-width="2"/>
        <rect x="35" y="105" width="8" height="8" fill="none" stroke="lightblue" stroke-width="1"/>
        <rect x="85" y="105" width="8" height="8" fill="none" stroke="lightblue" stroke-width="1"/>
        <text x="100" y="190" text-anchor="middle" font-family="Arial" font-size="12">Tog</text>
    </svg>`
};

// Write all drawing files
Object.entries(pawPatrolDrawings).forEach(([name, svg]) => {
    fs.writeFileSync(path.join(__dirname, 'paw_patrol', `${name}.svg`), svg);
});

Object.entries(disneyDrawings).forEach(([name, svg]) => {
    fs.writeFileSync(path.join(__dirname, 'disney', `${name}.svg`), svg);
});

Object.entries(animalDrawings).forEach(([name, svg]) => {
    fs.writeFileSync(path.join(__dirname, 'animals', `${name}.svg`), svg);
});

Object.entries(vehicleDrawings).forEach(([name, svg]) => {
    fs.writeFileSync(path.join(__dirname, 'vehicles', `${name}.svg`), svg);
});

console.log('Drawing files created successfully!');
console.log('Run this script to generate basic SVG drawings for testing the coloring game.');
