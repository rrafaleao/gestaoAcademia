# controller/user_controller.py
class UserController:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def adicionar_usuario(self, nome, email, senha, nivel_acesso="funcionario"):
        """
        Adiciona um novo usuário ao banco de dados.
        
        Args:
            nome (str): Nome completo do usuário
            email (str): Email do usuário (será usado como login)
            senha (str): Senha do usuário
            nivel_acesso (str, opcional): Nível de acesso do usuário (admin ou funcionario). Padrão é "funcionario"
        
        Returns:
            bool: True se o usuário foi adicionado com sucesso, False caso contrário
            str: Mensagem de sucesso ou erro
        """
        try:
            # Verifica se o email já está cadastrado
            query_verificacao = "SELECT COUNT(*) FROM usuarios WHERE email = %s"
            resultado = self.db_manager.executar_consulta(query_verificacao, (email,))
            
            if resultado and resultado[0][0] > 0:
                return False, "Email já cadastrado no sistema"
            
            # Valida o nível de acesso (conforme a constraint CHECK no banco)
            if nivel_acesso not in ["admin", "funcionario"]:
                nivel_acesso = "funcionario"  # Define como padrão se valor inválido
            
            # SQL para inserção de usuário
            query = """
            INSERT INTO usuarios (nome, email, senha, nivel_acesso) 
            VALUES (%s, %s, %s, %s)
            """
            
            # Executa a query
            self.db_manager.executar_comando(query, (nome, email, senha, nivel_acesso))
            
            return True, "Usuário cadastrado com sucesso"
        
        except Exception as e:
            return False, f"Erro ao cadastrar usuário: {str(e)}"
    
    def verificar_credenciais(self, email, senha):
        """
        Verifica as credenciais do usuário para login.
        
        Args:
            email (str): Email do usuário
            senha (str): Senha do usuário
        
        Returns:
            tuple: (sucesso, mensagem, dados_usuario)
                - sucesso (bool): True se as credenciais são válidas
                - mensagem (str): Mensagem de sucesso ou erro
                - dados_usuario (dict): Dados do usuário ou None
        """
        try:
            query = """
            SELECT id_usuario, nome, email, nivel_acesso 
            FROM usuarios 
            WHERE email = %s AND senha = %s
            """
            
            resultado = self.db_manager.executar_consulta(query, (email, senha))
            
            if resultado and len(resultado) > 0:
                usuario = {
                    "id": resultado[0][0],
                    "nome": resultado[0][1],
                    "email": resultado[0][2],
                    "nivel_acesso": resultado[0][3]
                }
                return True, "Login bem-sucedido", usuario
            else:
                return False, "Email ou senha incorretos", None
                
        except Exception as e:
            return False, f"Erro ao verificar credenciais: {str(e)}", None