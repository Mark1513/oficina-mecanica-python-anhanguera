"""Testes de regras e do fluxo do menu com a biblioteca padrão."""
import subprocess
import sys
import unittest
from dataclasses import FrozenInstanceError
from decimal import Decimal
from pathlib import Path
from main import Oficina, executar_menu
from ordem_servico import OrdemServico
from servico import Alinhamento, Servico, TrocaOleo, formatar_moeda
from veiculo import Veiculo


class CadastroTest(unittest.TestCase):
    def test_normaliza_placa_e_campos(self):
        v = Veiculo(" abc-1234 ", " Argo ", " Marcos ")
        self.assertEqual((v.placa, v.modelo, v.proprietario), ("ABC1234", "Argo", "Marcos"))

    def test_aceita_placa_mercosul(self):
        self.assertEqual(Veiculo("abc1d23", "Argo", "Marcos").placa, "ABC1D23")

    def test_rejeita_dados_invalidos(self):
        for dados in [("", "Argo", "Marcos"), ("1234567", "Argo", "Marcos"),
                      (None, "Argo", "Marcos"), ("ABC1234", " ", "Marcos"),
                      ("ABC1234", "Argo", None)]:
            with self.subTest(dados=dados), self.assertRaises(ValueError):
                Veiculo(*dados)

    def test_rejeita_duplicado_sem_alterar_cadastro(self):
        oficina = Oficina()
        original = oficina.cadastrar_veiculo("ABC1234", "Argo", "Marcos")
        with self.assertRaises(ValueError):
            oficina.cadastrar_veiculo("abc-1234", "Outro", "Ana")
        self.assertEqual(oficina.veiculos, (original,))

    def test_veiculo_imutavel(self):
        with self.assertRaises(FrozenInstanceError):
            Veiculo("ABC1234", "Argo", "Marcos").placa = "XYZ1234"


class ServicoTest(unittest.TestCase):
    def test_servico_abstrato_nao_pode_ser_instanciado(self):
        with self.assertRaises(TypeError):
            Servico("10")

    def test_tipos_de_servico_e_virgula_decimal(self):
        self.assertEqual(TrocaOleo("150,00").valor, Decimal("150.00"))
        self.assertEqual(Alinhamento("80").nome, "Alinhamento")

    def test_rejeita_valores_invalidos(self):
        for valor in ["0", "-1", "abc", "NaN", "Infinity", "-Infinity", "", None, True, "0.001"]:
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                TrocaOleo(valor)

    def test_arredonda_meio_centavo_para_cima(self):
        self.assertEqual(Alinhamento("12.345").valor, Decimal("12.35"))

    def test_preco_imutavel(self):
        with self.assertRaises(FrozenInstanceError):
            TrocaOleo("150").valor = Decimal("1")

    def test_formata_reais(self):
        self.assertEqual(formatar_moeda(Decimal("1234.50")), "R$ 1.234,50")


