DROP TABLE IF EXISTS tb_instituicao CASCADE;
DROP TABLE IF EXISTS tb_uf CASCADE;
DROP TABLE IF EXISTS tb_municipio CASCADE;
DROP TABLE IF EXISTS tb_mesorregiao CASCADE;
DROP TABLE IF EXISTS tb_microrregiao CASCADE;

CREATE TABLE tb_uf (
    coduf INTEGER PRIMARY KEY,
    uf TEXT,
    nomeestado TEXT,
    regiao TEXT
);

CREATE TABLE tb_mesorregiao (
    codmesorregiao INTEGER PRIMARY KEY,
    mesorregiao TEXT,
    coduf INTEGER,
    regiao TEXT,
    FOREIGN KEY (coduf) REFERENCES tb_uf (coduf)
);

CREATE TABLE tb_microrregiao (
    codmicrorregiao INTEGER PRIMARY KEY,
    microrregiao TEXT,
    codmesorregiao INTEGER,
    coduf INTEGER,
    regiao TEXT,
    FOREIGN KEY (coduf) REFERENCES tb_uf (coduf),
    FOREIGN KEY (codmesorregiao) REFERENCES tb_mesorregiao (codmesorregiao)
);

CREATE TABLE tb_municipio (
    idmunicipio INTEGER PRIMARY KEY,
    nomemunicipio TEXT,
    coduf INTEGER,
    regiao TEXT,
    codmesorregiao INTEGER,
    codmicrorregiao INTEGER,
    FOREIGN KEY (coduf) REFERENCES tb_uf (coduf),
    FOREIGN KEY (codmesorregiao) REFERENCES tb_mesorregiao (codmesorregiao),
    FOREIGN KEY (codmicrorregiao) REFERENCES tb_microrregiao (codmicrorregiao)
);

CREATE TABLE tb_instituicao (
    regiao TEXT,
    codregiao INTEGER,
    uf TEXT,
    coduf INTEGER,
    municipio TEXT,
    codmunicipio INTEGER,
    entidade TEXT,
    codentidade INTEGER,
    matriculas_base INTEGER,
    ano INTEGER,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (codentidade, ano),
    FOREIGN KEY (codmunicipio) REFERENCES tb_municipio (idmunicipio)
);
