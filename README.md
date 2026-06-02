# 📌 Sobre o GeoDev

O **GeoDev** é uma plataforma **Web GIS Full-Stack** (Sistema de Informação Geográfica para a Web) que transforma dados cartográficos brutos em um mapa totalmente interativo, visual e fluido direto no navegador.

O projeto une a **Ciência Geográfica** às tecnologias modernas de **Engenharia de Software** para demonstrar como capturar, processar de forma inteligente e renderizar malhas territoriais complexas com alta performance.

---

### 🔄 Como o Sistema Funciona? (O Fluxo dos Dados)

O ciclo de vida dos dados dentro do ecossistema é dividido em 4 passos simples:

* **1. Captura Automatizada (ETL):** Um script em Python se conecta à API oficial do **IBGE**, extrai o mapa bruto do Brasil subdividido em estados e limpa as informações.
* **2. Armazenamento Inteligente:** Esses dados geográficos são salvos no **PostgreSQL** com a extensão espacial **PostGIS**. Em vez de textos comuns, o banco armazena e indexa geometrias cartográficas reais de forma ultra-rápida.
* **3. Distribuição via API:** Um back-end construído com **FastAPI** atua como o garçom do sistema. Ele faz consultas otimizadas no banco de dados e entrega os mapas formatados no padrão internacional **GeoJSON**.
* **4. Interface Visual (Front-end):** Uma *Landing Page* moderna e corporativa utiliza a biblioteca **Leaflet.js** para ler a API e desenhar o mapa interativo na tela do usuário.

---

### 🎨 Recursos Visuais e Diferenciais

* **Interatividade Espacial (Hover):** Ao passar o mouse sobre qualquer estado do Brasil, o polígono ganha destaque visual imediato, alterando sua cor, borda e opacidade em tempo real.
* **Consulta de Metadados (Click):** Clicar sobre uma região dispara um balão (*Popup*) que exibe informações dinâmicas injetadas pelo banco de dados, como o código oficial do IBGE.
* **Alta Performance:** Todo o cálculo pesado de coordenadas é feito direto no motor do banco de dados. A página web recebe o arquivo leve e pronto, carregando o mapa em milissegundos.
* **Arquitetura Profissional:** O ambiente é totalmente isolado e portável com **Docker**, utiliza segurança de dados via variáveis de ambiente (`.env`) e proteção contra bloqueios de rede do navegador (**CORS**).

---

### 🛠️ Tecnologias Utilizadas

* **Banco de Dados:** PostgreSQL 15 + PostGIS 3.3 (Persistência e Computação Espacial)
* **Back-end & Automação:** Python 3.12, FastAPI, Uvicorn e Psycopg2 (API e Esteira ETL)
* **Front-end:** HTML5, CSS3 (Flexbox/Grid) e Leaflet.js (Camada Visual e Cartográfica)
* **Infraestrutura:** Docker (Conteinerização) e Git/GitHub (Versionamento de Código)

---

# 🚀 Guia de Inicialização e Ativação Rápida

Toda vez que precisar subir o ecossistema **GeoDev** do zero para trabalhar ou demonstrar a aplicação, siga os 3 passos abaixo na ordem indicada.

---

### 🗺️ Pré-requisitos de Infraestrutura
Certifique-se de que o **Docker Desktop** está aberto e rodando no seu Windows. Como estamos reutilizando uma instância compartilhada, o container que gerencia a porta `5432` precisa estar com o status **Running** (Verde).

---

### 🔌 Passo 1: Validar o Banco de Dados (Opcional)
Se quiser garantir que o banco `basegeo` e a tabela `malha_uf` estão operacionais antes de ligar a API:
1. Abra o **DBeaver**.
2. Conecte-se na sua instância padrão.
3. Certifique-se de que o banco `basegeo` está acessível.

---

### ⚡ Passo 2: Inicializar o Back-end (FastAPI)
A API precisa ser iniciada através do ambiente virtual isolado do Python.

1. Abra o **PowerShell** ou o terminal do seu VS Code na raiz do projeto (`C:\Users\HP\Documents\Projetos\graduacao`).
2. Ative o ambiente virtual (`.venv`) rodando o comando:
   ```powershell
   .\.venv\Scripts\Activate.ps1


*(O prefixo `(.venv)` deve aparecer no início da linha do terminal)*.

3. Inicie o servidor ASGI **Uvicorn** com recarregamento automático ativado:
```bash
uvicorn backend.main:app --reload

```


4. **Mantenha este terminal aberto.** O servidor estará escutando na porta `http://127.0.0.1:8000`.

---

### 🎨 Passo 3: Abrir a Interface Web (Front-end)

Com a infraestrutura e o back-end ativos, a camada visual já pode ser renderizada.

1. Abra o Explorador de Arquivos do Windows e navegue até a pasta do projeto:
`...\Projetos\graduacao\frontend\`
2. Dê um **duplo clique** no arquivo **`index.html`** para abri-lo no seu navegador padrão.
3. Role a Landing Page até a seção do mapa e interaja com os polígonos das UFs do Brasil.

---

## 🔍 Checklist de Verificação (Caso algo dê errado)

Se o mapa não exibir os polígonos dos estados, verifique rapidamente os seguintes pontos:

| Sintoma | Causa Provável | Como Corrigir |
| --- | --- | --- |
| **Erro de conexão no terminal da API** | O arquivo `.env` sumiu ou o container Docker está desligado. | Ligue o container no Docker Desktop e cheque as credenciais no `.env`. |
| **Mapa carrega vazio (sem estados)** | A API do FastAPI está desligada ou travou. | Vá ao terminal do Uvicorn e verifique se ele reporta erros na rota `/api/v1/malhas/uf`. |
| **Erro de CORS no console do navegador** | O middleware de segurança do FastAPI não foi carregado corretamente. | Reinicie o servidor Uvicorn com `Ctrl + C` e rode o comando de inicialização novamente. |

*Para limpar o cache do navegador e forçar o JavaScript a refazer a busca limpa dos dados na API, utilize o atalho **`Ctrl + F5`** na página do mapa.*

```

```