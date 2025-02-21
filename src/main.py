from database.db_connection import GerenciadorBancoDados
from views.auth.login import LoginApp
import customtkinter as tk

class MainApp:
    def __init__(self):
        self.db_management = GerenciadorBancoDados()
        self.db_management.conectar() 
        self.tela_login = LoginApp(self)
        self.tela_login.executar()
        
if __name__ == '__main__':
    app = MainApp()
