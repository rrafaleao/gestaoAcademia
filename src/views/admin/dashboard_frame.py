import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class MainScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F0F0F0", corner_radius=0)
        
        self.controller = controller
        self.current_frame = None

        try:
            self.title_font = ctk.CTkFont(family="Barlow", size=24, weight="bold")
            self.sidebar_font = ctk.CTkFont(family="Barlow", size=16, weight="bold")
            self.content_font = ctk.CTkFont(family="Barlow", size=14)
        except Exception as e:
            print(f"Erro ao carregar a fonte 'Barlow': {e}")
            self.title_font = ("Arial", 24, "bold")
            self.sidebar_font = ("Arial", 16, "bold")
            self.content_font = ("Arial", 14)
        self.create_layout()

        self.mostrar_conteudo("dashboard")
    
    def create_layout(self):
        self.sidebar = self.create_sidebar()
        self.sidebar.pack(side="left", fill="y")
        
        self.content_area = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        self.content_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, fg_color="#5A189A", width=250, corner_radius=0)
        
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.pack(pady=20)
        
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="FITPRO",
            font=ctk.CTkFont(family="Barlow", size=28, weight="bold"),
            text_color="white"
        )
        logo_label.pack()
        
        slogan_label = ctk.CTkLabel(
            logo_frame,
            text="Sistema de Gestão",
            font=ctk.CTkFont(family="Barlow", size=12),
            text_color="white"
        )
        slogan_label.pack()

        separator = ctk.CTkFrame(sidebar, height=2, fg_color="#9D4EDD")
        separator.pack(fill="x", padx=20, pady=10)
        
        menu_items = [
            {"id": "dashboard", "text": "Dashboard", "icon": "dashboard.png"},
            {"id": "alunos", "text": "Alunos", "icon": "users.png"},
            {"id": "planos", "text": "Planos", "icon": "planos.png"},
            {"id": "aulas", "text": "Aulas", "icon": "aulas.png"},
            {"id": "financeiro", "text": "Financeiro", "icon": "financeiro.png"},
            {"id": "relatorios", "text": "Relatórios", "icon": "report.png"},
            {"id": "configuracoes", "text": "Configurações", "icon": "settings.png"}
        ]
        
        for item in menu_items:
            self.create_menu_item(sidebar, item)
        
        separator = ctk.CTkFrame(sidebar, height=2, fg_color="#9D4EDD")
        separator.pack(fill="x", padx=20, pady=10)
        
        user_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        user_frame.pack(pady=10, padx=20, fill="x")
        
        user_label = ctk.CTkLabel(
            user_frame,
            text="Bem-vindo,",
            font=self.content_font,
            text_color="white"
        )
        user_label.pack(anchor="w")
        
        user_name = ctk.CTkLabel(
            user_frame,
            text="Usuário",
            font=self.sidebar_font,
            text_color="white"
        )
        user_name.pack(anchor="w")
        
        logout_btn = ctk.CTkButton(
            sidebar,
            text="Sair",
            fg_color="#9D4EDD",
            hover_color="#7B2CBF",
            font=self.sidebar_font,
            width=200,
            height=40,
            corner_radius=10,
            command=self.logout
        )
        logout_btn.pack(pady=20, padx=20)
        
        return sidebar
    
    def create_menu_item(self, sidebar, item):
        item_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        item_frame.pack(pady=5, padx=20, fill="x")

        item_btn = ctk.CTkButton(
            item_frame,
            text=item["text"],
            fg_color="transparent",
            hover_color="#9D4EDD",
            text_color="white",
            anchor="w",
            font=self.sidebar_font,
            width=200,
            height=40,
            corner_radius=10,
            command=lambda i=item["id"]: self.mostrar_conteudo(i)
        )
        item_btn.pack(fill="x")
    
    def mostrar_conteudo(self, content_id):
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        content_title_map = {
            "dashboard": "Dashboard",
            "alunos": "Gestão de Alunos",
            "planos": "Planos e Mensalidades",
            "aulas": "Aulas e Atividades",
            "financeiro": "Controle Financeiro",
            "relatorios": "Relatórios",
            "configuracoes": "Configurações"
        }

        title_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        title_frame.pack(fill="x", pady=10)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text=content_title_map.get(content_id, "Conteúdo"),
            font=self.title_font,
            text_color="black"
        )
        title_label.pack(anchor="w")

        separator = ctk.CTkFrame(self.content_area, height=2, fg_color="#5A189A")
        separator.pack(fill="x", pady=10)

        if content_id == "dashboard":
            self.criar_dashboard()
        elif content_id == "alunos":
            self.criar_secao_alunos()
    
    def criar_dashboard(self):
        grid_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, pady=20)
        
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        cards_info = [
            {"title": "Total de Alunos", "value": "152", "color": "#9D4EDD"},
            {"title": "Mensalidades Pendentes", "value": "28", "color": "#E63946"},
            {"title": "Aulas Hoje", "value": "12", "color": "#457B9D"},
            {"title": "Novos Cadastros", "value": "7", "color": "#2A9D8F"}
        ]
        
        for i, card in enumerate(cards_info):
            row, col = divmod(i, 2)
            self.criar_card_resumo(grid_frame, card, row, col)
 
        recent_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        recent_frame.pack(fill="both", expand=True, pady=20)
        
        recent_label = ctk.CTkLabel(
            recent_frame,
            text="Atividades Recentes",
            font=self.sidebar_font,
            text_color="black"
        )
        recent_label.pack(anchor="w", pady=10)
        
        activities = [
            "João Silva fez check-in às 08:30",
            "Maria Oliveira pagou mensalidade de Fevereiro",
            "Nova aula de Spinning adicionada para Quarta-feira",
            "Carlos Santos cancelou agendamento de personal trainer",
            "Atualização no plano Trimestral"
        ]
        
        for activity in activities:
            activity_frame = ctk.CTkFrame(recent_frame, fg_color="#F8F9FA", corner_radius=5)
            activity_frame.pack(fill="x", pady=5)
            
            activity_label = ctk.CTkLabel(
                activity_frame,
                text=activity,
                font=self.content_font,
                text_color="black"
            )
            activity_label.pack(anchor="w", padx=10, pady=10)
    
    def criar_card_resumo(self, parent, card_info, row, col):
        card = ctk.CTkFrame(parent, fg_color=card_info["color"], corner_radius=10)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        value_label = ctk.CTkLabel(
            card,
            text=card_info["value"],
            font=ctk.CTkFont(family="Barlow", size=36, weight="bold"),
            text_color="white"
        )
        value_label.pack(pady=(20, 5))
        
        title_label = ctk.CTkLabel(
            card,
            text=card_info["title"],
            font=self.sidebar_font,
            text_color="white"
        )
        title_label.pack(pady=(5, 20))
    
    def criar_secao_alunos(self):
        self.form_visible = False
        self.table_visible = True

        actions_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        actions_frame.pack(fill="x", pady=10)

        search_entry = ctk.CTkEntry(
            actions_frame,
            placeholder_text="Buscar aluno...",
            width=300,
            height=40,
            fg_color="white",
            text_color="black",
            corner_radius=10,
            border_color="#5A189A",
            border_width=2
        )
        search_entry.pack(side="left", padx=5)
        
        search_btn = ctk.CTkButton(
            actions_frame,
            text="Buscar",
            fg_color="#5A189A",
            hover_color="#3C096C",
            width=100,
            height=40,
            font=self.content_font,
            corner_radius=10
        )
        search_btn.pack(side="left", padx=5)

        self.alunos_container = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.alunos_container.pack(fill="both", expand=True, pady=10)
        
        add_btn = ctk.CTkButton(
            actions_frame,
            text="Novo Aluno",
            fg_color="#2A9D8F",
            hover_color="#1F7A6F",
            width=150,
            height=40,
            font=self.content_font,
            corner_radius=10,
            command=self.toggle_form_aluno
        )
        add_btn.pack(side="right", padx=5)

        self.mostrar_tabela_alunos()
    
    def toggle_form_aluno(self):
        """Alterna entre a visualização do formulário e da tabela de alunos"""
        if self.form_visible:
            self.form_visible = False
            self.mostrar_tabela_alunos()
        else:
            self.form_visible = True
            self.mostrar_formulario_aluno()
    
    def mostrar_tabela_alunos(self):
        for widget in self.alunos_container.winfo_children():
            widget.destroy()
        
        table_frame = ctk.CTkFrame(self.alunos_container, fg_color="white", corner_radius=10, border_width=1, border_color="#E0E0E0")
        table_frame.pack(fill="both", expand=True)

        header_frame = ctk.CTkFrame(table_frame, fg_color="#F0F0F0", corner_radius=0)
        header_frame.pack(fill="x")
        
        headers = ["ID", "Nome", "Plano", "Vencimento", "Status", "Ações"]
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=self.sidebar_font,
                text_color="black",
                width=100
            )
            header_label.grid(row=0, column=i, padx=10, pady=10, sticky="w")
        
        alunos_exemplo = [
            {"id": "001", "nome": "João Silva", "plano": "Mensal", "vencimento": "15/03/2025", "status": "Ativo"},
            {"id": "002", "nome": "Maria Oliveira", "plano": "Trimestral", "vencimento": "22/04/2025", "status": "Ativo"},
            {"id": "003", "nome": "Carlos Santos", "plano": "Anual", "vencimento": "05/01/2026", "status": "Inativo"},
            {"id": "004", "nome": "Ana Pereira", "plano": "Mensal", "vencimento": "10/03/2025", "status": "Pendente"},
            {"id": "005", "nome": "Lucas Mendes", "plano": "Semestral", "vencimento": "30/07/2025", "status": "Ativo"}
        ]
        
        for row_idx, aluno in enumerate(alunos_exemplo, start=1):
            row_bg = "#FFFFFF" if row_idx % 2 == 0 else "#F8F9FA"
            row_frame = ctk.CTkFrame(table_frame, fg_color=row_bg, corner_radius=0, height=40)
            row_frame.pack(fill="x")

            status_color = {
                "Ativo": "#4CAF50",
                "Inativo": "#F44336",
                "Pendente": "#FFC107"
            }.get(aluno["status"], "#757575")

            ctk.CTkLabel(row_frame, text=aluno["id"], text_color="black", width=100).grid(row=0, column=0, padx=10, pady=10, sticky="w")
            ctk.CTkLabel(row_frame, text=aluno["nome"], text_color="black", width=100).grid(row=0, column=1, padx=10, pady=10, sticky="w")
            ctk.CTkLabel(row_frame, text=aluno["plano"], text_color="black", width=100).grid(row=0, column=2, padx=10, pady=10, sticky="w")
            ctk.CTkLabel(row_frame, text=aluno["vencimento"], text_color="black", width=100).grid(row=0, column=3, padx=10, pady=10, sticky="w")
            
            status_frame = ctk.CTkFrame(row_frame, fg_color=status_color, corner_radius=5, width=80, height=25)
            status_frame.grid(row=0, column=4, padx=10, pady=10)
            ctk.CTkLabel(status_frame, text=aluno["status"], text_color="white", font=("Arial", 12)).pack(pady=2)
            
            actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            actions_frame.grid(row=0, column=5, padx=10, pady=5)
            
            edit_btn = ctk.CTkButton(
                actions_frame,
                text="Editar",
                fg_color="#5A189A",
                hover_color="#3C096C",
                width=70,
                height=30,
                font=("Arial", 12),
                corner_radius=5
            )
            edit_btn.pack(side="left", padx=2)
            
            del_btn = ctk.CTkButton(
                actions_frame,
                text="Excluir",
                fg_color="#E63946",
                hover_color="#C1121F",
                width=70,
                height=30,
                font=("Arial", 12),
                corner_radius=5
            )
            del_btn.pack(side="left", padx=2)
    
    def mostrar_formulario_aluno(self):
        for widget in self.alunos_container.winfo_children():
            widget.destroy()
        
        form_frame = ctk.CTkFrame(self.alunos_container, fg_color="white", corner_radius=10, border_width=1, border_color="#E0E0E0")
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        form_title = ctk.CTkLabel(
            form_frame,
            text="Cadastro de Novo Aluno",
            font=self.sidebar_font,
            text_color="#5A189A"
        )
        form_title.pack(pady=20)
        
        fields_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_container.pack(fill="both", expand=True, padx=30, pady=10)

        fields_container.columnconfigure(0, weight=1)
        fields_container.columnconfigure(1, weight=1)
        
        self.criar_campo_formulario(fields_container, 0, 0, "Nome Completo:", "nome")
        self.criar_campo_formulario(fields_container, 0, 1, "Telefone:", "telefone", placeholder="(00) 00000-0000")
        self.criar_campo_formulario(fields_container, 1, 0, "E-mail:", "email", placeholder="exemplo@email.com")
        self.criar_campo_formulario(fields_container, 1, 1, "Endereço:", "endereco")
        self.criar_campo_formulario(fields_container, 2, 0, "Data de Nascimento:", "data_nascimento", placeholder="DD/MM/AAAA")
        self.criar_campo_formulario(fields_container, 2, 1, "Data de Início:", "data_inicio", placeholder="DD/MM/AAAA", default=datetime.now().strftime("%d/%m/%Y"))
        
        plano_frame = ctk.CTkFrame(fields_container, fg_color="transparent")
        plano_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=(20, 10))
        
        plano_label = ctk.CTkLabel(
            plano_frame,
            text="Plano:",
            font=self.content_font,
            text_color="black"
        )
        plano_label.pack(anchor="w", pady=(0, 5))
        
        planos_opcoes = ["Mensal", "Trimestral", "Semestral", "Anual"]
        self.plano_var = ctk.StringVar(value=planos_opcoes[0])  # Guardando a referência como atributo da classe
        
        planos_container = ctk.CTkFrame(plano_frame, fg_color="transparent")
        planos_container.pack(fill="x")
        
        for i, plano in enumerate(planos_opcoes):
            radio = ctk.CTkRadioButton(
                planos_container,
                text=plano,
                variable=self.plano_var,
                value=plano,
                font=self.content_font,
                fg_color="#5A189A",
                hover_color="#3C096C"
            )
            radio.pack(side="left", padx=20)
        
        # Botões de ação
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=30, padx=30)
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            fg_color="#E0E0E0",
            hover_color="#BDBDBD",
            text_color="black",
            width=150,
            height=40,
            font=self.content_font,
            corner_radius=10,
            command=self.toggle_form_aluno
        )
        cancel_btn.pack(side="left", padx=5)
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Salvar",
            fg_color="#2A9D8F",
            hover_color="#1F7A6F",
            width=150,
            height=40,
            font=self.content_font,
            corner_radius=10,
            command=self.salvar_aluno
        )
        save_btn.pack(side="right", padx=5)
    
    def criar_campo_formulario(self, parent, row, col, label_text, field_name, placeholder="", default=""):
        """Cria um campo de formulário com label e entrada"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.grid(row=row, column=col, sticky="ew", padx=10, pady=10)
        
        label = ctk.CTkLabel(
            field_frame,
            text=label_text,
            font=self.content_font,
            text_color="black"
        )
        label.pack(anchor="w", pady=(0, 5))
        
        entry = ctk.CTkEntry(
            field_frame,
            placeholder_text=placeholder,
            width=300,
            height=40,
            fg_color="white",
            text_color="black",
            corner_radius=5,
            border_color="#5A189A",
            border_width=1
        )
        if default:
            entry.insert(0, default)
        entry.pack(fill="x")
        
        setattr(self, f"entry_{field_name}", entry)
    
    def salvar_aluno(self):
        """
        Coleta os dados do formulário e salva o novo aluno no banco de dados
        utilizando o AdminController.
        """
        # Obter todos os dados do formulário
        campos = ["nome", "telefone", "email", "endereco", "data_nascimento", "data_inicio"]
        cliente_data = {}
        
        # Verificar se todos os campos obrigatórios foram preenchidos
        campos_vazios = []
        for campo in campos:
            entry = getattr(self, f"entry_{campo}")
            valor = entry.get().strip()
            
            if not valor and campo != "email":  # Email pode ser opcional
                campos_vazios.append(campo)
            
            cliente_data[campo] = valor
        
        # Obter o plano selecionado
        cliente_data["plano"] = self.plano_var.get()
        
        # Validar se há campos obrigatórios vazios
        if campos_vazios:
            campos_formatados = ", ".join(campos_vazios).replace("_", " ")
            messagebox.showerror("Erro", f"Os seguintes campos são obrigatórios: {campos_formatados}")
            return
        
        # Formatar as datas para o formato SQL
        for campo_data in ["data_nascimento", "data_inicio"]:
            data_formatada = self.controller.admin_controller.formatar_data_para_sql(cliente_data[campo_data])
            if not data_formatada:
                messagebox.showerror("Erro", f"Formato de data inválido em {campo_data.replace('_', ' ')}. Use DD/MM/AAAA.")
                return
            cliente_data[campo_data] = data_formatada
        
        # Salvar no banco de dados utilizando o AdminController
        sucesso = self.controller.admin_controller.adicionar_cliente(cliente_data)
        
        if sucesso:
            messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
            self.toggle_form_aluno()  # Voltar para a tabela de alunos
        else:
            messagebox.showerror("Erro", "Não foi possível cadastrar o aluno. Verifique os dados e tente novamente.")
    
    def atualizar_tabela_alunos(self):
        """
        Atualiza a tabela de alunos com os dados mais recentes do banco de dados.
        """
        # Limpar a tabela atual
        for widget in self.alunos_container.winfo_children():
            widget.destroy()
        
        # Recriar o frame da tabela
        table_frame = ctk.CTkFrame(self.alunos_container, fg_color="white", corner_radius=10, border_width=1, border_color="#E0E0E0")
        table_frame.pack(fill="both", expand=True)

        header_frame = ctk.CTkFrame(table_frame, fg_color="#F0F0F0", corner_radius=0)
        header_frame.pack(fill="x")
        
        headers = ["ID", "Nome", "Plano", "Vencimento", "Status", "Ações"]
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=self.sidebar_font,
                text_color="black",
                width=100
            )
            header_label.grid(row=0, column=i, padx=10, pady=10, sticky="w")
        
        # Obter todos os clientes do banco de dados usando o AdminController
        alunos = self.controller.admin_controller.obter_todos_clientes()
        
        # Se não houver alunos, mostrar mensagem
        if not alunos:
            no_data_frame = ctk.CTkFrame(table_frame, fg_color="#F8F9FA", corner_radius=0)
            no_data_frame.pack(fill="x")
            
            no_data_label = ctk.CTkLabel(
                no_data_frame,
                text="Nenhum aluno cadastrado.",
                font=self.content_font,
                text_color="#757575"
            )
            no_data_label.pack(pady=30)
            return
        
        # Preencher a tabela com os dados dos alunos
        for row_idx, aluno in enumerate(alunos, start=1):
            row_bg = "#FFFFFF" if row_idx % 2 == 0 else "#F8F9FA"
            row_frame = ctk.CTkFrame(table_frame, fg_color=row_bg, corner_radius=0, height=40)
            row_frame.pack(fill="x")
            
            # Determinar status com base em alguma lógica (por exemplo, data de vencimento)
            hoje = datetime.now().date()
            data_inicio = datetime.strptime(str(aluno["data_inicio"]), "%Y-%m-%d").date()
            status = "Ativo"  # Por padrão, consideramos o aluno como ativo
            
            # Definir cor do status
            status_color = {
                "Ativo": "#4CAF50",
                "Inativo": "#F44336",
                "Pendente": "#FFC107"
            }.get(status, "#757575")
            
            # Calcular data de vencimento com base no plano e data de início
            vencimento = self.calcular_vencimento(data_inicio, aluno["plano"])
            
            # Mostrar os dados do aluno na tabela
            ctk.CTkLabel(row_frame, text=str(aluno["id"]), text_color="black", width=100).grid(row=0, column=0, padx=10, pady=10, sticky="w")
            ctk.CTkLabel(row_frame, text=aluno["nome"], text_color="black", width=100).grid(row=0, column=1, padx=10, pady=10, sticky="w")
            ctk.CTkLabel(row_frame, text=aluno["plano"], text_color="black", width=100).grid(row=0, column=2, padx=10, pady=10, sticky="w")
            ctk.CTkLabel(row_frame, text=vencimento.strftime("%d/%m/%Y"), text_color="black", width=100).grid(row=0, column=3, padx=10, pady=10, sticky="w")
            
            status_frame = ctk.CTkFrame(row_frame, fg_color=status_color, corner_radius=5, width=80, height=25)
            status_frame.grid(row=0, column=4, padx=10, pady=10)
            ctk.CTkLabel(status_frame, text=status, text_color="white", font=("Arial", 12)).pack(pady=2)
            
            # Botões de ação
            actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            actions_frame.grid(row=0, column=5, padx=10, pady=5)
            
            edit_btn = ctk.CTkButton(
                actions_frame,
                text="Editar",
                fg_color="#5A189A",
                hover_color="#3C096C",
                width=70,
                height=30,
                font=("Arial", 12),
                corner_radius=5,
                command=lambda aluno_id=aluno["id"]: self.editar_aluno(aluno_id)
            )
            edit_btn.pack(side="left", padx=2)
            
            del_btn = ctk.CTkButton(
                actions_frame,
                text="Excluir",
                fg_color="#E63946",
                hover_color="#C1121F",
                width=70,
                height=30,
                font=("Arial", 12),
                corner_radius=5,
                command=lambda aluno_id=aluno["id"]: self.excluir_aluno(aluno_id)
            )
            del_btn.pack(side="left", padx=2)

    def calcular_vencimento(self, data_inicio, plano):
        """
        Calcula a data de vencimento com base na data de início e no plano.
        
        Args:
            data_inicio (datetime.date): Data de início do plano
            plano (str): Tipo de plano (Mensal, Trimestral, Semestral, Anual)
        
        Returns:
            datetime.date: Data de vencimento
        """
        
        if plano == "Mensal":
            return data_inicio + relativedelta(months=1)
        elif plano == "Trimestral":
            return data_inicio + relativedelta(months=3)
        elif plano == "Semestral":
            return data_inicio + relativedelta(months=6)
        elif plano == "Anual":
            return data_inicio + relativedelta(years=1)
        else:
            return data_inicio + relativedelta(months=1)  # Padrão: mensal
        
    
    def buscar_cliente_por_id(self, cliente_id):
        """
        Busca um cliente pelo ID.
        
        Args:
            cliente_id (int): ID do cliente a ser buscado.
        
        Returns:
            list: Lista contendo um dicionário com os dados do cliente, ou lista vazia se não encontrado.
        """
        query = "SELECT * FROM clientes WHERE id = %s"
        resultados = self.db.executar_consulta(query, (cliente_id,))
        
        if resultados:
            colunas = ['id', 'nome', 'telefone', 'email', 'endereco', 'data_nascimento', 'data_inicio', 'plano']
            clientes = [dict(zip(colunas, cliente)) for cliente in resultados]
            return clientes
        return []

    def logout(self):
        """Realiza o logout do usuário"""
        if messagebox.askyesno("Logout", "Deseja realmente sair?"):
            self.controller.mostrar_frame("login")