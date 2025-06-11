
-- Tabela de Gêneros
CREATE TABLE Genero (
    ID INT PRIMARY KEY,
    Nome NVARCHAR(100) NOT NULL
);

-- Tabela de Artistas
CREATE TABLE Artista (
    ID INT PRIMARY KEY,
    Nome NVARCHAR(255) NOT NULL
);

-- Tabela de Músicas
CREATE TABLE Musica (
    ID INT PRIMARY KEY,
    Nome NVARCHAR(255) NOT NULL,
    DataLancamento DATE,
    BPM INT,
    Tom NVARCHAR(10),
    Modo NVARCHAR(10),
    Streams BIGINT,
    Danceability INT,
    Valence INT,
    Energy INT,
    Acousticness INT,
    Instrumentalness INT,
    Liveness INT,
    Speechiness INT,
    GeneroID INT FOREIGN KEY REFERENCES Genero(ID)
);

-- Tabela de Plataformas
CREATE TABLE Plataforma (
    ID INT PRIMARY KEY,
    Nome NVARCHAR(100) NOT NULL
);

-- Relacionamento N:N entre Música e Artista
CREATE TABLE Musica_Artista (
    ID_Musica INT,
    ID_Artista INT,
    PRIMARY KEY (ID_Musica, ID_Artista),
    FOREIGN KEY (ID_Musica) REFERENCES Musica(ID),
    FOREIGN KEY (ID_Artista) REFERENCES Artista(ID)
);

-- Relacionamento N:N entre Música e Plataforma
CREATE TABLE Musica_Plataforma (
    ID_Musica INT,
    ID_Plataforma INT,
    Qtd_Playlists INT,
    Qtd_Charts INT,
    PRIMARY KEY (ID_Musica, ID_Plataforma),
    FOREIGN KEY (ID_Musica) REFERENCES Musica(ID),
    FOREIGN KEY (ID_Plataforma) REFERENCES Plataforma(ID)
);
