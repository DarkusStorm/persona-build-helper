import pytest

from app import app
from data.database import Database, init_db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_rotas_principais(client):
    for rota in ['/', '/p3r', '/p4g', '/p5r']:
        resposta = client.get(rota)
        assert resposta.status_code == 200

def test_banco_em_memoria():
    # Banco temporário
    init_db(":memory:")
    with Database(":memory:") as db:
        db.executar("CREATE TABLE game (id TEXT PRIMARY KEY, titulo TEXT)")
        db.executar("INSERT INTO game VALUES (?, ?)", ("p3r", "Persona 3 Reload"))
        jogo = db.buscar_um("SELECT * FROM game WHERE id = ?", ("p3r",))
        assert jogo["titulo"] == "Persona 3 Reload"