import customtkinter as ctk
from tkinter import ttk, StringVar
import datetime
from tkcalendar import DateEntry

class AlunosFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F0F0F0", corner_radius=0)
        
        self.controller = controller
        
        # Configuração da fonte
        try:
            self.barlow_font = ctk.CTkFont(family="Barlow", size=16, weight="bold")
            self.title_font = ctk.CTkFont(family="Barlow", size=24, weight="bold")
            self.subtitle_font = ctk.CTkFont(family="Barlow", size=20, weight="bold")
            self.small_font = ctk.CTkFont(family="Barlow", size=14)
            self.large_value_font = ctk.CTkFont(family="Barlow", size=48, weight="bold")
            self.metric_label_font = ctk.CTkFont(family="Barlow", size=18)
        except Exception as e:
            print(f"Erro ao carregar a fonte 'Barlow': {e}")
            self.barlow_font = ("Arial", 16)
            self.title_font = ("Arial", 24, "bold")
            self.subtitle_font = ("Arial", 20, "bold")
            self.small_font = ("Arial", 14)
            self.large_value_font = ("Arial", 48, "bold")
            self.metric_label_font = ("Arial", 18)
        
        # Layout principal: sidebar e área de conteúdo
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(
            self,
            fg_color="#5A189A",
            corner_radius=0,
            width=250
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)  # Para empurrar os itens para cima
        
        # Logo ou nome do sistema
        logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="GymSystem",
            font=self.title_font,
            text_color="white"
        )
        logo_label.pack(pady=(30, 40))
        
        # Itens do menu
        self.criar_botao_menu("Dashboard", 0)
        self.criar_botao_menu("Membros", 1, True)
        self.criar_botao_menu("Planos", 2)
        self.criar_botao_menu("Pagamentos", 3)
        self.criar_botao_menu("Agenda", 4)
        self.criar_botao_menu("Funcionários", 5)
        self.criar_botao_menu("Relatórios", 6)
        self.criar_botao_menu("Configurações", 7)
        
        # Informações do usuário no rodapé da sidebar
        user_frame = ctk.CTkFrame(
            self.sidebar_frame,
            fg_color="transparent"
        )
        user_frame.pack(side="bottom", pady=20, fill="x")
        
        # Foto de perfil (simulada como um círculo)
        profile_frame = ctk.CTkFrame(
            user_frame,
            fg_color="transparent"
        )
        profile_frame.pack(pady=5)
        
        # Círculo para foto de perfil
        profile_size = 70
        profile_photo = ctk.CTkFrame(
            profile_frame,
            width=profile_size,
            height=profile_size,
            corner_radius=profile_size//2,
            fg_color="#E0E0E0"
        )
        profile_photo.pack(pady=5)
        
        # Iniciais do usuário dentro da foto de perfil
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
        
        # Área principal de conteúdo
        self.main_content = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=15
        )
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(2, weight=1)
        
        # Título e botões de ação
        title_frame = ctk.CTkFrame(
            self.main_content,
            fg_color="transparent"
        )
        title_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="Gerenciamento de Alunos",
            font=self.title_font,
            text_color="#333333"
        )
        title_label.grid(row=0, column=0, sticky="w")
        
        button_frame = ctk.CTkFrame(
            title_frame,
            fg_color="transparent"
        )
        button_frame.grid(row=0, column=1, sticky="e")
        
        add_button = ctk.CTkButton(
            button_frame,
            text="+ Novo Aluno",
            fg_color="#5A189A",
            hover_color="#7B2CBF",
            height=35,
            width=130,
            corner_radius=8,
            command=self.abrir_novo_aluno
        )
        add_button.pack(side="left", padx=5)
        
        # Barra de pesquisa
        search_frame = ctk.CTkFrame(
            self.main_content,
            fg_color="transparent",
            height=50
        )
        search_frame.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="ew")
        search_frame.grid_columnconfigure(1, weight=1)
        
        search_label = ctk.CTkLabel(
            search_frame,
            text="Buscar:",
            font=self.barlow_font,
            text_color="#333333"
        )
        search_label.grid(row=0, column=0, padx=(0, 10), sticky="w")
        
        self.search_var = StringVar()
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            height=35,
            corner_radius=8,
            border_width=1,
            placeholder_text="Digite nome, email ou telefone...",
            font=self.small_font
        )
        search_entry.grid(row=0, column=1, sticky="ew")
        self.search_var.trace_add("write", self.filtrar_alunos)
        
        search_button = ctk.CTkButton(
            search_frame,
            text="Buscar",
            fg_color="#5A189A",
            hover_color="#7B2CBF",
            height=35,
            width=100,
            corner_radius=8,
            command=self.filtrar_alunos
        )
        search_button.grid(row=0, column=2, padx=(10, 0), sticky="e")
        
        # Criação da tabela de alunos
        table_frame = ctk.CTkFrame(
            self.main_content,
            fg_color="transparent"
        )
        table_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        
        # Tabela com estilo usando ttk.Treeview
        style = ttk.Style()
        style.configure("Treeview", font=self.small_font, rowheight=40)
        style.configure("Treeview.Heading", font=self.barlow_font, background="#E6E6E6")
        style.map("Treeview", background=[("selected", "#9D4EDD")])
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=("nome", "telefone", "data_nascimento", "endereco", "email", "data_inicio", "plano", "acoes"),
            show="headings",
            height=10
        )
        
        # Definir cabeçalhos e larguras das colunas
        self.tree.heading("nome", text="Nome")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("data_nascimento", text="Data Nasc.")
        self.tree.heading("endereco", text="Endereço")
        self.tree.heading("email", text="Email")
        self.tree.heading("data_inicio", text="Data Início")
        self.tree.heading("plano", text="Plano")
        self.tree.heading("acoes", text="Ações")
        
        self.tree.column("nome", width=180)
        self.tree.column("telefone", width=120)
        self.tree.column("data_nascimento", width=100)
        self.tree.column("endereco", width=200)
        self.tree.column("email", width=180)
        self.tree.column("data_inicio", width=100)
        self.tree.column("plano", width=120)
        self.tree.column("acoes", width=120)
        
        # Adicionar scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Adicionar alguns dados de exemplo
        self.carregar_dados_exemplo()
        
        # Adicionar contexto para botões de ação
        self.tree.bind("<Double-1>", self.editar_aluno)
        
        # Mostrador de páginas
        paging_frame = ctk.CTkFrame(
            self.main_content,
            fg_color="transparent",
            height=50
        )
        paging_frame.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="ew")
        
        prev_button = ctk.CTkButton(
            paging_frame,
            text="< Anterior",
            fg_color="#E6E6E6",
            text_color="#333333",
            hover_color="#D0D0D0",
            height=30,
            width=100,
            corner_radius=8
        )
        prev_button.pack(side="left")
        
        page_label = ctk.CTkLabel(
            paging_frame,
            text="Página 1 de 5",
            font=self.small_font,
            text_color="#333333"
        )
        page_label.pack(side="left", padx=20)
        
        next_button = ctk.CTkButton(
            paging_frame,
            text="Próximo >",
            fg_color="#E6E6E6",
            text_color="#333333",
            hover_color="#D0D0D0",
            height=30,
            width=100,
            corner_radius=8
        )
        next_button.pack(side="left")
        
        # Resumo de dados
        info_frame = ctk.CTkFrame(
            paging_frame,
            fg_color="transparent"
        )
        info_frame.pack(side="right")
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="Total de Alunos: 45",
            font=self.small_font,
            text_color="#333333"
        )
        info_label.pack(side="right")
    
    def criar_botao_menu(self, texto, posicao, ativo=False):
        """Cria um botão no menu lateral"""
        fg_color = "#7B2CBF" if ativo else "transparent"
        botao = ctk.CTkButton(
            self.sidebar_frame,
            text=texto,
            fg_color=fg_color,
            text_color="white",
            hover_color="#7B2CBF",
            anchor="w",
            height=40,
            font=self.barlow_font,
            corner_radius=8,
            command=lambda t=texto: self.mudar_tela(t)
        )
        botao.pack(fill="x", padx=20, pady=5)
    
    def mudar_tela(self, tela):
        """Muda para a tela selecionada no menu"""
        nome_tela = tela.lower()
        if hasattr(self.controller, "mostrar_frame"):
            self.controller.mostrar_frame(nome_tela)
    
    def carregar_dados_exemplo(self):
        """Carrega dados de exemplo para a tabela"""
        # Limpar dados existentes
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Dados de exemplo
        dados = [
            ("Ana Silva", "(11) 99999-1234", "15/05/1990", "Rua das Flores, 123", "ana.silva@email.com", "01/01/2023", "Premium"),
            ("João Santos", "(11) 98888-5678", "22/08/1985", "Av. Principal, 456", "joao.santos@email.com", "15/02/2023", "Básico"),
            ("Maria Oliveira", "(11) 97777-9012", "10/12/1992", "Rua das Palmeiras, 789", "maria.oliveira@email.com", "05/03/2023", "Premium"),
            ("Pedro Souza", "(11) 96666-3456", "28/03/1988", "Av. Central, 321", "pedro.souza@email.com", "20/04/2023", "Intermediário"),
            ("Carla Lima", "(11) 95555-7890", "07/07/1995", "Rua dos Pinheiros, 654", "carla.lima@email.com", "10/05/2023", "Básico"),
            ("Marcos Pereira", "(11) 94444-1234", "14/10/1983", "Av. das Rosas, 987", "marcos.pereira@email.com", "25/06/2023", "Premium"),
            ("Juliana Costa", "(11) 93333-5678", "03/02/1991", "Rua das Acácias, 159", "juliana.costa@email.com", "15/07/2023", "Intermediário"),
            ("Lucas Martins", "(11) 92222-9012", "19/09/1987", "Av. dos Girassóis, 753", "lucas.martins@email.com", "01/08/2023", "Básico"),
        ]
        
        # Inserir dados na tabela
        for i, (nome, telefone, data_nasc, endereco, email, data_inicio, plano) in enumerate(dados):
            self.tree.insert("", "end", values=(nome, telefone, data_nasc, endereco, email, data_inicio, plano, "Editar / Excluir"))
    
    def filtrar_alunos(self, *args):
        """Filtra os alunos com base no texto de busca"""
        texto_busca = self.search_var.get().lower()
        
        # Se estiver vazio, recarregar todos os dados
        if not texto_busca:
            self.carregar_dados_exemplo()
            return
        
        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Carregar dados de exemplo para filtrar
        dados = [
            ("Ana Silva", "(11) 99999-1234", "15/05/1990", "Rua das Flores, 123", "ana.silva@email.com", "01/01/2023", "Premium"),
            ("João Santos", "(11) 98888-5678", "22/08/1985", "Av. Principal, 456", "joao.santos@email.com", "15/02/2023", "Básico"),
            ("Maria Oliveira", "(11) 97777-9012", "10/12/1992", "Rua das Palmeiras, 789", "maria.oliveira@email.com", "05/03/2023", "Premium"),
            ("Pedro Souza", "(11) 96666-3456", "28/03/1988", "Av. Central, 321", "pedro.souza@email.com", "20/04/2023", "Intermediário"),
            ("Carla Lima", "(11) 95555-7890", "07/07/1995", "Rua dos Pinheiros, 654", "carla.lima@email.com", "10/05/2023", "Básico"),
            ("Marcos Pereira", "(11) 94444-1234", "14/10/1983", "Av. das Rosas, 987", "marcos.pereira@email.com", "25/06/2023", "Premium"),
            ("Juliana Costa", "(11) 93333-5678", "03/02/1991", "Rua das Acácias, 159", "juliana.costa@email.com", "15/07/2023", "Intermediário"),
            ("Lucas Martins", "(11) 92222-9012", "19/09/1987", "Av. dos Girassóis, 753", "lucas.martins@email.com", "01/08/2023", "Básico"),
        ]
        
        # Filtrar e inserir dados
        for nome, telefone, data_nasc, endereco, email, data_inicio, plano in dados:
            if (texto_busca in nome.lower() or 
                texto_busca in email.lower() or 
                texto_busca in telefone.lower()):
                self.tree.insert("", "end", values=(nome, telefone, data_nasc, endereco, email, data_inicio, plano, "Editar / Excluir"))

    def abrir_novo_aluno(self):
        """Abre a janela para cadastrar novo aluno"""
        janela = ctk.CTkToplevel(self)
        janela.title("Novo Aluno")
        janela.geometry("600x650")
        janela.grab_set()  # Torna a janela modal
        
        # Criar formulário
        self.criar_formulario_aluno(janela)
    
    def editar_aluno(self, event):
        """Abre a janela para editar um aluno existente"""
        # Obter o item selecionado
        item = self.tree.identify_row(event.y)
        if not item:
            return
        
        # Obter os valores do item selecionado
        valores = self.tree.item(item, "values")
        
        janela = ctk.CTkToplevel(self)
        janela.title("Editar Aluno")
        janela.geometry("600x650")
        janela.grab_set()
        
        # Criar formulário preenchido
        self.criar_formulario_aluno(janela, valores)
    
    def criar_formulario_aluno(self, janela, valores=None):
        """Cria o formulário para cadastro/edição de aluno"""
        # Determinar se é edição ou novo cadastro
        modo_edicao = valores is not None
        titulo = "Editar Aluno" if modo_edicao else "Novo Aluno"
        
        # Frame principal
        main_frame = ctk.CTkFrame(janela, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo_label = ctk.CTkLabel(
            main_frame,
            text=titulo,
            font=self.title_font,
            text_color="#333333"
        )
        titulo_label.pack(pady=(20, 30))
        
        # Frame para os campos do formulário
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Definir campos
        campos = [
            {"label": "Nome:", "var": StringVar(value=valores[0] if modo_edicao else "")},
            {"label": "Telefone:", "var": StringVar(value=valores[1] if modo_edicao else "")},
            {"label": "Data de Nascimento:", "var": StringVar(value=valores[2] if modo_edicao else ""), "tipo": "data"},
            {"label": "Endereço:", "var": StringVar(value=valores[3] if modo_edicao else "")},
            {"label": "Email:", "var": StringVar(value=valores[4] if modo_edicao else "")},
            {"label": "Data de Início:", "var": StringVar(value=valores[5] if modo_edicao else ""), "tipo": "data"},
            {"label": "Plano:", "var": StringVar(value=valores[6] if modo_edicao else "Básico"), "tipo": "combobox", 
             "opcoes": ["Básico", "Intermediário", "Premium"]}
        ]
        
        # Criar campos do formulário
        for i, campo in enumerate(campos):
            frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            frame.pack(fill="x", pady=10)
            
            label = ctk.CTkLabel(
                frame,
                text=campo["label"],
                font=self.barlow_font,
                text_color="#333333",
                width=150,
                anchor="w"
            )
            label.pack(side="left")
            
            if campo.get("tipo") == "data":
                # Se tiver DateEntry disponível, usar ele
                try:
                    entry = DateEntry(
                        frame,
                        width=20,
                        background="#5A189A",
                        foreground="white",
                        date_pattern="dd/mm/yyyy"
                    )
                    try:
                        if modo_edicao and campo["var"].get():
                            dia, mes, ano = campo["var"].get().split("/")
                            entry.set_date(datetime.date(int(ano), int(mes), int(dia)))
                    except:
                        pass
                except:
                    # Fallback para entry normal
                    entry = ctk.CTkEntry(
                        frame,
                        textvariable=campo["var"],
                        width=400,
                        height=35,
                        corner_radius=8,
                        border_width=1
                    )
                    
            elif campo.get("tipo") == "combobox":
                entry = ctk.CTkComboBox(
                    frame,
                    values=campo["opcoes"],
                    variable=campo["var"],
                    width=400,
                    height=35,
                    corner_radius=8,
                    border_width=1
                )
            else:
                entry = ctk.CTkEntry(
                    frame,
                    textvariable=campo["var"],
                    width=400,
                    height=35,
                    corner_radius=8,
                    border_width=1
                )
            
            entry.pack(side="left", fill="x", expand=True)
        
        # Botões de ação
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)
        
        cancelar_btn = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            fg_color="#E6E6E6",
            text_color="#333333",
            hover_color="#D0D0D0",
            height=40,
            width=150,
            corner_radius=8,
            command=janela.destroy
        )
        cancelar_btn.pack(side="left", padx=(0, 10))
        
        salvar_btn = ctk.CTkButton(
            button_frame,
            text="Salvar",
            fg_color="#5A189A",
            hover_color="#7B2CBF",
            height=40,
            width=150,
            corner_radius=8,
            command=lambda: self.salvar_aluno(janela, campos, modo_edicao)
        )
        salvar_btn.pack(side="left")
    
    def salvar_aluno(self, janela, campos, modo_edicao):
        """Salva os dados do aluno e fecha a janela"""
        # Aqui você implementaria a lógica para salvar os dados
        # Por enquanto, apenas fechamos a janela
        janela.destroy()
        
        # Recarregar dados de exemplo (simulação)
        self.carregar_dados_exemplo()