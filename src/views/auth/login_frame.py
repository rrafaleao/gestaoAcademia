# views/auth/login_frame.py
import customtkinter as ctk
from tkinter import messagebox

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F0F0F0", corner_radius=0)
        
        self.controller = controller
        
        # Configuração da fonte
        try:
            self.barlow_font = ctk.CTkFont(family="Barlow", size=16, weight="bold")
        except Exception as e:
            print(f"Erro ao carregar a fonte 'Barlow': {e}")
            self.barlow_font = ("Arial", 16)
        
        # Container central para elementos do login
        self.content_frame = ctk.CTkFrame(
            self,
            fg_color="#F0F0F0",
            corner_radius=20
        )
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        label_titulo = ctk.CTkLabel(
            self.content_frame,
            text="Login",
            font=ctk.CTkFont(family="Barlow", size=24, weight="bold"),
            text_color="black"
        )
        label_titulo.pack(pady=20)
        
        # Campo de usuário/email
        self.entry_usuario = ctk.CTkEntry(
            self.content_frame,
            placeholder_text="Email",
            width=300,
            height=40,
            fg_color="white",
            text_color="black",
            corner_radius=10
        )
        self.entry_usuario.pack(pady=10)
        
        # Campo de senha
        self.entry_senha = ctk.CTkEntry(
            self.content_frame,
            placeholder_text="Senha",
            show="*",
            width=300,
            height=40,
            fg_color="white",
            text_color="black",
            corner_radius=10
        )
        self.entry_senha.pack(pady=10)
        
        # Botão de login
        btn_login = ctk.CTkButton(
            self.content_frame,
            text="Entrar",
            fg_color="#5A189A",
            hover_color="#3C096C",
            width=300,
            height=50,
            font=self.barlow_font,
            corner_radius=10,
            command=self.verificar_login
        )
        btn_login.pack(pady=10)
        
        # Botão para ir para registro
        btn_registrar = ctk.CTkButton(
            self.content_frame,
            text="Registrar",
            fg_color="#9D4EDD",
            hover_color="#7B2CBF",
            width=300,
            height=50,
            font=self.barlow_font,
            corner_radius=10,
            command=lambda: controller.mostrar_frame("register")
        )
        btn_registrar.pack(pady=10)
    
    def verificar_login(self):
        email = self.entry_usuario.get()
        senha = self.entry_senha.get()
        
        if not email or not senha:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos!")
            return
        
        # Usa o controlador para verificar as credenciais
        sucesso, mensagem, usuario = self.controller.user_controller.verificar_credenciais(email, senha)
        
        if sucesso:
            messagebox.showinfo("Login", mensagem)
            # Limpa os campos
            self.entry_usuario.delete(0, 'end')
            self.entry_senha.delete(0, 'end')
            # Inicia a interface principal passando os dados do usuário
            self.controller.iniciar_interface_principal(usuario)
        else:
            messagebox.showerror("Erro", mensagem)