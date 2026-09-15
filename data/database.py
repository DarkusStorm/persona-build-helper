import os
import sqlite3
from typing import Optional, Type, Any, Self
from types import TracebackType
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("DATABASE", "data/persona.db")


def init_db(db_name: str = DB_PATH) -> None:
    os.makedirs(os.path.dirname(db_name), exist_ok=True)
    
    with sqlite3.connect(db_name) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS game (
            id TEXT PRIMARY KEY, -- 'p3r', 'p4g', 'p5r'
            titulo TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS party_member (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id TEXT NOT NULL,
            nome TEXT NOT NULL,
            tipo_equipamento TEXT NOT NULL,
            FOREIGN KEY (game_id) REFERENCES game(id)
        );

        CREATE TABLE IF NOT EXISTS persona (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            party_member_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            arcana TEXT,
            estagio INTEGER DEFAULT 1, -- 1=Inicial, 2=Segunda Transmutação, 3=Terceira
            FOREIGN KEY (party_member_id) REFERENCES party_member(id)
        );

        CREATE TABLE IF NOT EXISTS skill (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_en TEXT NOT NULL,
            nome_pt TEXT NOT NULL,
            descricao_en TEXT,
            descricao_pt TEXT,
            custo TEXT,
            elemento TEXT
        );

        CREATE TABLE IF NOT EXISTS persona_skill (
            persona_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            nivel_aprendizado INTEGER DEFAULT 1,
            como_obter_en TEXT,
            como_obter_pt TEXT,
            PRIMARY KEY (persona_id, skill_id),
            FOREIGN KEY (persona_id) REFERENCES persona(id) ON DELETE CASCADE,
            FOREIGN KEY (skill_id) REFERENCES skill(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS equipamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            party_member_id INTEGER NOT NULL,
            nome_en TEXT NOT NULL,
            nome_pt TEXT NOT NULL,
            atributos TEXT,
            como_obter_en TEXT,
            como_obter_pt TEXT,
            FOREIGN KEY (party_member_id) REFERENCES party_member(id)
        );
        """)
        conn.commit()


class Database:
    def __init__(self, db_name: str = DB_PATH) -> None:
        self.connection = sqlite3.connect(db_name)
        # Permite acessar colunas como dicionário no Python/Jinja (ex: row['nome_en'])
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON;")
        self.cursor = self.connection.cursor()

    def executar(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor

    def buscar_tudo(self, query: str, params: tuple = ()) -> list[sqlite3.Row]:
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def buscar_um(self, query: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        if exc_type is not None:
            print(f"Erro no contexto: {exc_type.__name__} - {exc_value}")
        self.close()