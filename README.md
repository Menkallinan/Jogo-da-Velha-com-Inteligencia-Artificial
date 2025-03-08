# Jogo da Velha com Inteligência Artificial

Este projeto é uma recriação do clássico Jogo da Velha, desenvolvido em Python com a biblioteca pygame. O jogo foi proposto e parcialmente desenvolvido pelo Prof. Daniel Cavalcanti Jeronymo, e inclui uma inteligência artificial (IA) que sugere a melhor jogada para o jogador atual. A IA utiliza o algoritmo Minimax para avaliar os possíveis estados do jogo e tomar decisões ótimas.

## Funcionalidades

- **Jogo da Velha tradicional**: Jogue em uma grade 3x3, alternando entre vermelho e azul.
- **Inteligência Artificial**: A IA sugere a melhor jogada para o jogador atual, vermelho ou azul.
- **Interface gráfica**: Desenvolvida com pygame, proporcionando uma experiência visual e interativa.
- **Algoritmo Minimax**: A IA usa o Minimax para calcular jogadas ótimas, garantindo que o jogo seja desafiador.

## Requisitos

Para executar este projeto, você precisará das seguintes dependências:

- Python 3.x
- Biblioteca pygame
- Biblioteca numpy

## Instalação das Dependências

1. **Instale o Python 3.x**:
   Certifique-se de que o Python 3.x está instalado no seu sistema. Você pode verificar a versão do Python com o comando:
   ```bash
   python3 --version
   ```

2. **Instale o pygame**:
   Se ainda não tiver o pygame instalado, você pode instalá-lo usando o pip:
   ```bash
   pip3 install pygame
   ```

3. **Instale o numpy**:
   O numpy é usado para manipulação de matrizes. Instale-o com:
   ```bash
   pip3 install numpy
   ```

## Estrutura do Código

O código está organizado em classes e funções principais:

### Classes Principais

- **GameConstants**:
  - Contém constantes usadas no jogo, como cores, dimensões da tela, tamanho da grade e configurações de fonte.

- **Game**:
  - Gerencia o estado do jogo, incluindo a grade, o jogador atual e a lista de estados anteriores.
  - Métodos principais:
    - `generateSuccessors`: Gera todos os possíveis estados sucessores a partir do estado atual.
    - `minimax`: Implementa o algoritmo Minimax para avaliar os estados do jogo.
    - `oracle`: Usa o Minimax para sugerir a melhor jogada para o jogador atual.
    - `checkObjectiveState`: Verifica se o jogo terminou (vitória, derrota ou empate).
    - `update`: Atualiza o estado do jogo com base nas entradas do usuário.

### Funções de Renderização

- `drawGrid`: Desenha a grade do jogo na tela, colorindo as células com base no estado atual.
- `initialize`: Inicializa o pygame, a fonte, o relógio e a superfície de exibição.

### Funções de Controle

- `handleEvents`: Captura eventos do usuário, como cliques do mouse, e atualiza o estado do jogo.
- `mainGamePlayer`: Função principal que executa o loop do jogo, atualizando e renderizando o estado do jogo a cada quadro.

## Como Executar

1. Clone o repositório ou baixe o arquivo `tictactoe.py`.
2. Navegue até o diretório onde o arquivo está localizado.
3. Execute o script:
   ```bash
   python3 tictactoe.py
   ```

## Como Jogar

- Clique em uma célula para fazer sua jogada.
- O jogo alterna automaticamente entre os jogadores (vermelho e azul).
- A IA sugere a melhor jogada para o jogador atual no console.
- O jogo termina quando há um vencedor ou empate.

## Inteligência Artificial

A IA usa o algoritmo Minimax para explorar todos os possíveis estados do jogo a partir do estado atual. Ela avalia cada estado sucessor e escolhe a jogada que:

- Maximiza as chances de vitória para vermelho.
- Minimiza as chances de vitória para azul.

## Melhorias Implementadas

- A função `minimax` foi ajustada para garantir que a IA sugira jogadas ótimas para ambos os jogadores (vermelho e azul).
- A função `oracle` diferencia entre vermelho e azul, chamando o Minimax com os parâmetros corretos.

## Exemplo de Saída

Ao executar o jogo, você verá uma janela com a grade do Jogo da Velha. Na primeira rodada, não haverá sugestão de jogada pelo console; essa análise ocorrerá após a primeira escolha do jogador vermelho.
<img src="https://github.com/user-attachments/assets/beefdda1-ffa3-408c-bb99-e417719cb325" alt="Nova descrição" style="max-width: 100%; height: auto;">

```bash
Melhor jogada sugerida: (0, 1)
```

## Considerações Finais

Este projeto foi proposto e parcialmente desenvolvido pelo Prof. Daniel Cavalcanti Jeronymo, e a parte da inteligência artificial foi implementada por mim. A IA agora sugere jogadas ótimas para ambos os jogadores, tornando o jogo mais desafiador e justo.

Divirta-se jogando! 🎮

