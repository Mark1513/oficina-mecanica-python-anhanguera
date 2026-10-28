"""Sistema de Oficina Mecânica - Marcos Paulo Santos Mota - Anhanguera."""
import argparse
from ordem_servico import OrdemServico
from servico import Alinhamento, TrocaOleo, formatar_moeda
from veiculo import Veiculo


class Oficina:
    """Coordena os cadastros e as ordens, mantidos em memória."""
    def __init__(self):
        self._veiculos = {}
        self._ordens = {}

    @property
    def veiculos(self):
        return tuple(self._veiculos.values())

    @property
    def ordens(self):
        return tuple(self._ordens.values())

    def cadastrar_veiculo(self, placa, modelo, proprietario):
        veiculo = Veiculo(placa, modelo, proprietario)
        if veiculo.placa in self._veiculos:
            raise ValueError("Já existe um veículo com essa placa.")
        self._veiculos[veiculo.placa] = veiculo
        return veiculo

    def abrir_ordem(self, placa):
        if not isinstance(placa, str):
            raise ValueError("Informe a placa do veículo.")
        placa = placa.strip().upper().replace("-", "").replace(" ", "")
        veiculo = self._veiculos.get(placa)
        if veiculo is None:
            raise ValueError("Veículo não encontrado. Cadastre-o primeiro.")
        ordem = OrdemServico(len(self._ordens) + 1, veiculo)
        self._ordens[ordem.numero] = ordem
        return ordem

    def buscar_ordem(self, numero):
        if type(numero) is not int or numero not in self._ordens:
            raise ValueError("Ordem de serviço não encontrada.")
        return self._ordens[numero]


MENU = """
========================================================
                 SISTEMA DE OFICINA MECÂNICA
========================================================
1 - Cadastrar veículo
2 - Listar veículos
3 - Abrir ordem de serviço
4 - Lançar serviço em uma ordem
5 - Listar ordens de serviço
6 - Calcular valor do orçamento
7 - Exibir resumo da ordem de serviço
0 - Sair
========================================================"""


def executar_menu(oficina=None, entrada=input, saida=print):
    """Entrada e saída podem ser substituídas nos testes, mantendo as regras."""
    if oficina is None:
        oficina = Oficina()
    saida("Projeto acadêmico | Marcos Paulo Santos Mota | Anhanguera")
    saida("Os dados ficam em memória e são apagados ao encerrar.")
    while True:
        try:
            saida(MENU)
            opcao = entrada("Escolha uma opção: ").strip()
            if opcao == "0":
                saida("Sistema encerrado. Até logo!")
                return oficina
            if opcao == "1":
                veiculo = oficina.cadastrar_veiculo(
                    entrada("Placa: "), entrada("Modelo: "), entrada("Proprietário: ")
                )
                saida(f"Veículo cadastrado: {veiculo}")
            elif opcao == "2":
                saida("\n".join(map(str, oficina.veiculos)) or "Nenhum veículo cadastrado.")
            elif opcao == "3":
                ordem = oficina.abrir_ordem(entrada("Placa do veículo: "))
                saida(f"Ordem de serviço nº {ordem.numero:03d} aberta com sucesso.")
            elif opcao == "4":
                ordem = oficina.buscar_ordem(int(entrada("Número da ordem: ")))
                saida("1 - Troca de óleo | 2 - Alinhamento")
                tipo = entrada("Tipo de serviço: ").strip()
                tipos = {"1": TrocaOleo, "2": Alinhamento}
                if tipo not in tipos:
                    raise ValueError("Tipo de serviço inválido. Escolha 1 ou 2.")
                servico = tipos[tipo](entrada("Preço em reais (ex.: 150,00): "))
                ordem.adicionar_servico(servico)
                saida(f"Serviço lançado: {servico}")
            elif opcao == "5":
                if not oficina.ordens:
                    saida("Nenhuma ordem de serviço cadastrada.")
                for ordem in oficina.ordens:
                    saida(f"OS {ordem.numero:03d} | {ordem.veiculo.placa} | "
                          f"{len(ordem.servicos)} serviço(s) | {formatar_moeda(ordem.calcular_total())}")
            elif opcao in ("6", "7"):
                ordem = oficina.buscar_ordem(int(entrada("Número da ordem: ")))
                if opcao == "6":
                    saida(f"Valor do orçamento: {formatar_moeda(ordem.calcular_total())}")
                else:
                    saida(ordem.resumo())
            else:
                saida("Opção inválida. Escolha um número de 0 a 7.")
        except ValueError as erro:
            saida(f"Não foi possível concluir: {erro}")
        except (EOFError, KeyboardInterrupt):
            saida("\nEntrada interrompida. Sistema encerrado.")
            return oficina


def demonstrar():
    """Executa um exemplo reproduzível com dados fictícios."""
    oficina = Oficina()
    print("SISTEMA DE OFICINA MECÂNICA | DEMONSTRAÇÃO")
    print("Autor: Marcos Paulo Santos Mota | Anhanguera | Aula 16 - Unidade 4")
    print("Dados demonstrativos; os valores são exemplos acadêmicos.\n")
    veiculo = oficina.cadastrar_veiculo("ABC1D23", "Fiat Argo", "Marcos Paulo Santos Mota")
    print(f"Veículo cadastrado: {veiculo}")
    ordem = oficina.abrir_ordem(veiculo.placa)
    print(f"Ordem {ordem.numero:03d} aberta.")
    for servico in (TrocaOleo("150.00"), Alinhamento("80.00")):
        ordem.adicionar_servico(servico)
        print(f"Serviço lançado: {servico}")
    print("\n" + ordem.resumo())
    print("\nDemonstração concluída com sucesso.")


def main():
    parser = argparse.ArgumentParser(description="Sistema acadêmico de oficina mecânica.")
    parser.add_argument("--demo", action="store_true", help="executa uma demonstração pronta")
    args = parser.parse_args()
    if args.demo:
        demonstrar()
    else:
        executar_menu()


if __name__ == "__main__":
    main()
