
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
                print("Listar pets do tutor - ainda não implementado.")

            elif opcao_pet == "6":
                print("Buscar pet com tutor - ainda não implementado.")

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
                print("Agendar consulta - ainda não implementado.")

            elif opcao_consultas == "2":
                print("Adicionar procedimento - ainda não implementado.")

            elif opcao_consultas == "3":
                print("Remover procedimento - ainda não implementado.")

            elif opcao_consultas == "4":
                print("Listar procedimentos - ainda não implementado.")

            elif opcao_consultas == "5":
                print("Listar consultas por procedimento - ainda não implementado.")

            elif opcao_consultas == "6":
                print("Total da consulta - ainda não implementado.")

            elif opcao_consultas == "7":
                print("Atualizar status - ainda não implementado.")

            elif opcao_consultas == "8":
                print("Excluir consulta - ainda não implementado.")

            elif opcao_consultas == "0":
                break

            else:
                print("Opção inválida!")

    # ==========================================
    # 4 - HISTÓRICO DO PET
    # ==========================================
    elif opcao == "4":
        print("\n===== HISTÓRICO DO PET =====")
        print("Histórico do pet - ainda não implementado.")

    # ==========================================
    # 0 - ENCERRAR SISTEMA
    # ==========================================
    elif opcao == "0":
        print("Encerrando sistema...")
        break

    else:
        print("Opção inválida!")
