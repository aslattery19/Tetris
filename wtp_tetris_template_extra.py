from graphics import *
import random


############################################################
# BLOCK CLASS
############################################################

class Block(Rectangle):
    ''' Block class:
        Implement a block for a tetris piece
        Attributes: x - type: int
                    y - type: int
        specify the position on the tetris board
        in terms of the square grid
    '''

    BLOCK_SIZE = 30
    OUTLINE_WIDTH = 3

    def __init__(self, pos, color):
        self.x = pos.x
        self.y = pos.y
        
        p1 = Point(pos.x*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH,
                   pos.y*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH)
        p2 = Point(p1.x + Block.BLOCK_SIZE, p1.y + Block.BLOCK_SIZE)

        Rectangle.__init__(self, p1, p2)
        self.setWidth(Block.OUTLINE_WIDTH)
        self.setFill(color)
        self.setOutline('seashell4')

        

    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool
                        
            checks if the block can move dx squares in the x direction
            and dy squares in the y direction
            Returns True if it can, and False otherwise
        '''
##        if board.can_move(self.x + dx, self.y + dy) == True:
##            return True
##
##        elif board.can_move(self.x + dx, self.y + dy) == False:
##            return False
        return board.can_move(self.x + dx, self.y + dy)
    
    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int
                        
            moves the block dx squares in the x direction
            and dy squares in the y direction
        '''
        self.x += dx
        self.y += dy

        Rectangle.move(self, dx*Block.BLOCK_SIZE, dy*Block.BLOCK_SIZE)

############################################################
# SHAPE CLASS
############################################################

class Shape(object):
    ''' Shape class:
        Base class for all the tetris shapes
        Attributes: blocks - type: list - the list of blocks making up the shape
                    rotation_dir - type: int - the current rotation direction of the shape
                    shift_rotation_dir - type: bool - whether or not the shape shifts rotation direction
    '''

    def __init__(self, coords, color):
        self.blocks = []
        self.rotation_dir = 1
        # A boolean to indicate if a shape shifts rotation direction or not
        self.shift_rotation_dir = False

        for pos in coords:
            self.blocks.append(Block(pos, color))

    def get_blocks(self):
        '''returns the list of blocks
        '''
        return self.blocks

    def draw(self, win):
        ''' Parameter: win - type: CanvasFrame

            Draws the shape:
            i.e. draws each block
        ''' 
        for block in self.blocks:
            block.draw(win)

    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            moves the shape dx squares in the x direction
            and dy squares in the y direction, i.e.
            moves each of the blocks
        '''
        for block in self.blocks:
            block.move(dx, dy)

    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool
                        
            checks if the shape can move dx squares in the x direction
            and dy squares in the y direction
            Returns True if all of them can, and False otherwise
        '''
        for block in self.blocks:
            if block.can_move(board, dx, dy) == False:
                return False
        return True
                
    
    def can_rotate(self, board):
        ''' Parameters: board - type: Board object
            Return value: type : bool
            
            Checks if the shape can be rotated, return True
            if it can, False otherwise
        '''
        
        for block in self.blocks:
            x = self.center_block.x - self.rotation_dir*self.center_block.y + self.rotation_dir*block.y
            y = self.center_block.y + self.rotation_dir*self.center_block.x - self.rotation_dir*block.x
            if board.can_move(x, y) == False:
                return False
        return True

    def rotate(self, board):
        ''' Parameters: board - type: Board object

            rotates the shape in the direction
            specified by the value returned by
            rotation_dir
        '''
        for block in self.blocks:
             x = (self.center_block.x - self.rotation_dir*self.center_block.y + self.rotation_dir*block.y) - block.x
             y = (self.center_block.y + self.rotation_dir*self.center_block.x - self.rotation_dir*block.x) - block.y
             block.move(x,y)
             
        if self.shift_rotation_dir :
            self.rotation_dir *= -1
        

        

############################################################
# ALL SHAPE CLASSES
############################################################

 
class I_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x + 2, center.y)]
        Shape.__init__(self, coords, 'blue')
        self.center_block = self.blocks[1]
        self.rotation_dir = -1
        self.shift_rotation_dir = True
    
class J_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, 'orange')
        self.center_block = self.blocks[1]

class L_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'cyan')
        self.center_block = self.blocks[1]

class O_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x    , center.y + 1),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'red')
        self.center_block = self.blocks[0]

    def can_rotate(self, board):
        return False

class S_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'green')
        self.center_block = self.blocks[0]
        self.shift_rotation_dir = True

class T_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x    , center.y + 1)]
        Shape.__init__(self, coords, 'yellow')
        self.center_block = self.blocks[1]

class Z_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y), 
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, 'magenta')
        self.center_block = self.blocks[1]
        self.shift_rotation_dir = True



############################################################
# BOARD CLASS
############################################################

