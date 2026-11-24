import sqlite3

from data.database import Database


class Game:
    @staticmethod
    def criar(game_id: str, titulo: str) -> None:
        query = "INSERT OR IGNORE INTO game (id, titulo) VALUES (?, ?)"
        with Database() as db:
            db.executar(query, (game_id, titulo))

    @staticmethod
    def buscar_todos() -> list[sqlite3.Row]:
        query = "SELECT * FROM game"
        with Database() as db:
            return db.buscar_tudo(query)

    @staticmethod
    def buscar_por_id(game_id: str) -> sqlite3.Row | None:
        query = "SELECT * FROM game WHERE id = ?"
        with Database() as db:
            return db.buscar_um(query, (game_id,))