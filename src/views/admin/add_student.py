import customtkinter as ctk
from tkinter import ttk, messagebox

class MembersFrame(ctk.CTkFrame):
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
        self.criar_botao_menu("Membros", 1, True)  # "Membros" é marcado como ativo nesta tela
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
        
        # Área de conteúdo principal
        self.content_frame = ctk.CTkFrame(
            self,
            fg_color="#F0F0F0",
            corner_radius=0
        )
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        # Cabeçalho da área de conteúdo
        header_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        # Título da página
        page_title = ctk.CTkLabel(
            header_frame,
            text="Membros",
            font=self.title_font,
            text_color="black"
        )
        page_title.pack(side="left")
        
        # Botão Adicionar Novo Membro
        add_button = ctk.CTkButton(
            header_frame,
            text="+ Adicionar Membro",
            fg_color="#5A189A",
            hover_color="#7B2CBF",
            height=40,
            width=150,
            corner_radius=8,
            font=self.small_font,
            command=self.adicionar_membro
        )
        add_button.pack(side="right")
        
        # Frame principal da tabela
        table_container = ctk.CTkFrame(
            self.content_frame,
            fg_color="white",
            corner_radius=15
        )
        table_container.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        
        # Frame para filtros e pesquisa acima da tabela
        filter_frame = ctk.CTkFrame(
            table_container,
            fg_color="transparent"
        )
        filter_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Campo de pesquisa
        self.search_var = ctk.StringVar()
        search_field = ctk.CTkEntry(
            filter_frame,
            placeholder_text="Buscar membro...",
            width=250,
            height=35,
            font=self.small_font,
            textvariable=self.search_var
        )
        search_field.pack(side="left")
        
        search_button = ctk.CTkButton(
            filter_frame,
            text="Buscar",
            fg_color="#5A189A",
            hover_color="#7B2CBF",
            height=35,
            width=100,
            corner_radius=8,
            font=self.small_font,
            command=self.buscar_membro
        )
        search_button.pack(side="left", padx=10)
        
        # Filtro por status
        status_label = ctk.CTkLabel(
            filter_frame,
            text="Status:",
            font=self.small_font,
            text_color="black"
        )
        status_label.pack(side="left", padx=(20, 5))
        
        self.status_var = ctk.StringVar(value="Todos")
        status_combobox = ctk.CTkComboBox(
            filter_frame,
            values=["Todos", "Ativo", "Inativo", "Pendente"],
            variable=self.status_var,
            width=150,
            height=35,
            font=self.small_font,
            dropdown_font=self.small_font
        )
        status_combobox.pack(side="left")
        
        # Frame para a tabela
        table_frame = ctk.CTkFrame(
            table_container,
            fg_color="transparent"
        )
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Configuração da tabela
        style = ttk.Style()
        style.configure("Treeview", 
                        background="#FFFFFF", 
                        foreground="black", 
                        rowheight=35, 
                        fieldbackground="#FFFFFF")
        style.map('Treeview', background=[('selected', '#9D4EDD')])
        style.configure("Treeview.Heading", 
                        font=('Arial', 12, 'bold'),
                        background="#F0F0F0", 
                        foreground="black")
        
        # Criação da tabela
        self.tabela = ttk.Treeview(
            table_frame,
            columns=("id", "nome", "email", "telefone", "plano", "status"),
            show="headings",
            selectmode="browse"
        )
        
        # Definição das colunas
        self.tabela.heading("id", text="ID")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("email", text="E-mail")
        self.tabela.heading("telefone", text="Telefone")
        self.tabela.heading("plano", text="Plano")
        self.tabela.heading("status", text="Status")
        
        # Configuração da largura das colunas
        self.tabela.column("id", width=60, anchor="center")
        self.tabela.column("nome", width=200)
        self.tabela.column("email", width=200)
        self.tabela.column("telefone", width=150)
        self.tabela.column("plano", width=150)
        self.tabela.column("status", width=100, anchor="center")
        
        # Scroll vertical
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tabela.pack(side="left", fill="both", expand=True)
        
        # Adicionando dados de exemplo
        self.carregar_dados_exemplo()
        
        # Frame para os botões de ação
        action_frame = ctk.CTkFrame(
            table_container,
            fg_color="transparent"
        )
        action_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Botões de ação
        edit_button = ctk.CTkButton(
            action_frame,
            text="Editar",
            fg_color="#7B2CBF",
            hover_color="#5A189A",
            height=35,
            width=120,
            corner_radius=8,
            font=self.small_font,
            command=self.editar_membro
        )
        edit_button.pack(side="left", padx=(0, 10))
        
        delete_button = ctk.CTkButton(
            action_frame,
            text="Remover",
            fg_color="#E63946",
            hover_color="#C1121F",
            height=35,
            width=120,
            corner_radius=8,
            font=self.small_font,
            command=self.remover_membro
        )
        delete_button.pack(side="left")
        
        # Estatísticas de membros
        stats_frame = ctk.CTkFrame(
            action_frame,
            fg_color="transparent"
        )
        stats_frame.pack(side="right")
        
        total_stats = ctk.CTkLabel(
            stats_frame,
            text="Total: 342 membros | Ativos: 298 | Inativos: 44",
            font=self.small_font,
            text_color="gray"
        )
        total_stats.pack()
    
    def criar_botao_menu(self, texto, indice, ativo=False):
        """Cria um botão na sidebar com estilização adequada"""
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
    
    def navegacao_menu(self, texto):
        """Função para navegar entre as telas do menu"""
        # Se o botão clicado for diferente da tela atual, navegar para a tela correspondente
        if texto == "Dashboard" and self.controller:
            self.controller.mostrar_frame("dashboard")
        elif texto == "Membros" and self.controller:
            self.controller.mostrar_frame("members")
        elif texto == "Planos" and self.controller:
            print(f"Navegando para: {texto}")
            # self.controller.mostrar_frame("plans")
        elif texto == "Pagamentos" and self.controller:
            print(f"Navegando para: {texto}")
            # self.controller.mostrar_frame("payments")
        elif texto == "Agenda" and self.controller:
            print(f"Navegando para: {texto}")
            # self.controller.mostrar_frame("schedule")
        elif texto == "Funcionários" and self.controller:
            print(f"Navegando para: {texto}")
            # self.controller.mostrar_frame("employees")
        elif texto == "Relatórios" and self.controller:
            print(f"Navegando para: {texto}")
            # self.controller.mostrar_frame("reports")
        elif texto == "Configurações" and self.controller:
            print(f"Navegando para: {texto}")
            # self.controller.mostrar_frame("settings")
    
    def carregar_dados_exemplo(self):
        """Carrega dados de exemplo na tabela"""
        # Limpar dados existentes
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        
        # Adicionar dados de exemplo
        dados = [
            (1, "João Silva", "joao.silva@email.com", "(11) 98765-4321", "Premium", "Ativo"),
            (2, "Maria Santos", "maria.santos@email.com", "(11) 97654-3210", "Básico", "Ativo"),
            (3, "Pedro Almeida", "pedro.almeida@email.com", "(11) 96543-2109", "Standard", "Ativo"),
            (4, "Ana Oliveira", "ana.oliveira@email.com", "(11) 95432-1098", "Premium", "Inativo"),
            (5, "Carlos Souza", "carlos.souza@email.com", "(11) 94321-0987", "Standard", "Ativo"),
            (6, "Juliana Lima", "juliana.lima@email.com", "(11) 93210-9876", "Premium", "Ativo"),
            (7, "Roberto Pereira", "roberto.pereira@email.com", "(11) 92109-8765", "Básico", "Pendente"),
            (8, "Fernanda Costa", "fernanda.costa@email.com", "(11) 91098-7654", "Premium", "Ativo"),
            (9, "Lucas Martins", "lucas.martins@email.com", "(11) 90987-6543", "Standard", "Inativo"),
            (10, "Mariana Gomes", "mariana.gomes@email.com", "(11) 99876-5432", "Básico", "Ativo"),
            (11, "Ricardo Ferreira", "ricardo.ferreira@email.com", "(11) 98765-4321", "Premium", "Ativo"),
            (12, "Camila Rodrigues", "camila.rodrigues@email.com", "(11) 97654-3210", "Standard", "Ativo"),
            (13, "Bruno Santos", "bruno.santos@email.com", "(11) 96543-2109", "Básico", "Pendente"),
            (14, "Patrícia Alves", "patricia.alves@email.com", "(11) 95432-1098", "Premium", "Ativo"),
            (15, "Alexandre Lopes", "alexandre.lopes@email.com", "(11) 94321-0987", "Standard", "Inativo"),
        ]
        
        for dado in dados:
            self.tabela.insert("", "end", values=dado)
    
    def adicionar_membro(self):
        """Abre a janela para adicionar um novo membro"""
        self.abrir_janela_membro()
    
    def editar_membro(self):
        """Edita o membro selecionado na tabela"""
        # Verificar se um item está selecionado
        item_selecionado = self.tabela.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um membro para editar.")
            return
        
        # Obter dados do item selecionado
        item = self.tabela.item(item_selecionado)
        dados = item['values']
        
        # Abrir janela de edição com os dados preenchidos
        self.abrir_janela_membro(modo_edicao=True, dados=dados)
    
    def remover_membro(self):
        """Remove o membro selecionado na tabela"""
        # Verificar se um item está selecionado
        item_selecionado = self.tabela.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um membro para remover.")
            return
        
        # Confirmar remoção
        item = self.tabela.item(item_selecionado)
        dados = item['values']
        nome = dados[1]
        
        confirmacao = messagebox.askyesno("Confirmar Remoção", f"Deseja realmente remover o membro {nome}?")
        if confirmacao:
            self.tabela.delete(item_selecionado)
            messagebox.showinfo("Sucesso", f"Membro {nome} removido com sucesso.")
    
    def buscar_membro(self):
        """Busca membros com base no texto pesquisado"""
        texto_busca = self.search_var.get().lower()
        status_filtro = self.status_var.get()
        
        # Limpar tabela atual
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        
        # Recarregar dados de exemplo para fazer a busca
        dados = [
            (1, "João Silva", "joao.silva@email.com", "(11) 98765-4321", "Premium", "Ativo"),
            (2, "Maria Santos", "maria.santos@email.com", "(11) 97654-3210", "Básico", "Ativo"),
            (3, "Pedro Almeida", "pedro.almeida@email.com", "(11) 96543-2109", "Standard", "Ativo"),
            (4, "Ana Oliveira", "ana.oliveira@email.com", "(11) 95432-1098", "Premium", "Inativo"),
            (5, "Carlos Souza", "carlos.souza@email.com", "(11) 94321-0987", "Standard", "Ativo"),
            (6, "Juliana Lima", "juliana.lima@email.com", "(11) 93210-9876", "Premium", "Ativo"),
            (7, "Roberto Pereira", "roberto.pereira@email.com", "(11) 92109-8765", "Básico", "Pendente"),
            (8, "Fernanda Costa", "fernanda.costa@email.com", "(11) 91098-7654", "Premium", "Ativo"),
            (9, "Lucas Martins", "lucas.martins@email.com", "(11) 90987-6543", "Standard", "Inativo"),
            (10, "Mariana Gomes", "mariana.gomes@email.com", "(11) 99876-5432", "Básico", "Ativo"),
            (11, "Ricardo Ferreira", "ricardo.ferreira@email.com", "(11) 98765-4321", "Premium", "Ativo"),
            (12, "Camila Rodrigues", "camila.rodrigues@email.com", "(11) 97654-3210", "Standard", "Ativo"),
            (13, "Bruno Santos", "bruno.santos@email.com", "(11) 96543-2109", "Básico", "Pendente"),
            (14, "Patrícia Alves", "patricia.alves@email.com", "(11) 95432-1098", "Premium", "Ativo"),
            (15, "Alexandre Lopes", "alexandre.lopes@email.com", "(11) 94321-0987", "Standard", "Inativo"),
        ]
        
        # Filtrar dados
        for dado in dados:
            # Verificar se o texto de busca está presente em algum campo do membro
            texto_presente = any(texto_busca in str(campo).lower() for campo in dado)
            
            # Verificar filtro de status
            status_ok = status_filtro == "Todos" or status_filtro == dado[5]
            
            # Se passar nos filtros, adicionar à tabela
            if texto_presente and status_ok:
                self.tabela.insert("", "end", values=dado)
    
    def abrir_janela_membro(self, modo_edicao=False, dados=None):
        """Abre uma janela para adicionar ou editar um membro"""
        janela = ctk.CTkToplevel(self)
        janela.title("Editar Membro" if modo_edicao else "Novo Membro")
        janela.geometry("500x550")
        janela.resizable(False, False)
        janela.grab_set()  # Torna a janela modal
        janela.focus_set()
        
        # Frame principal
        frame_principal = ctk.CTkFrame(janela, fg_color="transparent")
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(
            frame_principal,
            text="Editar Membro" if modo_edicao else "Adicionar Novo Membro",
            font=self.title_font,
            text_color="black"
        )
        titulo.pack(pady=(0, 20))
        
        # Campos
        campos_frame = ctk.CTkFrame(frame_principal, fg_color="transparent")
        campos_frame.pack(fill="both", expand=True)
        
        # Função para criar campos de formulário
        def criar_campo(label_texto, valor_padrao="", linha=0):
            label = ctk.CTkLabel(
                campos_frame,
                text=label_texto,
                font=self.small_font,
                text_color="black"
            )
            label.grid(row=linha, column=0, sticky="w", pady=(10, 5))
            
            entry = ctk.CTkEntry(
                campos_frame,
                height=35,
                width=400,
                font=self.small_font
            )
            entry.grid(row=linha+1, column=0, sticky="ew", pady=(0, 10))
            
            if valor_padrao:
                entry.insert(0, valor_padrao)
                
            return entry
        
        # Campos do formulário
        nome_entry = criar_campo("Nome completo:", dados[1] if dados else "", 0)
        email_entry = criar_campo("E-mail:", dados[2] if dados else "", 2)
        telefone_entry = criar_campo("Telefone:", dados[3] if dados else "", 4)
        
        # Seleção de plano
        plano_label = ctk.CTkLabel(
            campos_frame,
            text="Plano:",
            font=self.small_font,
            text_color="black"
        )
        plano_label.grid(row=6, column=0, sticky="w", pady=(10, 5))
        
        plano_var = ctk.StringVar(value=dados[4] if dados else "Básico")
        plano_combobox = ctk.CTkComboBox(
            campos_frame,
            values=["Básico", "Standard", "Premium"],
            variable=plano_var,
            width=400,
            height=35,
            font=self.small_font,
            dropdown_font=self.small_font
        )
        plano_combobox.grid(row=7, column=0, sticky="ew", pady=(0, 10))
        
        # Seleção de status
        status_label = ctk.CTkLabel(
            campos_frame,
            text="Status:",
            font=self.small_font,
            text_color="black"
        )
        status_label.grid(row=8, column=0, sticky="w", pady=(10, 5))
        
        status_var = ctk.StringVar(value=dados[5] if dados else "Ativo")
        status_frame = ctk.CTkFrame(campos_frame, fg_color="transparent")
        status_frame.grid(row=9, column=0, sticky="ew", pady=(0, 10))
        
        # Opções de status como radiobuttons
        status_ativo = ctk.CTkRadioButton(
            status_frame,
            text="Ativo",
            variable=status_var,
            value="Ativo",
            font=self.small_font,
            fg_color="#5A189A"
        )
        status_ativo.pack(side="left", padx=(0, 20))
        
        status_inativo = ctk.CTkRadioButton(
            status_frame,
            text="Inativo",
            variable=status_var,
            value="Inativo",
            font=self.small_font,
            fg_color="#5A189A"
        )
        status_inativo.pack(side="left", padx=(0, 20))
        
        status_pendente = ctk.CTkRadioButton(
            status_frame,
            text="Pendente",
            variable=status_var,
            value="Pendente",
            font=self.small_font,
            fg_color="#5A189A"
        )
        status_pendente.pack(side="left")
        
        # Botões de ação
        botoes_frame = ctk.CTkFrame(frame_principal, fg_color="transparent")
        botoes_frame.pack(fill="x", pady=(20, 0))
        
        # Função para salvar o membro
        def salvar_membro():
            # Aqui você implementaria a lógica para salvar os dados
            # Por simplicidade, vamos apenas mostrar uma mensagem
            if modo_edicao:
                messagebox.showinfo("Sucesso", f"Membro {nome_entry.get()} atualizado com sucesso!")
            else:
                messagebox.showinfo("Sucesso", f"Membro {nome_entry.get()} adicionado com sucesso!")
            janela.destroy()
        
        cancelar_button = ctk.CTkButton(
            botoes_frame,
            text="Cancelar",
            fg_color="#E0E0E0",
            text_color="black",
            hover_color="#C0C0C0",
            height=40,
            width=180,
            corner_radius=8,
            font=self.small_font,
            command=janela.destroy
        )
        cancelar_button.pack(side="left", padx=(0, 10))
        
        salvar_button = ctk.CTkButton(
            botoes_frame,
            text="Salvar",
            fg_color="#5A189A",
            hover_color="#7B2CBF",
            height=40,
            width=180,
            corner_radius=8,
            font=self.small_font,
            command=salvar_membro
        )
        salvar_button.pack(side="left")