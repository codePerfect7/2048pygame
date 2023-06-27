import pygame
from random import randint, choice
import colors as c

WIDTH, HEIGHT = 400, 500
FPS = 30

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048 Game')

class Game:
    def __init__(self, window):
        self.window = window
        self.matrix = [[0]*4 for _ in range(4)]    # The matrix that holds the values
        self.cells = []    # Store data about tiles and text to draw on the screen 
        self.score = [0,0]   # List to store the score in first index and data to draw in second position
        self.fontEngine = pygame.font.SysFont(c.SCORE_LABEL_FONT, 45)
        self.over = [False, False]   # First index stores whether the game is over. Second index stores whether game is lost or won
        self.startGame()
    
    def startGame(self):
        ''' Entry point for the game. Executes every time a new board is made '''

        # Adding two random tiles to the matrix
        row, col = randint(0,3), randint(0,3)
        self.matrix[row][col] = 2
        while self.matrix[row][col] != 0:
            row, col = randint(0,3), randint(0,3)
        self.matrix[row][col] = 2

        # To populate self.cells list with required data to draw
        for i in range(1,5):
            row = []
            for j in range(4):
                rect = pygame.Rect(10+j*100, 10+i*100, 80, 80)
                textRect, textSurface = None, None
                if (x:=self.matrix[i-1][j]) != 0:
                    textSurface = self.fontEngine.render(str(x), True, c.CELL_NUMBER_COLORS[x])
                    textRect = textSurface.get_rect()
                    textRect.center = rect.center
                row.append({
                    "rect": rect,
                    "textRect": textRect,
                    "textSurface": textSurface
                })
            self.cells.append(row)

        # To populate self.score with required data to draw
        scoreSurface = pygame.font.SysFont(c.SCORE_LABEL_FONT, 50).render('Score : ', True, (0,0,0))
        scoreRect = scoreSurface.get_rect()
        scoreRect.top = 25
        self.score[1] = [scoreSurface, scoreRect]
    
    def addNewTile(self):
        ''' Adds a new tile to the matrix '''
        row, col = randint(0,3), randint(0,3)
        while self.matrix[row][col] != 0:
            row, col = randint(0,3), randint(0,3)
        self.matrix[row][col] = choice([2,2,2,2,4])
    
    def horMoveExists(self):
        ''' Checks whether a horizontal move exists or not '''
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j+1] == self.matrix[i][j]:
                    return True
        return False
    
    def verMoveExists(self):
        ''' Checks whether a vertical move exists or not '''
        for i in range(3):
            for j in range(4):
                if self.matrix[i+1][j] == self.matrix[i][j]:
                    return True
        return False
    
    def gameOver(self):
        ''' Checks whether the game is over or not '''
        if any(2048 in row for row in self.matrix):
            self.over = [True, True]
        if not any(0 in row for row in self.matrix) and not self.horMoveExists() and not self.verMoveExists():
            self.over = [True, False]
    
    def updateTiles(self):
        ''' Updates self.cells with the new data when something changes it's position on the board '''
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
    
    def stack(self):
        ''' Stacks all the elements to the left of the matrix '''
        new_matrix = [[0]*4 for _ in range(4)]
        for i in range(4):
            position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][position] = self.matrix[i][j]
                    position += 1
        self.matrix = new_matrix
    
    def combine(self):
        ''' Combines two elements if they are of same value into one and updates the matrix '''
        for i in range(4):
            for j in range(3):
                x = self.matrix[i][j]
                if x != 0 and x == self.matrix[i][j+1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j+1] = 0
                    self.score[0] += self.matrix[i][j]
        
    def reverse(self):
        ''' Mirrors the matrix. Ex. [[2,4,8,8],...] will give [[8,8,4,2],...] '''
        new_matrix = []
        for row in self.matrix:
            new_matrix.append(row[::-1])
        self.matrix = new_matrix
    
    def transpose(self):
        ''' Takes the transpose of matrix. Ref : https://www.geeksforgeeks.org/program-to-find-transpose-of-a-matrix/ '''
        new_matrix = [[0]*4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[j][i] = self.matrix[i][j]
        self.matrix = new_matrix
    
    def scs(self):
        ''' Helper function to stack, combine and stack '''
        oldmatrix = self.matrix
        self.stack()
        self.combine()
        self.stack()
        return oldmatrix

    def aug(self):
        ''' Helper function to add new tile, updating tiles and checking whether game is over '''
        self.addNewTile()
        self.updateTiles()
        self.gameOver()
    
    def left(self):
        oldmatrix = self.scs()
        if oldmatrix == self.matrix:
            return
        self.aug()
    
    def right(self):
        oldmatrix = self.matrix
        self.reverse()
        self.scs()
        self.reverse()
        if oldmatrix == self.matrix:
            return
        self.aug()
    
    def up(self):
        oldmatrix = self.matrix
        self.transpose()
        self.scs()
        self.transpose()
        if oldmatrix == self.matrix:
            return
        self.aug()

    def down(self):
        oldmatrix =self.matrix
        self.transpose()
        self.reverse()
        self.scs()
        self.reverse()
        self.transpose()
        if oldmatrix == self.matrix:
            return
        self.aug()
    
    def reset(self):
        ''' Resets the game by calling the constructor '''
        self.__init__(self.window)

def draw(window, matrix, cells, score, over):
    ''' Single function to populate the board with the elements '''
    # Background and Score label
    window.fill(c.GRID_COLOR)
    window.blit(score[1][0], score[1][1])
    # Score
    scoreSurface = pygame.font.SysFont(c.SCORE_LABEL_FONT, 50).render(str(score[0]), True, (0,0,0))
    scoreRect = scoreSurface.get_rect()
    scoreRect.top = 25
    scoreRect.left = score[1][1].right + 10
    window.blit(scoreSurface, scoreRect)
    # Cells
    for i in range(4):
        for j in range(4):
            cell = cells[i][j]
            if (x:=matrix[i][j]) != 0:
                pygame.draw.rect(window, c.CELL_COLORS[x], cell['rect'])
                window.blit(cell['textSurface'], cell['textRect'])
            elif x == 0:
                pygame.draw.rect(window, c.EMPTY_CELL_COLOR, cell['rect'])
    # Game Over
    if over[0] and over[1]:
        gameOverSurface = pygame.font.SysFont(c.SCORE_LABEL_FONT, 25).render('2048 Completed. Ctrl + q to reset', True, (0,0,0))
        gameOverRect = gameOverSurface.get_rect()
        gameOverRect.center = (WIDTH//2, HEIGHT//2)
        window.blit(gameOverSurface, gameOverRect)
    if over[0] and not over[1]:
        gameOverSurface = pygame.font.SysFont(c.SCORE_LABEL_FONT, 25).render('No moves left. Ctrl + q to reset', True, (0,0,0))
        gameOverRect = gameOverSurface.get_rect()
        gameOverRect.center = (WIDTH//2, HEIGHT//2)
        window.blit(gameOverSurface, gameOverRect)

    pygame.display.update()

def main():
    ''' Main entry point for the program '''
    running = True
    clock = pygame.time.Clock()
    game = Game(window)

    while running:
        clock.tick(FPS)

        draw(window, game.matrix, game.cells, game.score, game.over)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    game.left()
                if event.key == pygame.K_RIGHT:
                    game.right()
                if event.key == pygame.K_UP:
                    game.up()
                if event.key == pygame.K_DOWN:
                    game.down()
                if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL and game.over:
                    game.reset()
        
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
