import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(__file__), "vagas.db")


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS vagas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                empresa TEXT NOT NULL,
                plataforma TEXT NOT NULL,
                link TEXT NOT NULL UNIQUE,
                palavra_chave TEXT,
                data_coleta TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS candidaturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                empresa TEXT NOT NULL,
                plataforma TEXT NOT NULL,
                link TEXT NOT NULL UNIQUE,
                data_candidatura TEXT NOT NULL
            )
        """)


def salvar_vagas_batch(vagas_list):
    with get_conn() as conn:
        for vaga in vagas_list:
            try:
                conn.execute(
                    """INSERT OR IGNORE INTO vagas
                       (titulo, empresa, plataforma, link, palavra_chave, data_coleta)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (vaga["titulo"], vaga["empresa"], vaga["plataforma"],
                     vaga["link"], vaga.get("palavra_chave", ""),
                     datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
            except sqlite3.IntegrityError:
                pass


def ja_candidatou(link):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT 1 FROM candidaturas WHERE link = ?", (link,)
        ).fetchone()
        return row is not None


def salvar_candidatura(titulo, empresa, plataforma, link):
    with get_conn() as conn:
        try:
            conn.execute(
                """INSERT OR IGNORE INTO candidaturas
                   (titulo, empresa, plataforma, link, data_candidatura)
                   VALUES (?, ?, ?, ?, ?)""",
                (titulo, empresa, plataforma, link,
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
        except sqlite3.IntegrityError:
            pass


def listar_vagas_novas():
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT v.* FROM vagas v
            LEFT JOIN candidaturas c ON v.link = c.link
            WHERE c.id IS NULL
            ORDER BY v.data_coleta DESC
        """).fetchall()
        return [dict(r) for r in rows]


def listar_candidaturas():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM candidaturas ORDER BY data_candidatura DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def contar_vagas():
    with get_conn() as conn:
        return conn.execute("SELECT COUNT(*) FROM vagas").fetchone()[0]


def contar_candidaturas():
    with get_conn() as conn:
        return conn.execute("SELECT COUNT(*) FROM candidaturas").fetchone()[0]