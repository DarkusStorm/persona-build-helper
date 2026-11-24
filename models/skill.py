import sqlite3

from data.database import Database


class Skill:
    @staticmethod
    def criar(
        nome_en: str,
        nome_pt: str,
        descricao_en: str | None = None,
        descricao_pt: str | None = None,
        custo: str | None = None,
        elemento: str | None = None,
    ) -> int | None:
        query = """
            INSERT INTO skill (nome_en, nome_pt, descricao_en, descricao_pt, custo, elemento)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        with Database() as db:
            cursor = db.executar(
                query,
                (nome_en, nome_pt, descricao_en, descricao_pt, custo, elemento),
            )
            return cursor.lastrowid

    @staticmethod
    def buscar_todas() -> list[sqlite3.Row]:
        query = "SELECT * FROM skill ORDER BY nome_en ASC"
        with Database() as db:
            return db.buscar_tudo(query)

    @staticmethod
    def buscar_por_id(skill_id: int) -> sqlite3.Row | None:
        query = "SELECT * FROM skill WHERE id = ?"
        with Database() as db:
            return db.buscar_um(query, (skill_id,))

    @staticmethod
    def buscar_por_nome(nome_en: str) -> sqlite3.Row | None:
        """Útil para evitar cadastrar skills repetidas (ex: Garudyne, Maragidyne) entre personagens."""
        query = "SELECT * FROM skill WHERE nome_en = ?"
        with Database() as db:
            return db.buscar_um(query, (nome_en,))