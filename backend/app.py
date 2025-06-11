import os
from flask import Flask, render_template, request, jsonify
import db

app = Flask(
    __name__,
    template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
)

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para renderizar test.html com dados
@app.route('/top-musicas')
def top_musicas():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 10 Nome, Streams FROM Musica ORDER BY Streams DESC")
    musicas = cursor.fetchall()
    conn.close()
    return render_template("test.html", musicas=musicas)

# Rota para busca de músicas (AJAX)
@app.route('/buscar-musica', methods=['POST'])
def buscar_musica():
    nome = request.json.get('nome', '')
    resultados = db.buscar_musica(nome)
    return jsonify(resultados)

# Rota para busca de artistas (AJAX)
@app.route('/buscar-artista', methods=['POST'])
def buscar_artista():
    nome = request.json.get('nome', '')
    resultados = db.buscar_artista(nome)
    return jsonify(resultados)

# Rota para dados das plataformas
@app.route('/dados-plataformas')
def dados_plataformas():
    conn = db.get_connection()
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
    plataformas = cursor.fetchall()
    conn.close()
    
    # Converter para dicionário tratando valores nulos
    dados = []
    for row in plataformas:
        dados.append({
            'Plataforma': row.Plataforma,
            'Media_Playlists': float(row.Media_Playlists) if row.Media_Playlists is not None else 0.0,
            'Media_Charts': float(row.Media_Charts) if row.Media_Charts is not None else 0.0
        })
    
    return jsonify(dados)

# Rota para obter lista de gêneros
@app.route('/generos')
def generos():
    generos = db.buscar_generos()
    return jsonify(generos)

# Rota para buscar músicas por gênero
@app.route('/buscar-por-genero', methods=['POST'])
def buscar_por_genero():
    genero_id = request.json.get('genero_id')
    if not genero_id:
        return jsonify([])
    
    resultados = db.buscar_musicas_por_genero(genero_id)
    return jsonify(resultados)

@app.route('/filtrar-musicas', methods=['POST'])
def filtrar_musicas():
    genero_id = request.json.get('genero_id')
    ordenar_por = request.json.get('ordenar_por')

    conn = db.get_connection()
    cursor = conn.cursor()

    base_query = """
        SELECT 
            m.Nome, 
            m.DataLancamento, 
            m.Streams,
            m.Danceability,
            m.Valence,
            m.Energy,
            a.Nome AS Artista
        FROM Musica m
        INNER JOIN Musica_Artista ma ON m.ID = ma.ID_Musica
        INNER JOIN Artista a ON ma.ID_Artista = a.ID
    """

    params = []
    where_clause = ""
    if genero_id:
        where_clause = "WHERE m.GeneroID = ?"
        params.append(genero_id)

    order_clause = ""
    if ordenar_por in ['Danceability', 'Valence', 'Energy']:
        order_clause = f"ORDER BY m.{ordenar_por} DESC"
    else:
        order_clause = "ORDER BY m.Streams DESC"

    final_query = f"{base_query} {where_clause} {order_clause}"
    cursor.execute(final_query, params)

    columns = [column[0] for column in cursor.description]
    resultados = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
