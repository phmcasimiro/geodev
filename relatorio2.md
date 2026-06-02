# RELATÓRIO DE ESTÁGIO SUPERVISIONADO II

**CURSO:** Análise e Desenvolvimento de Sistemas (ADS)

**ESTAGIÁRIO:** Pedro Casimiro

**PROJETO:** GeoDev — Sistema de Análise e Visualização Espacial

**REPOSITÓRIO OFICIAL:** [https://github.com/phmcasimiro/geodev.git](https://github.com/phmcasimiro/geodev.git)

---

## Relatório 2: Engenharia de Back-end, Endpoints RESTful e Otimização Espacial

### 1. Arquitetura do Serviço Web e Lógica Assíncrona

O segundo ciclo de atividades do estágio teve como escopo a transformação do banco de dados geográfico em um serviço web distribuído. Para atuar como a ponte lógica entre a persistência de dados e a camada do cliente, foi projetado e implementado o back-end da aplicação utilizando o ecossistema **FastAPI** e o servidor ASGI **Uvicorn**.

A escolha desta pilha tecnológica justificou-se pelos seguintes critérios de engenharia de software:

* **Lógica Assíncrona:** Capacidade nativa de gerenciar múltiplas requisições simultâneas sem bloqueio de thread (*non-blocking I/O*), o que é essencial para o tráfego de dados volumosos como coordenadas cartográficas.
* **Modularidade e Desacoplamento:** Criação do diretório isolado `/backend` e centralização do ponto de entrada do serviço no arquivo `main.py`, separando totalmente a lógica de consumo do script de ingestão desenvolvido no relatório anterior.

---

### 2. Controle de Acesso e Segurança de Rede (CORS)

Durante o desenvolvimento de arquiteturas distributivas (onde o servidor e o cliente operam em contextos distintos), um dos principais desafios de rede é o bloqueio nativo de segurança dos navegadores conhecido como **CORS (Cross-Origin Resource Sharing)**.

* **O Problema:** Por padrão, um navegador bloqueia requisições de scripts que tentam acessar uma API hospedada em uma origem (porta ou domínio) diferente da origem de onde o script está sendo executado.
* **A Solução:** Implementou-se no código o componente `CORSMiddleware` fornecido pelo FastAPI. O back-end foi configurado para injetar cabeçalhos HTTP específicos nas respostas de rede (`allow_origins=["*"]`, `allow_methods=["*"]`, `allow_headers=["*"]`). Essa configuração liberou o controle de origens cruzadas de forma segura, permitindo que a futura interface em HTML/JavaScript consuma os endpoints locais sem sofrer interrupções de segurança no navegador.

---

### 3. Otimização de Performance e Computação Espacial no SGBD

Um gargalo crítico na engenharia de dados geográficos é a perda de performance ao serializar geometrias pesadas do formato binário do banco para objetos legíveis na aplicação. Para solucionar essa restrição e garantir respostas em tempo subsegundo, adotou-se o padrão de **Delegação de Computação ao SGBD**.

Em vez de trazer os dados espaciais brutos para o Python e realizar a conversão em nível de aplicação, a rota executa uma query otimizada utilizando a função nativa do PostGIS **`ST_AsGeoJSON(geom)`**:

```sql
SELECT codigo_uf, ST_AsGeoJSON(geom) as geojson 
FROM malha_uf;

```

> 🧠 **Nota de Engenharia (Performance Espacial):** Ao utilizar a função `ST_AsGeoJSON()`, o processamento de baixo nível para converter os polígonos binários complexos em texto formatado é executado diretamente na memória do motor do PostGIS, que é altamente otimizado em linguagem C. O Python recebe a estrutura praticamente pronta, atuando apenas como um roteador e poupando ciclos severos de processamento da CPU do back-end.

---

### 4. Padronização de Payload (GeoJSON FeatureCollection)

Para que a API seja interoperável e possa ser consumida por qualquer software de geoprocessamento do mercado, o payload de resposta da rota **`GET /api/v1/malhas/uf`** foi padronizado estritamente sob as especificações da RFC 7946 (padrão internacional GeoJSON).

O script coleta as linhas retornadas pelo banco e reconstrói o objeto sob a hierarquia de uma **`FeatureCollection`**:

1. O texto retornado pelo PostGIS é convertido em um dicionário estruturado através do método `json.loads()`.
2. O back-end monta dinamicamente o array de feições, onde cada estado do país é envelopado como uma `Feature`.
3. Os atributos alfanuméricos (como o código do IBGE) são injetados na chave `properties`, enquanto as coordenadas puras alimentam a chave `geometry`.

Essa padronização garante que a API entregue um JSON perfeitamente encapsulado, pronto para ser mapeado de forma automática por bibliotecas de mapas no client-side.

---

### 5. Validação Automatizada e Ciclo de Vida de Recursos

Como parte da cultura de garantia de qualidade (QA) e governança de código, o desenvolvimento do back-end incorporou rotinas estritas de validação e controle de recursos de infraestrutura:

* **Documentação Técnica Interativa:** Com a integração nativa do FastAPI à especificação OpenAPI, o endpoint `/docs` passou a disponibilizar a interface do **Swagger UI**. Isso permitiu testar a rota diretamente pelo navegador, inspecionar a árvore do JSON retornado e validar o tempo de resposta do servidor.
* **Prevenção de Vazamento de Conexões (*Connection Leaks*):** Toda a comunicação com a base de dados `basegeo` foi estruturada dentro de blocos de tratamento de exceção `try/except/finally`. Garantiu-se que, independentemente do sucesso ou falha na requisição, os métodos `.close()` sejam obrigatoriamente invocados no bloco `finally` tanto para o cursor quanto para a conexão física com o PostgreSQL, evitando o esgotamento do pool de conexões do banco de dados sob cenários de alta concorrência.

---

### 6. Considerações Finais do Relatório 2

Este segundo ciclo concluiu a entrega da inteligência de back-end do ecossistema GeoDev. Com as rotas mapeadas, a segurança de rede (CORS) tratada, a computação espacial otimizada diretamente no PostGIS e o payload padronizado internacionalmente como GeoJSON, o microsserviço está totalmente estabilizado. A aplicação encontra-se pronta e madura para receber a implementação da interface visual do cliente e fechar o ciclo de integração de dados.