import time
import random

class Planta:
    def __init__(self, nome, tempo_crescimento, preco_venda):
        self.nome = nome
        self.tempo_crescimento = tempo_crescimento
        self.estagio = 0  # 0: Semente, 1: Crescendo, 2: Pronta para colheita
        self.regada = False
        self.data_plantio = time.time()
        self.preco_venda = preco_venda

    def regar(self):
        if not self.regada:
            self.regada = True
            print(f"Você regou a {self.nome}.")
            return True
        else:
            print(f"A {self.nome} já está regada.")
            return False

    def verificar_crescimento(self):
        if self.estagio == 2:
            return

        if self.regada and (time.time() - self.data_plantio) >= self.tempo_crescimento:
            self.estagio = 2
            print(f"**A sua {self.nome} está pronta para ser colhida!**")
        elif self.regada and (time.time() - self.data_plantio) >= self.tempo_crescimento / 2:
            if self.estagio == 0:
                self.estagio = 1
                print(f"A sua {self.nome} começou a crescer.")
        elif not self.regada and (time.time() - self.data_plantio) >= self.tempo_crescimento * 1.5:
            # Se não regou a tempo, a planta morre
            self.estagio = -1 # -1 significa planta morta
            print(f"A sua {self.nome} murchou e morreu por falta de água.")


class Fazenda:
    def __init__(self):
        self.dinheiro = 100
        self.inventario = []
        self.plantas_disponiveis = {
            "Tomate": {"tempo": 10, "preco": 20},
            "Cenoura": {"tempo": 15, "preco": 30},
            "Alface": {"tempo": 8, "preco": 15}
        }
        self.campo = [None] * 5  # 5 espaços para plantas

    def exibir_status(self):
        print("\n--- Status da Fazenda ---")
        print(f"Dinheiro: R${self.dinheiro}")
        print("Inventário de Colheitas:", self.inventario)
        print("Campo:")
        for i, planta in enumerate(self.campo):
            if planta is None:
                print(f"  [{i+1}] - Vazio")
            elif planta.estagio == 0:
                print(f"  [{i+1}] - {planta.nome} (Semente)")
            elif planta.estagio == 1:
                print(f"  [{i+1}] - {planta.nome} (Crescendo)")
            elif planta.estagio == 2:
                print(f"  [{i+1}] - {planta.nome} (Pronta para Colher!)")
            else:
                print(f"  [{i+1}] - {planta.nome} (Murcha)")
        print("--------------------------\n")

    def plantar(self):
        print("\n--- Plantar ---")
        print("Plantas disponíveis para compra:")
        for nome, dados in self.plantas_disponiveis.items():
            print(f"- {nome}: Tempo de crescimento: {dados['tempo']} segundos, Preço de venda: R${dados['preco']}")
        
        escolha_planta = input("Qual planta você quer plantar? (Ex: Tomate): ").title()
        if escolha_planta not in self.plantas_disponiveis:
            print("Planta inválida.")
            return

        for i, espaco in enumerate(self.campo):
            if espaco is None:
                preco_planta = self.plantas_disponiveis[escolha_planta]['preco'] * 0.25 # Preço da semente é 25% do valor da colheita
                if self.dinheiro >= preco_planta:
                    self.dinheiro -= preco_planta
                    tempo_crescimento = self.plantas_disponiveis[escolha_planta]['tempo']
                    nova_planta = Planta(escolha_planta, tempo_crescimento, preco_planta*4) # Preço de venda é 4x o da semente
                    self.campo[i] = nova_planta
                    print(f"Você plantou uma semente de {escolha_planta} no espaço {i+1}.")
                    break
                else:
                    print("Você não tem dinheiro suficiente para comprar esta semente.")
                    break
        else:
            print("Não há espaços vazios no seu campo.")
    
    def regar(self):
        try:
            espaco = int(input("Qual espaço você quer regar? (1-5): ")) - 1
            if 0 <= espaco < len(self.campo) and self.campo[espaco] is not None:
                self.campo[espaco].regar()
            else:
                print("Espaço inválido ou vazio.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

    def colher(self):
        try:
            espaco = int(input("Qual espaço você quer colher? (1-5): ")) - 1
            if 0 <= espaco < len(self.campo) and self.campo[espaco] is not None:
                planta = self.campo[espaco]
                if planta.estagio == 2:
                    self.dinheiro += planta.preco_venda
                    self.inventario.append(planta.nome)
                    print(f"Você colheu {planta.nome} e vendeu por R${planta.preco_venda}. Seu dinheiro agora é R${self.dinheiro}.")
                    self.campo[espaco] = None # Libera o espaço
                elif planta.estagio == -1:
                    print(f"Não é possível colher. A {planta.nome} murchou e está morta.")
                    self.campo[espaco] = None # Remove a planta morta
                else:
                    print("Esta planta ainda não está pronta para a colheita.")
            else:
                print("Espaço inválido ou vazio.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

    def main_loop(self):
        print("Bem-vindo ao Simulador de Fazenda!")
        fazenda = Fazenda()
        
        while True:
            fazenda.exibir_status()
            for planta in fazenda.campo:
                if planta:
                    planta.verificar_crescimento()
                    
            print("\nO que você quer fazer?")
            print("[1] Plantar")
            print("[2] Regar")
            print("[3] Colher")
            print("[4] Sair")
            
            escolha = input("> ")
            
            if escolha == '1':
                fazenda.plantar()
            elif escolha == '2':
                fazenda.regar()
            elif escolha == '3':
                fazenda.colher()
            elif escolha == '4':
                print("Obrigado por jogar!")
                break
            else:
                print("Escolha inválida.")
            
            time.sleep(1) # Aguarda 1 segundo para dar tempo das ações serem processadas e o tempo passar

if __name__ == "__main__":
    jogo = Fazenda()
    jogo.main_loop()