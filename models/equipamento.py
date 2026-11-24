import sqlite3

from data.database import Database


class Equipamento:
    @staticmethod
    def criar(
        party_member_id: int,
        nome_en: str,
        nome_pt: str,
        atributos: str | None = None,
        como_obter_en: str | None = None,
        como_obter_pt: str | None = None,
    ) -> int | None:
        query = """
            INSERT INTO equipamento (
                party_member_id, nome_en, nome_pt, atributos, como_obter_en, como_obter_pt
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """
        with Database() as db:
            cursor = db.executar(
                query,
                (party_member_id, nome_en, nome_pt, atributos, como_obter_en, como_obter_pt),
            )
            return cursor.lastrowid

    @staticmethod
    def buscar_por_membro(party_member_id: int) -> list[sqlite3.Row]:
        query = "SELECT * FROM equipamento WHERE party_member_id = ? ORDER BY id ASC"
        with Database() as db:
            return db.buscar_tudo(query, (party_member_id,))

    @staticmethod
    def buscar_por_id(equipamento_id: int) -> sqlite3.Row | None:
        query = "SELECT * FROM equipamento WHERE id = ?"
        with Database() as db:
            return db.buscar_um(query, (equipamento_id,))