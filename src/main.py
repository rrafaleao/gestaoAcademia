# main_app.py
import customtkinter as ctk
from database.db_connection import GerenciadorBancoDados
from controller.user_controller import UserController
from views.auth.login_frame import LoginFrame
from views.auth.register_frame import RegisterFrame

class MainApp:
    def __init__(self):
        # Inicializa o banco de dados
        self.db_management = GerenciadorBancoDados()
        self.db_management.conectar()
        
        # Inicializa o controlador de usuários
        self.user_controller = UserController(self.db_management)
        
        # Configuração da janela principal
        self.root = ctk.CTk()
        self.root.title("Academia - Sistema de Gestão")
        self.root.geometry("800x800")
        self.root.minsize(400, 400)
        self.root.configure(fg_color="#F0F0F0")
        
        # Container para os frames
        self.container = ctk.CTkFrame(self.root, fg_color="#F0F0F0")
        self.container.pack(fill="both", expand=True)
        
        # Usuário logado
        self.usuario_atual = None
        
        # Dicionário para armazenar os frames
        self.frames = {}
        
        # Inicializa os frames
        self.inicializar_frames()
        
        # Começa com o frame de login
        self.mostrar_frame("login")
    
    def inicializar_frames(self):
        # Cria e armazena os frames
        login_frame = LoginFrame(self.container, self)
        register_frame = RegisterFrame(self.container, self)
        
        self.frames["login"] = login_frame
        self.frames["register"] = register_frame
        
        # Posiciona os frames (inicialmente ocultos)
        login_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)
        register_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)
    
    def mostrar_frame(self, nome_frame):
        # Oculta todos os frames
        for frame in self.frames.values():
            frame.place_forget()
        
        # Mostra o frame solicitado
        frame = self.frames[nome_frame]
        frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)
    
    def iniciar_interface_principal(self, usuario=None):
        # Armazena o usuário logado
        self.usuario_atual = usuario
        
        # Método para iniciar a interface principal após login/registro bem-sucedido
        # Implementar posteriormente conforme necessidade
        print(f"Interface principal iniciada para: {usuario['nome'] if usuario else 'Usuário não identificado'}")
    
    def executar(self):
        self.root.mainloop()
        
    def __del__(self):
        # Garante que a conexão com o banco seja fechada quando o app for encerrado
        if hasattr(self, 'db_management'):
            self.db_management.desconectar()

if __name__ == '__main__':
    app = MainApp()
    app.executar()