# Roteiro de Construção GeoDev

Projeto: **GEODEV**
Desenvolvedor: phmcasimiro

## Etapa 1: Infraestrutura e Banco de Dados (Docker + PostGIS)

O objetivo aqui é deixar o seu ecossistema espacial pronto para receber dados.

1. **Estrutura de diretórios e arquivos do projeto:**

```text
GEODEV/
├── backend/
├── frontend/
├── docker-compose.yml
├── README.md
├── Etapas.md
├── requirements.txt
└── .gitignore
```


2. **Escrever o `docker-compose.yml`:** Configurar o serviço do Postgres com a imagem do PostGIS, definindo variáveis de ambiente (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`) e o volume para persistência.
3. **Subir o container:** Executar `docker compose up -d` e verificar se o banco está ativo.
4. **Habilitar a extensão espacial:** Conectar ao banco (via DBeaver, pgAdmin ou terminal) e rodar o comando:
```sql
CREATE EXTENSION IF NOT EXISTS postgis;

```


5. **Criar a tabela `malha_uf`:** Executar o DDL de criação da tabela com a coluna geométrica (`GEOMETRY(MultiPolygon, 4326)`) e o índice espacial GIST.

---

### Etapa 2: Script de Ingestão de Dados (ETL em Python)

Agora vamos buscar o GeoJSON do IBGE e salvá-lo localmente.

1. **Criar um script isolado (ex: `ingestao.py`):** Configurar o ambiente virtual (`venv`) e instalar as dependências necessárias (`requests` e um driver de banco como `psycopg3` ou `SQLAlchemy`).
2. **Consumir a API do IBGE:** Fazer o `GET` na URL da malha das UFs e capturar o JSON de resposta.
3. **Tratar e Inserir os Dados:** * Iterar pelas `features` do GeoJSON.
* Para cada estado, extrair o código identificador e o objeto de geometria.
* Converter o dicionário da geometria de volta para string (`json.dumps(geometry)`) e passá-lo na query SQL usando a função `ST_GeomFromGeoJSON()`.


4. **Validar a carga:** Rodar uma consulta no banco para checar se os 27 registros (26 estados + DF) foram inseridos corretamente.

---

### Etapa 3: Construção da API (Back-end com FastAPI)

Sua API será a ponte que lê o banco e entrega os dados para a web.

1. **Estruturar o app FastAPI:** Instalar `fastapi` e `uvicorn`.
2. **Configurar o CORS (Crucial!):** Adicionar o middleware de CORS no FastAPI para permitir que sua página HTML (rodando localmente ou em outro porto) consiga consumir os dados da API sem ser bloqueada pelo navegador.
3. **Criar a rota de consulta:** Desenhar o endpoint (ex: `/api/v1/malhas/uf`).
4. **Escrever a lógica SQL:** Fazer a query buscando o código da UF e a geometria convertida para string via `ST_AsGeoJSON(geom)`.
5. **Formatar a saída:** Montar a estrutura da resposta para que ela retorne como uma `FeatureCollection` válida do padrão GeoJSON e testar a rota pelo painel automático do Swagger (`/docs`).

---

### Etapa 4: Interface Web (Front-end com HTML/CSS e Leaflet)

A camada visual onde a mágica do mapa acontece.

1. **Criar o arquivo `index.html`:** Estruturar a página básica e incluir as tags `<link>` e `<script>` do CDN do Leaflet.js.
2. **Criar o arquivo `style.css`:** Garantir que o contêiner do mapa (`#map`) ocupe toda a tela (`width: 100vw; height: 100vh;`) e remover as margens padrão do body.
3. **Inicializar o mapa no JavaScript:** Apontar as coordenadas centrais do Brasil, definir o zoom inicial e adicionar a camada de azulejos (Tiles) do OpenStreetMap como fundo.

---

### Etapa 5: Integração e Refinamento

O momento de conectar o front-end ao back-end.

1. **Consumir a API via Fetch:** No JavaScript do front-end, fazer uma requisição `fetch()` para a URL da sua API FastAPI local.
2. **Plotar a camada no Leaflet:** Passar o JSON recebido diretamente para a função `L.geoJSON(dados).addTo(map)`.
3. **Estilização dos polígonos:** Personalizar as cores das bordas, preenchimento e opacidade dos estados para deixar o visual harmônico.
4. **Adicionar Interatividade (Dica extra):** Implementar uma função simples de `onEachFeature` para abrir um popup com o código ou nome da UF quando o usuário clicar sobre o estado.

---