# RELATÓRIO DE ESTÁGIO SUPERVISIONADO III

**CURSO:** Análise e Desenvolvimento de Sistemas (ADS)

**ESTAGIÁRIO:** Pedro Casimiro

**PROJETO:** GeoDev — Sistema de Análise e Visualização Espacial

**REPOSITÓRIO OFICIAL:** [https://github.com/phmcasimiro/geodev.git](https://github.com/phmcasimiro/geodev.git)

---

## Relatório 3: Interface do Cliente, Integração Assíncrona e Engenharia de Usabilidade

### 1. Arquitetura Frontend e Design de Apresentação (HTML5/CSS3)

O terceiro e último ciclo de atividades do estágio englobou o desenvolvimento da camada de apresentação da aplicação (*Client-side*). O escopo desta fase consistiu em criar uma interface imersiva e de alta usabilidade que integrasse o mapa interativo não como uma tela isolada, mas como um componente central de uma *Landing Page* corporativa de engenharia de dados.

A estruturação da interface baseou-se em padrões modernos de design e semântica web:

* **Estruturação Semântica:** O arquivo `frontend/index.html` foi segmentado utilizando as tags semânticas do HTML5 (`<header>`, `<nav>`, `<section>`), organizando a página em seções fluidas: Barra Superior de Contatos, Seção *Hero* (Banner Principal), Grade de Cartões de Recursos Tecnológicos, Seção do Webmap e painel institucional "Sobre".
* **Design Responsivo e Layout de Alto Impacto:** No arquivo `frontend/style.css`, aplicou-se engenharia de folhas de estilo baseada em CSS Grid e Flexbox. Para o Banner Principal, utilizou-se unidades baseadas no viewport do navegador (`140px 0 180px 0` de padding), criando uma transição onde os cartões de recursos flutuam e sobrepõem o banner através de margens negativas (`margin-top: -100px`) e controle de empilhamento de camadas (`z-index: 3`). A moldura do mapa foi projetada para atuar de forma responsiva, com uma altura fixa controlada de `600px`, ideal para a usabilidade em resoluções desktop e portfólios profissionais.

---

### 2. Orquestração Cartográfica Client-Side com Leaflet.js

A inicialização e o gerenciamento de projeções cartográficas no navegador do usuário foram delegados à biblioteca de mapeamento de código aberto **Leaflet.js**, acoplada ao projeto via redes de distribuição de conteúdo (CDNs).

O JavaScript (`frontend/app.js`) assumiu o papel de motor cartográfico através das seguintes ações estruturadas:

* **Instanciação do Contexto Geográfico:** Utilizou-se o construtor `L.map('map')` para capturar a div HTML correspondente e convertê-la em uma área geográfica ativa, definindo as coordenadas do centro geográfico do Brasil (Latitude: `-14.2350`, Longitude: `-51.9253`) e um fator de escala de zoom inicial nível `4`.
* **Injeção da Camada de Mosaicos (Raster Tile Layer):** Conexão com o servidor de mapas raster do *OpenStreetMap* por meio do método `L.tileLayer()`. O motor JavaScript gerencia em tempo de execução o download e o posicionamento dinâmico dos quadrantes de imagem de fundo conforme o usuário interage, arrasta ou altera a escala do mapa, limitando o teto de zoom ao nível `19` para evitar perda de resolução do mapa de fundo.

---

### 3. Comunicação Inter-Sistemas e Consumo Assíncrono (Fetch API)

Com a interface estruturada e o mapa base inicializado, implementou-se o acoplamento definitivo entre o cliente web e o servidor de microsserviços criado no relatório anterior.

A engenharia de comunicação utilizou o mecanismo nativo **Fetch API** do JavaScript para realizar requisições assíncronas em segundo plano:

```javascript
// Requisição em segundo plano via Promises
fetch(API_URL)
    .then(response => response.json())
    .then(geoJsonData => { /* Lógica de renderização espacial */ })

```

O fluxo de integração segue o modelo de ciclo de vida assíncrono: o navegador renderiza a interface visual instantaneamente e, em paralelo, o JavaScript dispara uma promessa (`Promise`) em direção ao endpoint `http://127.0.0.1:8000/api/v1/malhas/uf`. Ao receber o payload estruturado como *FeatureCollection*, o JavaScript intercepta o fluxo e injeta os dados espaciais no mapa de forma dinâmica, sem a necessidade de recarregar a página, simulando o comportamento de uma *Single Page Application (SPA)* de alta performance.

---

### 4. Engenharia de Usabilidade e Refinamento de UX Espacial

Para elevar o software ao nível de maturidade de mercado, foram desenvolvidas rotinas avançadas de manipulação de vetores no *client-side*, focando na experiência do usuário (UX).

* **Harmonização Visual Temática:** Criou-se a função `estiloEstado()`, responsável por interceptar a geometria injetada e aplicar propriedades estéticas que casam com a identidade visual verde-corporativa da Landing Page. Configurou-se as bordas das fronteiras em verde escuro (`#2e7d32`), espessura de `1.5` pixels e preenchimento interno suave (`#81c784`) com opacidade calibrada em `0.4` para preservar a visualização das vias terrestres da camada base.
* **Injeção de Metadados via Popups:** Através da propriedade `onEachFeature`, o script varre as propriedades alfanuméricas contidas no GeoJSON e vincula um balão de informações dinâmico (`bindPopup`) a cada polígono. Ao clicar em um estado, o sistema exibe o código de área do IBGE formatado em HTML.
* **Manipulação Dinâmica de Eventos de Tela (Hover):** Implementou-se ouvintes de eventos de mouse (`mouseover` e `mouseout`) para criar respostas visuais imediatas à navegação do usuário:

```javascript
mouseover: function (e) {
    const layer = e.target;
    layer.setStyle({ weight: 3, color: '#1b5e20', fillOpacity: 0.7 });
    layer.bringToFront(); // Evita oclusão de bordas vizinhas
}

```

> 🧠 **Nota de Engenharia (Manipulação do DOM Espacial):** Em mapas web, os polígonos são desenhados como elementos de vetor SVG na árvore do navegador. Quando o usuário passa o mouse sobre um estado, o método **`bringToFront()`** reposiciona o elemento SVG correspondente no topo da pilha de renderização. Isso impede que as linhas de fronteira expandidas pelo efeito visual de destaque sejam sobrepostas ou cortadas pelos polígonos dos estados vizinhos, mitigando bugs visuais de oclusão.

---

### 5. Considerações Finais do Estágio (Encerramento do Ciclo)

A conclusão do Relatório 3 marca o encerramento do ciclo de desenvolvimento do projeto **GeoDev**. O ecossistema completo foi integrado com sucesso, provando a viabilidade técnica de uma arquitetura que separa rigorosamente a persistência cartográfica indexada (PostGIS), as rotas de transmissão distribuída (FastAPI) e a interface imersiva enriquecida com eventos assíncronos de mapas (Leaflet.js/Fetch API).

As competências adquiridas durante o estágio englobaram desde o provisionamento de infraestrutura ágil e modelagem de dados espaciais até a segurança de rede (CORS) e técnicas avançadas de engenharia de usabilidade no front-end. O código final encontra-se devidamente documentado, padronizado segundo as RFCs internacionais e publicado no repositório oficial do GitHub para livre distribuição.