class Board(object):
    ''' Board class: it represents the Tetris board

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:CanvasFrame - where the pieces will be drawn
                    grid - type:Dictionary - keeps track of the current state of
                    the board; stores the blocks for a given position
    '''
    
    def __init__(self, win, width, height):
        self.width = width
        self.height = height

        # create a canvas to draw the tetris shapes on
        self.canvas = CanvasFrame(win, self.width * Block.BLOCK_SIZE,
                                        self.height * Block.BLOCK_SIZE)
        self.canvas.setBackground('black')

        # create an empty dictionary
        # currently we have no shapes on the board
        self.grid = {}

    def draw_shape(self, shape):
        ''' Parameters: shape - type: Shape
            Return value: type: bool

            draws the shape on the board if there is space for it
            and returns True, otherwise it returns False
        '''
        if shape.can_move(self, 0, 0):
            shape.draw(self.canvas)
            return True
        return False

    def can_move(self, x, y):
        ''' Parameters: x - type:int
                        y - type:int
            Return value: type: bool

            1. check if it is ok to move to square x,y
            if the position is outside of the board boundaries, can't move there
            return False

            2. if there is already a block at that postion, can't move there
            return False

            3. otherwise return True
        '''
        if x < 0 or x >= self.width or y >= self.height:
            return False
        elif (x,y) in self.grid:
            return False
        else:
            return True

        

    def add_shape(self, shape):
        ''' Parameter: shape - type:Shape
            
            add a shape to the grid, i.e.
            add each block to the grid using its
            (x, y) coordinates as a dictionary key

            Hint: use the get_blocks method onShape to
            get the list of blocks
        '''
        for block in shape.get_blocks():
            self.grid[(block.x, block.y)] = block

    def delete_row(self, y):
        ''' Parameters: y - type:int

            delete all the blocks in row y from the grid
            and erase them from the canvas
        '''
        for x in range(10):
            block = self.grid[x,y]
            block.undraw()
            del self.grid[x,y]
            
    
    def is_row_complete(self, y):        
        ''' Parameter: y - type: int
            Return value: type: bool

            check if all the squares in row y are occupied.
            return True if they are, False otherwise
        '''
        for x in range(0, 10) :
            if (x, y) not in self.grid:
                return False
        return True
    
    def move_down_rows(self, y_start):
        ''' Parameters: y_start - type:int                        

            move all the blocks in each row starting at y_start and up
            down 1 square
            Note: make sure you update the grid as well.
        '''
        

        for row in range(y_start, 0, -1):
            for column in range(10):
                if (column, row) in self.grid:
                    block = self.grid[(column, row)]
                    del self.grid[column, row]
                    block.move(0,1)
                    self.grid[(block.x, block.y)] = block
                    
    
    def remove_complete_rows(self, score, scoreboard):
        ''' removes all the complete rows
            and moves all rows above them down
        '''
        for y in range(20):
            if self.is_row_complete(y) == True:
                self.delete_row(y)
                self.move_down_rows(y - 1)
                score += 1
                scoreboard.update_score(score)
        return score
          

                

    def game_over(self):
        ''' display "Game Over !!!" message in the center of the board
            HINT: use the Tremove_complete_rows(seext class from the graphics library
        '''
        self.text = Text(Point(150,250), 'Game Over!')
        self.text.setFace('arial')
        self.text.setSize(36)
        self.text.setTextColor('white')
        self.text.setStyle('bold')
        self.text.draw(self.canvas)
        win = Window("WTP Tetris")
        game = WTPTetris(win)
        win.mainloop()

    

############################################################
# SCOREBOARD CLASS
############################################################

class Scoreboard(object):
    '''Scoreboard class: it represents the scoreboard

        Attributes:
    '''

    def __init__(self, win, width, height, score):
        self.width = width 
        self.height = height
        self.score = score
        #self.level = 

        # create a canvas to draw the scoreboard on
        self.scoreboard = CanvasFrame(win,self.width * Block.BLOCK_SIZE,
                                        self.height * Block.BLOCK_SIZE)
        self.scoreboard.setBackground('gray')
        self.text = Text(Point(145, 15), 'Scoreboard')
        self.text.setFace('arial')
        self.text.setSize(15)
        self.text.setTextColor('black')
        self.text.draw(self.scoreboard)

        self.text2 = Text(Point(30, 40), "Score:")
        self.text2.draw(self.scoreboard)

        self.text3 = Text(Point(65, 40), self.score)
        self.text3.draw(self.scoreboard)
        self.text3.setText(self.score)

        self.text4 = Text(Point (200, 40), 'Level:')
        self.text4.draw(self.scoreboard)

        self.text5 = Text(Point(230, 40), 1)
        self.text5.draw(self.scoreboard)
        

    def update_score(self, score):
        self.text3.setText(score)


    def levels(self, score, delay):
        if score < 10:
            delay = 1000
            self.text5.setText(1)
        elif score >= 10 and score < 20:
            delay = 800
            self.text5.setText(2)
        elif score >= 20 and score < 30:
            delay = 600
            self.text5.setText(3)
        elif score >= 30 and score < 40:
            delay = 400
            self.text5.setText(4)
        elif score >= 40 and score < 50:
            delay = 200
            self.text5.setText(5)
        elif score >= 50 and score < 60:
            delay = 100
            self.text5.setText(6)

        return delay
    

        
    

