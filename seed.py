import os
from data.database import DB_PATH, init_db
from models import (
    Game,
    PartyMember,
    Persona,
    Skill,
    PersonaSkill,
    Equipamento,
)


def resetar_banco() -> None:
    """Remove o banco anterior (se existir) e recria as tabelas limpas."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db(DB_PATH)


def obter_ou_criar_skill(dados_skill: dict) -> int:
    """Evita duplicar skills compartilhadas entre vários personagens."""
    existente = Skill.buscar_por_nome(dados_skill["nome_en"])
    if existente:
        return existente["id"]

    skill_id = Skill.criar(
        nome_en=dados_skill["nome_en"],
        nome_pt=dados_skill["nome_pt"],
        descricao_en=dados_skill.get("descricao_en"),
        descricao_pt=dados_skill.get("descricao_pt"),
        custo=dados_skill.get("custo"),
        elemento=dados_skill.get("elemento"),
    )
    assert skill_id is not None
    return skill_id


def popular_jogo(game_id: str, titulo: str, elenco: list[dict]) -> None:
    """Insere um jogo e toda a cadeia de membros, personas, skills e equipamentos."""
    Game.criar(game_id, titulo)

    for membro in elenco:
        member_id = PartyMember.criar(
            game_id=game_id,
            nome=membro["nome"],
            tipo_equipamento=membro["tipo_equipamento"],
        )
        assert member_id is not None

        # Cadastra as Personas e suas respectivas Skills
        for persona_data in membro.get("personas", []):
            persona_id = Persona.criar(
                party_member_id=member_id,
                nome=persona_data["nome"],
                arcana=persona_data["arcana"],
                estagio=persona_data.get("estagio", 1),
            )
            assert persona_id is not None

            for skill_entry in persona_data.get("skills", []):
                skill_id = obter_ou_criar_skill(skill_entry["skill"])
                PersonaSkill.vincular(
                    persona_id=persona_id,
                    skill_id=skill_id,
                    nivel_aprendizado=skill_entry.get("nivel", 1),
                    como_obter_en=skill_entry.get("como_obter_en"),
                    como_obter_pt=skill_entry.get("como_obter_pt"),
                )

        # Cadastra os Equipamentos recomendados
        for equip in membro.get("equipamentos", []):
            Equipamento.criar(
                party_member_id=member_id,
                nome_en=equip["nome_en"],
                nome_pt=equip["nome_pt"],
                atributos=equip.get("atributos"),
                como_obter_en=equip.get("como_obter_en"),
                como_obter_pt=equip.get("como_obter_pt"),
            )


# A preencher com personagens e equipamentos.

DADOS_P3R = [
    {
        "nome": "Makoto Yuki",
        "tipo_equipamento": "Sword",
        "personas": [],
        "equipamentos": [
            {
                "nome_en": "Lucifer's Blade",
                "nome_pt": "Lâmina de Lúcifer",
                "atributos_en": "ATK 425 / HIT 95 / Magic Ability + All Stats +7 (Magic Builds)",
                "atributos_pt": "ATK 425 / HIT 95 / Habilidade Mágica + Todos os atributos +7 (Builds Físicas)",
                "como_obter_en": "Mayoido Antiques",
                "como_obter_pt": "Antiquário Mayoido",
            },
            {
                "nome_en": "Deus Xiphos",
                "nome_pt": "Deus Xiphos",
                "atributos_en": "ATK 360 / HIT 99 / Ignore Resistances + Strength +7 (Physical Builds)",
                "atributos_pt": "ATK 360 / HIT 99 / Ignora Resistências + Força +7 (Builds Físicas)",
                "como_obter_en": "Mayoido Antiques",
                "como_obter_pt": "Antiquário Mayoido",
            }
        ],
    },
    {
        "nome": "Yukari Takeba",
        "tipo_equipamento": "Bow",
        "personas": [
            {
                "nome": "Io",
                "arcana": "Lovers",
                "estagio": 1,
                "skills": [
                    {
                        "nivel": 38,
                        "como_obter_en": "Learned at Level 38",
                        "como_obter_pt": "Aprendida no Nível 38",
                        "skill": {
                            "nome_en": "Garudyne",
                            "nome_pt": "Garudyne",
                            "descricao_en": "Deals heavy Wind damage to 1 foe.",
                            "descricao_pt": "Causa dano pesado de Vento a 1 inimigo.",
                            "custo": "12 SP",
                            "elemento": "Wind",
                        },
                    },
                ],
            },
            {
                "nome": "Isis",
                "arcana": "Lovers",
                "estagio": 2,
                "skills": [
                    {
                        "nivel": 68,
                        "como_obter_en": "Learned at Level 68 (Second Awakening)",
                        "como_obter_pt": "Aprendida no Nível 68 (Segundo Despertar)",
                        "skill": {
                            "nome_en": "Mediarahan",
                            "nome_pt": "Mediarahan",
                            "descricao_en": "Fully restores party's HP.",
                            "descricao_pt": "Restaura totalmente o HP do grupo.",
                            "custo": "32 SP",
                            "elemento": "Healing",
                        },
                    },
                ],
            },
        ],
        "equipamentos": [
            {
                "nome_en": "Quintessence Bow",
                "nome_pt": "Arco da Quintessência",
                "atributos": "ATK 410 / ACC 98 / Magic +5",
                "como_obter_en": "Antique Shop (Fusion: Chi You)",
                "como_obter_pt": "Antiquário (Fusão: Chi You)",
            }
        ],
    },
]

DADOS_P4G = [
    {
        "nome": "Chie Satonaka",
        "tipo_equipamento": "Greaves",
        "personas": [
            {
                "nome": "Tomoe",
                "arcana": "Chariot",
                "estagio": 1,
                "skills": [],
            },
            {
                "nome": "Suzuka Gongen",
                "arcana": "Chariot",
                "estagio": 2,
                "skills": [],
            },
            {
                "nome": "Haraedo-no-Okami",
                "arcana": "Chariot",
                "estagio": 3,
                "skills": [
                    {
                        "nivel": 75,
                        "como_obter_en": "Third Awakening (Winter Event)",
                        "como_obter_pt": "Terceiro Despertar (Evento de Inverno)",
                        "skill": {
                            "nome_en": "Dragon Hustle",
                            "nome_pt": "Agito do Dragão",
                            "descricao_en": "Increases party's Attack, Defense and Agility for 3 turns.",
                            "descricao_pt": "Aumenta Ataque, Defesa e Agilidade do grupo por 3 turnos.",
                            "custo": "150 SP",
                            "elemento": "Support",
                        },
                    },
                ],
            },
        ],
        "equipamentos": [
            {
                "nome_en": "Moses Sandals",
                "nome_pt": "Sandálias de Moisés",
                "atributos": "ATK 402 / HIT 95 / Critical Rate Up (High)",
                "como_obter_en": "Defeat The Reaper",
                "como_obter_pt": "Derrote O Ceifador (The Reaper)",
            }
        ],
    },
]

DADOS_P5R = [
    {
        "nome": "Ryuji Sakamoto",
        "tipo_equipamento": "Bludgeon / Shotgun",
        "personas": [
            {
                "nome": "Captain Kidd",
                "arcana": "Chariot",
                "estagio": 1,
                "skills": [],
            },
            {
                "nome": "Seiten Taisei",
                "arcana": "Chariot",
                "estagio": 2,
                "skills": [],
            },
            {
                "nome": "William",
                "arcana": "Chariot",
                "estagio": 3,
                "skills": [
                    {
                        "nivel": 75,
                        "como_obter_en": "Third Awakening (Third Semester)",
                        "como_obter_pt": "Terceiro Despertar (Terceiro Semestre)",
                        "skill": {
                            "nome_en": "Fighting Spirit",
                            "nome_pt": "Espírito de Luta",
                            "descricao_en": "Next Physical attack deals more than double damage for all allies.",
                            "descricao_pt": "Próximo ataque físico causa mais que o dobro de dano para todos os aliados.",
                            "custo": "80 SP",
                            "elemento": "Support",
                        },
                    },
                ],
            },
        ],
        "equipamentos": [
            {
                "nome_en": "Imprisoned Mjolnir",
                "nome_pt": "Mjolnir Aprisionado",
                "atributos": "ATK 324 / ACC 90 / Elec Damage +25%",
                "como_obter_en": "Electric Chair: Thor (Fusion Alarm)",
                "como_obter_pt": "Cadeira Elétrica: Thor (Alarme de Fusão)",
            }
        ],
    },
]


def executar_seed() -> None:
    print("Recriando banco de dados...")
    resetar_banco()

    print("Populando Persona 3 Reload...")
    popular_jogo("p3r", "Persona 3 Reload", DADOS_P3R)

    print("Populando Persona 4 Golden...")
    popular_jogo("p4g", "Persona 4 Golden", DADOS_P4G)

    print("Populando Persona 5 Royal...")
    popular_jogo("p5r", "Persona 5 Royal", DADOS_P5R)

    print("Seed concluído com sucesso!")


if __name__ == "__main__":
    executar_seed()