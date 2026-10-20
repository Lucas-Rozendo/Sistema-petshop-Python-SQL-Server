
import pyodbc
from contextlib import contextmanager


def montar_connection_string(usuario, senha):
    conn_str = (
        r"Driver={SQL Server};"
        r"Server=(local);"
        r"Database=PetVida;"
        f"UID={usuario};"
        f"PWD={senha};"
    )

    return conn_str


def conectar(conn_str):
    return pyodbc.connect(conn_str, autocommit=False)


@contextmanager
def transacao(conn_str):
    conn = conectar(conn_str)
    cursor = None

    try:
        cursor = conn.cursor()

        yield cursor

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


def testar_conexao(conn_str):
    conn = conectar(conn_str)

    try:
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT
                    @@SERVERNAME AS servidor,
                    DB_NAME() AS banco,
                    SERVERPROPERTY('ProductVersion') AS versao
            """)

            resultado = cursor.fetchone()

            return (
                resultado.servidor,
                resultado.banco,
                resultado.versao
            )

        finally:
            cursor.close()

    finally:
        conn.close()
