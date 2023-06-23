import colors as c
import pygame
from random import randint, choice

WIDTH, HEIGHT = 400, 500
FPS = 30

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')

class Game:
    def __init__(self, window):
        self.window = window
        self.matrix = [[0]*4 for _ in range(4)]
        self.cells = []
        self.score = [0,0]
        self.fontEngine = pygame.font.SysFont('Helvetica',45)
        self.over = False
        self.startGame()
        self.updateTiles()
    
    def startGame(self):
        row, col = randint(0,3), randint(0,3)
        self.matrix[row][col] = 2
        while self.matrix[row][col] != 0:
            row, col = randint(0,3), randint(0,3)
        self.matrix[row][col] = 2

        for i in range(1,5):
            row = []
            for j in range(4):
                rect = pygame.Rect(10+j*100, 10+i*100,80,80)
                textRect,textSurface = None, None
                if (x:=self.matrix[i-1][j]) != 0:
                    textSurface = self.fontEngine.render(str(x), True, c.CELL_NUMBER_COLORS[x])
                    textRect = textSurface.get_rect()
                    textRect.center = rect.center
                row.append({"rect": rect, "textRect": textRect,"textSurface": textSurface})
            self.cells.append(row)
        scoreSurface = pygame.font.SysFont(c.SCORE_LABEL_FONT[0], 50).render('Score : ', True, (0,0,0))
        scoreRect = scoreSurface.get_rect()
        scoreRect.top = 25
        self.score[1] = [scoreSurface, scoreRect]
    
    def stack(self):
        new_matrix = [[0]*4 for _ in range(4)]
        for i in range(4):
            position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][position] = self.matrix[i][j]
                    position += 1
        self.matrix = new_matrix
    
    def combine(self):
        for i in range(4):
            for j in range(3):
                x=self.matrix[i][j]
                if x != 0 and x == self.matrix[i][j+1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j+1] = 0
                    self.score[0] += self.matrix[i][j]
    
    def reverse(self):
        new_matrix = []
        for row in self.matrix:
            new_matrix.append(row[::-1])
        self.matrix = new_matrix
    
    def transpose(self):
        new_matrix = [[0]*4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[j][i] = self.matrix[i][j]
        self.matrix = new_matrix

    def addNewTile(self):
        row, col = randint(0,3),randint(0,3)
        while self.matrix[row][col] != 0:
            row, col = randint(0,3),randint(0,3)
        self.matrix[row][col] = choice([2,2,2,2,4])
    
    def horMoveExists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j+1]:
                    return True
        return False
    
    def verMoveExists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i+1][j] == self.matrix[i][j]:
                    return True
        return False
    
    def gameOver(self):
        if any(2048 in row for row in self.matrix):
            pass # Game over code
        elif not any(0 in row for row in self.matrix) and not self.horMoveExists() and not self.verMoveExists():
            pass # Game over code

    def updateTiles(self):
        for i in range(4):
            for j in range(4):
                if (x:=self.matrix[i][j]) != 0:
                    textSurface = self.fontEngine.render(str(x), True, c.CELL_NUMBER_COLORS[x])
                    textRect = textSurface.get_rect()
                    textRect.center = self.cells[i][j]['rect'].center
                    self.cells[i][j]['textRect'] = textRect
                    self.cells[i][j]['textSurface'] = textSurface
                elif x == 0:
                    self.cells[i][j]['textRect'] = None
                    self.cells[i][j]['textSurface'] = None

    def scs(self):
        self.stack()
        self.combine()
        self.stack()
    
    def aug(self):
        self.addNewTile()
        self.updateTiles()
        self.gameOver()
    
    def left(self):
        self.scs()
        self.aug()
    def right(self):
        self.reverse()
        self.scs()
        self.reverse()
        self.aug()
    def up(self):
        self.transpose()
        self.scs()
        self.transpose()
        self.aug()
    def down(self):
        self.transpose()
        self.reverse()
        self.scs()
        self.reverse()
        self.transpose()
        self.aug()

def draw(window, matrix, cells, score):
    window.fill(c.GRID_COLOR)
    window.blit(score[1][0], score[1][1])
    scoreSurface = pygame.font.SysFont(c.SCORE_LABEL_FONT[0], 50).render(str(score[0]), True, (0,0,0))
    scoreRect = scoreSurface.get_rect()
    scoreRect.top = 25
    scoreRect.left = score[1][1].right + 10
    window.blit(scoreSurface, scoreRect)
    for i in range(4):
        for j in range(4):
            cell=cells[i][j]
            if (x:=matrix[i][j]) != 0:
                pygame.draw.rect(window, c.CELL_COLORS[x], cell['rect'])
                window.blit(cell['textSurface'], cell['textRect'])
            elif x == 0:
                pygame.draw.rect(window, c.EMPTY_CELL_COLOR, cell['rect'])

    pygame.display.update()

def main():
    running = True
    clock = pygame.time.Clock()
    game = Game(window)

    while running:
        clock.tick(FPS)
        draw(window, game.matrix, game.cells, game.score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    game.left()
                elif event.key == pygame.K_RIGHT:
                    game.right()
                elif event.key == pygame.K_UP:
                    game.up()
                elif event.key == pygame.K_DOWN:
                    game.down()

    pygame.quit()

if __name__ == "__main__":
    main()