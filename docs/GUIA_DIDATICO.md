# Guia didático e apresentação

**Marcos Paulo Santos Mota | Anhanguera | Aula 16 - Unidade 4**

## O que foi pedido nesta aula

O material destaca o arquivo `README.md`: documentar o sistema, seu objetivo, tecnologias, arquivos, execução, exemplos e melhorias. O README desta entrega reúne esses itens. O projeto executável acompanha a documentação para que os comandos e exemplos possam ser conferidos na prática.

## Função de cada arquivo

| Arquivo | Explicação em linguagem simples |
| --- | --- |
| `veiculo.py` | Representa o veículo, valida a placa e os campos obrigatórios. |
| `servico.py` | Define o contrato de serviço e implementa troca de óleo e alinhamento. |
| `ordem_servico.py` | Reúne veículo e serviços, soma os valores e monta o resumo. |
| `main.py` | Mantém os cadastros, mostra o menu e oferece a demonstração pronta. |
| `README.md` | Orienta quem vai utilizar, avaliar ou continuar o projeto. |
| `tests/test_oficina.py` | Confere as regras e simula a navegação pelo menu. |

## Como o sistema funciona

1. O programa cria uma oficina vazia e abre o menu.
2. O usuário cadastra um veículo. A classe `Veiculo` valida seus dados.
3. A oficina abre uma ordem e a associa ao veículo.
4. Cada serviço lançado vira um objeto `TrocaOleo` ou `Alinhamento`.
5. A ordem guarda esses objetos e soma seus preços.
6. O resumo apresenta placa, modelo, proprietário, serviços e total.
7. Ao sair, os dados em memória são descartados.

## Principais métodos

- `cadastrar_veiculo()`: cria o objeto e verifica se a placa já existe.
- `abrir_ordem()`: procura o veículo e cria uma ordem com número sequencial.
- `adicionar_servico()`: inclui um serviço válido na ordem.
- `calcular_total()`: soma os preços usando `Decimal`.
- `resumo()`: transforma os dados em um texto organizado.
- `executar_menu()`: lê opções, chama operações e trata erros de entrada.

## Orientação a objetos

O veículo reúne seus dados. O serviço reúne nome e preço. A ordem combina esses objetos. A classe abstrata `Servico` impede criar um serviço sem nome definido. As subclasses seguem o mesmo contrato, permitindo que a ordem some seus preços sem distinguir o tipo de serviço.

Os campos com `_` indicam uso interno por convenção do Python; isso não é uma barreira de segurança. Propriedades permitem consultar os dados. A lista de serviços é exposta como tupla para impedir a alteração direta da coleção por quem apenas a consulta.

## Respostas às reflexões da aula

**1. Por que a documentação é importante?**  
Porque registra o objetivo, a organização e a utilização do sistema. Isso facilita a manutenção e evita que o conhecimento fique restrito a quem escreveu o código.

**2. Como o README pode ajudar outras pessoas a utilizar o sistema?**  
Ele informa a versão do Python, onde abrir o terminal, qual comando executar e como preencher um exemplo completo. Assim, outra pessoa consegue repetir o uso e conferir o resultado.

**3. Quais informações adicionais poderiam ser incluídas?**  
Autor, instituição, data, regras de validação, limitações, testes, registros de execução, condições de uso e propostas de melhoria.

**4. Como essa documentação será útil na próxima etapa de interface web?**  
Ela registra as classes e regras existentes. Isso ajuda a planejar como reaproveitar a lógica em páginas, formulários e rotas, mantendo os mesmos dados e cálculos.

## Apresentação sugerida

“Meu projeto é um sistema de oficina mecânica em Python. Ele permite cadastrar veículos, abrir ordens, lançar troca de óleo e alinhamento e calcular o orçamento. Organizei o código em quatro módulos e documentei tudo no README, que é o foco da Aula 16. Usei classes para separar as responsabilidades e Decimal para trabalhar com valores em reais. Na demonstração, uma troca de óleo de 150 reais e um alinhamento de 80 reais totalizam 230 reais. Os dados ficam na memória; uma evolução seria salvar os cadastros e criar uma interface web.”

## Roteiro de demonstração

1. Mostre no README a descrição, a estrutura de arquivos e as instruções de execução.
2. Execute `python main.py --demo` para exibir um fluxo completo.
3. Execute `python main.py` e mostre o menu interativo.
4. Execute `python -m unittest discover -s tests -v` para repetir a validação.
5. Explique o armazenamento em memória e as melhorias propostas.

## Perguntas que o professor pode fazer

**O que é Markdown?**  
Uma forma de escrever texto com marcações simples para títulos, listas, tabelas e código. O GitHub apresenta esse conteúdo com formatação.

**Qual é a relação entre veículo e ordem?**  
Uma ordem pertence a um veículo; o mesmo veículo pode ter várias ordens durante a sessão.

**Por que separar os módulos?**  
Cada arquivo concentra uma responsabilidade, facilitando a leitura e futuras alterações.

**Onde há herança e polimorfismo?**  
TrocaOleo e Alinhamento herdam de Servico. A ordem utiliza seus nomes e preços pelo mesmo contrato, independentemente da subclasse.

**Por que usar Decimal?**  
Para representar valores decimais e somar centavos com precisão: 0,10 mais 0,20 deve resultar em 0,30.

**O que acontece com entradas inválidas?**  
O programa mostra uma mensagem e continua no menu. O lançamento inválido não é incluído.

**Os dados ficam salvos?**  
Não. Eles existem apenas durante a execução. Persistência é uma melhoria futura.

**Os serviços são executados pelo programa?**  
O programa registra os serviços e calcula o orçamento. O trabalho mecânico é externo ao software.

**Como verificar que funciona?**  
Utilizando o menu, executando a demonstração e repetindo os testes. A pasta docs contém os registros reais desta entrega.
