# -*- coding: utf-8 -*-
"""
Recriação do Jogo da Velha do Prof. Daniel Cavalcanti Jeronymo
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
            self.currentPlayer = 1  # Começa com o jogador X

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

    def minimax(self, gs, depth, isMaximizing):
        result = self.checkObjectiveState(gs)
        if result == 1:  # Vitória de X
            return 10 - depth
        elif result == 2:  # Vitória de O
            return depth - 10
        elif result == 3:  # Empate
            return 0

        if isMaximizing:  # Jogador X (maximiza)
            best_score = -float('inf')
            for _, _, new_gs in self.generateSuccessors(gs):
                score = self.minimax(new_gs, depth + 1, False)
                best_score = max(best_score, score)
            return best_score
        else:  # Jogador O (minimiza)
            best_score = float('inf')
            for _, _, new_gs in self.generateSuccessors(gs):
                score = self.minimax(new_gs, depth + 1, True)
                best_score = min(best_score, score)
            return best_score

    def oracle(self):
        gs = self.states[-1]  # Estado atual do jogo
        best_score = -float('inf') if gs.currentPlayer == 1 else float('inf')
        best_move = None

        for row, col, new_gs in self.generateSuccessors(gs):
            # Se o jogador atual é X, maximiza; se é O, minimiza
            isMaximizing = gs.currentPlayer == 1
            score = self.minimax(new_gs, 0, not isMaximizing)

            if (gs.currentPlayer == 1 and score > best_score) or (gs.currentPlayer == 2 and score < best_score):
                best_score = score
                best_move = (row, col)

        return best_move

    def checkObjectiveState(self, gs):
        for i in range(GameConstants.gridHeight):
            if np.all(gs.grid[i, :] == 1) or np.all(gs.grid[:, i] == 1):
                return 1  # Vitória de X
            if np.all(gs.grid[i, :] == 2) or np.all(gs.grid[:, i] == 2):
                return 2  # Vitória de O

        if np.all(np.diag(gs.grid) == 1) or np.all(np.diag(np.fliplr(gs.grid)) == 1):
            return 1  # Vitória de X
        if np.all(np.diag(gs.grid) == 2) or np.all(np.diag(np.fliplr(gs.grid)) == 2):
            return 2  # Vitória de O

        if not np.any(gs.grid == 0):
            return 3  # Empate

        return 0  # Jogo ainda em andamento

    def update(self):
        if not self.alive or not self.eventJournal:
            return

        gs = copy.deepcopy(self.states[-1])
        x, y = self.eventJournal.pop()

        if 0 <= x < GameConstants.gridHeight and 0 <= y < GameConstants.gridWidth and gs.grid[x][y] == 0:
            gs.grid[x][y] = gs.currentPlayer
            gs.currentPlayer = 3 - gs.currentPlayer  # Alternar jogador

            if self.checkObjectiveState(gs):
                self.alive = False

            self.states.append(gs)


def drawGrid(screen, game):
    screen.fill(GameConstants.BackgroundColor)

    gs = game.states[-1]
    grid = gs.grid

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

            game.update()

            if game.alive:
                best_move = game.oracle()
                if best_move:
                    print(f"Melhor jogada sugerida: {best_move}")

        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()


def mainGamePlayer():
    try:
        screen, font, game, fpsClock = initialize()

        while game.alive:
            handleEvents(game)
            game.update()
            drawGrid(screen, game)
            pygame.display.flip()
            fpsClock.tick(GameConstants.FPS)

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
