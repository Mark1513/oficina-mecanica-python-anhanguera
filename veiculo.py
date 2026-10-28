"""Cadastro de veículos - Marcos Paulo Santos Mota - Anhanguera."""
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class Veiculo:
    """A placa identifica o veículo; o cadastro é imutável após validado."""
    placa: str
    modelo: str
    proprietario: str

    def __post_init__(self):
        if not isinstance(self.placa, str):
            raise ValueError("Informe uma placa válida.")
        placa = self.placa.strip().upper().replace("-", "").replace(" ", "")
        if not re.fullmatch(r"[A-Z]{3}(?:[0-9]{4}|[0-9][A-Z][0-9]{2})", placa):
            raise ValueError("Placa inválida. Exemplos: ABC-1234 ou ABC1D23.")
        object.__setattr__(self, "placa", placa)
        for campo in ("modelo", "proprietario"):
            valor = getattr(self, campo)
            if not isinstance(valor, str) or not valor.strip():
                raise ValueError(f"O campo {campo} não pode ficar vazio.")
            object.__setattr__(self, campo, valor.strip())

    def __str__(self):
        return f"{self.placa} | {self.modelo} | Proprietário: {self.proprietario}"
