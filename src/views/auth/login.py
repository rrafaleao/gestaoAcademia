import customtkinter as ctk
from tkinter import messagebox

class LoginApp:
    def __init__(self, main_app):
        self.main_app = main_app
        self.root = ctk.CTk()
        self.root.title("Login - Academia")
        self.root.geometry("800x800")
        self.root.minsize(400, 400)  # Define um tamanho mínimo para a janela
        
        # Frame principal
        self.frame = ctk.CTkFrame(self.root, fg_color="#2D033B", corner_radius=20)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Título
        label_titulo = ctk.CTkLabel(self.frame, text="Login", font=("Arial", 24, "bold"), text_color="white")
        label_titulo.pack(pady=10)
        
        # Campo de Usuário
        self.entry_usuario = ctk.CTkEntry(self.frame, placeholder_text="Usuário", width=300, height=40)
        self.entry_usuario.pack(pady=10)
        
        # Campo de Senha
        self.entry_senha = ctk.CTkEntry(self.frame, placeholder_text="Senha", show="*", width=300, height=40)
        self.entry_senha.pack(pady=10)
        
        # Botão "Esqueceu a Senha?"
        btn_esqueceu = ctk.CTkButton(self.frame, text="Esqueceu a senha?", fg_color="transparent", text_color="white", hover_color="#5A189A")
        btn_esqueceu.pack(pady=10)
        
        # Botões de Login e Registro
        btn_login = ctk.CTkButton(self.frame, text="Entrar", fg_color="#5A189A", width=300, height=50, font=("Arial", 16, "bold"), corner_radius=10, command=self.verificar_login)
        btn_login.pack(pady=10)
        
        btn_registrar = ctk.CTkButton(self.frame, text="Registrar", fg_color="#9D4EDD", width=300, height=50, font=("Arial", 16, "bold"), corner_radius=10)
        btn_registrar.pack(pady=10)
        
        # Configurar redimensionamento
        self.root.bind("<Configure>", self.ajustar_tamanho)
    
    def ajustar_tamanho(self, event):
        self.frame.pack_configure(fill="both", expand=True)
    
    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        
        # Simulação de verificação no banco de dados
        if usuario == "admin" and senha == "admin":  # Aqui você deve integrar com o banco de dados
            messagebox.showinfo("Login", "Login bem-sucedido!")
            self.root.destroy()
            self.main_app.iniciar_interface()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")
    
    def executar(self):
        self.root.mainloop()
