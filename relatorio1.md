# RELATÓRIO DE ESTÁGIO SUPERVISIONADO I

**CURSO:** Análise e Desenvolvimento de Sistemas (ADS)

**ESTAGIÁRIO:** Pedro Casimiro

**PROJETO:** GeoDev — Sistema de Análise e Visualização Espacial

**REPOSITÓRIO OFICIAL:** [https://github.com/phmcasimiro/geodev.git](https://github.com/phmcasimiro/geodev.git)

---

## Relatório 1: Infraestrutura, Modelagem Espacial e Esteira ETL

### 1. Introdução e Engenharia de Requisitos

O primeiro ciclo de atividades do estágio concentrou-se na fundação estrutural do projeto **GeoDev**, uma solução de inteligência geográfica baseada na web (Web GIS). O objetivo principal desta fase foi mapear as necessidades do sistema, preparar um ambiente de desenvolvimento isolado, modelar uma base de dados com suporte cartográfico e implementar um pipeline automatizado de extração, transformação e carga de dados (ETL).

Para o direcionamento técnico, foram estabelecidos os seguintes requisitos de engenharia de software:

* **Requisitos Funcionais (RF):** O sistema deve automatizar a captura de dados geográficos oficiais do IBGE e persistir essas feições de maneira íntegra para consumo posterior.
* **Requisitos Não-Funcionais (RNF):** O banco de dados deve utilizar indexação bidimensional para otimizar buscas espaciais; as credenciais de acesso locais devem ser protegidas fora do controle de versão; e a estrutura do projeto deve ser portável e independente do sistema operacional hospedeiro.

---

### 2. Configuração da Infraestrutura Local e Versionamento

A estruturação do ecossistema técnico priorizou as boas práticas de portabilidade de código e o isolamento de dependências.

* **Versionamento e Governança:** O projeto foi inicializado através do Git e acoplado ao repositório remoto no GitHub. Configurou-se um arquivo `.gitignore` estrito para impedir a indexação de arquivos de cache (`__pycache__`), diretórios virtuais e chaves de configuração locais. Adicionalmente, ajustou-se a governança do Git para tratar de forma segura as quebras de linha (`CRLF` vs `LF`) entre ambientes Windows e Linux.
* **Isolamento do Ambiente Python:** Para o desenvolvimento dos scripts de automação, instanciou-se um ambiente virtual isolado (`.venv`) rodando Python 3.12+. As bibliotecas core utilizadas foram controladas via arquivo de requerimentos (`requirements.txt`).
* **Segurança de Credenciais:** Adotou-se a biblioteca `python-dotenv` para criar uma barreira de segurança através de um arquivo `.env` local, hospedando as variáveis sensíveis de infraestrutura.
* **Conteinerização:** A camada de persistência foi provisionada por meio de um container Docker rodando em uma instância compartilhada. O ecossistema foi centralizado na porta padrão `5432`, executando uma imagem base Linux Debian com o motor relacional PostgreSQL e suporte nativo a dados geográficos.

---

### 3. Modelagem de Dados Espaciais no SGBD

A modelagem lógica e física do banco de dados exigiu regras específicas da ciência da computação espacial, distanciando-se de modelagens puramente alfanuméricas.

Utilizou-se o SGBD **PostgreSQL 15.4** tunado com a extensão **PostGIS 3.3.4** (composto pelas bibliotecas core `GEOS 3.9.0` e `PROJ 7.2.1`). Através da IDE DBeaver, ajustou-se a configuração do driver para o modo *Multi-Database* ("Show all databases"), permitindo a gerência isolada da nova base de dados criada, batizada de **`basegeo`**.

Dentro do schema `public`, a tabela **`malha_uf`** foi criada por meio do seguinte script DDL (Data Definition Language):

```sql
CREATE TABLE malha_uf (
    id SERIAL PRIMARY KEY,
    codigo_uf VARCHAR(2) UNIQUE NOT NULL, -- Armazena o código de 2 dígitos do IBGE (ex: '53' para DF)
    geom GEOMETRY(MultiPolygon, 4326)     -- Coluna espacial usando o SRID 4326 (WGS 84)
);

-- Criação do índice espacial GiST
CREATE INDEX idx_malha_uf_geom ON malha_uf USING GIST(geom);

```

> 🧠 **Nota de Engenharia (Indexação Espacial):** Ao contrário dos índices tradicionais do tipo B-Tree (lineares), o índice **GiST (Generalized Search Tree)** organiza os dados geométricos por meio de partições hierárquicas conhecidas como *Bounding Boxes* (caixas envolventes). Essa estrutura otimiza drasticamente as futuras varreduras bidimensionais no mapa, permitindo que o banco intercepte e filtre coordenadas geográficas sem realizar leituras sequenciais completas na tabela.

---

### 4. Implementação da Esteira de Ingestão de Dados (Pipeline ETL)

Com a infraestrutura validada, foi desenvolvido o script de automação **`ingestion.py`**, estabelecendo a primeira conexão física entre o interpretador Python e o banco de dados via driver `psycopg2-binary`. O script desempenha o papel de um pipeline de ETL dividindo-se em três etapas claras:

1. **Extração:** Disparo de requisição HTTP síncrona (via biblioteca `requests`) consumindo a API oficial de malhas do IBGE, capturando em tempo real a malha do Brasil subdividida em Unidades Federativas.
2. **Transformação:** O arquivo bruto retornado foi tratado como um objeto JSON estruturado. O script isolou as 27 *features* espaciais (26 estados + DF), convertendo os dicionários de coordenadas nativos do Python em strings de texto limpas via `json.dumps()`.
3. **Carga:** Iteração e persistência dos dados no banco utilizando cláusulas de salvaguarda contra duplicidade (`ON CONFLICT DO NOTHING`).

#### 🛠️ Resolução do Desafio Técnico de Tipagem Cartográfica

Durante a execução inicial da esteira de carga, o banco de dados interrompeu a transação retornando a seguinte exceção de restrição geométrica: `Geometry type (Polygon) does not match column type (MultiPolygon)`.

* **Análise do Problema:** A coluna `geom` da tabela foi estritamente modelada como `MultiPolygon` para suportar estados com ilhas ou territórios desconectados. Porém, a API do IBGE otimiza os payloads enviando estados com massas de terra contínuas (como Minas Gerais ou Goiás) sob a tipagem primitiva simples `Polygon`.
* **Solução Implementada:** A query de persistência dentro do laço Python foi refatorada. Aplicou-se a combinação das funções espaciais **`ST_GeomFromGeoJSON()`** para ler a string de texto e **`ST_Multi()`** para envelopar e promover automaticamente qualquer polígono simples para polígono múltiplo em tempo de execução, harmonizando os registros sob a projeção global **WGS 84 (SRID: 4326)**.

```python
query = """
    INSERT INTO malha_uf (codigo_uf, geom)
    VALUES (%s, ST_Multi(ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326)))
    ON CONFLICT (codigo_uf) DO NOTHING;
"""

```

**Validação da Carga:** O pipeline foi executado com sucesso através do PowerShell. A validação final foi realizada diretamente no DBeaver utilizando a instrução `SELECT id, codigo_uf, ST_AsText(geom) FROM malha_uf;`, confirmando o correto armazenamento e a indexação de todos os 27 territórios nacionais.

---

### 5. Considerações Finais do Relatório 1

Este primeiro ciclo concluiu com êxito a montagem do alicerce tecnológico do projeto GeoDev. O isolamento do ambiente de desenvolvimento local, a proteção de variáveis de ambiente sensíveis, a criação da base de dados indexada no PostGIS e o sucesso da esteira de ingestão de dados garantem que o sistema possua uma base de dados populada e de alta performance. O ecossistema está maduro e preparado para o início do desenvolvimento da camada de microsserviços e APIs de entrega web.