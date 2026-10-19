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



        