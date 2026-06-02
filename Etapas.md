# Roteiro de Construção GeoDev

Projeto: **GEODEV**
Desenvolvedor: phmcasimiro

## Etapa 1: Infraestrutura e Versionamento

O objetivo aqui é deixar o seu ecossistema espacial pronto para receber dados.

1. **Estrutura de diretórios e arquivos do projeto:**

```text
GEODEV/
├── backend/            # Códigos da API (FastAPI) - A ser construído
├── frontend/           # Interface Web (HTML/CSS/JS) - A ser construído
├── docker-compose.yml  # Configuração da infraestrutura (Portabilidade)
├── requirements.txt    # Dependências do ecossistema Python
├── .gitignore          # Filtro de arquivos para o Git
├── Etapas.md           # Este plano de voo
├── README.md           # Documentação principal do projeto
└── ingestao.py         # Script de automação ETL (IBGE -> PostGIS)

```

### 🗄️ Banco de Dados Espacial

* **SGBD:** PostgreSQL 15.4 (Debian 15.4-1.pgdg110+1) on x86_64-pc-linux-gnu, 64-bit
* **Extensão GIS:** PostGIS 3.3.4
* **Componentes Core:** GEOS 3.9.0, PROJ 7.2.1, LIBXML 2.9.10
* **Projeção Adotada:** WGS 84 (SRID: 4326) - Padrão nativo para mapas web.
* **Database Name:** `basegeo`
* **Schema Utilizado:** `public`

### 🐳 Infraestrutura Docker

* **Tipo de Instância:** Container Docker multi-banco compartilhado (reutilizado na porta padrão `5432`).
* **Porta Local (Host):** `5432`
* **Porta do Container:** `5432`

### 🐍 Ecossistema Python (Back-end & ETL)

* **Versão do Python:** Python 3.12+ (Ambiente isolado em `.venv`)
* **Driver de Conexão:** `psycopg2-binary` (v2.9+)
* **Client HTTP:** `requests`

