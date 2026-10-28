"""Serviços e regras de valores monetários da oficina."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def formatar_moeda(valor):
    texto = f"{valor:,.2f}"
    return "R$ " + texto.replace(",", "_").replace(".", ",").replace("_", ".")


@dataclass(frozen=True)
class Servico(ABC):
    """Contrato comum de serviço. Cada lançamento tem preço imutável."""
    valor: Decimal

    def __post_init__(self):
        try:
            if isinstance(self.valor, bool):
                raise ValueError
            valor = Decimal(str(self.valor).strip().replace(",", "."))
            if not valor.is_finite() or valor <= 0:
                raise ValueError
            valor = valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if valor <= 0:
                raise ValueError
        except (InvalidOperation, ValueError):
            raise ValueError("Informe um preço positivo, com formato como 150,00.") from None
        object.__setattr__(self, "valor", valor)

    @property
    @abstractmethod
    def nome(self):
        """Nome apresentado no orçamento."""

    def __str__(self):
        return f"{self.nome}: {formatar_moeda(self.valor)}"


class TrocaOleo(Servico):
    @property
    def nome(self):
        return "Troca de óleo"


class Alinhamento(Servico):
    @property
    def nome(self):
        return "Alinhamento"
