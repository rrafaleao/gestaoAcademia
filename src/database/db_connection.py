import mysql.connector
from mysql.connector import Error

class GerenciadorBancoDados:
    def __init__(self, host="ivvdi.h.filess.io", usuario="gestaoAcademia_fewerfully", senha="d02b041498b5d3807d4095c30ae7e1e90b7777db", banco="gestaoAcademia_fewerfully", porta=3307):
        self.host = host
        self.usuario = usuario
        self.senha = senha
        self.banco = banco
        self.porta = porta
        self.conexao = None
        self.cursor = None
    
    def conectar(self):
        """Estabelece conexão com o banco de dados"""
        try:
            self.conexao = mysql.connector.connect(
                host=self.host,
                user=self.usuario,
                password=self.senha,
                database=self.banco,
                port=self.porta
            )
            
            if self.conexao.is_connected():
                self.cursor = self.conexao.cursor()
                db_info = self.conexao.get_server_info()
                print(f"Conectado ao MySQL Server versão {db_info}")
                self.cursor.execute("SELECT DATABASE();")
                record = self.cursor.fetchone()
                print(f"Você está conectado ao banco de dados: {record}")
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
