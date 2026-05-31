// 1. Inicializa o mapa focado nas coordenadas centrais do Brasil
const map = L.map('map').setView([-14.2350, -51.9253], 4);

// 2. Adiciona a camada base do OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// URL da sua API local rodando no FastAPI
const API_URL = 'http://127.0.0.1:8000/api/v1/malhas/uf';

console.log("⏳ Solicitando dados geográficos ao back-end...");

// 3. Função de estilização padrão para os estados (Tema Verde)
function estiloEstado(feature) {
    return {
        color: '#2e7d32',       // Cor da linha de fronteira (Verde escuro)
        weight: 1.5,            // Espessura da linha
        fillColor: '#81c784',   // Cor de preenchimento (Verde claro)
        fillOpacity: 0.4        // Opacidade padrão
    };
}

// 4. Requisição assíncrona para buscar o GeoJSON do PostGIS
fetch(API_URL)
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erro na conexão com a API: Status ${response.status}`);
        }
        return response.json();
    })
    .then(geoJsonData => {
        console.log("🌐 Dados espaciais recebidos com sucesso! Plotando no mapa...");
        
        // 5. Injeta a camada GeoJSON no mapa com interatividade
        L.geoJSON(geoJsonData, {
            style: estiloEstado,
            onEachFeature: function (feature, layer) {
                // Adiciona o Popup para abrir ao clicar no estado
                if (feature.properties && feature.properties.codigo_uf) {
                    layer.bindPopup(`
                        <div style="font-family: sans-serif; font-size: 14px;">
                            <b style="color: #2e7d32;">Unidade Federativa</b><br>
                            <b>Código IBGE:</b> ${feature.properties.codigo_uf}
                        </div>
                    `);
                }

                // Efeito visual interativo (Hover)
                layer.on({
                    mouseover: function (e) {
                        const l = e.target;
                        l.setStyle({
                            weight: 3,
                            color: '#1b5e20',
                            fillOpacity: 0.7
                        });
                        l.bringToFront();
                    },
                    mouseout: function (e) {
                        e.target.setStyle(estiloEstado(feature));
                    }
                });
            }
        }).addTo(map);
    })
    .catch(error => {
        console.error("❌ Falha ao renderizar a malha espacial:", error);
    });