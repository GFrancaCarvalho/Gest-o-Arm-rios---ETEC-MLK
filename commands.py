import mysql.connector
import datetime as dt   
from dateutil.relativedelta import relativedelta
import pandas as pd
import os

# Conexões --------> 

# Conexão com o banco de dados - 

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='stproject'
)

cursor = connection.cursor()  

# Identifica e salva o nome do usuário

usuario = os.getlogin()

# Conexão com a planilha excel

planilha = pd.read_excel(r'C:\Users\%s\Desktop\Armários.xlsx' % f'{usuario}', index_col=0)  

# Comandos -------->

def registro(aluno, curso, armário):
    try:
        comandoR = f'SELECT nome_aluno FROM lockers WHERE num_arm = "{armário}"' # Seleciona a coluna "nome_aluno" onde o armário inserido no software existe também no BD.
        cursor.execute(comandoR)
        resultado = cursor.fetchall() # ler o banco de dados
        data_today = dt.date.today() # Salva a data atual
        data_expire = data_today + relativedelta(months=6) # Adiciona 6 meeses a data atual
        comandoU = f'UPDATE lockers SET nome_aluno = "{aluno}", curso = "{curso}", data_reserv = "{str(data_today)}", data_expir = "{str(data_expire)}", situation = "OK" WHERE num_arm = "{armário}"'
        cursor.execute(comandoU)
        connection.commit() # edita o banco de dados
        print("Registro realizado com sucesso.")

                
    except mysql.connector.Error as error: # Caso ocorra um erro na conexão com o BD, exibe o erro no console
        print("Não foi possível conectar-se ao banco de dados: ", error)

    # Adiciona os dados na planilha do excel

    planilha.loc[planilha["num_arm"]==armário, "nome_aluno"] = aluno
    planilha.loc[planilha["num_arm"]==armário, "curso"] = curso
    planilha.loc[planilha["num_arm"]==armário, "data_reserva"] = str(data_today)
    planilha.loc[planilha["num_arm"]==armário, "data_expira"] = str(data_expire)
    planilha.loc[planilha["num_arm"]==armário, "situação"] = "Ok"
    planilha.to_excel(r'C:\Users\%s\Desktop\Armários.xlsx' % f'{usuario}')

    return resultado
    


def buscar_todos():
    comandoR = 'SELECT * FROM lockers' # Seleciona todas as informações do BD.
    cursor.execute(comandoR)
    resultado = cursor.fetchall() # ler o banco de dados

    return resultado

def buscar(search):
    comandoR = f'SELECT * FROM lockers' # Seleciona todas as informações do BD.
    cursor.execute(comandoR)
    resultado = cursor.fetchall() # ler o banco de dados

    for i in resultado: # Analisa cada armário indivudalmente
        if i[3] == search or i[1] == search: # Verifica se o nome do aluno é igual a entrada do usuário OU o armário é igual a entrada do usuário
            return i

def excluir_cadastro(excluir):
    comandoR = f'SELECT * FROM lockers WHERE nome_aluno = "{excluir}"' # Seleciona todos os dados onde o nome do aluno for igual a entrada do usuário
    cursor.execute(comandoR)
    resultado = cursor.fetchall() # ler o banco de dados
    if resultado == []: # Caso não encontre a informação
        print("Usuário não encontrado")
        return []
    else: # Caso encontre a informação
        try:
            for linha in resultado:

                # Dados exibidos no console (Não visível ao usuário)

                print("Número do armário:", linha[1])
                print("Nome do aluno:", linha[3])
                print("Curso:", linha[4])
                print("Data de Cadastro:", linha[5])
                print("Data Expirado:", linha[6])
                print("Situação:", linha[7], "\n")

                comandoU = f'UPDATE lockers SET nome_aluno = NULL, curso = NULL, data_reserv = NULL, data_expir = NULL, situation = "OK" WHERE nome_aluno = "{excluir}"'
                cursor.execute(comandoU)
                connection.commit() # edita o banco de dados
                print("\nCadastro excluido com sucesso.")

        except mysql.connector.Error as error:
            print("Não foi possível conectar-se ao banco de dados: ", error)

        
         # Altera os dados na planilha do excel

        try:
            planilha.loc[planilha["nome_aluno"]==excluir, "curso"] = ""
            planilha.loc[planilha["nome_aluno"]==excluir, "data_reserva"] = ""
            planilha.loc[planilha["nome_aluno"]==excluir, "data_expira"] = ""
            planilha.loc[planilha["nome_aluno"]==excluir, "situação"] = ""
            planilha.loc[planilha["nome_aluno"]==excluir, "nome_aluno"] = ""
            planilha.to_excel(r'C:\Users\%s\Desktop\Armários.xlsx' % f'{usuario}')

        except:
            print("Não foi possível atuaizar os dados no Excel")

        
####### Possíveis expansões - 

# Expansão - Adicionar novos armários no software ->

def criar_armário():
    armário = input("Digite o nome do armário: ")
    local = input("Digite onde está localizado este armário: ")
    try:
        comandoC = f'INSERT INTO lockers (num_arm, local_arm) VALUES ("{armário}", "{local}")'
        cursor.execute(comandoC)
        connection.commit() # edita o banco de dados

    except mysql.connector.Error as error:
        print("Não foi possível conectar-se ao banco de dados: ", error)

# Atualiza a situação dos cadastros, realizado ao iniciar o aplicativo.

def atualizar_cadastros():
    comandoR = f'SELECT data_expir FROM lockers' 
    cursor.execute(comandoR)
    resultado = cursor.fetchall() # ler o banco de dados
    for linha in resultado:
        if str(linha) != "(None,)":
            linha = linha[0]
            x = linha.split("-")
            year = x[0]
            month = x[1]
            day = x[2]
            expire = dt.date(int(year), int(month), int(day))
            today = dt.date.today()
            if today > expire:
                comandoU = f'UPDATE lockers SET situation = "EXPIRADO" WHERE data_expir = "{linha}"'
                cursor.execute(comandoU)
                connection.commit() # edita o banco de dados
                
