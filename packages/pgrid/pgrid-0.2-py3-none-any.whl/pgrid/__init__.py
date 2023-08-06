import pygame

class cell():
    Position = None
    Value = None
    Direction = None
    def __init__(self, Position: tuple, Value: int = 0, Direction: tuple = None):
        self.Position = Position
        self.Value = Value
        self.Direction = Direction
    
    def modify(self, Value: int = Value, Direction: tuple = Direction):
        self.Value = Value
        self.Direction = Direction

class board():
    widthPixels = None
    cellsPerLine = None
    Colors = None

    data: list [cell] = []
    def __init__(self, widthPixels: int = 500, cellsPerLine: int = 20, Colors = [(255,255,255),(255,0,0),(0,255,0),(0,0,255)]):
        self.widthPixels = widthPixels
        self.cellsPerLine = cellsPerLine
        self.Colors = Colors
      # Setup first time data:
        for i in range(cellsPerLine**2):
            cell_ = cell(Position=(i%cellsPerLine,i//cellsPerLine), Value=0)
            self.data.append(cell_)
    
    def find(self, xPos, yPos):
        for x in self.data:
            if x.Position == (xPos,yPos):
                desiredCell = x
        return desiredCell
    
    def drawBoard(self, Screen):
        squerePixel = self.widthPixels/self.cellsPerLine
      # Color the background
        for cell_ in self.data:
            rect = pygame.Rect(cell_.Position[0], cell_.Position[1], squerePixel, squerePixel)
            pygame.draw.rect(Screen, self.Colors[cell_.Value], rect)

      # Draw the lines
        blockSize = self.widthPixels/self.cellsPerLine
        for x in range(0, self.widthPixels, blockSize):
            for y in range(0, self.widthPixels, blockSize):
                rect = pygame.Rect(x,y, blockSize, blockSize)
                pygame.draw.rect(Screen, (0,0,0), rect, 1)

myBoard = board()
myBoard.find(0,0).modify(Value=3)
myBoard.find(0,1).modify(Value=2)

print([x.Value for x in myBoard.data])
