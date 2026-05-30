from datetime import datetime

class User:
    def __init__(self, nome, sobrenome, email, senha):

        self.__nome = nome
        self.__sobrenome = sobrenome
        self.__email = email
        self.__senha = senha

    def getNome(self):
        return self.__nome
    
    def getSobrenome(self):
        return self.__sobrenome
    
    def toDict(self):
        return {
            "nome": self.__nome,
            "sobrenome": self.__sobrenome,
            "email": self.__email,
            "senha": self.__senha
        }
    
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
       
       