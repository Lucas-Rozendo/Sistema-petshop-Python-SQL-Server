
import pyodbc
from getpass import getpass
from db import montar_connection_string, conectar, transacao
from repositorio import *
from datetime import datetime


usuario = input("Usuário: ")
senha = getpass("Senha: ")

conn_str = montar_connection_string(usuario, senha)


try:
    conn = conectar(conn_str)
    conn.close()
    print("Conectado com sucesso!")

except Exception as erro:
    print("Erro ao conectar:", erro)
    exit()


# MENU PRINCIPAL
while True:
    print("\n========== PETVIDA ==========")
    print("1 - Gerenciar tutores")
    print("2 - Gerenciar pets")
    print("3 - Gerenciar consultas e procedimentos")
    print("4 - Histórico do pet")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")

    # ==========================================
    # 1 - GERENCIAR TUTORES
    # ==========================================
    if opcao == "1":

        while True:
            print("\n===== GERENCIAR TUTORES =====")
            print("1 - Cadastrar tutor")
            print("2 - Consultar tutor")
            print("3 - Atualizar tutor")
            print("4 - Excluir tutor")
            print("0 - Voltar")

            opcao_tutor = input("Escolha uma opção: ")

            if opcao_tutor == "1":
                nome = input("Nome: ")
                cpf = input("CPF: ")
                email = input("Email: ")
                telefone = input("Telefone: ")

                try:
                    with transacao(conn_str) as cursor:
                        id_gerado = criar_tutor(
                            cursor, nome, cpf, email, telefone
                        )

                    print("Tutor cadastrado com ID:", id_gerado)

                except Exception as erro:
                    print("Erro ao cadastrar tutor:", erro)

            elif opcao_tutor == "2":

                while True:
                    print("\n===== CONSULTAR TUTOR =====")
                    print("1 - Buscar por ID")
                    print("2 - Filtrar por nome")
                    print("3 - Listar todos")
                    print("0 - Voltar")

                    opcao_consulta = input("Escolha uma opção: ")

                    if opcao_consulta == "1":
                        id_tutor = int(input("Digite o ID do tutor: "))

                        with transacao(conn_str) as cursor:
                            tutor = buscar_tutor(cursor, id_tutor)

                        if tutor:
                            print("ID:", tutor.id_tutor)
                            print("Nome:", tutor.nome)
                            print("CPF:", tutor.cpf)
                            print("Email:", tutor.email)
                            print("Telefone:", tutor.telefone)
                        else:
                            print("Tutor não encontrado!")

                    elif opcao_consulta == "2":
                        nome_tutor = input("Nome: ")

                        with transacao(conn_str) as cursor:
                            tutores = listar_tutores(cursor, nome_tutor)

                        if tutores:
                            for tutor in tutores:
                                print("ID:", tutor.id_tutor)
                                print("Nome:", tutor.nome)
                                print("CPF:", tutor.cpf)
                                print("Email:", tutor.email)
                                print("Telefone:", tutor.telefone)
                                print("----------------------")
                        else:
                            print("Nenhum tutor encontrado!")

                    elif opcao_consulta == "3":
                        with transacao(conn_str) as cursor:
                            tutores = listar_tutores(cursor)

                        for tutor in tutores:
                            print("ID:", tutor.id_tutor)
                            print("Nome:", tutor.nome)
                            print("CPF:", tutor.cpf)
                            print("Email:", tutor.email)
                            print("Telefone:", tutor.telefone)
                            print("----------------------")

                    elif opcao_consulta == "0":
                        break

                    else:
                        print("Opção inválida!")

            elif opcao_tutor == "3":
                id_tutor = int(input("ID do tutor: "))

                campos = {}

                nome = input("Novo nome (Enter para manter): ")
                email = input("Novo email (Enter para manter): ")
                telefone = input("Novo telefone (Enter para manter): ")

                if nome:
                    campos["nome"] = nome

                if email:
                    campos["email"] = email

                if telefone:
                    campos["telefone"] = telefone

                with transacao(conn_str) as cursor:
                    dados_antigos = atualizar_tutor(
                        cursor, id_tutor, **campos
                    )

                if dados_antigos:
                    with transacao(conn_str) as cursor:
                        dados_novos = buscar_tutor(cursor, id_tutor)

                    print("\n===== DADOS ANTIGOS =====")
                    print("Nome:", dados_antigos.nome)
                    print("Email:", dados_antigos.email)
                    print("Telefone:", dados_antigos.telefone)

                    print("\n===== DADOS NOVOS =====")
                    print("Nome:", dados_novos.nome)
                    print("Email:", dados_novos.email)
                    print("Telefone:", dados_novos.telefone)

                else:
                    print("Tutor não encontrado!")

            elif opcao_tutor == "4":
                try:
                    id_tutor = int(input("ID do tutor: "))

                    with transacao(conn_str) as cursor:
                        excluir_tutor(cursor, id_tutor)

                    print("Tutor excluído com sucesso!")

                except ValueError as erro:
                    print("Erro:", erro)

            elif opcao_tutor == "0":
                break

            else:
                print("Opção inválida!")

    # ==========================================
    # 2 - GERENCIAR PETS
    # ==========================================
    elif opcao == "2":

        while True:
            print("\n===== GERENCIAR PETS =====")
            print("1 - Cadastrar pet")
            print("2 - Atualizar peso do pet")
            print("3 - Transferir pet para outro tutor")
            print("4 - Excluir pet")
            print("5 - Listar pets de um tutor")
            print("6 - Buscar pet com informações do tutor")
            print("0 - Voltar")

            opcao_pet = input("Escolha uma opção: ")


            if opcao_pet == "1":

                with transacao(conn_str) as cursor:
                    tutores = listar_tutores(cursor)

                for tutor in tutores:
                    print("ID:", tutor.id_tutor)
                    print("Nome:", tutor.nome)
                    print("----------------------")

                try:
                    id_tutor = int(input("Digite o ID do Tutor: "))
                    nome = input("Nome do pet: ")
                    especie = input("Espécie: ")
                    raca = input("Raça: ")
                    peso_kg = input("Peso: ")
                    data = input("Data de nascimento (DD/MM/AAAA): ")
        
                    if peso_kg == "":
                        peso_kg = None
                    else:
                        peso_kg = float(peso_kg)

                    if raca == "":
                        raca = None

                    if data == "":
                        data_formatada = None
                    else:
                        data_formatada = datetime.strptime(
                            data, "%d/%m/%Y"
                        ).date()

                    with transacao(conn_str) as cursor:
                        id_gerado = criar_pet(
                            cursor,
                            id_tutor,
                            nome,
                            especie,
                            raca,
                            data_formatada,
                            peso_kg
                        )

                    print("Pet cadastrado com ID:", id_gerado)

                except ValueError as erro:
                    print("Erro nos dados informados:", erro)

                except Exception as erro:
                    print("Erro ao cadastrar pet:", erro)

            elif opcao_pet == "2":
                try:
                    id_pet = int(input("ID do pet: "))
                    peso_kg = float(input("Novo peso (kg): "))

                    with transacao(conn_str) as cursor:
                        dados_antigos = atualizar_peso_pet(
                            cursor, id_pet, peso_kg
                        )

                    if dados_antigos:
                        with transacao(conn_str) as cursor:
                            cursor.execute(
                                "SELECT * FROM dbo.pet WHERE id_pet = ?",
                                id_pet
                            )
                            dados_novos = cursor.fetchone()

                        print("\n===== ATUALIZAÇÃO DE PESO =====")
                        print("Pet:", dados_antigos.nome)
                        print("Peso antigo:", dados_antigos.peso_kg, "kg")
                        print("Peso novo:", dados_novos.peso_kg, "kg")

                    else:
                        print("Pet não encontrado!")

                except ValueError as erro:
                    print("Erro:", erro)

                except pyodbc.Error as erro:
                    print("Erro no banco de dados:", erro)


            elif opcao_pet == "3":
                try:
                    id_pet = int(input("ID do pet: "))
                    id_tutor = int(input("ID do novo tutor: "))

                    with transacao(conn_str) as cursor:
                        mensagem = transferir_pet(
                            cursor, id_pet, id_tutor
                        )

                    print(mensagem)

                except ValueError as erro:
                    print("Erro:", erro)

                except pyodbc.Error as erro:
                    print("Erro no banco de dados:", erro)

            elif opcao_pet == "4":
                try:
                    id_pet = int(input("ID do pet: "))

                    with transacao(conn_str) as cursor:
                        excluir_pet(cursor, id_pet)

                    print("Pet excluído com sucesso!")

                except ValueError as erro:
                    print("Erro:", erro)

            elif opcao_pet == "5":
                try:
                    id_tutor = int(input("ID do tutor: "))

                    with transacao(conn_str) as cursor:
                        pets = listar_pets_do_tutor(cursor, id_tutor)

                    if pets:
                        for pet in pets:
                            print("ID:", pet.id_pet)
                            print("Nome:", pet.nome)
                            print("Espécie:", pet.especie)
                            print("Raça:", pet.raca)
                            print("Data de nascimento:", pet.data_nascimento)
                            print("Peso (kg):", pet.peso_kg)
                            print("----------------------")
                    else:
                        print("Nenhum pet encontrado para esse tutor.")

                except ValueError as erro:
                    print("Erro:", erro)

            elif opcao_pet == "6":
                try:
                    id_pet = int(input("ID do pet: "))

                    with transacao(conn_str) as cursor:
                        pet_info = buscar_pet_com_tutor(cursor, id_pet)

                    if pet_info:
                        print("ID do Pet:", pet_info.id_pet)
                        print("Nome do Pet:", pet_info.nome)
                        print("Espécie:", pet_info.especie)
                        print("Raça:", pet_info.raca)
                        print("Data de nascimento:", pet_info.data_nascimento)
                        print("Peso (kg):", pet_info.peso_kg)
                        print("ID do Tutor:", pet_info.id_tutor)
                        print("Nome do Tutor:", pet_info.nome_tutor)
                    else:
                        print("Pet não encontrado.")

                except ValueError as erro:
                    print("Erro:", erro)

            elif opcao_pet == "0":
                break

            else:
                print("Opção inválida!")

    # ==========================================
    # 3 - CONSULTAS E PROCEDIMENTOS
    # ==========================================
    elif opcao == "3":

        while True:
            print("\n===== CONSULTAS E PROCEDIMENTOS =====")
            print("1 - Agendar consulta")
            print("2 - Adicionar procedimento")
            print("3 - Remover procedimento")
            print("4 - Listar procedimentos da consulta")
            print("5 - Listar consultas por procedimento")
            print("6 - Consultar total da consulta")
            print("7 - Atualizar status da consulta")
            print("8 - Excluir consulta")
            print("0 - Voltar")

            opcao_consultas = input("Escolha uma opção: ")

            
            if opcao_consultas == "1":
                try:
                    print("\n===== AGENDAR CONSULTA =====")

                  
                    with transacao(conn_str) as cursor:
                        cursor.execute("""
                            SELECT id_pet, nome, especie
                            FROM dbo.pet
                            ORDER BY id_pet
                        """)
                        pets = cursor.fetchall()

                    print("\n===== PETS CADASTRADOS =====")

                    for pet in pets:
                        print("ID:", pet.id_pet)
                        print("Nome:", pet.nome)
                        print("Espécie:", pet.especie)
                        print("----------------------")

                    if not pets:
                        raise ValueError("Nenhum pet cadastrado!")

                    id_pet = int(input("Digite o ID do pet: "))

                    
                    with transacao(conn_str) as cursor:
                        cursor.execute("""
                            SELECT id_veterinario, nome, especialidade
                            FROM dbo.veterinario
                            WHERE ativo = 1
                            ORDER BY id_veterinario
                        """)
                        veterinarios = cursor.fetchall()

                    print("\n===== VETERINÁRIOS DISPONÍVEIS =====")

                    for vet in veterinarios:
                        print("ID:", vet.id_veterinario)
                        print("Nome:", vet.nome)
                        print("Especialidade:", vet.especialidade)
                        print("----------------------")

                    if not veterinarios:
                        raise ValueError("Nenhum veterinário ativo disponível!")

                    id_vet = int(input("Digite o ID do veterinário: "))

                    # Informações da consulta
                    data_hora = input(
                        "Data e hora da consulta (DD/MM/AAAA HH:MM): "
                    )

                    data_hora_formatada = datetime.strptime(
                        data_hora, "%d/%m/%Y %H:%M"
                    )

                    motivo = input("Motivo da consulta: ")
                    observacoes = input("Observações: ")

                    if observacoes == "":
                        observacoes = None

                    with transacao(conn_str) as cursor:
                        cursor.execute("""
                            SELECT id_procedimento, descricao, preco_base
                            FROM dbo.procedimento
                            ORDER BY id_procedimento
                        """)
                        procedimentos_existentes = cursor.fetchall()

                    print("\n===== PROCEDIMENTOS DISPONÍVEIS =====")

                    for proc in procedimentos_existentes:
                        print(
                            f"{proc.id_procedimento} - "
                            f"{proc.descricao} - "
                            f"R$ {proc.preco_base:.2f}"
                        )

                    # Selecionar procedimentos
                    procedimentos_selecionados = []

                    ids_validos = {
                        proc.id_procedimento
                        for proc in procedimentos_existentes
                    }

                    while True:
                        id_procedimento = int(input(
                            "\nID do procedimento (0 para finalizar): "
                        ))

                        if id_procedimento == 0:
                            break

                        if id_procedimento not in ids_validos:
                            print("Procedimento não encontrado!")
                            continue

                        if any(
                            p[0] == id_procedimento
                            for p in procedimentos_selecionados
                        ):
                            print("Procedimento já selecionado!")
                            continue

                        quantidade = int(input("Quantidade: "))

                        if quantidade <= 0:
                            print("A quantidade deve ser maior que zero!")
                            continue

                        procedimentos_selecionados.append(
                            (id_procedimento, quantidade)
                        )

                    print("\n===== PROCEDIMENTOS SELECIONADOS =====")

                    for id_proc, quantidade in procedimentos_selecionados:
                        print(f"ID: {id_proc} | Quantidade: {quantidade}")

                    
                    with transacao(conn_str) as cursor:
                        id_consulta = agendar_consulta(
                            cursor,
                            id_pet,
                            id_vet,
                            data_hora_formatada,
                            motivo,
                            observacoes,
                            procedimentos_selecionados
                        )

                    print("\nConsulta agendada com sucesso!")
                    print("ID da consulta:", id_consulta)

                except ValueError as erro:
                    print("Erro nos dados informados:", erro)

                except pyodbc.Error as erro:
                    print("Erro no banco de dados:", erro)

                            

            elif opcao_consultas == "2":
                try:
                    id_consulta = int(input("ID da consulta: "))
                    with transacao(conn_str) as cursor:
                        cursor.execute("""
                            SELECT id_procedimento, descricao, preco_base
                            FROM dbo.procedimento ORDER BY id_procedimento
                        """)
                        procedimentos = cursor.fetchall()

                    print("\n===== PROCEDIMENTOS DISPONÍVEIS =====")
                    for proc in procedimentos:
                        print(f"{proc.id_procedimento} - {proc.descricao} - R$ {proc.preco_base:.2f}")

                    id_procedimento = int(input("ID do procedimento: "))
                    quantidade = int(input("Quantidade: "))

                    with transacao(conn_str) as cursor:
                        adicionar_procedimento(cursor, id_consulta, id_procedimento, quantidade)

                    print("Procedimento adicionado à consulta com sucesso!")
                except ValueError as erro:
                    print("Erro:", erro)
                except pyodbc.Error as erro:
                    print("Erro no banco de dados:", erro)

            elif opcao_consultas == "3":
                try:
                    id_consulta = int(input("ID da consulta: "))
                    id_procedimento = int(input("ID do procedimento: "))

                    with transacao(conn_str) as cursor:
                        remover_procedimento(
                            cursor, id_consulta, id_procedimento
                        )

                    print("Procedimento removido da consulta com sucesso!")

                except ValueError as erro:
                    print("Erro nos dados informados:", erro)

                except pyodbc.Error as erro:
                    print("Erro no banco de dados:", erro)

            elif opcao_consultas == "4":
                try:
                    id_consulta = int(input("ID da consulta: "))

                    with transacao(conn_str) as cursor:
                        procedimentos = listar_procedimentos_da_consulta(
                            cursor, id_consulta
                        )

                    if procedimentos:
                        print("\n===== PROCEDIMENTOS DA CONSULTA =====")
                        for proc in procedimentos:
                            print("ID:", proc.id_procedimento)
                            print("Descrição:", proc.descricao)
                            print("Preço base:", proc.preco_base)
                            print("Quantidade:", proc.quantidade)
                            print("----------------------")
                    else:
                        print("Nenhum procedimento encontrado para essa consulta.")

                except ValueError as erro:
                    print("Erro nos dados informados:", erro)

            elif opcao_consultas == "5":
                try:
                    id_procedimento = int(input("ID do procedimento: "))

                    with transacao(conn_str) as cursor:
                        consultas = listar_consultas_por_procedimento(
                            cursor, id_procedimento
                        )

                    if consultas:
                        print("\n===== CONSULTAS COM O PROCEDIMENTO =====")
                        for consulta in consultas:
                            print("ID da Consulta:", consulta.id_consulta)
                            print("ID do Pet:", consulta.id_pet)
                            print("ID do Veterinário:", consulta.id_veterinario)
                            print("Data e Hora:", consulta.data_hora)
                            print("Motivo:", consulta.motivo)
                            print("Observações:", consulta.observacoes)
                            print("----------------------")
                    else:
                        print("Nenhuma consulta encontrada para esse procedimento.")

                except ValueError as erro:
                    print("Erro nos dados informados:", erro)

            elif opcao_consultas == "6":
                try:
                    id_consulta = int(input("ID da consulta: "))

                    with transacao(conn_str) as cursor:
                        total = total_da_consulta(cursor, id_consulta)

                    print(f"Total da consulta (ID {id_consulta}): R$ {total:.2f}")

                except ValueError as erro:
                    print("Erro nos dados informados:", erro)

                except pyodbc.Error as erro:
                    print("Erro no banco de dados:", erro)

            elif opcao_consultas == "7":
                try:
                    id_consulta = int(input("ID da consulta: "))
                    novo_status = input("Novo status (AGENDADA, REALIZADA, CANCELADA): ")

                    with transacao(conn_str) as cursor:
                        atualizar_status_consulta(
                            cursor, id_consulta, novo_status
                        )

                    print("Status da consulta atualizado com sucesso!")

                except ValueError as erro:
                    print("Erro nos dados informados:", erro)

                except pyodbc.Error as erro:
                    print("Erro no banco de dados:", erro)

            elif opcao_consultas == "8":
                try:
                    id_consulta = int(input("ID da consulta: "))

                    with transacao(conn_str) as cursor:
                        excluir_consulta(cursor, id_consulta)

                    print("Consulta excluída com sucesso!")

                except ValueError as erro:
                    print("Erro nos dados informados:", erro)

                except pyodbc.Error as erro:
                    print("Erro no banco de dados:", erro)

            elif opcao_consultas == "0":
                break

            else:
                print("Opção inválida!")

    # ==========================================
    # 4 - HISTÓRICO DO PET
    # ==========================================
    elif opcao == "4":
        try:
            print("\n===== HISTÓRICO DO PET =====")
            id_pet = int(input("ID do pet: "))
            with transacao(conn_str) as cursor:
                historico = historico_do_pet(cursor, id_pet)

            if historico:
                for consulta in historico:
                    print("\nID da consulta:", consulta.id_consulta)
                    print("Pet:", consulta.pet)
                    print("Tutor:", consulta.tutor)
                    print("Veterinário:", consulta.veterinario)
                    print("Data e hora:", consulta.data_hora)
                    print("Status:", consulta.status)
                    print("Quantidade de itens:", consulta.qtd_itens)
                    print("Valor total:", consulta.valor_total)
                    print("----------------------")
            else:
                print("Nenhuma consulta encontrada para esse pet.")
        except ValueError as erro:
            print("Erro:", erro)
        except pyodbc.Error as erro:
            print("Erro no banco de dados:", erro)

    # ==========================================
    # 0 - ENCERRAR SISTEMA
    # ==========================================
    elif opcao == "0":
        print("Encerrando sistema...")
        break

    else:
        print("Opção inválida!")
