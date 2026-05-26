import json 
import os
from pathlib import Path
#Caminho da pasta onde este arquivo database.py está
BASE_DIR = Path(__file__).parent

class BancoDeDados:
    def __init__(self, file = "accounts.json"):
        #Une pasta + arquivo = caminho: C:TP1/database/accounts.json
        self.file = BASE_DIR / file

    def salvarPerfil(self, user):
        usuarios = []
        #leitura do arquivo, se não vazio
        if self.file.exists():
            try:
                with open(self.file, 'r', encoding='utf-8') as arquivo:
                    usuarios = json.load(arquivo)
                   

            except json.JSONDecodeError:
                #inicia como lista vazia caso não exista nada
                pass

            usuarios.append(user.to_dict())

            #Aqui salva a lista com o perfil novo
            try:
                with open(self.file, 'w', encoding='utf-8') as arquivo:
                    json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)
                    print(f"Sucesso: Dados salvos em {self.file}")
                    return True

            except Exception as e:
                print(f"Erro ao salvar: {e}")
                return False

class Feed:
    def __init__(self, file):
        self.__file = BASE_DIR / file

    def postar(self, post):
        try:
            try:
                with open(self.__file, 'r', encoding='utf-8') as arquivo:
                    posts = json.load(arquivo)
            
            except:
              print(f"Erro ao postar: {e}")

            posts.append(post.toDict())

            with open(self.__file, 'w', encoding='utf-8') as arquivo:
                json.dump(posts, arquivo, indent=4, ensure_ascii=False)
                print(f"Sucesso: sua publicacao foi postada em {self.__file}")

        except Exception as e:
            print(f"Erro ao postar: {e}")
