import customtkinter as ctk
from tkcalendar import DateEntry
import datetime
from database.db_connection import GerenciadorBancoDados

class NovoAlunoFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F9F9F9", corner_radius=0)
        self.controller = controller
        self.db = GerenciadorBancoDados()

        # Cores do tema
        self.cor_primaria = "#5A189A"
        self.cor_secundaria = "#9D4EDD"
        self.cor_hover = "#7B2CBF"
        self.cor_texto = "#333333"
        self.cor_texto_claro = "#FFFFFF"
        self.cor_input = "#FFFFFF"
        self.cor_input_bg = "#F0F0F0"
        self.cor_borda = "#E0E0E0"

        # Configuração de fontes
        try:
            self.barlow_font = ctk.CTkFont(family="Barlow", size=16, weight="bold")
            self.title_font = ctk.CTkFont(family="Barlow", size=24, weight="bold")
            self.subtitle_font = ctk.CTkFont(family="Barlow", size=20, weight="bold")
            self.small_font = ctk.CTkFont(family="Barlow", size=14)
            self.button_font = ctk.CTkFont(family="Barlow", size=15, weight="bold")
        except:
            self.barlow_font = ("Arial", 16)
            self.title_font = ("Arial", 24, "bold")
            self.subtitle_font = ("Arial", 20, "bold")
            self.small_font = ("Arial", 14)
            self.button_font = ("Arial", 15, "bold")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar (idêntica ao Old_alunosframe)
        self.sidebar_frame = ctk.CTkFrame(
            self,
            fg_color="#5A189A",
            corner_radius=0,
            width=250
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)
        
        logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="GymSystem",
            font=self.title_font,
            text_color="white"
        )
        logo_label.pack(pady=(30, 40))
        
        self.criar_botao_menu("Dashboard", 0)
        self.criar_botao_menu("Membros", 1, True)
        self.criar_botao_menu("Agenda", 2)
        self.criar_botao_menu("Configurações", 3)
        
        user_frame = ctk.CTkFrame(
            self.sidebar_frame,
            fg_color="transparent"
        )
        user_frame.pack(side="bottom", pady=20, fill="x")
        
        profile_frame = ctk.CTkFrame(
            user_frame,
            fg_color="transparent"
        )
        profile_frame.pack(pady=5)
        
        profile_size = 70
        profile_photo = ctk.CTkFrame(
            profile_frame,
            width=profile_size,
            height=profile_size,
            corner_radius=profile_size//2,
            fg_color="#E0E0E0"
        )
        profile_photo.pack(pady=5)
        
        initials_label = ctk.CTkLabel(
            profile_photo,
            text="AD",
            font=self.title_font,
            text_color="#5A189A"
        )
        initials_label.place(relx=0.5, rely=0.5, anchor="center")
        
        user_name = ctk.CTkLabel(
            user_frame,
            text="Admin",
            font=self.small_font,
            text_color="white"
        )
        user_name.pack(pady=2)
        
        logout_button = ctk.CTkButton(
            user_frame,
            text="Sair",
            fg_color="#9D4EDD",
            hover_color="#7B2CBF",
            height=30,
            width=100,
            corner_radius=8,
            command=lambda: controller.mostrar_frame("login") if hasattr(controller, "mostrar_frame") else None
        )
        logout_button.pack(pady=5)

        # Conteúdo principal
        self.main_content = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=15,
            border_width=1,
            border_color=self.cor_borda
        )
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)

        # Cabeçalho
        header_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            header_frame,
            text="Novo Aluno",
            font=self.title_font,
            text_color=self.cor_texto
        ).grid(row=0, column=0, sticky="w")

        # Botão de voltar mais moderno
        voltar_btn = ctk.CTkButton(
            header_frame,
            text="← Voltar para Lista",
            fg_color=self.cor_secundaria,
            hover_color=self.cor_hover,
            command=lambda: controller.mostrar_frame("members"),
            width=150,
            height=35,
            corner_radius=8,
            font=self.button_font
        )
        voltar_btn.grid(row=0, column=1, sticky="e")

        # Linha divisória
        divider = ctk.CTkFrame(
            self.main_content,
            height=2,
            fg_color=self.cor_borda
        )
        divider.grid(row=0, column=0, sticky="ew", padx=20, pady=(60, 0))

        # Formulário
        form_frame = ctk.CTkScrollableFrame(
            self.main_content,
            fg_color="transparent"
        )
        form_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        form_frame.grid_columnconfigure(1, weight=1)

        # Campos do formulário
        campos = [
            ("Nome Completo", "nome", True),
            ("Telefone", "telefone", True),
            ("Data de Nascimento", "data_nascimento", False),
            ("Endereço", "endereco", False),
            ("Email", "email", False),
            ("Data de Início", "data_inicio", False),
            ("Plano", "plano", True)
        ]

        self.entries = {}
        row = 0
        for label, key, required in campos:
            # Label com estilo melhorado
            label_text = f"{label}{' *' if required else ''}"
            ctk.CTkLabel(
                form_frame,
                text=label_text,
                font=self.small_font,
                text_color=self.cor_texto
            ).grid(row=row, column=0, padx=(10, 20), pady=12, sticky="e")

            # Estilizando cada tipo de input
            if "data" in key:
                # Frame para envolver DateEntry com bordas personalizadas
                entry_frame = ctk.CTkFrame(
                    form_frame,
                    fg_color=self.cor_input_bg,
                    corner_radius=8,
                    border_width=1,
                    border_color=self.cor_borda
                )
                entry_frame.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
                
                entry = DateEntry(
                    entry_frame,
                    font=("Arial", 12),
                    date_pattern='dd/mm/yyyy',
                    background=self.cor_input_bg,
                    foreground=self.cor_texto,
                    borderwidth=0,
                    selectbackground=self.cor_secundaria
                )
                entry.pack(padx=8, pady=8, fill="both", expand=True)
                
            elif key == "plano":
                entry = ctk.CTkComboBox(
                    form_frame,
                    values=["Básico", "Intermediário", "Premium"],
                    font=self.small_font,
                    fg_color=self.cor_input,
                    bg_color="transparent",
                    border_color=self.cor_borda,
                    button_color=self.cor_secundaria,
                    button_hover_color=self.cor_hover,
                    dropdown_fg_color=self.cor_input,
                    dropdown_hover_color=self.cor_input_bg,
                    dropdown_text_color=self.cor_texto,
                    width=300,
                    height=38,
                    corner_radius=8
                )
                entry.set("Básico")
                entry.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
                
            else:
                entry = ctk.CTkEntry(
                    form_frame,
                    font=self.small_font,
                    fg_color=self.cor_input,
                    bg_color="transparent",
                    border_color=self.cor_borda,
                    text_color=self.cor_texto,
                    placeholder_text_color="#999999",
                    width=300,
                    height=38,
                    corner_radius=8,
                    placeholder_text=f"Digite {label.lower()}..."
                )
                entry.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
                
            self.entries[key] = entry
            row += 1

        # Botão de salvar melhorado
        salvar_btn = ctk.CTkButton(
            form_frame,
            text="SALVAR CADASTRO",
            fg_color=self.cor_primaria,
            hover_color=self.cor_hover,
            font=self.button_font,
            height=45,
            corner_radius=8,
            command=self.salvar_aluno
        )
        salvar_btn.grid(row=row, column=0, columnspan=2, pady=25, padx=50, sticky="ew")

    def criar_botao_menu(self, texto, indice, ativo=False):
        # Mantido do Old_alunosframe
        bg_color = "#9D4EDD" if ativo else "transparent"
        fg_color = "white" if ativo else "#E0E0E0"
        
        btn = ctk.CTkButton(
            self.sidebar_frame,
            text=texto,
            fg_color=bg_color,
            text_color=fg_color,
            hover_color="#7B2CBF",
            anchor="w",
            height=40,
            width=220,
            corner_radius=8,
            font=self.barlow_font,
            command=lambda t=texto: self.navegacao_menu(t)
        )
        btn.pack(pady=5, padx=15)
        return btn

    def salvar_aluno(self):
    # Coletar e formatar dados
        dados = {}
        try:
            for key, entry in self.entries.items():
                if isinstance(entry, DateEntry):
                    dados[key] = entry.get_date().strftime("%Y-%m-%d")
                elif isinstance(entry, ctk.CTkComboBox):
                    dados[key] = entry.get()
                else:
                    dados[key] = entry.get().strip()
                    
            # Verificar campos obrigatórios
            campos_obrigatorios = {
                "nome": "Nome Completo",
                "telefone": "Telefone",
                "plano": "Plano"
            }
            
            for key, label in campos_obrigatorios.items():
                if not dados.get(key):
                    self.mostrar_mensagem_erro(f"Preencha o campo {label}")
                    return

            # Validações adicionais
            if len(dados["telefone"]) > 15:
                self.mostrar_mensagem_erro("Telefone deve ter no máximo 15 caracteres")
                return

            # Definir padrões para campos opcionais
            if not dados.get("data_inicio"):
                dados["data_inicio"] = datetime.date.today().strftime("%Y-%m-%d")
            
            # Inserir no banco de dados
            query = """INSERT INTO clientes 
                    (nome, telefone, data_nascimento, endereco, email, data_inicio, plano)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            params = (
                dados["nome"],
                dados["telefone"],
                dados.get("data_nascimento"),
                dados.get("endereco"),
                dados.get("email"),
                dados["data_inicio"],
                dados["plano"]
            )

            if self.db.executar_comando(query, params):
                self.mostrar_mensagem_sucesso("Aluno cadastrado com sucesso!")
                self.controller.mostrar_frame("members")
            else:
                self.mostrar_mensagem_erro("Erro ao cadastrar aluno. Verifique os dados.")
                
        except Exception as e:
            self.mostrar_mensagem_erro(f"Erro inesperado: {str(e)}")
        finally:
            self.db.desconectar()
            
    def mostrar_mensagem_sucesso(self, mensagem):
        # Criar uma janela popup para mensagens de sucesso
        popup = ctk.CTkToplevel(self)
        popup.title("Sucesso")
        popup.geometry("300x150")
        popup.resizable(False, False)
        popup.attributes('-topmost', True)
        
        # Centralizar no frame pai
        popup.geometry(f"+{self.winfo_rootx() + 250}+{self.winfo_rooty() + 200}")
        
        frame = ctk.CTkFrame(popup, fg_color="#E8F5E9", corner_radius=10)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            frame, 
            text="✓ Sucesso", 
            font=self.subtitle_font, 
            text_color="#2E7D32"
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            frame,
            text=mensagem,
            font=self.small_font,
            text_color="#33691E"
        ).pack(pady=5)
        
        ctk.CTkButton(
            frame,
            text="OK",
            fg_color="#4CAF50",
            hover_color="#388E3C",
            corner_radius=8,
            command=popup.destroy
        ).pack(pady=10)
        
    def mostrar_mensagem_erro(self, mensagem):
        # Criar uma janela popup para mensagens de erro
        popup = ctk.CTkToplevel(self)
        popup.title("Erro")
        popup.geometry("300x150")
        popup.resizable(False, False)
        popup.attributes('-topmost', True)
        
        # Centralizar no frame pai
        popup.geometry(f"+{self.winfo_rootx() + 250}+{self.winfo_rooty() + 200}")
        
        frame = ctk.CTkFrame(popup, fg_color="#FFEBEE", corner_radius=10)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            frame, 
            text="⚠ Erro", 
            font=self.subtitle_font, 
            text_color="#C62828"
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            frame,
            text=mensagem,
            font=self.small_font,
            text_color="#B71C1C"
        ).pack(pady=5)
        
        ctk.CTkButton(
            frame,
            text="OK",
            fg_color="#F44336",
            hover_color="#D32F2F",
            corner_radius=8,
            command=popup.destroy
        ).pack(pady=10)

    def navegacao_menu(self, texto):
        if texto == "Membros" and self.controller:
            self.controller.mostrar_frame("members")
        elif texto == "Dashboard" and self.controller:
            self.controller.mostrar_frame("dashboard")
        elif texto == "Agenda" and self.controller:
            self.controller.mostrar_frame("agendar")
        elif texto == "Configurações" and self.controller:
            self.controller.mostrar_frame("settings")