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

// API-Endpunkt
app.get('/api/ways', async (req, res) => {
    const { table } = req.query;

    if (!table) {
        return res.status(400).json({ error: "Table name is required" });
    }

    try {
        // Query aus der Tabelle
        const query = `
            SELECT id, active
            FROM ${table}
        `;
        const result = await pool.query(query);

        // IDs und active-Status in ein Map-Objekt umwandeln
        const activeStatus = Object.fromEntries(
            result.rows.map(row => [String(row.id), row.active]) // IDs als String speichern
        );

        // Alle IDs in einer Liste
        const ids = result.rows.map(row => row.id);

        // Overpass Query (inkl. Knoten)
        const osmQuery = `
            [out:json];
            (
                way(id:${ids.join(",")});
                node(w); // Holt alle Nodes zu den Wegen
            );
            out body;
            >;
            out skel qt;
        `;

        const axios = require('axios');
        const response = await axios.post('https://overpass-api.de/api/interpreter', osmQuery, {
            headers: { 'Content-Type': 'text/plain' },
        });

        // Geometrie der Wege + active-Status zurückgeben
        const ways = response.data.elements.map(way => {
            if (!way.nodes || way.nodes.length === 0) {
                // Wenn keine nodes vorhanden sind, überspringen wir diesen Weg
                console.warn(`Way ${way.id} has no nodes or is malformed`);
                return null;
            }

            const geometry = way.nodes.map(node => ({
                lat: node.lat,
                lon: node.lon,
            }));

            return {
                id: way.id,
                geometry,
                active: activeStatus[String(way.id)] || false, // ID als String abgleichen
            };
        }).filter(way => way !== null); // Entfernt null-Werte (falls ein Weg ohne Nodes übersprungen wurde)

        res.json(ways);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: "Internal server error" });
    }
});

// Server starten
app.listen(port, () => {
    console.log(`Backend läuft auf http://localhost:${port}`);
});
