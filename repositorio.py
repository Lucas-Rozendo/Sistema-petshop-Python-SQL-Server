import pyodbc

def criar_tutor(cursor, nome, cpf, email, telefone):

    query = """
        INSERT INTO dbo.tutor (nome, cpf, email, telefone)
        OUTPUT INSERTED.id_tutor
        VALUES (?, ?, ?, ?)
    """

    try:
        cursor.execute(query, nome, cpf, email, telefone)
        return cursor.fetchone()[0]

    except pyodbc.IntegrityError as erro:

        if "uq_tutor_cpf" in str(erro):
            raise ValueError("CPF já cadastrado.") from erro

        elif "ck_tutor_cpf" in str(erro):
            raise ValueError("CPF deve conter 11 números.") from erro

        else:
            raise ValueError("Erro de integridade nos dados.") from erro

def buscar_tutor(cursor, id_tutor):
    query = """
            SELECT * FROM dbo.tutor
            WHERE id_tutor = ?"""

    cursor.execute(query,id_tutor)

    return cursor.fetchone()

def listar_tutores(cursor,filtro_nome=''):
    cursor.execute("SELECT * FROM dbo.tutor WHERE nome LIKE ?",
        f"%{filtro_nome}%")


    return cursor.fetchall()


def atualizar_tutor(cursor, id_tutor, **campos):

    campos_permitidos = {"nome", "email", "telefone"}

    if not campos:
        raise ValueError("Nenhum campo informado!")

    for campo in campos:
        if campo not in campos_permitidos:
            raise ValueError("Campo não permitido!")

    cursor.execute(
        "SELECT * FROM dbo.tutor WHERE id_tutor = ?",
        id_tutor
    )

    dados_antigos = cursor.fetchone()

    if dados_antigos is None:
        return None

    colunas = ", ".join(
        f"{campo} = ?" for campo in campos
    )

    query = f"""
        UPDATE dbo.tutor
        SET {colunas}
        WHERE id_tutor = ?
    """

    valores = list(campos.values())
    valores.append(id_tutor)

    cursor.execute(query, *valores)

    return dados_antigos

def excluir_tutor(cursor, id_tutor):
    try:
        cursor.execute(
            "DELETE FROM dbo.tutor WHERE id_tutor = ?",
            id_tutor
        )

        if cursor.rowcount == 0:
            raise ValueError("Tutor não encontrado!")

    except pyodbc.IntegrityError as erro:
        if "fk_pet_tutor" in str(erro):
            raise ValueError(
                "Não é possível excluir tutor com pets cadastrados!"
            ) from erro

        raise

def criar_pet(cursor, id_tutor, nome, especie, raca, data_nascimento, peso):

    query = """
        INSERT INTO dbo.pet (id_tutor, nome, especie, raca, data_nascimento, peso_kg)
        OUTPUT INSERTED.id_pet
        VALUES (?, ?, ?, ?, ?, ?)
    """

    try:
        cursor.execute(query, id_tutor, nome, especie, raca, data_nascimento, peso)
        return cursor.fetchone()[0]

    except pyodbc.IntegrityError as erro:

        if "fk_pet_tutor" in str(erro):
            raise ValueError("Não existe tutor com esse ID.") from erro

        elif "ck_pet_peso" in str(erro):
            raise ValueError("O peso do animal deve ser maior que 0.") from erro

        elif "ck_pet_especie" in str(erro):
            raise ValueError(
                "Espécie inválida! Use Cão, Gato, Ave, Roedor, Réptil ou Outro."
            ) from erro

        else:
            raise ValueError("Erro de integridade nos dados.") from erro



def atualizar_peso_pet(cursor, id_pet, peso_kg):

    cursor.execute(
        "SELECT * FROM dbo.pet WHERE id_pet = ?",
        id_pet
    )

    dados_antigos = cursor.fetchone()

    if dados_antigos is None:
        return None

    query = """
        UPDATE dbo.pet
        SET peso_kg = ?
        WHERE id_pet = ?
    """

    try:
        cursor.execute(query, peso_kg, id_pet)

    except pyodbc.IntegrityError as erro:
        if "ck_pet_peso" in str(erro):
            raise ValueError(
                "O peso do pet deve ser maior que zero!"
            ) from erro
        raise

    return dados_antigos


