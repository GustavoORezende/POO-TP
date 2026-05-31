import customtkinter as ctk
from Models.models import User, Post
from Database.database import BancoDeDados, Feed

class AppRedeSocial(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configurações da Janela
        self.title("Mini Rede Social")
        self.geometry("400x550")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.usuario_atual = None
        # O aplicativo agora começa na tela de Login!
        self.telaLogin()

    def limparTela(self):
        """Remove todos os widgets da tela para transição de frames."""
        for widget in self.winfo_children():
            widget.destroy()

    # ==========================================
    # TELA DE LOGIN
    # ==========================================
    def telaLogin(self):
        self.limparTela()
        self.geometry("400x550")

        titulo = ctk.CTkLabel(self, text="Login", font=("Arial", 24, "bold"))
        titulo.pack(pady=(60, 20))

        self.entry_email_login = ctk.CTkEntry(self, placeholder_text="E-mail", width=250)
        self.entry_email_login.pack(pady=10)

        self.entry_senha_login = ctk.CTkEntry(self, placeholder_text="Senha", show="*", width=250)
        self.entry_senha_login.pack(pady=10)

        self.lbl_mensagem_login = ctk.CTkLabel(self, text="")
        self.lbl_mensagem_login.pack(pady=5)

        btn_entrar = ctk.CTkButton(self, text="Entrar", command=self.actionLogin)
        btn_entrar.pack(pady=10)

        btn_ir_registro = ctk.CTkButton(self, text="Não tem conta? Criar agora", fg_color="transparent", command=self.telaRegistro)
        btn_ir_registro.pack(pady=10)

    def actionLogin(self):
        email = self.entry_email_login.get().strip()
        senha = self.entry_senha_login.get().strip()

        if not email or not senha:
            self.lbl_mensagem_login.configure(text="Preencha todos os campos!", text_color="red")
            return

        banco = BancoDeDados()
        dados_usuario = banco.verificarLogin(email, senha)

        if dados_usuario:
            # Se achou no banco, nós recriamos o objeto User com os dados puxados
            self.usuario_atual = User(
                dados_usuario["nome"],
                dados_usuario["sobrenome"],
                dados_usuario["email"],
                dados_usuario["senha"]
            )
            self.telaFeed() # Vai para o feed logado!
        else:
            self.lbl_mensagem_login.configure(text="E-mail ou senha incorretos.", text_color="red")

    # ==========================================
    # TELA DE REGISTRO
    # ==========================================
    def telaRegistro(self):
        self.limparTela()
        self.geometry("400x550") 

        titulo = ctk.CTkLabel(self, text="Criar Conta", font=("Arial", 24, "bold"))
        titulo.pack(pady=(40, 20))

        self.entry_nome = ctk.CTkEntry(self, placeholder_text="Nome", width=250)
        self.entry_nome.pack(pady=10)

        self.entry_sobrenome = ctk.CTkEntry(self, placeholder_text="Sobrenome", width=250)
        self.entry_sobrenome.pack(pady=10)

        self.entry_email = ctk.CTkEntry(self, placeholder_text="E-mail", width=250)
        self.entry_email.pack(pady=10)

        self.entry_senha = ctk.CTkEntry(self, placeholder_text="Senha", show="*", width=250)
        self.entry_senha.pack(pady=10)

        self.lbl_mensagem = ctk.CTkLabel(self, text="")
        self.lbl_mensagem.pack(pady=10)

        btn_salvar = ctk.CTkButton(self, text="Salvar e Entrar", command=self.actionSalvarPerfil)
        btn_salvar.pack(pady=10)
        
        # NOVO: Botão para voltar para o login caso a pessoa já tenha conta
        btn_voltar_login = ctk.CTkButton(self, text="Já tenho conta", fg_color="transparent", command=self.telaLogin)
        btn_voltar_login.pack(pady=5)

    def actionSalvarPerfil(self):
        nome = self.entry_nome.get().strip()
        sobrenome = self.entry_sobrenome.get().strip()
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get().strip()

        if not nome or not sobrenome or not email or not senha:
            self.lbl_mensagem.configure(text="Todos os campos são obrigatórios!", text_color="red")
            return

        self.usuario_atual = User(nome, sobrenome, email, senha)
        banco = BancoDeDados()
        
        if banco.salvarPerfil(self.usuario_atual):
            self.telaFeed()
        else:
            self.lbl_mensagem.configure(text="Erro ao salvar dados.", text_color="red")
    def telaFeed(self):
        self.limparTela()
        self.geometry("450x650") # Deixa a tela um pouco maior para caber o feed

        saudacao = ctk.CTkLabel(self, text=f"Bem-vindo(a), {self.usuario_atual.getNome()}!", font=("Arial", 20, "bold"))
        saudacao.pack(pady=(20, 10))

        # --- ÁREA DE NOVA POSTAGEM ---
        frame_nova_postagem = ctk.CTkFrame(self)
        frame_nova_postagem.pack(pady=5, padx=20, fill="x")

        lbl_instrucao = ctk.CTkLabel(frame_nova_postagem, text="No que você está pensando?")
        lbl_instrucao.pack(pady=(10, 0))

        self.caixa_texto = ctk.CTkTextbox(frame_nova_postagem, height=60)
        self.caixa_texto.pack(pady=10, padx=10, fill="x")

        btn_postar = ctk.CTkButton(frame_nova_postagem, text="Publicar", command=self.actionPostar)
        btn_postar.pack(pady=(0, 5))

        self.lbl_feedback_feed = ctk.CTkLabel(frame_nova_postagem, text="", height=10)
        self.lbl_feedback_feed.pack(pady=(0, 5))

        # --- ÁREA DO FEED (ROLÁVEL) ---
        titulo_feed = ctk.CTkLabel(self, text="Últimas Publicações", font=("Arial", 14, "bold"))
        titulo_feed.pack(pady=(10, 5))

        self.frame_feed = ctk.CTkScrollableFrame(self, width=400, height=300)
        self.frame_feed.pack(pady=5, padx=20, fill="both", expand=True)

        # Carrega os posts na tela assim que o feed abre
        self.carregarFeed()

        btn_sair = ctk.CTkButton(self, text="Sair", fg_color="transparent", border_width=1, command=self.telaLogin)
        btn_sair.pack(pady=15)

    def carregarFeed(self):
        """Busca os posts no banco de dados e desenha na tela."""
        for widget in self.frame_feed.winfo_children():
            widget.destroy()

        feed_db = Feed("feed.json")
        posts = feed_db.lerPosts() 

        if not posts:
            lbl_vazio = ctk.CTkLabel(self.frame_feed, text="Nenhuma publicação ainda. Seja o primeiro!")
            lbl_vazio.pack(pady=20)
            return

        for p in reversed(posts):
            cartao_post = ctk.CTkFrame(self.frame_feed, fg_color="#2b2b2b")
            cartao_post.pack(pady=5, padx=5, fill="x")

            nome_completo = f"{p['autor']['nome']} {p['autor']['sobrenome']}"
            cabecalho = f"{nome_completo} • {p['data']}"
            
            lbl_autor = ctk.CTkLabel(cartao_post, text=cabecalho, font=("Arial", 11, "bold"), text_color="#1f6aa5")
            lbl_autor.pack(anchor="w", padx=10, pady=(5, 0))

            lbl_texto = ctk.CTkLabel(cartao_post, text=p['texto'], justify="left", wraplength=350)
            lbl_texto.pack(anchor="w", padx=10, pady=(0, 5))

            # --- LINHA 1: CURTIDAS ---
            frame_acoes = ctk.CTkFrame(cartao_post, fg_color="transparent")
            frame_acoes.pack(fill="x", padx=10, pady=(0, 5))

            lbl_likes = ctk.CTkLabel(frame_acoes, text=f"❤️ {p.get('curtidas', 0)}")
            lbl_likes.pack(side="left")

            # O "lambda" faz o botão lembrar o ID único exato deste post
            btn_like = ctk.CTkButton(frame_acoes, text="Curtir", width=50, height=24,
                                     command=lambda pid=p.get('id'): self.actionCurtir(pid))
            btn_like.pack(side="left", padx=10)

            # --- LINHA 2: LISTA DE COMENTÁRIOS ---
            for c in p.get('comentarios', []):
                lbl_c = ctk.CTkLabel(cartao_post, text=f"↳ {c}", text_color="gray", font=("Arial", 11))
                lbl_c.pack(anchor="w", padx=20, pady=(0, 2))

            # --- LINHA 3: CAIXA PARA NOVO COMENTÁRIO ---
            frame_comentar = ctk.CTkFrame(cartao_post, fg_color="transparent")
            frame_comentar.pack(fill="x", padx=10, pady=(5, 10))

            entry_coment = ctk.CTkEntry(frame_comentar, placeholder_text="Comentar...", height=24)
            entry_coment.pack(side="left", fill="x", expand=True)

            btn_enviar_coment = ctk.CTkButton(frame_comentar, text="Enviar", width=50, height=24,
                                              command=lambda pid=p.get('id'), ent=entry_coment: self.actionComentar(pid, ent))
            btn_enviar_coment.pack(side="left", padx=5)

    # --- FUNÇÕES DE AÇÃO DOS BOTÕES ---
    def actionCurtir(self, post_id):
        """Dispara quando o usuário clica em curtir."""
        if not post_id: return
        feed_db = Feed("feed.json")
        feed_db.atualizarInteracao(post_id, "curtir")
        self.carregarFeed() # Recarrega a tela para atualizar o coração

    def actionComentar(self, post_id, entry_widget):
        """Dispara quando o usuário clica em enviar comentário."""
        if not post_id: return
        texto_comentario = entry_widget.get().strip()
        
        if not texto_comentario: return # Ignora se estiver vazio

        # Junta o nome de quem está logado com o texto para ficar "Nome: Comentário"
        comentario_formatado = f"{self.usuario_atual.getNome()}: {texto_comentario}"

        feed_db = Feed("feed.json")
        feed_db.atualizarInteracao(post_id, "comentar", comentario_formatado)
        self.carregarFeed() # Recarrega a tela para o comentário aparecer
    def actionPostar(self):
        texto = self.caixa_texto.get("1.0", "end-1c").strip()
        
        if not texto:
            self.lbl_feedback_feed.configure(text="O post não pode estar vazio!", text_color="red")
            return

        nova_postagem = Post(self.usuario_atual, texto)
        feed_db = Feed("feed.json") 
        if feed_db.postar(nova_postagem):
            self.lbl_feedback_feed.configure(text="Post publicado com sucesso!", text_color="green")
            self.caixa_texto.delete("1.0", "end")
            
            self.carregarFeed()
        else:
            self.lbl_feedback_feed.configure(text="Erro ao publicar.", text_color="red")

if __name__ == "__main__":
    app = AppRedeSocial()
    app.mainloop()