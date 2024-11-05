// NodeJS implementation

const https = require('https');
const fs = require('fs');
const path = require('path');

// Global variables
let base = 'https://b.tile.openstreetmap.org/';
const filetype = '.png';
let zoom1 = 13;
const zoom2 = 14;
const lat1 = 53.67;
const lon1 = 4.2;
const lat2 = 58.17;
const lon2 = 18.7;

// Main function
async function main() {
    await downloadSet(zoom1);
    console.log("Done downloading");
}

// Function to download a set of tiles
async function downloadSet(zoom) {
    const startTile = getTileNumber(lat1, lon1, zoom);
    const stopTile = getTileNumber(lat2, lon2, zoom);

    const y1 = stopTile[1];
    const y2 = startTile[1];
    const z1 = startTile[0];
    const z2 = stopTile[0];

    let m = 1;
    const totalTiles = (y2 - y1 + 1) * (z2 - z1 + 1);

    for (let j = y1; j <= y2; j++) {
        for (let k = z1; k <= z2; k++, m++) {
            await saveTile(zoom, j, k);
            console.log(`Tile ${m} of ${totalTiles} (${zoom}/${k}/${j}${filetype})`);
        }
    }

    if (zoom < zoom2) {
        await downloadSet(zoom + 1);
    }
}

// Function to download and save a tile
function saveTile(zoom, x, y) {
    const url = `${base}${zoom}/${x}/${y}${filetype}`;
    const filePath = path.join(__dirname, `${zoom}_${x}_${y}${filetype}`);

    return new Promise((resolve, reject) => {
        https.get(url, (response) => {
            if (response.statusCode !== 200) {
                console.error(`Failed to download tile ${zoom}/${x}/${y}: Status Code ${response.statusCode}`);
                return reject(new Error(`Failed to download tile: ${response.statusCode}`));
            }

            const fileStream = fs.createWriteStream(filePath);
            response.pipe(fileStream);

            fileStream.on('finish', () => {
                fileStream.close(resolve);
            });

            fileStream.on('error', (error) => {
                fs.unlink(filePath, () => reject(error));
            });
        }).on('error', (error) => {
            console.error(`Failed to download tile ${zoom}/${x}/${y}:`, error);
            reject(error);
        });
    });
}

// Function to calculate tile number for given latitude, longitude, and zoom level
function getTileNumber(lat, lon, zoom) {
    const xtile = Math.floor((lon + 180) / 360 * (1 << zoom));
    const ytile = Math.floor(
        (1 - Math.log(Math.tan(toRadians(lat)) + 1 / Math.cos(toRadians(lat))) / Math.PI) / 2 * (1 << zoom)
    );

    return [
        Math.max(0, Math.min(xtile, (1 << zoom) - 1)),
        Math.max(0, Math.min(ytile, (1 << zoom) - 1))
    ];
}

// Helper function to convert degrees to radians
function toRadians(deg) {
    return deg * (Math.PI / 180);
}

// Run the main function
main().catch(error => console.error(error));
