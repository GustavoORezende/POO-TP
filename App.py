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
        self.telaRegistro()

    def limparTela(self):
        """Remove todos os widgets da tela para transição de frames."""
        for widget in self.winfo_children():
            widget.destroy()

    def telaRegistro(self):
        self.limparTela()
        self.geometry("400x550") # Garante o tamanho original do registro

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
        btn_salvar.pack(pady=20)

    def actionSalvarPerfil(self):
        nome = self.entry_nome.get().strip()
        sobrenome = self.entry_sobrenome.get().strip()
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get().strip()

        if not nome or not sobrenome:
            self.lbl_mensagem.configure(text="Nome e Sobrenome são obrigatórios!", text_color="red")
            return

        # Instancia as classes importadas de models.py e database.py
        self.usuario_atual = User(nome, sobrenome, email, senha)
        banco = BancoDeDados()
        
        if banco.salvarPerfil(self.usuario_atual):
            self.telaFeed()
        else:
            self.lbl_mensagem.configure(text="Erro ao salvar dados.", text_color="red")

    def telaFeed(self):
        self.limparTela()
        self.geometry("450x650") # Deixa a tela um pouco maior para caber o feed

        # Nota: Se você aplicou o @property no models.py, troque getNome() por apenas nome
        saudacao = ctk.CTkLabel(self, text=f"Bem-vindo(a), {self.usuario_atual.getNome()}!", font=("Arial", 20, "bold"))
        saudacao.pack(pady=(20, 10))

        # --- ÁREA DE NOVA POSTAGEM ---
        frame_nova_postagem = ctk.CTkFrame(self)
        frame_nova_postagem.pack(pady=5, padx=20, fill="x")

        lbl_instrucao = ctk.CTkLabel(frame_nova_postagem, text="No que você está pensando?")
        lbl_instrucao.pack(pady=(10, 0))

        self.caixa_texto = ctk.CTkTextbox(frame_nova_postagem, height=60)
        self.caixa_texto.pack(pady=10, padx=10, fill="x")

        # CORRIGIDO: command aponta para self.actionPostar
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

        btn_sair = ctk.CTkButton(self, text="Sair / Nova Conta", fg_color="transparent", border_width=1, command=self.telaRegistro)
        btn_sair.pack(pady=15)

    def carregarFeed(self):
        """Busca os posts no banco de dados e desenha na tela."""
        # Primeiro, limpa o feed atual para não duplicar os posts ao recarregar
        for widget in self.frame_feed.winfo_children():
            widget.destroy()

        feed_db = Feed("feed.json")
        posts = feed_db.lerPosts() # Lembre-se que você precisa ter criado o ler_posts() no database.py!

        if not posts:
            lbl_vazio = ctk.CTkLabel(self.frame_feed, text="Nenhuma publicação ainda. Seja o primeiro!")
            lbl_vazio.pack(pady=20)
            return

        # Lemos a lista ao contrário (reversed) para o post mais novo ficar no topo
        for p in reversed(posts):
            # Cria um "cartão" para cada post
            cartao_post = ctk.CTkFrame(self.frame_feed, fg_color="#2b2b2b")
            cartao_post.pack(pady=5, padx=5, fill="x")

            # Nome do autor e Data
            nome_completo = f"{p['autor']['nome']} {p['autor']['sobrenome']}"
            cabecalho = f"{nome_completo} • {p['data']}"
            
            lbl_autor = ctk.CTkLabel(cartao_post, text=cabecalho, font=("Arial", 11, "bold"), text_color="#1f6aa5")
            lbl_autor.pack(anchor="w", padx=10, pady=(5, 0))

            # Texto do post
            lbl_texto = ctk.CTkLabel(cartao_post, text=p['texto'], justify="left", wraplength=350)
            lbl_texto.pack(anchor="w", padx=10, pady=(0, 10))

    def actionPostar(self):
        texto = self.caixa_texto.get("1.0", "end-1c").strip()
        
        if not texto:
            self.lbl_feedback_feed.configure(text="O post não pode estar vazio!", text_color="red")
            return

        nova_postagem = Post(self.usuario_atual, texto)
        feed_db = Feed("feed.json") # Não precisa passar "feed.json" se você configurou o default no database.py

        if feed_db.postar(nova_postagem):
            self.lbl_feedback_feed.configure(text="Post publicado com sucesso!", text_color="green")
            self.caixa_texto.delete("1.0", "end")
            
            self.carregarFeed()
        else:
            self.lbl_feedback_feed.configure(text="Erro ao publicar.", text_color="red")

if __name__ == "__main__":
    app = AppRedeSocial()
    app.mainloop()