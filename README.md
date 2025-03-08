# Jogo da Velha com Inteligência Artificial

Este projeto é uma recriação do clássico Jogo da Velha, desenvolvido em Python com a biblioteca Pygame. O jogo foi proposto pelo Prof. Daniel Cavalcanti Jeronymo, que também desenvolveu boa parte da estrutura inicial do código. O projeto inclui uma funcionalidade de inteligência artificial que sugere a melhor jogada para o jogador atual, utilizando uma abordagem de busca em profundidade (DFS) para avaliar os possíveis estados do jogo.

## Requisitos

Para executar este projeto, você precisará das seguintes dependências:

- Python 3.x
- Biblioteca Pygame
- Biblioteca NumPy

### Instalação das Dependências

1. **Verifique a versão do Python**:
   ```bash
   python3 --version
   ```

2. **Instale o Pygame**:
   ```bash
   pip3 install pygame
   ```

3. **Instale o NumPy**:
   ```bash
   pip3 install numpy
   ```

## Estrutura do Código

O código está organizado em uma única classe principal (`Game`) que gerencia o estado do jogo, a lógica de atualização e a renderização. Abaixo está uma visão geral das principais partes do código:

### Classes e Métodos Principais

- **GameConstants**:
  - Contém constantes usadas no jogo, como cores, dimensões da tela, tamanho da grade e configurações de fonte.

- **Game**:
  - Gerencia o estado do jogo, incluindo a grade, o jogador atual e a lista de estados anteriores.
  - Métodos principais:
    - `generateSuccessors`: Gera todos os possíveis estados sucessores a partir do estado atual.
    - `dfs`: Realiza uma busca em profundidade para avaliar os possíveis estados do jogo e determinar a melhor jogada.
    - `oracle`: Usa o método DFS para sugerir a melhor jogada para o jogador atual.
    - `checkObjectiveState`: Verifica se o jogo terminou (vitória, derrota ou empate).
    - `update`: Atualiza o estado do jogo com base nas entradas do usuário.

- **Funções de Renderização**:
  - `drawGrid`: Desenha a grade do jogo na tela, colorindo as células com base no estado atual.
  - `initialize`: Inicializa o Pygame, a fonte, o relógio e a superfície de exibição.

- **Funções de Controle**:
  - `handleEvents`: Captura eventos do usuário, como cliques do mouse, e atualiza o estado do jogo.
  - `mainGamePlayer`: Função principal que executa o loop do jogo, atualizando e renderizando o estado do jogo a cada quadro.

## Executando o Jogo

1. Clone o repositório ou baixe o arquivo `tictactoe.py`.
2. Navegue até o diretório onde o arquivo está localizado.
3. Execute o script:
   ```bash
   python3 tictactoe.py
   ```

## Como Jogar

- Clique em uma célula para fazer sua jogada.
- O jogo alterna automaticamente entre os jogadores (X e O).
- A inteligência artificial sugere a melhor jogada para o jogador atual no console.
- O jogo termina quando há um vencedor ou empate.

## Inteligência Artificial

A IA usa uma abordagem de busca em profundidade (DFS) para explorar todos os possíveis estados do jogo a partir do estado atual. Ela avalia cada estado sucessor e escolhe a jogada que maximiza as chances de vitória para o jogador atual (X) e minimiza as chances de vitória para o oponente (O).

## Personalização

Você pode personalizar o jogo alterando as constantes na classe `GameConstants`, como o tamanho da grade, as cores e as dimensões da tela.

## Exemplo de Saída

Ao executar o jogo, você verá uma janela com a grade do Jogo da Velha. No console, a IA sugerirá a melhor jogada para o jogador atual, como no exemplo abaixo:

```bash
Melhor jogada sugerida: (1, 1)
```

## Considerações Finais

Este projeto é uma implementação simples, mas eficaz, do Jogo da Velha com uma IA básica. Ele foi proposto e parcialmente desenvolvido pelo Prof. Daniel Cavalcanti Jeronymo, que criou a estrutura do jogo e a parte gráfica. A parte da inteligência artificial e da lógica para melhores jogadas foi desenvolvida por mim. O projeto pode ser expandido para incluir funcionalidades adicionais, como:

- Um modo de dois jogadores.
- Diferentes níveis de dificuldade.
- Uma interface gráfica mais elaborada.

Divirta-se jogando! 🎮

