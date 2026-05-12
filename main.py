import json 
import os
class User:
    def __init__(self, nome, sobrenome, email, senha):

        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.senha = senha

class BancoDeDados:
    def __init__(self, arquivo):
        self.arquivo = arquivo

    def salvarPerfil(self, user):
        try:
            with open(self.arquivo, 'w', encoding='utf-8') as arquivo:
                json.dump(user.__dict__, arquivo, indent=4, ensure_ascii=False)
                print(f"Sucesso: Dados salvos em {self.arquivo}")
                caminho_real = os.path.abspath(self.arquivo)

        except Exception as e:
            print(f"Erro ao salvar: {e}")

def main():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo = os.path.join(diretorio_atual, "accounts.json")
    print(f" salvo de verdade em {caminho_arquivo}")
    Banco = BancoDeDados("accounts.json")
    User1 = User("Ana", "Lafaiete","ana@email.com", "anaBanana" )
    Banco.salvarPerfil(User1)

main()