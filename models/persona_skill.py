import sqlite3

from data.database import Database


class PersonaSkill:
    @staticmethod
    def vincular(
        persona_id: int,
        skill_id: int,
        nivel_aprendizado: int = 1,
        como_obter_en: str | None = None,
        como_obter_pt: str | None = None,
    ) -> None:
        query = """
            INSERT INTO persona_skill (
                persona_id, skill_id, nivel_aprendizado, como_obter_en, como_obter_pt
            )
            VALUES (?, ?, ?, ?, ?)
        """
        with Database() as db:
            db.executar(
                query,
                (persona_id, skill_id, nivel_aprendizado, como_obter_en, como_obter_pt),
            )

    @staticmethod
    def buscar_skills_da_persona(persona_id: int) -> list[sqlite3.Row]:
        query = """
            SELECT
                s.id,
                s.nome_en,
                s.nome_pt,
                s.descricao_en,
                s.descricao_pt,
                s.custo,
                s.elemento,
                ps.nivel_aprendizado,
                ps.como_obter_en,
                ps.como_obter_pt
            FROM skill s
            JOIN persona_skill ps ON s.id = ps.skill_id
            WHERE ps.persona_id = ?
            ORDER BY ps.nivel_aprendizado ASC
        """
        with Database() as db:
            return db.buscar_tudo(query, (persona_id,))

    @staticmethod
    def remover_vinculo(persona_id: int, skill_id: int) -> None:
        query = "DELETE FROM persona_skill WHERE persona_id = ? AND skill_id = ?"
        with Database() as db:
            db.executar(query, (persona_id, skill_id))