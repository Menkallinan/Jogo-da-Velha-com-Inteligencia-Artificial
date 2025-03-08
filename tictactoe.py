# -*- coding: utf-8 -*-
"""
Recriação do Jogo da Velha

@author: Prof. Daniel Cavalcanti Jeronymo
"""

import pygame
import sys
import os
import traceback
import random
import numpy as np
import copy


class GameConstants:
    #              R    G    B
    ColorWhite = (255, 255, 255)
    ColorBlack = (0, 0, 0)
    ColorRed = (255, 0, 0)
    ColorBlue = (0, 0, 255)
    BackgroundColor = ColorBlack

    screenScale = 1
    screenWidth = screenScale * 600
    screenHeight = screenScale * 600

    # Grid size in units
    gridWidth = 3
    gridHeight = 3

    # Grid size in pixels
    gridMarginSize = 5
    gridCellWidth = screenWidth // gridWidth - 2 * gridMarginSize
    gridCellHeight = screenHeight // gridHeight - 2 * gridMarginSize

    randomSeed = 0
    FPS = 30
    fontSize = 20


class Game:
    class GameState:
        def __init__(self):
            # 0 empty, 1 X, 2 O
            self.grid = np.zeros((GameConstants.gridHeight, GameConstants.gridWidth), dtype=int)
            self.currentPlayer = 1

    def __init__(self, expectUserInputs=True):
        self.expectUserInputs = expectUserInputs

        # Game state list - stores a state for each time step (initial state)
        self.states = [Game.GameState()]

        # Determines if simulation is active or not
        self.alive = True

        # Journal of inputs by users (stack)
        self.eventJournal = []

    def generateSuccessors(self, gs):
        successors = []
        for row in range(GameConstants.gridHeight):
            for col in range(GameConstants.gridWidth):
                if gs.grid[row][col] == 0:  # Empty cell
                    new_gs = copy.deepcopy(gs)
                    new_gs.grid[row][col] = new_gs.currentPlayer
                    new_gs.currentPlayer = 3 - new_gs.currentPlayer  # Alternate player (1 -> 2, 2 -> 1)
                    successors.append((row, col, new_gs))
        return successors

    def dfs(self, gs, visited):
        # Serialize grid to check for revisited states
        grid_tuple = tuple(map(tuple, gs.grid))
        if grid_tuple in visited:
            return 0  # Empate (estado já visitado)
        visited.add(grid_tuple)

        # Check if the current state is a winning state
        result = self.checkObjectiveState(gs)
        if result != 0:
            return 1 if result == 1 else -1 if result == 2 else 0

        # Generate successors
        successors = self.generateSuccessors(gs)
        if not successors:
            return 0  # Empate se não houver movimentos possíveis

        # Avaliar cada estado sucessor
        scores = []
        for _, _, new_gs in successors:
            scores.append(self.dfs(new_gs, visited.copy()))

        # Escolher o melhor resultado para o jogador atual
        if gs.currentPlayer == 1:
            return max(scores)
        else:
            return min(scores)


    def oracle(self):
        gs = self.states[-1]  # Estado game atual
        best_score = -float('inf')
        best_move = None

        for row, col, new_gs in self.generateSuccessors(gs):
            score = self.dfs(new_gs, set())
            if score > best_score:
                best_score = score
                best_move = (row, col)

        return best_move

    def checkObjectiveState(self, gs):
        
        for i in range(GameConstants.gridHeight):
            if np.all(gs.grid[i, :] == 1) or np.all(gs.grid[:, i] == 1):
                return 1
            if np.all(gs.grid[i, :] == 2) or np.all(gs.grid[:, i] == 2):
                return 2

        # Checagem diagnoias
        if np.all(np.diag(gs.grid) == 1) or np.all(np.diag(np.fliplr(gs.grid)) == 1):
            return 1
        if np.all(np.diag(gs.grid) == 2) or np.all(np.diag(np.fliplr(gs.grid)) == 2):
            return 2

    
        if not np.any(gs.grid == 0):
            return 3

        # Sem vencedores
        return 0

    def update(self):
        if not self.alive or not self.eventJournal:
            return

        # Get the current (last) game state
        gs = copy.deepcopy(self.states[-1])

        # Mark the cell clicked by this player if it's an empty cell
        x, y = self.eventJournal.pop()

        # Check if in bounds
        if 0 <= x < GameConstants.gridHeight and 0 <= y < GameConstants.gridWidth and gs.grid[x][y] == 0:
            gs.grid[x][y] = gs.currentPlayer
            gs.currentPlayer = 3 - gs.currentPlayer  # Switch player

            # check if end of game
            if self.checkObjectiveState(gs):
                self.alive = False

           # Add the new modified state
            self.states.append(gs)


def drawGrid(screen, game):
    screen.fill(GameConstants.BackgroundColor)

    # Get the current game state
    gs = game.states[-1]
    grid = gs.grid

    # Draw the grid
    for row in range(GameConstants.gridHeight):
        for col in range(GameConstants.gridWidth):
            color = GameConstants.ColorWhite
            if grid[row][col] == 1:
                color = GameConstants.ColorRed
            elif grid[row][col] == 2:
                color = GameConstants.ColorBlue

            m = GameConstants.gridMarginSize
            w = GameConstants.gridCellWidth
            h = GameConstants.gridCellHeight
            pygame.draw.rect(screen, color, [(2 * m + w) * col + m, (2 * m + h) * row + m, w, h])


def initialize():
    random.seed(GameConstants.randomSeed)
    pygame.init()
    game = Game()
    font = pygame.font.SysFont('Courier', GameConstants.fontSize)
    fpsClock = pygame.time.Clock()

    # Create display surface
    screen = pygame.display.set_mode((GameConstants.screenWidth, GameConstants.screenHeight), pygame.DOUBLEBUF)
    screen.fill(GameConstants.BackgroundColor)

    return screen, font, game, fpsClock


def handleEvents(game):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            col = pos[0] // (GameConstants.screenWidth // GameConstants.gridWidth)
            row = pos[1] // (GameConstants.screenHeight // GameConstants.gridHeight)
            game.eventJournal.append((row, col))

            # Atualizar o estado do jogo antes de sugerir a melhor jogada
            game.update()

            # Sugerir a melhor jogada usando o oracle
            if game.alive:  # Certificar que o jogo ainda está em andamento
                best_move = game.oracle()
                if best_move:
                    print(f"Melhor jogada sugerida: {best_move}")

        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

def mainGamePlayer():
    try:
        # Initialize pygame and etc.
        screen, font, game, fpsClock = initialize()

        # Main game loop
        while game.alive:
            # Handle events
            handleEvents(game)

            # Update world
            game.update()

            # Draw this world frame
            drawGrid(screen, game)
            pygame.display.flip()

            # Delay for required FPS
            fpsClock.tick(GameConstants.FPS)

        # Close pygame
        pygame.quit()
    except SystemExit:
        pass
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        pygame.quit()


if __name__ == "__main__":
    file_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(file_path)

    mainGamePlayer()
