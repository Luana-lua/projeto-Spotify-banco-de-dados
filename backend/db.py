from flask import jsonify
import pyodbc
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

# Configurações de conexão
server = os.getenv('DB_SERVER')
database = os.getenv('DB_NAME')
trusted_connection = 'yes'


def get_connection():
    return pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};DATABASE={database};'
        f'Trusted_Connection={trusted_connection};'
    )


def buscar_musica(nome: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT Nome, DataLancamento, Streams, Danceability, Energy
    FROM Musica
    WHERE Nome LIKE ?
    ORDER BY Streams DESC
    """
    
    cursor.execute(query, f'%{nome}%')
    columns = [column[0] for column in cursor.description]
    resultados = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    conn.close()
    return resultados


def buscar_artista(nome: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    
    # Primeiro busca o artista
    cursor.execute("SELECT ID FROM Artista WHERE Nome LIKE ?", f'%{nome}%')
    artistas = cursor.fetchall()
    
    if not artistas:
        conn.close()
        return []
    
    resultados = []
    
    # Para cada artista encontrado, busca suas músicas
    for artista in artistas:
        artista_id = artista[0]
        
        # Busca as músicas do artista
        query = """
        SELECT m.Nome, m.DataLancamento, m.Streams
        FROM Musica m
        INNER JOIN Musica_Artista ma ON m.ID = ma.ID_Musica
        WHERE ma.ID_Artista = ?
        ORDER BY m.Streams DESC
        """
        cursor.execute(query, artista_id)
        columns = [column[0] for column in cursor.description]
        musicas = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        resultados.extend(musicas)
    
    conn.close()
    return resultados


def dados_plataformas() -> List[Dict[str, Any]]:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            p.Nome AS Plataforma,
            AVG(CAST(ISNULL(mp.Qtd_Playlists, 0) AS FLOAT)) AS Media_Playlists,
            AVG(CAST(ISNULL(mp.Qtd_Charts, 0) AS FLOAT)) AS Media_Charts
        FROM Plataforma p
        LEFT JOIN Musica_Plataforma mp ON p.ID = mp.ID_Plataforma
        GROUP BY p.Nome
        """
        
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        resultados = []
        
        for row in cursor.fetchall():
            # Converter None para 0.0
            row_dict = dict(zip(columns, row))
            row_dict['Media_Playlists'] = row_dict['Media_Playlists'] or 0.0
            row_dict['Media_Charts'] = row_dict['Media_Charts'] or 0.0
            resultados.append(row_dict)
        
        return resultados
    except Exception as e:
        print(f"Erro ao buscar dados das plataformas: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()

def buscar_generos() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT ID, Nome FROM Genero ORDER BY Nome"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    resultados = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    conn.close()
    return resultados

def buscar_musicas_por_genero(genero_id: int) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT 
        m.Nome, 
        m.DataLancamento, 
        m.Streams,
        a.Nome AS Artista
    FROM Musica m
    INNER JOIN Musica_Artista ma ON m.ID = ma.ID_Musica
    INNER JOIN Artista a ON ma.ID_Artista = a.ID
    WHERE m.GeneroID = ?
    ORDER BY m.Streams DESC
    """
    
    cursor.execute(query, genero_id)
    columns = [column[0] for column in cursor.description]
    resultados = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    conn.close()
    return resultados