############################################################
# WTP TETRIS CLASS
############################################################

class WTPTetris(object):
    ''' WTPTetris class: Controls the game play
        Attributes:
            SHAPES - type: list (list of Shape classes)
            DIRECTION - type: dictionary - converts string direction to (dx, dy)
            BOARD_WIDTH - type:int - the width of the board
            BOARD_HEIGHT - type:int - the height of the board
            board - type:Board - the tetris board
            win - type:Window - the window for the tetris game
            delay - type:int - the speed in milliseconds for moving the shapes
            current_shapes - type: Shape - the current moving shape on the board
    '''
    
    SHAPES = [I_shape, J_shape, L_shape, O_shape, S_shape, T_shape, Z_shape]
    DIRECTION = {'Left':(-1, 0), 'Right':(1, 0), 'Down':(0, 1),}
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
    SCOREBOARD_WIDTH = 10
    SCOREBOARD_HEIGHT = 2

    PREVIEW_WIDTH = 10
    PREVIEW_HEIGHT = 5

    
    def __init__(self, win):
        self.board = Board(win, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.win = win
         #creating scoreboard
        self.score = 0
        self.delay = 1000
        self.scoreboard = Scoreboard(win, self.SCOREBOARD_WIDTH,
                                     self.SCOREBOARD_HEIGHT, self.score)
 
        
        self.delay = self.scoreboard.levels(self.score, 1000) #ms

        # sets up the keyboard events
        # when a key is called the method key_pressed will be called
        self.win.bind_all('<Key>', self.key_pressed)

        # set the current shape to a random new shape
        self.current_shape = self.create_new_shape()
        self.current_shape.draw(self.board.canvas)
        self.animate_shape()

 


    def create_new_shape(self):
        ''' Return value: type: Shape
            
            create a random new shape that is centered
            at the top center of the board
            return the shape
        '''
        rand = random.randint(1,7)
        if rand == 1:
            return I_shape(Point(4,0))
        if rand == 2:
            return J_shape(Point(4,0))
        if rand == 3:
            return L_shape(Point(4,0))
        if rand == 4:
            return O_shape(Point(4,0))
        if rand == 5:
            return S_shape(Point(4,0))
        if rand == 6:
            return T_shape(Point(4,0))
        if rand == 7:
            return Z_shape(Point(4,0))
    
    def animate_shape(self):
        ''' animate the shape - move down at equal intervals
            specified by the delay attribute
        '''
        self.delay = self.scoreboard.levels(self.score, self.delay)
        
        self.do_move('Down')
        self.win.after(self.delay, self.animate_shape)
    
    def do_move(self, direction):
        ''' Parameters: direction - type: string
            Return value: type: bool

            Move the current shape in the direction specified by the parameter:
            First check if the shape can move. If it can, move it and return True
            Otherwise if the direction we tried to move was 'Down',
            1. add the current shape to the board
            2. remove the completed rows if any 
            3. create a new random shape and set current_shape attribute
            4. If the shape cannot be drawn on the board, display a
               game over message

            return False
        '''
    
        if direction == 'space':
            while self.current_shape.can_move(self.board, 0,1) == True:
                self.do_move('Down')
            self.board.add_shape(self.current_shape)
            self.current_shape = self.create_new_shape()
            if not self.board.draw_shape(self.current_shape):
                self.board.game_over()
                return False
            self.score = self.board.remove_complete_rows(self.score, self.scoreboard)
            return self.current_shape

        #accesses dictionary to find the proper direction to move the shape
        self.direction = self.DIRECTION[direction]

        if self.current_shape.can_move(self.board, self.direction[0], self.direction[1]) == True:
            #moves the shape
            self.current_shape.move(self.direction[0],self.direction[1])
            return True

        elif direction == 'Down':
            self.board.add_shape(self.current_shape)
            self.current_shape = self.create_new_shape()
            if not self.board.draw_shape(self.current_shape):
                self.board.game_over()
                return False
            self.score = self.board.remove_complete_rows(self.score, self.scoreboard)
            return self.current_shape

                
    def do_rotate(self):
        ''' Checks if the current_shape can be rotated and
            rotates if it can
        '''
        if self.current_shape.can_rotate(self.board):
            self.current_shape.rotate(self.board)
    
    def key_pressed(self, event):
        ''' this function is called when a key is pressed on the keyboard
            it currenly just prints the value of the key

            Modify the function so that if the user presses the arrow keys
            'Left', 'Right' or 'Down', the current_shape will move in
            the appropriate direction

            if the user presses the space bar 'space', the shape will move
            down until it can no longer move and is added to the board

            if the user presses the 'Up' arrow key ,
                the shape should rotate.
        '''
        key = event.keysym

        if key == 'Up':
            self.do_rotate()

        #calls the do_move function for the variable 'key', which corresponds to
        #to the key that was pressed'''

        else:
            self.do_move(key)

        

        
       
################################################################
# Start the game
################################################################

win = Window("WTP Tetris")
game = WTPTetris(win)
win.mainloop()
