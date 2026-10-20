# PetVida — Python + SQL Server com pyodbc

Projeto acadêmico de acesso a dados para uma clínica veterinária, desenvolvido em Python com SQL Server, como parte do **Desafio Técnico — Conexão Python + SQL Server com pyodbc**.

## Objetivo

Implementar operações de cadastro, consulta, atualização e exclusão em um banco relacional já fornecido pelo professor, utilizando consultas parametrizadas, transações e tratamento de erros de integridade.

## Tecnologias

- Python 3
- Microsoft SQL Server (2019, 2022 ou 2025, conforme o script fornecido)
- SQL Server Management Studio (SSMS), para executar o script e administrar o banco
- `pyodbc` (biblioteca Python para conexão ODBC)
- Driver ODBC compatível com SQL Server, instalado no Windows

## Arquivos do projeto

```text
.
├── db.py             # String de conexão, conexão e gerenciamento de transações
├── repositorio.py    # Operações SQL de tutores, pets, consultas e procedimentos
├── main.py           # Menu de terminal
├── README.md         # Instruções do projeto
└── .gitignore        # Arquivos locais que não devem ser versionados (recomendado)
```

O arquivo SQL de estrutura e dados iniciais é fornecido separadamente pelo professor. Se ele estiver incluído no repositório, execute-o a partir do SSMS.

## Preparação do ambiente

1. Instale Python 3 e SQL Server.
2. Abra o SSMS, conecte-se à sua instância e execute o script **`01_estrutura_petvida.sql`** fornecido pelo professor. Ele cria o banco `PetVida`, as seis tabelas, restrições, a view e os dados de exemplo.
3. **Atenção:** o script fornecido pode excluir e recriar o banco `PetVida` se ele já existir. Não o execute novamente sobre dados que queira preservar.
4. No terminal, instale a dependência Python:

   ```bash
   python -m pip install pyodbc
   ```

5. Para verificar os drivers ODBC instalados:

   ```bash
   python -c "import pyodbc; print(pyodbc.drivers())"
   ```

   O código atual usa `Driver={SQL Server}`. Se não estiver instalado, será necessário instalar um driver compatível e ajustar esse valor em `db.py` (por exemplo, `ODBC Driver 17 for SQL Server` ou `ODBC Driver 18 for SQL Server`, observando as opções de criptografia e certificados de cada driver).

## Configuração da conexão

O código atual usa uma instância local:

```text
Server=(local)
Database=PetVida
```

Se sua instância tiver outro nome, modifique `Server=` na função `montar_connection_string()` em `db.py`.

### Autenticação com login SQL Server

1. No SSMS, conecte-se com uma conta administrativa usando a autenticação do Windows.
2. Em **Propriedades do servidor > Segurança**, habilite **Modo de Autenticação do SQL Server e do Windows** e reinicie o serviço SQL Server.
3. Execute a seção opcional de criação do login, ajustando a senha para uma senha forte de uso próprio. Essa seção cria o login da aplicação, associa-o ao banco e atribui as funções `db_datareader` e `db_datawriter`.
4. No terminal, ao executar `main.py`, informe o login e a senha criados.

**Segurança:** não inclua senhas reais em `db.py`, `README.md`, commits ou capturas de tela. O programa usa `getpass()` para não exibir a senha digitada. Em produção, prefira gerenciamento de segredos ou variáveis de ambiente e evite manter credenciais em texto puro por mais tempo do que o necessário.

## Execução

Na pasta do projeto:

```bash
python main.py
```

O programa pede as credenciais e tenta uma conexão inicial. Em seguida, apresenta menus para tutores, pets, consultas/procedimentos e histórico.

## Estrutura do banco

- `tutor`: dados dos tutores; CPF com restrições de formato e unicidade.
- `pet`: animais vinculados a tutores (1:N).
- `veterinario`: profissionais que atendem os pets.
- `procedimento`: catálogo de serviços e preços-base.
- `consulta`: atendimentos ligados a pet e veterinário.
- `consulta_procedimento`: relação N:M entre consultas e procedimentos, incluindo quantidade e valor cobrado.
- `vw_resumo_consulta`: visão de apoio com totais por consulta.

## Regras técnicas

- Consultas com dados fornecidos pelo usuário devem usar parâmetros `?`, nunca concatenação direta no SQL.
- Atualizações com colunas dinâmicas devem usar uma lista branca de nomes permitidos.
- Conexões não devem permanecer abertas globalmente; o gerenciador `transacao()` usa `commit()` em caso de sucesso, `rollback()` em caso de falha e fecha cursor/conexão no `finally`.
- As constraints, chaves estrangeiras e estrutura do script fornecido não devem ser removidas ou alteradas para contornar erros.

## Estado e validação

As funcionalidades de tutores e pets e parte das operações de consultas e procedimentos foram implementadas. **Antes da entrega final, revise e teste as operações de associação/remoção de procedimentos, listagem com quantidade, status de consultas, histórico do pet e tratamento de falhas de conexão/integridade.** A presença de uma opção no menu não garante que sua implementação esteja correta.

Testes recomendados: conexão válida e inválida; CPF inválido e duplicado; tentativa de excluir tutor com pets; tentativa de excluir pet com consultas; atualização de peso inválido; agendamento com múltiplos procedimentos; erro em item da consulta para confirmar `rollback`; status permitido e inválido; exclusão em cascata dos itens de uma consulta; consultas à view de histórico.

## Entrega

O enunciado solicita `db.py`, `repositorio.py`, `README.md` e **um print do verificador**. Inclua a captura verdadeira após executar o verificador disponibilizado pelo professor; não considere este README como evidência de testes concluídos. O `main.py` é uma funcionalidade bônus.