class OrdemTest(unittest.TestCase):
    def setUp(self):
        self.oficina = Oficina()
        self.veiculo = self.oficina.cadastrar_veiculo("ABC1D23", "Argo", "Marcos")

    def test_abre_ordem_com_veiculo_cadastrado(self):
        ordem = self.oficina.abrir_ordem("abc1d23")
        self.assertIs(ordem.veiculo, self.veiculo)
        self.assertIs(self.oficina.buscar_ordem(1), ordem)

    def test_veiculo_ausente_nao_consome_numero(self):
        with self.assertRaises(ValueError):
            self.oficina.abrir_ordem("XYZ1234")
        self.assertEqual(self.oficina.ordens, ())
        self.assertEqual(self.oficina.abrir_ordem("ABC1D23").numero, 1)

    def test_numeracao_sequencial(self):
        self.assertEqual(self.oficina.abrir_ordem("ABC1D23").numero, 1)
        self.assertEqual(self.oficina.abrir_ordem("ABC1D23").numero, 2)

    def test_rejeita_ordem_inexistente(self):
        for numero in [0, -1, 99, "1", True]:
            with self.subTest(numero=numero), self.assertRaises(ValueError):
                self.oficina.buscar_ordem(numero)

    def test_valida_construtor(self):
        for numero, veiculo in [(0, self.veiculo), (True, self.veiculo), (1, None)]:
            with self.subTest(numero=numero), self.assertRaises(ValueError):
                OrdemServico(numero, veiculo)

    def test_ordem_vazia(self):
        ordem = self.oficina.abrir_ordem("ABC1D23")
        self.assertEqual(ordem.calcular_total(), Decimal("0.00"))
        self.assertIn("Nenhum serviço lançado", ordem.resumo())

    def test_total_exato_e_resumo(self):
        ordem = self.oficina.abrir_ordem("ABC1D23")
        ordem.adicionar_servico(TrocaOleo("150"))
        ordem.adicionar_servico(Alinhamento("80"))
        self.assertEqual(ordem.calcular_total(), Decimal("230.00"))
        for texto in ["ABC1D23", "Marcos", "Troca de óleo", "Alinhamento", "R$ 230,00"]:
            self.assertIn(texto, ordem.resumo())

    def test_centavos_sem_imprecisao(self):
        ordem = self.oficina.abrir_ordem("ABC1D23")
        ordem.adicionar_servico(TrocaOleo("0.10"))
        ordem.adicionar_servico(Alinhamento("0.20"))
        self.assertEqual(ordem.calcular_total(), Decimal("0.30"))

    def test_rejeita_item_invalido(self):
        ordem = self.oficina.abrir_ordem("ABC1D23")
        with self.assertRaises(ValueError):
            ordem.adicionar_servico("Troca de óleo")
        self.assertEqual(ordem.servicos, ())

    def test_ordens_independentes(self):
        primeira = self.oficina.abrir_ordem("ABC1D23")
        segunda = self.oficina.abrir_ordem("ABC1D23")
        primeira.adicionar_servico(TrocaOleo("150"))
        self.assertEqual(segunda.calcular_total(), Decimal("0.00"))

    def test_consulta_nao_altera_lista(self):
        ordem = self.oficina.abrir_ordem("ABC1D23")
        with self.assertRaises(AttributeError):
            ordem.servicos.append(TrocaOleo("150"))


class MenuTest(unittest.TestCase):
    def executar(self, respostas):
        respostas = iter(respostas)
        saidas = []
        oficina = executar_menu(entrada=lambda _: next(respostas), saida=saidas.append)
        return oficina, "\n".join(saidas)

    def test_fluxo_completo_do_menu(self):
        oficina, texto = self.executar([
            "1", "ABC1D23", "Fiat Argo", "Marcos Paulo Santos Mota", "2",
            "3", "ABC1D23", "4", "1", "1", "150,00", "4", "1", "2", "80",
            "5", "6", "1", "7", "1", "0"
        ])
        self.assertEqual(len(oficina.veiculos), 1)
        self.assertEqual(len(oficina.ordens), 1)
        self.assertEqual(oficina.buscar_ordem(1).calcular_total(), Decimal("230.00"))
        self.assertIn("TOTAL DO ORÇAMENTO: R$ 230,00", texto)
        self.assertIn("Sistema encerrado", texto)

    def test_recuperacao_de_entradas_invalidas(self):
        oficina, texto = self.executar(["99", "6", "abc", "3", "ABC1234", "0"])
        self.assertEqual(oficina.ordens, ())
        self.assertIn("Opção inválida", texto)
        self.assertIn("Veículo não encontrado", texto)
        self.assertIn("Sistema encerrado", texto)

    def test_servico_invalido_nao_entra_na_ordem(self):
        oficina, texto = self.executar([
            "1", "ABC1234", "Argo", "Marcos", "3", "ABC1234",
            "4", "1", "9", "4", "1", "1", "-20", "0"
        ])
        self.assertEqual(oficina.buscar_ordem(1).servicos, ())
        self.assertIn("Tipo de serviço inválido", texto)
        self.assertIn("preço positivo", texto)

    def test_listas_vazias(self):
        _, texto = self.executar(["2", "5", "0"])
        self.assertIn("Nenhum veículo", texto)
        self.assertIn("Nenhuma ordem", texto)

    def test_fim_da_entrada_encerra_sem_falha(self):
        def fim(_):
            raise EOFError
        saidas = []
        executar_menu(entrada=fim, saida=saidas.append)
        self.assertIn("Entrada interrompida", "\n".join(saidas))

    def test_demo_em_processo_real(self):
        resultado = subprocess.run(
            [sys.executable, "-X", "utf8", "main.py", "--demo"],
            cwd=Path(__file__).resolve().parents[1],
            capture_output=True, text=True, encoding="utf-8", timeout=20
        )
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn("TOTAL DO ORÇAMENTO: R$ 230,00", resultado.stdout)
        self.assertIn("Marcos Paulo Santos Mota", resultado.stdout)


if __name__ == "__main__":
    unittest.main()
