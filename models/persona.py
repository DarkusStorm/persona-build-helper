import sqlite3

from data.database import Database


class Persona:
    @staticmethod
    def criar(
        party_member_id: int,
        nome: str,
        arcana: str,
        estagio: int = 1,
    ) -> int | None:
        query = """
            INSERT INTO persona (party_member_id, nome, arcana, estagio)
            VALUES (?, ?, ?, ?)
        """
        with Database() as db:
            cursor = db.executar(query, (party_member_id, nome, arcana, estagio))
            return cursor.lastrowid

    @staticmethod
    def buscar_por_membro(party_member_id: int) -> list[sqlite3.Row]:
        query = """
            SELECT * FROM persona
            WHERE party_member_id = ?
            ORDER BY estagio ASC
        """
        with Database() as db:
            return db.buscar_tudo(query, (party_member_id,))

    @staticmethod
    def buscar_por_id(persona_id: int) -> sqlite3.Row | None:
        query = "SELECT * FROM persona WHERE id = ?"
        with Database() as db:
            return db.buscar_um(query, (persona_id,))