def transferir_pet(cursor, id_pet, id_tutor):
    try:
        cursor.execute(
            """
            UPDATE dbo.pet
            SET id_tutor = ?
            WHERE id_pet = ?
            """,
            id_tutor,
            id_pet
        )

        if cursor.rowcount == 0:
            raise ValueError("Pet não encontrado!")

        return "Transferência concluída com sucesso!"

    except pyodbc.IntegrityError as erro:

        if "fk_pet_tutor" in str(erro):
            raise ValueError(
                "Não existe tutor com esse ID."
            ) from erro

        else:
            raise ValueError(
                "Erro de integridade nos dados."
            ) from erro

def excluir_pet(cursor, id_pet):
    try:
        cursor.execute(
            "DELETE FROM dbo.pet WHERE id_pet = ?",
            id_pet
        )

        if cursor.rowcount == 0:
            raise ValueError("Pet não encontrado!")

    except pyodbc.IntegrityError as erro:
        if "fk_consulta_pet" in str(erro):
            raise ValueError(
                "Não é possível excluir um pet que possui consultas cadastradas!"
            ) from erro

        raise



def listar_pets_do_tutor(cursor, id_tutor):
    cursor.execute("SELECT id_tutor FROM dbo.tutor WHERE id_tutor = ?", id_tutor)
    if cursor.fetchone() is None:
        raise ValueError("Tutor não encontrado!")

    cursor.execute("SELECT * FROM dbo.pet WHERE id_tutor = ?", id_tutor)
    return cursor.fetchall()

def buscar_pet_com_tutor(cursor, id_pet):
    query = """
        SELECT p.*, t.nome AS nome_tutor, t.cpf AS cpf_tutor,
               t.email AS email_tutor, t.telefone AS telefone_tutor
        FROM dbo.pet p
        JOIN dbo.tutor t ON p.id_tutor = t.id_tutor
        WHERE p.id_pet = ?
    """
    cursor.execute(query, id_pet)
    return cursor.fetchone()

def agendar_consulta(cursor, id_pet, id_vet, data_hora, motivo, observacoes, procedimentos):

    if not procedimentos:
        raise ValueError("Selecione pelo menos um procedimento.")

    query = """
        INSERT INTO dbo.consulta
        (id_pet, id_veterinario, data_hora, motivo, observacoes)
        OUTPUT INSERTED.id_consulta
        VALUES (?, ?, ?, ?, ?)
    """

    try:
        cursor.execute(
            query,
            id_pet,
            id_vet,
            data_hora,
            motivo,
            observacoes
        )

        id_consulta = cursor.fetchone()[0]

        for id_procedimento, quantidade in procedimentos:

            if quantidade <= 0:
                raise ValueError(
                    "A quantidade deve ser maior que zero."
                )

            cursor.execute(
                """
                SELECT preco_base
                FROM dbo.procedimento
                WHERE id_procedimento = ?
                """,
                id_procedimento
            )

            resultado = cursor.fetchone()

            if resultado is None:
                raise ValueError(
                    f"Procedimento {id_procedimento} não encontrado."
                )

            preco_base = resultado.preco_base

            cursor.execute(
                """
                INSERT INTO dbo.consulta_procedimento
                (id_consulta, id_procedimento, quantidade, valor_cobrado)
                VALUES (?, ?, ?, ?)
                """,
                id_consulta,
                id_procedimento,
                quantidade,
                preco_base
            )

        return id_consulta

    except pyodbc.IntegrityError as erro:

        if "fk_consulta_pet" in str(erro):
            raise ValueError(
                "Não existe pet com esse ID."
            ) from erro

        elif "fk_consulta_vet" in str(erro):
            raise ValueError(
                "Não existe veterinário com esse ID."
            ) from erro

        elif "pk_consulta_procedimento" in str(erro):
            raise ValueError(
                "Existe um procedimento repetido na consulta."
            ) from erro

        elif "ck_cp_qtd" in str(erro):
            raise ValueError(
                "A quantidade do procedimento deve ser maior que zero."
            ) from erro

        else:
            raise ValueError(
                "Erro de integridade ao agendar consulta."
            ) from erro