* **Inicialização do Git:** Repositório local inicializado e conectado com sucesso ao repositório remoto em [https://github.com/phmcasimiro/geodev.git](https://github.com/phmcasimiro/geodev.git).
* **Criação do .gitignore:** Configurado para ignorar ambientes virtuais (.venv), caches do Python (**pycache**) e arquivos de configuração locais.
* **Ajuste de Quebra de Linha (CRLF vs LF):** Configuração do Git ajustada para tratar o comportamento de quebras de linha entre ambientes Windows/Linux de forma segura.

Etapa 2: Infraestrutura e Banco de Dados Espacial

* **Estratégia de Banco de Dados:** Optou-se por utilizar bancos de dados distintos dentro da mesma instância do PostgreSQL já ativa na máquina local (porta 5432), otimizando o uso de recursos.
* **Configuração do Modo Multi-Database:** Ajustada a configuração do driver no DBeaver ("Show all databases") para permitir o gerenciamento de múltiplos bancos na mesma conexão.
* **Criação da Base de Dados:** Criação bem-sucedida do banco de dados dedicado chamado `basegeo`.
* **Ativação do PostGIS:** Extensão espacial habilitada com sucesso via comando CREATE EXTENSION IF NOT EXISTS postgis; e validada estruturalmente.
* **Criar a tabela `malha_uf`:** Executar o DDL de criação da tabela com a coluna geométrica (`GEOMETRY(MultiPolygon, 4326)`) e o índice espacial GIST.

---

### Etapa 2: Script de Ingestão de Dados (ETL em Python)

O objetivo desta etapa foi consumir a API oficial de malhas do IBGE, tratar as estruturas espaciais e persistir os dados geográficos de forma segura no banco local.

1. **Segurança de Credenciais (`.env`):**
* Instalação da biblioteca `python-dotenv`.
* Criação do arquivo `.env` para isolar variáveis sensíveis (`DB_USER`, `DB_PASSWORD`), garantindo que dados de acesso locais fiquem protegidos e fora do controle de versão do Git.


2. **Desenvolvimento do Script de Automação (`ingestion.py`):**
* Configuração de requisição HTTP assíncrona com `requests` para capturar a malha do Brasil no formato `application/vnd.geo+json` com subdivisão por UFs.
* Isolamento e iteração das 27 `features` geográficas retornadas (26 estados + DF).


3. **Tratamento de Desafios Técnicos (Erros de Tipagem Espacial):**
* **Problema:** O PostGIS impõe tipagem rígida e rejeitou a inserção de estados com polígonos contínuos e sem ilhas (enviados pelo IBGE como `Polygon`), pois a coluna `geom` foi modelada estritamente como `MultiPolygon`.
* **Solução:** Atualização da query de inserção para encapsular a conversão espacial utilizando a função **`ST_Multi()`** combinada com **`ST_GeomFromGeoJSON()`**. Isso garantiu a promoção automática de qualquer `Polygon` para `MultiPolygon` em tempo de execução.


4. **Validação da Carga:**
* Execução do script com sucesso no PowerShell.
* Confirmação da persistência através de consultas diretas no DBeaver via comando `SELECT id, codigo_uf, ST_AsText(geom) FROM malha_uf;`, comprovando o correto armazenamento das coordenadas espaciais indexadas.



---

### Etapa 3: Construção da API (Back-end com FastAPI)

Esta etapa transformou o banco de dados geográfico em um serviço web, criando uma API estável responsável por expor as malhas do IBGE em um padrão internacional de mapas.

1. **Estruturação do Ambiente Web:**
* Instalação do framework **FastAPI** e do servidor ASGI **Uvicorn**.
* Criação do diretório dedicado `/backend` e do arquivo `main.py`.
* Exportação do estado do ambiente virtual para o arquivo global `requirements.txt`.


2. **Configuração de Segurança CORS (Cross-Origin Resource Sharing):**
* Implementação do middleware `CORSMiddleware` configurado com `allow_origins=["*"]`. Esta etapa é crucial para permitir que a interface do front-end consuma os dados da API sem sofrer bloqueios de segurança nativos dos navegadores.


3. **Otimização de Performance Espacial:**
* Construção da rota `GET /api/v1/malhas/uf`.
* Em vez de processar coordenadas pesadas na camada de aplicação (Python), a API delega a serialização de dados geográficos diretamente ao banco através da função **`ST_AsGeoJSON(geom)`** do PostGIS, resultando em respostas de altíssima velocidade.


4. **Formatação no Padrão GeoJSON:**
* Criação de uma estrutura limpa no back-end que agrupa as linhas lidas do banco e gera um dicionário formatado estritamente como uma **`FeatureCollection`** do GeoJSON. Cada item encapsula o código do IBGE em `properties` e o desenho do mapa em `geometry`.


5. **Validação e Testes:**
* Inicialização do servidor via comando `uvicorn backend.main:app --reload`.
* Homologação e validação completa do funcionamento da API através da interface de testes automática do Swagger em `http://127.0.0.1:8000/docs`.
---

### Etapa 4: Interface Web (Front-end com HTML/CSS e Leaflet)

O objetivo desta etapa é construir a camada de apresentação da aplicação (Client-side), criando uma interface imersiva e de alta performance para a renderização de mapas vetoriais.

1. **Estruturação e Acoplamento de Dependências (`index.html`):**
   * Criação do arquivo estrutural básico da página web.
   * Integração dos pacotes de distribuição da biblioteca **Leaflet.js** utilizando redes de distribuição de conteúdo (CDNs) oficiais para o CSS e o motor JavaScript.
   * Definição do contêiner de montagem (`<div id="map"></div>`), elemento DOM que servirá de âncora onde o mapa será injetado e manipulado.

2. **Design de Interface Imersiva (`style.css`):**
   * Aplicação de técnicas de reset de estilos globais (`margin: 0; padding: 0; overflow: hidden;`) para eliminar margens nativas dos navegadores e evitar barras de rolagem indesejadas.
   * Configuração do contêiner do mapa utilizando unidades de medida baseadas no viewport do usuário (`width: 100vw; height: 100vh;`). Isso garante uma experiência imersiva (Full-Screen), adaptando o mapa automaticamente ao tamanho de qualquer tela ou monitor.

3. **Orquestração e Inicialização do Mapa Geográfico (`app.js`):**
   * **Instanciação do Objeto Base:** Utilização do construtor `L.map()` para converter a div HTML em um ambiente geográfico ativo.
   * **Definição Cartográfica Inicial:** Configuração do ponto de vista centralizado no território brasileiro (Latitude: `-14.2350`, Longitude: `-51.9253`) e definição do nível de zoom inicial em `4` (escala ideal para visualização continental).
   * **Injeção da Camada Base (Raster Tile Layer):** Conexão com o servidor de mapas do *OpenStreetMap* via método `L.tileLayer()`. O JavaScript fica responsável por realizar o download e o posicionamento dinâmico dos mosaicos de imagem de fundo à medida que o usuário interage com o mapa.

---

### Etapa 5: Integração e Refinamento

Esta etapa consolidou o fechamento do ciclo de desenvolvimento do ecossistema Web GIS, realizando o acoplamento completo entre a interface do cliente (Front-end) e o servidor de microsserviços (Back-end), além de refinar a experiência do usuário através de interatividades espaciais.

1. **Consumo Assíncrono de Dados (Fetch API):**
   * Implementação de uma requisição HTTP assíncrona utilizando a `Fetch API` nativa do JavaScript, apontando para o endpoint local do FastAPI (`http://127.0.0.1:8000/api/v1/malhas/uf`).
   * Tratamento de promessas (`Promises`) com validação de status de resposta (`response.ok`) e captura de exceções em bloco estruturado (`.catch`), garantindo resiliência caso a API esteja offline.

2. **Renderização Vetorial Fluida via Leaflet:**
   * Utilização do método especializado `L.geoJSON()` para fazer a leitura em tempo real da `FeatureCollection` recebida da API.
   * Injeção dinâmica dos polígonos das Unidades Federativas do Brasil sobre o mosaico de mapas do OpenStreetMap sem necessidade de recarregamento da página (Single Page Application behavior).

3. **Estilização Temática e Harmonia Visual:**
   * Customização estética do mapa através de uma função de estilo dedicada (`estiloEstado`), adotando uma paleta de cores verde-corporativa alinhada à identidade visual da Landing Page.
   * Definição técnica dos parâmetros de design: bordas nítidas em verde escuro (`#2e7d32`), preenchimento suave (`#81c784`) e opacidade equilibrada (`0.4`) para manter a legibilidade das vias e nomes do mapa base inferior.

4. **Interatividade Avançada (Eventos de Hover e Click):**
   * **Injeção de Popups Dinâmicos:** Uso do método `onEachFeature` para varrer os atributos de cada feição e vincular um balão de informações (`bindPopup`), exibindo o código oficial do IBGE formatado em HTML ao clicar em qualquer estado.
   * **Efeito Visual de Hover (`mouseover` e `mouseout`):** Implementação de ouvintes de eventos para destacar a região sob o cursor do mouse, aumentando a espessura da linha (`weight: 3`), escurecendo a bordas e elevando a opacidade de preenchimento (`0.7`). O método `bringToFront()` foi acoplado para garantir que o polígono focado assuma o topo da pilha de renderização, limpando o rastro visual imediatamente ao retirar o cursor.

---