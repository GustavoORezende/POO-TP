import json 
import os
from datetime import datetime
#TODO: COMENTARIOS NO CODIGO
class User:
    def __init__(self, nome, sobrenome):
        self.__nome = nome
        self.__sobrenome = sobrenome

    def getNome(self):
        return self.__nome
    
    def getSobrenome(self):
        return self.__sobrenome
       

class Post:
    def __init__(self, user, texto):
        self.autor = {
            "nome": user.getNome(),
            "sobrenome": user.getSobrenome()
        }
        self.texto = texto
        self.__curtidas = 0
        self.__comentarios = []
        self.__data = datetime.now().strftime("%d/%m/%Y %H:%M")

    def toDict(self):
        return{
            "autor": self.autor,
            "texto": self.texto,
            "curtidas": self.__curtidas,
            "comentarios": self.__comentarios,
            "data": self.__data

        }
        
    def curtir(self):
        self.__curtidas += 1

    def comentar(self, comentario):
        if comentario.strip()=="":
            raise ValueError("Comentario nao pode ser vazio")
        self.__comentarios.append(comentario)
    

    def exibirAutor(self):
        print(f"postado por {self.autor}")

    def exibirTexto(self):
        print(f"{self.texto}")
       
class Feed:
    def __init__(self, arquivo):
        self.__arquivo = arquivo

    def postar(self, post):
        try:
            try:
                with open(self.__arquivo, 'r', encoding='utf-8') as arquivo:
                    posts = json.load(arquivo)
            
            except:
                posts =[]

            posts.append(post.toDict())

            with open(self.__arquivo, 'w', encoding='utf-8') as arquivo:
                json.dump(posts, arquivo, indent=4, ensure_ascii=False)
                print(f"Sucesso: sua publicacao foi postada em {self.__arquivo}")

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
