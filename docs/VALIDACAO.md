# Validação da entrega

**Autor:** Marcos Paulo Santos Mota  
**Data:** 28 de outubro de 2026  
**Ambiente local:** Windows, Python 3.12.14

## Verificações executadas

| Verificação | Resultado |
| --- | --- |
| `python -m unittest discover -s tests -v` | 28 testes aprovados; saída 0 |
| `python main.py --demo` | Demonstração concluída; saída 0 |
| Fluxo completo do menu | Cadastro, abertura da ordem, dois serviços, listagem, orçamento e resumo verificados pelos testes |
| Entradas inválidas | Menu continua após opção, ordem, veículo, tipo e preço inválidos |
| Atalhos Windows | demonstrar.cmd e testar.cmd executados com sucesso neste computador |
| Cálculo em reais | 150,00 + 80,00 = 230,00; 0,10 + 0,20 = 0,30 |

Os arquivos [testes_reais.txt](testes_reais.txt) e [execucao_real.txt](execucao_real.txt) contêm a saída capturada dos processos executados. Os testes usam somente a biblioteca padrão.

## Alcance da validação

Os testes locais foram executados em Python 3.12.14. O projeto utiliza recursos compatíveis com Python 3.10 ou superior. A configuração do GitHub Actions foi preparada para Python 3.10 e 3.14; o resultado remoto deve ser consultado na aba Actions do repositório.

A demonstração utiliza dados fictícios e entradas predefinidas. O teste do menu fornece respostas automatizadas às mesmas operações disponíveis ao usuário. Não houve serviço mecânico ou pagamento real.

Os dados não persistem após o encerramento, conforme documentado no README.

## Registro visual

A imagem `execucao.png` foi composta a partir da saída real de `python main.py --demo`. É uma apresentação visual do registro, e não uma captura de uma janela de terminal. O texto original permanece em `execucao_real.txt`.
