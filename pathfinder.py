# import modules
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from actor import TILE_SIZE

# pathfinder class handles all the pathfinding


class Pathfinder:
    def __init__(self, matrix):
        self.matrix = matrix
        for row in range(0, len(self.matrix)):
            for col in range(0, len(self.matrix[0])):
                if self.matrix[row][col] == "-1":
                    self.matrix[row][col] = "1"
                else:
                    self.matrix[row][col] = "0"

        self.grid = Grid(matrix=self.matrix)
        # pathfinding
        self.path = []

    def empty_path(self):
        self.path = []

    def create_path(self, x, y, player):
        # start
        start_x, start_y = x//TILE_SIZE, y//TILE_SIZE
        start = self.grid.node(start_x, start_y)

        # end
        for p in player:
            # replace with tile size
            end_x, end_y = p.rect.centerx // TILE_SIZE, p.rect.centery // TILE_SIZE
        end = self.grid.node(end_x, end_y)
        # path
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        self.path, _ = finder.find_path(start, end, self.grid)
        self.grid.cleanup()

    def update(self, x, y, player):
        self.create_path(x, y, player)