def adicionar_procedimento(cursor, id_consulta, id_procedimento, quantidade):
    if quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero!")

    cursor.execute("SELECT status FROM dbo.consulta WHERE id_consulta = ?", id_consulta)
    consulta = cursor.fetchone()
    if consulta is None:
        raise ValueError("Consulta não encontrada!")
    if consulta.status == "CANCELADA":
        raise ValueError("Não é possível adicionar procedimento a consulta cancelada!")

    cursor.execute("SELECT preco_base FROM dbo.procedimento WHERE id_procedimento = ?", id_procedimento)
    resultado = cursor.fetchone()
    if resultado is None:
        raise ValueError("Procedimento não encontrado!")

    try:
        cursor.execute("""
            INSERT INTO dbo.consulta_procedimento
            (id_consulta, id_procedimento, quantidade, valor_cobrado)
            VALUES (?, ?, ?, ?)
        """, id_consulta, id_procedimento, quantidade, resultado.preco_base)
    except pyodbc.IntegrityError as erro:
        if "pk_consulta_procedimento" in str(erro):
            raise ValueError("Procedimento já adicionado à consulta!") from erro
        raise

def remover_procedimento(cursor, id_consulta, id_procedimento):
    cursor.execute("SELECT status FROM dbo.consulta WHERE id_consulta = ?", id_consulta)
    consulta = cursor.fetchone()
    if consulta is None:
        raise ValueError("Consulta não encontrada!")
    if consulta.status == "CANCELADA":
        raise ValueError("Não é possível remover procedimento de consulta cancelada!")

    cursor.execute("""
        DELETE FROM dbo.consulta_procedimento
        WHERE id_consulta = ? AND id_procedimento = ?
    """, id_consulta, id_procedimento)
    if cursor.rowcount == 0:
        raise ValueError("Procedimento não encontrado nessa consulta!")

def listar_procedimentos_da_consulta(cursor, id_consulta):
    cursor.execute("""
        SELECT p.id_procedimento, p.descricao, p.preco_base,
               cp.quantidade, cp.valor_cobrado
        FROM dbo.procedimento p
        INNER JOIN dbo.consulta_procedimento cp
            ON p.id_procedimento = cp.id_procedimento
        WHERE cp.id_consulta = ?
    """, id_consulta)
    return cursor.fetchall()

def listar_consultas_por_procedimento(cursor, id_procedimento):
    try:
        cursor.execute(
            """SELECT c.* FROM dbo.consulta c 
            INNER JOIN dbo.consulta_procedimento cp ON c.id_consulta = cp.id_consulta 
            WHERE cp.id_procedimento = ?""",
            id_procedimento
        )
        return cursor.fetchall()

    except pyodbc.IntegrityError as erro:
        raise ValueError(
            "Erro de integridade ao listar consultas por procedimento."
        ) from erro

def total_da_consulta(cursor, id_consulta):
    cursor.execute("SELECT id_consulta FROM dbo.consulta WHERE id_consulta = ?", id_consulta)
    if cursor.fetchone() is None:
        raise ValueError("Consulta não encontrada!")

    cursor.execute("""
        SELECT SUM(quantidade * valor_cobrado) AS total
        FROM dbo.consulta_procedimento
        WHERE id_consulta = ?
    """, id_consulta)
    resultado = cursor.fetchone()
    return resultado.total if resultado.total is not None else 0.0

def atualizar_status_consulta(cursor, id_consulta, status):
    status = status.strip().upper()
    if status not in ("AGENDADA", "REALIZADA", "CANCELADA"):
        raise ValueError("Status inválido! Use AGENDADA, REALIZADA ou CANCELADA.")

    cursor.execute("UPDATE dbo.consulta SET status = ? WHERE id_consulta = ?", status, id_consulta)
    if cursor.rowcount == 0:
        raise ValueError("Consulta não encontrada!")

def excluir_consulta(cursor, id_consulta):
    cursor.execute("DELETE FROM dbo.consulta WHERE id_consulta = ?", id_consulta)
    if cursor.rowcount == 0:
        raise ValueError("Consulta não encontrada!")

def historico_do_pet(cursor, id_pet):
    cursor.execute("SELECT id_pet FROM dbo.pet WHERE id_pet = ?", id_pet)
    if cursor.fetchone() is None:
        raise ValueError("Pet não encontrado!")

    cursor.execute("""
        SELECT v.* FROM dbo.vw_resumo_consulta v
        INNER JOIN dbo.consulta c ON v.id_consulta = c.id_consulta
        WHERE c.id_pet = ?
        ORDER BY v.data_hora
    """, id_pet)
    return cursor.fetchall()

