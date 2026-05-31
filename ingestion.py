import os
import json
import requests
import psycopg2
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# 1. Configurações de Conexão puxadas dinamicamente do .env
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

IBGE_URL = "https://servicodados.ibge.gov.br/api/v4/malhas/paises/BR?formato=application/vnd.geo+json&qualidade=intermediaria&intrarregiao=UF"

def rodar_ingestao():
    print("📥 Buscando dados geográficos na API do IBGE...")
    resposta = requests.get(IBGE_URL)
    
    if resposta.status_code != 200:
        print(f"❌ Erro ao acessar a API do IBGE: Status {resposta.status_code}")
        return
        
    geojson_data = resposta.json()
    features = geojson_data.get("features", [])
    print(f"🌐 Sucesso! {len(features)} estados (UFs) encontrados no GeoJSON.")

    # 2. Conectar ao banco de dados basegeo
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        print("🔌 Conexão com o banco basegeo (PostGIS) estabelecida com sucesso!")

        # 3. Iterar e salvar cada estado no banco de dados
        print("💾 Iniciando a persistência espacial no banco...")
        for feature in features:
            codigo_uf = feature["properties"]["codarea"]
            geometria = feature["geometry"]
            geometria_str = json.dumps(geometria)

            query = """
                INSERT INTO malha_uf (codigo_uf, geom)
                VALUES (%s, ST_Multi(ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326)))
                ON CONFLICT (codigo_uf) DO NOTHING;
            """
            
            # Trecho corrigido sem o caractere intruso:
            cursor.execute(query, (codigo_uf, geometria_str))

        conn.commit()
        print("✨ Carga finalizada! Todos os dados espaciais foram salvos com sucesso.")

    except Exception as e:
        print(f"❌ Ocorreu um erro durante a ingestão: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    rodar_ingestao()