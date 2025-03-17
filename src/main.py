import customtkinter as ctk
from database.db_connection import GerenciadorBancoDados
from controller.auth.auth_controller import UserController
from controller.admin.admin_controller import AdminController
from views.auth.login_frame import LoginFrame
from views.auth.register_frame import RegisterFrame
from views.admin.dashboard import DashboardFrame
from views.admin.student import AlunosFrame
from views.admin.add_student import NovoAlunoFrame
from views.admin.schedule import TelaAgendamentoAulas
from views.admin.config import TelaConfiguracao

class MainApp:
    def __init__(self):
        self.db_management = GerenciadorBancoDados()
        self.db_management.conectar()
        
        self.user_controller = UserController(self.db_management)
        self.admin_controller = AdminController(self.db_management)

        self.root = ctk.CTk()
        self.root.title("Academia - Sistema de Gestão")
        self.root.geometry("800x800")
        self.root.minsize(400, 400)
        self.root.configure(fg_color="#F0F0F0")
        
        self.container = ctk.CTkFrame(self.root, fg_color="#F0F0F0")
        self.container.pack(fill="both", expand=True)
        
        self.usuario_atual = None

        self.frames = {}
        
        self.inicializar_frames()
        
        self.mostrar_frame("login")
    
    def inicializar_frames(self):
        # Atualize a inicialização dos frames
        login_frame = LoginFrame(self.container, self)
        register_frame = RegisterFrame(self.container, self)
        dashboard_frame = DashboardFrame(self.container, self)
        members_frame = AlunosFrame(self.container, self)
        add_student_frame = NovoAlunoFrame(self.container, self)
        agendar_frame = TelaAgendamentoAulas(self.container, self)  # Novo frame
        config_frame = TelaConfiguracao(self.container, self)

        self.frames = {
            "login": login_frame,
            "register": register_frame,
            "dashboard": dashboard_frame,
            "members": members_frame,
            "novo_aluno": add_student_frame,
            "agendar": agendar_frame,
            "config": config_frame
        }

        # Configura posicionamento dos frames
        for frame in self.frames.values():
            frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)
    
    def mostrar_frame(self, nome_frame):
        # Esconde todos os frames e mostra o solicitado
        for frame in self.frames.values():
            frame.place_forget()
        
        frame = self.frames.get(nome_frame)
        if frame:
            frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)
    
    def iniciar_interface_principal(self, usuario=None):
        # Inicia a interface após login
        self.usuario_atual = usuario
        self.mostrar_frame("dashboard")
    
    def executar(self):
        self.root.mainloop()
        
    def __del__(self):
        if hasattr(self, 'db_management'):
            self.db_management.desconectar()

if __name__ == '__main__':
    app = MainApp()
    app.executar()