import customtkinter as ctk
from database.db_connection import GerenciadorBancoDados
from controller.auth.auth_controller import UserController
from controller.admin.admin_controller import AdminController
from views.auth.login_frame import LoginFrame
from views.auth.register_frame import RegisterFrame
from views.admin.dashboard import DashboardFrame
from views.admin.student import AlunosFrame

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
        login_frame = LoginFrame(self.container, self)
        register_frame = RegisterFrame(self.container, self)
        dashboard_frame = DashboardFrame(self.container, self)
        members_frame = AlunosFrame(self.container, self)
        
        self.frames["login"] = login_frame
        self.frames["register"] = register_frame
        self.frames["dashboard"] = dashboard_frame
        self.frames["members"] = members_frame

        for frame in self.frames.values():
            frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)
    
    def mostrar_frame(self, nome_frame):
        for frame in self.frames.values():
            frame.place_forget()
        
        frame = self.frames.get(nome_frame)
        if frame:
            frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)
    
    def iniciar_interface_principal(self, usuario=None):
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