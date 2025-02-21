import mysql.connector
from mysql.connector import Error

class GerenciadorBancoDados:
    def __init__(self):
        self.conexao = None

    def conectar(self):
        try:
            self.conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="gestao_academia"
            )
            if self.conexao.is_connected():
                print("Conexão ao banco de dados estabelecida com sucesso!")
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self.conexao = None