# views/auth/register_frame.py
import customtkinter as ctk
import re
from tkinter import messagebox, StringVar

class RegisterFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F0F0F0", corner_radius=0)
        
        self.controller = controller
        
        # Configuração da fonte
        try:
            self.barlow_font = ctk.CTkFont(family="Barlow", size=16, weight="bold")
        except Exception as e:
            print(f"Erro ao carregar a fonte 'Barlow': {e}")
            self.barlow_font = ("Arial", 16)
        
        # Container central para elementos do registro
        self.content_frame = ctk.CTkFrame(
            self,
            fg_color="#F0F0F0",
            corner_radius=20
        )
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        label_titulo = ctk.CTkLabel(
            self.content_frame,
            text="Registro de Usuário",
            font=ctk.CTkFont(family="Barlow", size=24, weight="bold"),
            text_color="black"
        )
        label_titulo.pack(pady=20)
        
        # Campo de nome
        self.entry_nome = ctk.CTkEntry(
            self.content_frame,
            placeholder_text="Nome",
            width=300,
            height=40,
            fg_color="white",
            text_color="black",
            corner_radius=10
        )
        self.entry_nome.pack(pady=10)
        
        # Campo de email
        self.entry_email = ctk.CTkEntry(
            self.content_frame,
            placeholder_text="Email",
            width=300,
            height=40,
            fg_color="white",
            text_color="black",
            corner_radius=10
        )
        self.entry_email.pack(pady=10)
        
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
        
        # Tipo de acesso
        self.nivel_acesso_var = StringVar(value="funcionario")
        
        acesso_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        acesso_frame.pack(pady=10)
        
        acesso_label = ctk.CTkLabel(
            acesso_frame,
            text="Nível de Acesso:",
            text_color="black"
        )
        acesso_label.pack(side="left", padx=(0, 10))
        
        # Radio buttons para nível de acesso
        radio_funcionario = ctk.CTkRadioButton(
            acesso_frame,
            text="Funcionário",
            variable=self.nivel_acesso_var,
            value="funcionario",
            text_color="black",
            fg_color="#5A189A"
        )
        radio_funcionario.pack(side="left", padx=5)
        
        radio_admin = ctk.CTkRadioButton(
            acesso_frame,
            text="Administrador",
            variable=self.nivel_acesso_var,
            value="admin",
            text_color="black",
            fg_color="#5A189A"
        )
        radio_admin.pack(side="left", padx=5)
        
        # Botão de registro
        btn_registrar = ctk.CTkButton(
            self.content_frame,
            text="Registrar",
            fg_color="#5A189A",
            hover_color="#3C096C",
            width=300,
            height=50,
            font=self.barlow_font,
            corner_radius=10,
            command=self.registrar_usuario
        )
        btn_registrar.pack(pady=10)
        
        # Botão para ir para login
        btn_login = ctk.CTkButton(
            self.content_frame,
            text="Fazer Login",
            fg_color="#9D4EDD",
            hover_color="#7B2CBF",
            width=300,
            height=50,
            font=self.barlow_font,
            corner_radius=10,
            command=lambda: controller.mostrar_frame("login")
        )
        btn_login.pack(pady=10)
    
    def _validar_email(self, email):
        """Valida o formato do email"""
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(padrao, email) is not None
    
    def _validar_senha(self, senha):
        """Valida a força da senha (mínimo 6 caracteres)"""
        return len(senha) >= 6
    
    def registrar_usuario(self):
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        senha = self.entry_senha.get()
        nivel_acesso = self.nivel_acesso_var.get()
        
        # Validações básicas
        if not nome or not email or not senha:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos!")
            return
        
        if not self._validar_email(email):
            messagebox.showerror("Erro", "Por favor, informe um email válido!")
            return
        
        if not self._validar_senha(senha):
            messagebox.showerror("Erro", "A senha deve ter pelo menos 6 caracteres!")
            return
        
        # Usa o controlador para adicionar o usuário
        sucesso, mensagem = self.controller.user_controller.adicionar_usuario(
            nome, email, senha, nivel_acesso=nivel_acesso
        )
        
        if sucesso:
            messagebox.showinfo("Registro", mensagem)
            # Limpa os campos
            self.entry_nome.delete(0, 'end')
            self.entry_email.delete(0, 'end')
            self.entry_senha.delete(0, 'end')
            self.nivel_acesso_var.set("funcionario")
            # Volta para a tela de login
            self.controller.mostrar_frame("login")
        else:
            messagebox.showerror("Erro", mensagem)