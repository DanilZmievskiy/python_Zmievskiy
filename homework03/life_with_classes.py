import pygame
import random
from pygame.locals import *
from pprint import pprint as pp
from copy import deepcopy


class GameOfLife:
    def __init__(self, width=640, height=480, cell_size=10, speed=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self):
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        clist = CellList(self.cell_width, self.cell_height, True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_grid()
            self.draw_cell_list(clist)

            clist = CellList.update(clist)

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def draw_cell_list(self, clist) -> None:

        for cell in clist:

            color_cell = pygame.Color('white')

            if cell.is_alive():
                color_cell = pygame.Color('green')

            rect = Rect(cell.row * self.cell_size+1, cell.col * self.cell_size+1, self.cell_size-1, self.cell_size-1)
            pygame.draw.rect(self.screen, color_cell, rect)


class Cell:

    def __init__(self, row: int, col: int, state: bool = False) -> None:
        self.row = row
        self.col = col
        self.state = state

    def is_alive(self) -> bool:
        return self.state


class CellList:

    def __init__(self, nrows: int, ncols: int, randomize: bool = True) -> None:
        self.nrows = nrows
        self.ncols = ncols
        if randomize:
            self.grid = [[Cell(i, j, random.randint(0, 1))
                          for j in range(self.ncols)]
                         for i in range(self.nrows)]
        else:
            self.grid = [[Cell(i, j, 0)
                          for j in range(self.ncols)]
                         for i in range(self.nrows)]

    def get_neighbours(self, cell: tuple) -> list:
        neighbours = []
        row, col = cell.row, cell.col
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i in range(0, self.nrows - 1) and j in range(0, self.ncols - 1) and (i != row or j != col):
                    neighbours.append(self.grid[i][j])
        return neighbours

    def update(self):
        new_clist = deepcopy(self.grid)
        for cell in self:
            neighbours = self.get_neighbours(cell)
            neighbour_alive = sum(c.is_alive() for c in neighbours)
            if cell.is_alive():
                if neighbour_alive < 2 or neighbour_alive > 3:
                    new_clist[cell.row][cell.col].state = 0
            else:
                if neighbour_alive == 3:
                    new_clist[cell.row][cell.col].state = 1
        self.grid = new_clist
        return self

    def __iter__(self):
        self.count_rows = 0
        self.count_cols = 0
        return(self)

    def __next__(self):
        if (self.count_rows == self.nrows):
            raise StopIteration

        cell = self.grid[self.count_rows][self.count_cols]
        self.count_cols += 1
        if self.count_cols == self.ncols:
            self.count_rows += 1
            self.count_cols = 0

        return cell

    def __str__(self) -> str:
        str = ""
        for i in range(self.nrows):
            for j in range(self.ncols):
                if (self.grid[i][j].state):
                    str += '1 '
                else:
                    str += '0 '
            str += '\n'
        return str

    @classmethod
    def from_file(cls, filename: str):
        grid = []
        with open(filename) as f:
            for i, line in enumerate(f):
                grid.append([Cell(i, j, int(c))
                             for j, c in enumerate(line) if c in '01'])
        clist = cls(len(grid), len(grid[0]), False)
        clist.grid = grid
        return clist


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()