"""Relaciona um veículo aos serviços de seu orçamento."""
from decimal import Decimal
from servico import Servico, formatar_moeda
from veiculo import Veiculo


class OrdemServico:
    def __init__(self, numero, veiculo):
        if type(numero) is not int or numero <= 0:
            raise ValueError("O número da ordem deve ser um inteiro positivo.")
        if not isinstance(veiculo, Veiculo):
            raise ValueError("Associe a ordem a um veículo cadastrado.")
        self._numero = numero
        self._veiculo = veiculo
        self._servicos = []

    @property
    def numero(self):
        return self._numero

    @property
    def veiculo(self):
        return self._veiculo

    @property
    def servicos(self):
        # A tupla impede a alteração da coleção por quem apenas a consulta.
        return tuple(self._servicos)

    def adicionar_servico(self, servico):
        if not isinstance(servico, Servico):
            raise ValueError("Selecione um serviço válido.")
        self._servicos.append(servico)

    def calcular_total(self):
        return sum((servico.valor for servico in self._servicos), Decimal("0.00"))

    def resumo(self):
        linhas = [
            f"ORDEM DE SERVIÇO Nº {self.numero:03d}",
            f"Veículo: {self.veiculo.modelo} | Placa: {self.veiculo.placa}",
            f"Proprietário: {self.veiculo.proprietario}",
            "Serviços:",
        ]
        if self._servicos:
            linhas.extend(f"  {i}. {servico}" for i, servico in enumerate(self._servicos, 1))
        else:
            linhas.append("  Nenhum serviço lançado.")
        linhas.append(f"TOTAL DO ORÇAMENTO: {formatar_moeda(self.calcular_total())}")
        return "\n".join(linhas)
