# SoundInsights - Análise de Sucesso Musical
Desenvolvido por: Arthur Pierry, Beatriz Araújo, Caio Tavares e Luana Ferreira

# 📌 Visão Geral
O SoundInsights é uma aplicação web que utiliza análise de dados para desvendar os fatores por trás do sucesso de músicas em plataformas digitais. Combinando métricas técnicas (Danceability, Energy, Valence) com dados reais de streams e desempenho em playlists, a ferramenta oferece insights estratégicos para:
- Produtores e gravadoras (otimização de lançamentos).

- Plataformas de streaming (curadoria inteligente de playlists).

- Artistas e estudantes (entendimento prático de tendências).

# ✨ Funcionalidades
Busca por música ou artista (com atributos técnicos).
Filtros por gênero e métricas (Danceability, Energy, Valence).
Rankings: Top 10 músicas por streams.
Análise de desempenho em plataformas.

# 🛠️ Tecnologias
- Backend: Python (Flask), SQL Server
- Frontend: HTML, CSS, Bootstrap, JavaScript
- Banco de Dados: Base pública do Spotify (Kaggle).

# 🚀 Como rodar o projeto localmente

✅Requisitos:
- SQL Server Management Studio (SSMS)
- ODBC Driver 17
- Python 3.10
- Git
- (Opcional) VS Code ou outro editor de sua preferência

# 🖥️ Criando as tabelas e inserindo os dados:
- Abrir o SSMS e definir o nome do servidor como 'localhost' e o nome do banco de dados como 'SpotifyDB'
- Executar os seguintes arquivos no SSMS, nesta ordem:
1. criar_tabelas.sql
2. insercao_spotify.sql

# 🖥️ Instruções para Windows para rodar o projeto:
#Clonar repositório
git clone https://github.com/Luana-lua/projeto-Spotify-banco-de-dados.git

#Navegar para o diretório do projeto
cd projeto-Spotify-banco-de-dados

#Instalações de bibliotecas necessárias
pip install python-dotenv Flask pyodbc

#--Mostrar instalações para verificaçar(caso necessário)--
pip show flask
pip show python-dotenv
pip show Flask
pip show pyodbc

#Rodar servidor
python app.py

#Acesse no navegador
http://127.0.0.1:3000


# 📌 Links Úteis
Vídeo de Apresentação: https://youtu.be/FeDLVA9Oa_8

Base de Dados Pública Utilizada: https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023