# database/db_connection.py
import mysql.connector
from mysql.connector import Error

class GerenciadorBancoDados:
    def __init__(self, host="localhost", usuario="root", senha="", banco="gestao_academia"):
        self.host = host
        self.usuario = usuario
        self.senha = senha
        self.banco = banco
        self.conexao = None
        self.cursor = None
    
    def conectar(self):
        """Estabelece conexão com o banco de dados"""
        try:
            self.conexao = mysql.connector.connect(
                host=self.host,
                user=self.usuario,
                password=self.senha,
                database=self.banco
            )
            
            if self.conexao.is_connected():
                self.cursor = self.conexao.cursor()
                print("Conexão com o banco de dados estabelecida com sucesso.")
                return True
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return False
    
    def desconectar(self):
        """Fecha a conexão com o banco de dados"""
        if self.conexao and self.conexao.is_connected():
            if self.cursor:
                self.cursor.close()
            self.conexao.close()
            print("Conexão com o banco de dados encerrada.")
    
    def executar_comando(self, query, params=None):
        """
        Executa um comando SQL (INSERT, UPDATE, DELETE).
        
        Args:
            query (str): Query SQL a ser executada
            params (tuple, opcional): Parâmetros para a query
        
        Returns:
            bool: True se o comando foi executado com sucesso
        """
        try:
            if not self.conexao or not self.conexao.is_connected():
                self.conectar()
                
            self.cursor.execute(query, params or ())
            self.conexao.commit()
            return True
        except Error as e:
            print(f"Erro ao executar comando: {e}")
            return False
    
    def executar_consulta(self, query, params=None):
        """
        Executa uma consulta SQL (SELECT).
        
        Args:
            query (str): Query SQL a ser executada
            params (tuple, opcional): Parâmetros para a query
        
        Returns:
            list: Resultados da consulta ou None em caso de erro
        """
        try:
            if not self.conexao or not self.conexao.is_connected():
                self.conectar()
                
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Error as e:
            print(f"Erro ao executar consulta: {e}")
            return None