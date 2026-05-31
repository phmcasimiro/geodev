import os
import json
import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Carrega o arquivo .env localizado na raiz do projeto
load_dotenv()

app = FastAPI(title="GeoDev API", version="1.0.0")

# ⚠️ Configuração de CORS (Crucial para integração com o Front-end)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite que qualquer página web consuma esta API localmente
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurações do Banco de Dados
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def obter_conexao_banco():
    """Retorna uma conexão ativa com o banco basegeo."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.get("/")
def raiz():
    return {"mensagem": "API GeoDev está online e operando com PostGIS!"}

@app.get("/api/v1/malhas/uf")
def listar_malhas_uf():
    """
    Busca as geometrias no PostGIS, converte para strings GeoJSON
    e monta uma FeatureCollection válida para consumo em mapas web.
    """
    try:
        conn = obter_conexao_banco()
        cursor = conn.cursor()
        
        # Query otimizada: o PostGIS converte a geometria para texto GeoJSON direto no banco
        query = """
            SELECT codigo_uf, ST_AsGeoJSON(geom) as geojson 
            FROM malha_uf;
        """
        cursor.execute(query)
        linhas = cursor.fetchall()
        
        # Estrutura inicial do padrão GeoJSON esperado por bibliotecas como o Leaflet
        feature_collection = {
            "type": "FeatureCollection",
            "features": []
        }
        
        for linha in linhas:
            codigo_uf = linha[0]
            # O PostGIS retorna uma string JSON. Precisamos dar um 'loads' para virar dicionário Python
            geometria_dict = json.loads(linha[1])
            
            # Monta a estrutura de cada feição (Feature)
            feature = {
                "type": "Feature",
                "properties": {
                    "codigo_uf": codigo_uf
                },
                "geometry": geometria_dict
            }
            feature_collection["features"].append(feature)
            
        return feature_collection

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no banco de dados: {e}")
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()