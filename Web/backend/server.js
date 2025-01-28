const express = require('express');
const { Pool } = require('pg');
const axios = require('axios');
const cors = require('cors');

const app = express();
const port = 3000;

// PostgreSQL-Konfiguration
const pool = new Pool({
    user: 'user',
    host: '192.168.2.13',
    database: 'Wirtschaftsmodul',
    password: 'user',
    port: 5432
});

// CORS aktivieren
app.use(cors({
    origin: true, // Frontend-Adresse
}));
app.use(express.json());

async function fetchGeometryFromOverpass(ids) {
    const query = `
        [out:json];
        (
          way(id:${ids.join(',')});
        );
        out geom;`;

    try {
        const response = await axios.post('https://overpass-api.de/api/interpreter', query, {
            headers: { 'Content-Type': 'text/plain' }
        });

        const elements = response.data.elements || [];
        return elements.map(way => ({
            id: way.id,
            geometry: way.geometry.map(coord => ({ lat: coord.lat, lon: coord.lon }))
        }));
    } catch (error) {
        console.error('Error fetching data from Overpass API:', error);
        throw new Error('Overpass API request failed');
    }
}

// API-Endpunkt für Wege
app.get('/api/ways', async (req, res) => {
    const table = req.query.table;

    if (!table) {
        return res.status(400).json({ error: 'Table parameter is required.' });
    }

    try {
        // IDs und Active-Werte aus der Datenbank abrufen
        const result = await pool.query(`
            SELECT id, active
            FROM ${table};
        `);

        const rows = result.rows;
        const ids = rows.map(row => row.id);

         const activeStatus = Object.fromEntries(
            result.rows.map(row => [String(row.id), row.active]) // IDs als String speichern
        );

        // Geometrien über Overpass API abrufen
        const geometries = await fetchGeometryFromOverpass(ids);

        // Daten kombinieren (Geometrien + Active-Wert)
        const ways = geometries.map(geometry => {
            return {
                id: geometry.id,
                geometry: geometry.geometry,
                active: activeStatus[String(geometry.id)] || false, // ID als String abgleichen
            };
        });

        res.json(ways);
    } catch (err) {
        console.error('Error processing request:', err);
        res.status(500).send({ error: 'Fehler beim Abrufen der Daten.' });
    }
});

// Server starten
app.listen(port, () => {
    console.log(`Backend läuft auf http://localhost:${port}`);
});
