import json 
import os
from datetime import datetime

class User:
    def __init__(self, nome, sobrenome):
        self.nome = nome
        self.sobrenome = sobrenome
       

class Post:
    def __init__(self, user, texto):
        self.autor = {
            "nome": user.nome,
            "sobrenome": user.sobrenome
        }
        self.texto = texto
        self.curtidas = 0
        self.comentarios = []
        self.data = datetime.now().strftime("%d/%m/%Y %H:%M")
        
    def curtir(self):
        self.curtidas =+ 1

    def comentar(self, comentario):
        self.comentarios.append(comentario)
    

    def exibirAutor(self):
        print(f"postado por {self.autor}")

    def exibirTexto(self):
        print(f"{self.texto}")
       
class Feed:
    def __init__(self, arquivo):
        self.arquivo = arquivo

    def postar(self, post):
        try:
            try:
                with open(self.arquivo, 'r', encoding='utf-8') as arquivo:
                    posts = json.load(arquivo)
            
            except:
                posts =[]

            posts.append(post.__dict__)

            with open(self.arquivo, 'w', encoding='utf-8') as arquivo:
                json.dump(posts, arquivo, indent=4, ensure_ascii=False)
                print(f"Sucesso: sua publicacao foi postada em {self.arquivo}")

        except Exception as e:
            print(f"Erro ao postar: {e}")

def main():
    feed = Feed("feed.json")
    User1 = User("Ana", "Lafaiete" )
    postagem = Post(User1, "Primeira publicacao do feed")
    postagem.curtir()
    postagem.comentar("Primeiro Comentario!")
    feed.postar(postagem)

main()
