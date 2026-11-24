import sqlite3
from typing import Any

from data.database import Database


class PartyMember:
    @staticmethod
    def criar(game_id: str, nome: str, tipo_equipamento: str, wild_card: bool) -> int | None:
        query = """
            INSERT INTO party_member (game_id, nome, tipo_equipamento, wild_card)
            VALUES (?, ?, ?, ?)
        """
        with Database() as db:
            cursor = db.executar(query, (game_id, nome, tipo_equipamento, int(wild_card)))
            return cursor.lastrowid

    @staticmethod
    def buscar_por_jogo(game_id: str) -> list[sqlite3.Row]:
        query = "SELECT * FROM party_member WHERE game_id = ? ORDER BY id ASC"
        with Database() as db:
            return db.buscar_tudo(query, (game_id,))

    @staticmethod
    def buscar_por_id(member_id: int) -> sqlite3.Row | None:
        query = "SELECT * FROM party_member WHERE id = ?"
        with Database() as db:
            return db.buscar_um(query, (member_id,))

    @staticmethod
    def buscar_build_completa(member_id: int) -> dict[str, Any] | None:
        with Database() as db:
            membro = db.buscar_um("SELECT * FROM party_member WHERE id = ?", (member_id,))
            if not membro:
                return None

            equipamentos = db.buscar_tudo(
                "SELECT * FROM equipamento WHERE party_member_id = ? ORDER BY id ASC",
                (member_id,),
            )

            personas_rows = db.buscar_tudo(
                "SELECT * FROM persona WHERE party_member_id = ? ORDER BY estagio ASC",
                (member_id,),
            )

            personas_com_skills = []
            for p in personas_rows:
                skills = db.buscar_tudo(
                    """
                    SELECT s.*, ps.nivel_aprendizado, ps.como_obter_en, ps.como_obter_pt
                    FROM skill s
                    JOIN persona_skill ps ON s.id = ps.skill_id
                    WHERE ps.persona_id = ?
                    ORDER BY ps.nivel_aprendizado ASC
                    """,
                    (p["id"],),
                )
                personas_com_skills.append({
                    "dados": p,
                    "skills": skills,
                })

            return {
                "membro": membro,
                "equipamentos": equipamentos,
                "personas": personas_com_skills,
            }