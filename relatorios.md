# 🗺️ Divisão do Projeto GeoDev em 3 Relatórios de Estágio

## 📋 Relatório 1: Infraestrutura, Modelagem Espacial e Esteira ETL

* **Foco:** Fundação do projeto, preparação do ecossistema e carga inicial de dados.
* **Etapas Absorvidas:** * **Etapa 1 (Infraestrutura e Versionamento):** Configuração do repositório Git, ambiente virtual Python (`.venv`), container Docker com PostgreSQL/PostGIS e criação da tabela estruturada `malha_uf` com indexação GiST no DBeaver.
* **Etapa 2 (Script de Ingestão de Dados - ETL):** Desenvolvimento do script seguro `ingestion.py` alimentado por `.env`, consumo da API do IBGE, tratamento do bug de tipagem cartográfica com a função `ST_Multi()` e persistência final no banco.



---

### 💻 Relatório 2: Engenharia de Back-end, Endpoints RESTful e Otimização Espacial

* **Foco:** Construção da inteligência de microsserviços, tratamento de segurança de rede e performance.
* **Etapas Absorvidas:**
* **Etapa 3 (Construção da API com FastAPI):** Estruturação do servidor com FastAPI e Uvicorn, configuração do middleware de CORS para liberar o acesso ao front-end, criação do endpoint geográfico `/api/v1/malhas/uf`, otimização de performance delegando a conversão de coordenadas para o PostGIS com `ST_AsGeoJSON()` e montagem do padrão internacional `FeatureCollection`.



---

### 🚀 Relatório 3: Interface do Cliente, Integração Assíncrona e Engenharia de Usabilidade

* **Foco:** Camada visual (Client-side), comunicação entre sistemas em segundo plano e refinamento de experiência do usuário (UX).
* **Etapas Absorvidas:**
* **Etapa 4 (Interface Web com Leaflet.js):** Construção da Landing Page corporativa (HTML/CSS), estilização imersiva do contêiner do mapa e instanciação cartográfica inicial do motor Leaflet com as camadas do OpenStreetMap.
* **Etapa 5 (Integração e Refinamento):** Implementação do consumo assíncrono via `Fetch API` para conectar o front ao back-end, renderização dinâmica dos polígonos e aplicação de recursos visuais avançados (popups de metadados do IBGE e alteração de opacidade/borda nos eventos de *hover* do mouse).