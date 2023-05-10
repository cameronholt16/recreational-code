import random
import copy
import tkinter as tk

class Board:
    
    def __init__(self, position = None):
        if position == None: # If I didn't specify the position of the board when I made it, create starting board
            self.position = [
                ['Black Rook', 'Black Knight', 'Black Bishop', 'Black Queen', 'Black King', 'Black Bishop', 'Black Knight', 'Black Rook'], #black's back rank
                ['Black Pawn', 'Black Pawn', 'Black Pawn', 'Black Pawn', 'Black Pawn', 'Black Pawn', 'Black Pawn', 'Black Pawn'],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                ['White Pawn', 'White Pawn', 'White Pawn', 'White Pawn', 'White Pawn', 'White Pawn', 'White Pawn', 'White Pawn'],
                ['White Rook', 'White Knight', 'White Bishop', 'White Queen', 'White King', 'White Bishop', 'White Knight', 'White Rook']
                ]
            
            self.turn_player = 'White'
            self.not_turn_player = 'Black' #surprisingly useful variable
            #the next few things track things relating to whether castling is legal
            self.white_king_moved = False
            self.white_queen_rook_moved = False #count not being on the board as moving, so we don't castle into a non-existent rook
            self.white_king_rook_moved = False
            self.black_king_moved = False
            self.black_queen_rook_moved = False
            self.black_king_rook_moved = False
            #the following tracks something important for checking if en passant is possible
            self.pawn_just_moved_two = False
            #the following is for the 50 move_rule
            self.consecutive_boring_moves = 0 #Remember to declare a draw at 100 (2x50). Or is it just when someone wants one? Google it
            self.white_king_castled = False #this is for the position evaluator. castling is good
            self.black_king_castled = False
            self.move_count = 0 #number of moves made

    def change_turn_player(self):
        if self.turn_player == 'White':
            self.turn_player = 'Black'
            self.not_turn_player = 'White'
        else:
            self.turn_player = 'White'
            self.not_turn_player = 'Black'
    
    def print_position(self):
        for row in self.position:
            print(row)
    
    def make_move(self, start, finish, promote_to = None): # start and finish are lists of 2 digits each. [row index, column index. 0, 0 is top left]
        #promote_to should be set when promoting. For now, to sth like 'Queen'. I'll grab the colour from the turn player.
        #The following updates the 'has such-and-such piece moved' checker for castling
        if start == [7, 4]: #if a piece ever moves from this square, the white king must have moved
            self.white_king_moved = True
            
        if start == [7, 0]:
            self.white_queen_rook_moved = True
            
        if start == [7, 7]:
            self.white_king_rook_moved = True
            
        if start == [0, 4]:
            self.black_king_moved = True
            
        if start == [0, 0]:
            self.black_queen_rook_moved = True
            
        if start == [0, 7]:
            self.black_king_rook_moved = True
        
        #the following fixes the 'pawn just moved two' flag to the correct value, usually 'False'
        if self.position[start[0]][start[1]] == 'White Pawn' or self.position[start[0]][start[1]] == 'Black Pawn': # if we're moving a pawn...
            if abs(finish[0] - start[0]) == 2: # and we went 2 squares forwards (either direction)
                self.pawn_just_moved_two = finish
            else: #if the pawn doesn't move two, then make sure the en passant flag is flipped. Every ineligible move should try to flip this flag
                self.pawn_just_moved_two = False
        else: # if it's not a pawn, flip the en passant flag to false
            self.pawn_just_moved_two = False
            
        #the following changes the 50-move-counter as necessary. It's a bit inefficient, because some of these checks are being made elsewhere, but I'm bunching them together for clarity
        if self.position[start[0]][start[1]] == 'White Pawn' or self.position[start[0]][start[1]] == 'Black Pawn': # pawns reset the counter
            self.consecutive_boring_moves = 0
        elif self.position[finish[0]][finish[1]] !=0: # if we land on a piece, we're taking it, so reset the counter.
            self.consecutive_boring_moves = 0
        else:
            self.consecutive_boring_moves += 1
            
        #the following checks if a rook is being taken, making sure we count it as 'moved' so we don't castle into a non-existent rook
        if finish == [0, 0]: # this doesn't actually check if the rook is being taken, but if a piece moves there, we can't castle there
            self.black_queen_rook_moved = True
        if finish == [0, 7]:
            self.black_king_rook_moved = True
        if finish == [7, 0]:
            self.white_queen_rook_moved = True
        if finish == [7, 7]:
            self.white_king_rook_moved = True
            
        # the following moves the appropriate rook, if the move was castling
        if self.position[start[0]][start[1]] == 'White King' and start == [7, 4] and finish == [7, 6]: #then we're castling kingside
            self.white_king_castled = True
            self.position[7][7] = 0 #rook moves from h1...
            self.position[7][5] = 'White Rook' #to f1
            
        if self.position[start[0]][start[1]] == 'White King' and start == [7, 4] and finish == [7, 2]: #then we're castling queenside
            self.white_king_castled = True
            self.position[7][0] = 0 #rook moves from a1...
            self.position[7][3] = 'White Rook' #to d1
            
        if self.position[start[0]][start[1]] == 'Black King' and start == [0, 4] and finish == [0, 6]: #then we're castling kingside
            self.black_king_castled = True
            self.position[0][7] = 0 #rook moves from h8...
            self.position[0][5] = 'Black Rook' #to f8
            
        if self.position[start[0]][start[1]] == 'Black King' and start == [0, 4] and finish == [0, 2]: #then we're castling queenside
            self.black_king_castled = True
            self.position[0][0] = 0 #rook moves from a8...
            self.position[0][3] = 'Black Rook' #to d8
        
        #the following takes the appropriate pawn if we're taking en passant
        if self.position[start[0]][start[1]] == 'White Pawn' or self.position[start[0]][start[1]] == 'Black Pawn':
            if self.position[finish[0]][finish[1]] == 0 and finish[1] != start[1]: # if we're moving to an empty square, but not vertically, we must be taking en passant
                if self.turn_player == 'White':
                    self.position[finish[0] + 1][finish[1]] = 0 # take the piece behind us #remember indexing goes down vertically
                else:
                    self.position[finish[0] - 1][finish[1]] = 0 # take the piece in front (from white's perspective) 
                    
        #the following actually moves the piece
        self.position[finish[0]][finish[1]] = self.position[start[0]][start[1]] #replace destiniation square with the piece on the start square
        self.position[start[0]][start[1]] = 0 # Nothing is on the start square anymore
        
        #the following handles promotion
        if (finish[0] == 0) or (finish[0] == 7): #if the destination square was on a back rank
            if self.position[finish[0]][finish[1]][6 : ] == 'Pawn': # and the piece that moved there was a pawn
                if promote_to == None:
                    raise ValueError('You have not told me what to promote to!!')
                if promote_to not in ['Rook', 'Knight', 'Bishop', 'Queen']: 
                    raise ValueError('You have not provided me a proper piece to promote to')
                new_piece = self.turn_player + ' ' + promote_to
                self.position[finish[0]][finish[1]] = new_piece
        
        #add count to move counter, used for changing eval strategy as the game progresses/
        self.move_count += 1
        #next player's turn
        self.change_turn_player()
        
    def generate_all_legal_moves(self, checks_and_captures_only = False):
        #in hindsight, the name of this function is confusing to another reader. This generates all the moves that the pieces might be able to make. It doen't bother with things like check
        legal_moves = [] # A list of lists of pairs of lists e.g. [[[0, 0], [0, 1]], [[0, 0], [0, 2]]] for moves Rb8, Rc8 from a rook on a8.
        squares_with_your_pieces_on = [] # a list of 2-element lists
        for i in range(8): #column (going down)
            for j in range(8): #row
                if self.position[i][j] != 0: # if the square isn't empty
                    if self.position[i][j][:5] == self.turn_player: #if the piece is yours
                        squares_with_your_pieces_on.append([i, j])

        for square in squares_with_your_pieces_on:
            if self.position[square[0]][square[1]][6:] == 'Rook': #increase/decrease column/row number.
                #stop at your piece exclusive and their piece inclusive
                rook_destinations = [] #list of destination squares. be careful if this is empty!
                
                #going down
                for i in range(7): #can only ever go 7 in one direction
                    if square[0] + i + 1 == 8: #we have fallen off the bottom
                        break
                    elif self.position[square[0] + i + 1][square[1]] == 0: #if the square is empty
                        rook_destinations.append([square[0] + i + 1, square[1]])
                    elif self.position[square[0] + i + 1][square[1]][ : 5] == self.turn_player: #if it's your own piece
                        break
                    else: # opponent's piece, can't go beyond it
                        rook_destinations.append([square[0] + i + 1, square[1]])
                        break                      

                #going up
                for i in range(7): #can only ever go 7 in one direction
                    if square[0] - i - 1 == -1: #we have fallen off the top
                        break
                    elif self.position[square[0] - i - 1][square[1]] == 0:
                        rook_destinations.append([square[0] - i - 1, square[1]])
                    elif self.position[square[0] - i - 1][square[1]][ : 5] == self.turn_player: #if it's your own piece
                        break
                    else: # opponent's piece, can't go beyond it
                        rook_destinations.append([square[0] - i - 1, square[1]])
                        break

                #going right
                for i in range(7): #can only ever go 7 in one direction
                    if square[1] + i + 1 == 8: #we have fallen off the right
                        break
                    elif self.position[square[0]][square[1] + i + 1] == 0:
                        rook_destinations.append([square[0], square[1] + i + 1])
                    elif self.position[square[0]][square[1] + i + 1][ : 5] == self.turn_player: #if it's your own piece
                        break
                    else: # opponent's piece, can't go beyond it
                        rook_destinations.append([square[0], square[1] + i + 1])
                        break
                
                #going left
                for i in range(7): #can only ever go 7 in one direction
                    if square[1] - i - 1 == -1: #we have fallen off the left
                        break
                    elif self.position[square[0]][square[1] - i - 1] == 0:
                        rook_destinations.append([square[0], square[1] - i - 1])
                    elif self.position[square[0]][square[1] - i - 1][ : 5] == self.turn_player: #if it's your own piece
                        break
                    else: # opponent's piece, can't go beyond it
                        rook_destinations.append([square[0], square[1] - i - 1])
                        break
                        
                if rook_destinations != []: # if the rook can move to at least one square
                    for destination in rook_destinations:
                        legal_moves.append([square, destination])
            
            elif self.position[square[0]][square[1]][6:] == 'Knight':
                knight_destinations = []
                # only ever 8 moves to consider
                
                # 2 up 1 right
                if (square[0] - 2 > -1) and (square[1] + 1 < 8):
                    if self.position[square[0] - 2][square[1] + 1] == 0:
                        knight_destinations.append([square[0] - 2, square[1] + 1])
                    elif self.position[square[0] - 2][square[1] + 1][ : 5] != self.turn_player: #if it's not your own piece
                        knight_destinations.append([square[0] - 2, square[1] + 1])

                # 1 up 2 right
                if (square[0] - 1 > -1) and (square[1] + 2 < 8):
                    if self.position[square[0] - 1][square[1] + 2] == 0:
                        knight_destinations.append([square[0] - 1, square[1] + 2])
                    elif self.position[square[0] - 1][square[1] + 2][ : 5] != self.turn_player: #if it's not your own piece
                        knight_destinations.append([square[0] - 1, square[1] + 2])
                        
                # 1 down 2 right
                if (square[0] + 1 < 8) and (square[1] + 2 < 8):
                    if self.position[square[0] + 1][square[1] + 2] == 0:
                        knight_destinations.append([square[0] + 1, square[1] + 2])
                    elif self.position[square[0] + 1][square[1] + 2][ : 5] != self.turn_player: #if it's not your own piece
                        knight_destinations.append([square[0] + 1, square[1] + 2])
                        
                # 2 down 1 right
                if (square[0] + 2 < 8) and (square[1] + 1 < 8):
                    if self.position[square[0] + 2][square[1] + 1] == 0:
                        knight_destinations.append([square[0] + 2, square[1] + 1])
                    elif self.position[square[0] + 2][square[1] + 1][ : 5] != self.turn_player: #if it's not your own piece
                        knight_destinations.append([square[0] + 2, square[1] + 1])
                        
                # 2 down 1 left
                if (square[0] + 2 < 8) and (square[1] - 1 > -1):
                    if self.position[square[0] + 2][square[1] - 1] == 0:
                        knight_destinations.append([square[0] + 2, square[1] - 1])
                    elif self.position[square[0] + 2][square[1] - 1][ : 5] != self.turn_player: #if it's not your own piece
                        knight_destinations.append([square[0] + 2, square[1] - 1])
                        
                # 1 down 2 left
                if (square[0] + 1 < 8) and (square[1] - 2 > -1):
                    if self.position[square[0] + 1][square[1] - 2] == 0:
                        knight_destinations.append([square[0] + 1, square[1] - 2])
                    elif self.position[square[0] + 1][square[1] - 2][ : 5] != self.turn_player: #if it's not your own piece
                        knight_destinations.append([square[0] + 1, square[1] - 2])
                        
                # 1 up 2 left
                if (square[0] - 1 > -1) and (square[1] - 2 > -1):
                    if self.position[square[0] - 1][square[1] - 2] == 0:
                        knight_destinations.append([square[0] - 1, square[1] - 2])
                    elif self.position[square[0] - 1][square[1] - 2][ : 5] != self.turn_player: #if it's not your own piece
                        knight_destinations.append([square[0] - 1, square[1] - 2])
                        
                # 2 up 1 left
                if (square[0] - 2 > -1) and (square[1] - 1 > -1):
                    if self.position[square[0] - 2][square[1] - 1] == 0:
                        knight_destinations.append([square[0] - 2, square[1] - 1])
                    elif self.position[square[0] - 2][square[1] - 1][ : 5] != self.turn_player: #if it's not your own piece
                        knight_destinations.append([square[0] - 2, square[1] - 1])
                
                if knight_destinations != []: # if the knight can move to at least one square
                    for destination in knight_destinations:
                        legal_moves.append([square, destination])
                
            elif self.position[square[0]][square[1]][6:] == 'Bishop':
                bishop_destinations = []
                
                #up and to the right
                for i in range(7): #can only go 7 in any direction
                    if (square[0] - i - 1 == -1) or (square[1] + i + 1 == 8):
                        break
                    elif self.position[square[0] - i - 1][square[1] + i + 1] == 0:
                        bishop_destinations.append([square[0] - i - 1, square[1] + i + 1])
                    elif self.position[square[0] - i - 1][square[1] + i + 1][ : 5] == self.turn_player: # if it's your own piece
                        break
                    else: #opponent's piece, can't go beyond it
                        bishop_destinations.append([square[0] - i - 1, square[1] + i + 1])
                        break
                    
                #down and to the right
                for i in range(7): #can only go 7 in any direction
                    if (square[0] + i + 1 == 8) or (square[1] + i + 1 == 8):
                        break
                    elif self.position[square[0] + i + 1][square[1] + i + 1] == 0:
                        bishop_destinations.append([square[0] + i + 1, square[1] + i + 1])
                    elif self.position[square[0] + i + 1][square[1] + i + 1][ : 5] == self.turn_player: # if it's your own piece
                        break
                    else: #opponent's piece, can't go beyond it
                        bishop_destinations.append([square[0] + i + 1, square[1] + i + 1])
                        break

                #down and to the left
                for i in range(7): #can only go 7 in any direction
                    if (square[0] + i + 1 == 8) or (square[1] - i - 1 == -1):
                        break
                    elif self.position[square[0] + i + 1][square[1] - i - 1] == 0:
                        bishop_destinations.append([square[0] + i + 1, square[1] - i - 1])
                    elif self.position[square[0] + i + 1][square[1] - i - 1][ : 5] == self.turn_player: # if it's your own piece
                        break
                    else: #opponent's piece, can't go beyond it
                        bishop_destinations.append([square[0] + i + 1, square[1] - i - 1])
                        break

                #up and to the left
                for i in range(7): #can only go 7 in any direction
                    if (square[0] - i - 1 == -1) or (square[1] - i - 1 == -1):
                        break
                    elif self.position[square[0] - i - 1][square[1] - i - 1] == 0:
                        bishop_destinations.append([square[0] - i - 1, square[1] - i - 1])
                    elif self.position[square[0] - i - 1][square[1] - i - 1][ : 5] == self.turn_player: # if it's your own piece
                        break
                    else: #opponent's piece, can't go beyond it
                        bishop_destinations.append([square[0] - i - 1, square[1] - i - 1])
                        break
                    
                if bishop_destinations != []: # if the bishop can move to at least one square
                    for destination in bishop_destinations:
                        legal_moves.append([square, destination])
                                        
            elif self.position[square[0]][square[1]][6:] == 'Queen':
                queen_destinations = []
                #just copied the code from bishop and rook
                
                #up and to the right
                for i in range(7): #can only go 7 in any direction
                    if (square[0] - i - 1 == -1) or (square[1] + i + 1 == 8):
                        break
                    elif self.position[square[0] - i - 1][square[1] + i + 1] == 0:
                        queen_destinations.append([square[0] - i - 1, square[1] + i + 1])
                    elif self.position[square[0] - i - 1][square[1] + i + 1][ : 5] == self.turn_player: # if it's your own piece
                        break
                    else: #opponent's piece, can't go beyond it
                        queen_destinations.append([square[0] - i - 1, square[1] + i + 1])
                        break
                    
                #down and to the right
                for i in range(7): #can only go 7 in any direction
                    if (square[0] + i + 1 == 8) or (square[1] + i + 1 == 8):
                        break
                    elif self.position[square[0] + i + 1][square[1] + i + 1] == 0:
                        queen_destinations.append([square[0] + i + 1, square[1] + i + 1])
                    elif self.position[square[0] + i + 1][square[1] + i + 1][ : 5] == self.turn_player: # if it's your own piece
                        break
                    else: #opponent's piece, can't go beyond it
                        queen_destinations.append([square[0] + i + 1, square[1] + i + 1])
                        break

                #down and to the left
                for i in range(7): #can only go 7 in any direction
                    if (square[0] + i + 1 == 8) or (square[1] - i - 1 == -1):
                        break
                    elif self.position[square[0] + i + 1][square[1] - i - 1] == 0:
                        queen_destinations.append([square[0] + i + 1, square[1] - i - 1])
                    elif self.position[square[0] + i + 1][square[1] - i - 1][ : 5] == self.turn_player: # if it's your own piece
                        break
                    else: #opponent's piece, can't go beyond it
                        queen_destinations.append([square[0] + i + 1, square[1] - i - 1])
                        break

                #up and to the left
                for i in range(7): #can only go 7 in any direction
                    if (square[0] - i - 1 == -1) or (square[1] - i - 1 == -1):
                        break
                    elif self.position[square[0] - i - 1][square[1] - i - 1] == 0:
                        queen_destinations.append([square[0] - i - 1, square[1] - i - 1])
                    elif self.position[square[0] - i - 1][square[1] - i - 1][ : 5] == self.turn_player: # if it's your own piece
                        break
                    else: #opponent's piece, can't go beyond it
                        queen_destinations.append([square[0] - i - 1, square[1] - i - 1])
                        break
                
                #going down
                for i in range(7): #can only ever go 7 in one direction
                    if square[0] + i + 1 == 8: #we have fallen off the bottom
                        break
                    elif self.position[square[0] + i + 1][square[1]] == 0: #if the square is empty
                        queen_destinations.append([square[0] + i + 1, square[1]])
                    elif self.position[square[0] + i + 1][square[1]][ : 5] == self.turn_player: #if it's your own piece
                        break
                    else: # opponent's piece, can't go beyond it
                        queen_destinations.append([square[0] + i + 1, square[1]])
                        break                      

                #going up
                for i in range(7): #can only ever go 7 in one direction
                    if square[0] - i - 1 == -1: #we have fallen off the top
                        break
                    elif self.position[square[0] - i - 1][square[1]] == 0:
                        queen_destinations.append([square[0] - i - 1, square[1]])
                    elif self.position[square[0] - i - 1][square[1]][ : 5] == self.turn_player: #if it's your own piece
                        break
                    else: # opponent's piece, can't go beyond it
                        queen_destinations.append([square[0] - i - 1, square[1]])
                        break

                #going right
                for i in range(7): #can only ever go 7 in one direction
                    if square[1] + i + 1 == 8: #we have fallen off the right
                        break 
                    elif self.position[square[0]][square[1] + i + 1] == 0:
                        queen_destinations.append([square[0], square[1] + i + 1])
                    elif self.position[square[0]][square[1] + i + 1][ : 5] == self.turn_player: #if it's your own piece
                        break
                    else: # opponent's piece, can't go beyond it
                        queen_destinations.append([square[0], square[1] + i + 1])
                        break
                
                #going left
                for i in range(7): #can only ever go 7 in one direction
                    if square[1] - i - 1 == -1: #we have fallen off the left
                        break
                    elif self.position[square[0]][square[1] - i - 1] == 0:
                        queen_destinations.append([square[0], square[1] - i - 1])
                    elif self.position[square[0]][square[1] - i - 1][ : 5] == self.turn_player: #if it's your own piece
                        break
                    else: # opponent's piece, can't go beyond it
                        queen_destinations.append([square[0], square[1] - i - 1])
                        break

                if queen_destinations != []: # if the queen can move to at least one square
                    for destination in queen_destinations:
                        legal_moves.append([square, destination])
                
            elif self.position[square[0]][square[1]] == 'White King':
                king_destinations = []
                #draw a square around it
                for i in [-1, 0, 1]: #up and down
                    for j in [-1, 0, 1]: #left and right
                        if (i != 0) or (j != 0): #don't want to consider moving to where it already is
                            if (square[0] + i != 8) and (square[0] + i != -1): #if we don't go off the bottom or top
                                if (square[1] + j != 8) and (square[1] + j != -1): #if we don't go off the side
                                    if self.position[square[0] + i][square[1] + j] == 0: #if the square is empty
                                        king_destinations.append([square[0] + i, square[1] + j])
                                    elif self.position[square[0] + i][square[1] + j][ : 5] != self.turn_player: #if it's not my own piece
                                        king_destinations.append([square[0] + i, square[1] + j])
                #now to sort out castling
                if not self.white_king_moved:
                    if not self.white_king_rook_moved:
                        if (self.position[7][5] == 0) and (self.position[7][6] == 0):
                            king_destinations.append([7, 6])
                    if not self.white_queen_rook_moved:
                        if (self.position[7][3] == 0) and (self.position[7][2] == 0) and (self.position[7][1] == 0):
                            king_destinations.append([7, 2])
                
                if king_destinations != []: # if the king can move to at least one square
                    for destination in king_destinations:
                        legal_moves.append([square, destination])

            elif self.position[square[0]][square[1]] == 'Black King':
                king_destinations = []
                #draw a square around it
                for i in [-1, 0, 1]: #up and down
                    for j in [-1, 0, 1]: #left and right
                        if (i != 0) or (j != 0): #don't want to consider moving to where it already is
                            if (square[0] + i != 8) and (square[0] + i != -1): #if we don't go off the bottom or top
                                if (square[1] + j != 8) and (square[1] + j != -1): #if we don't go off the side
                                    if self.position[square[0] + i][square[1] + j] == 0: #if the square is empty
                                        king_destinations.append([square[0] + i, square[1] + j])
                                    elif self.position[square[0] + i][square[1] + j][ : 5] != self.turn_player: #if it's not my own piece
                                        king_destinations.append([square[0] + i, square[1] + j])
                #now to sort out castling
                if not self.black_king_moved:
                    if not self.black_king_rook_moved:
                        if (self.position[0][5] == 0) and (self.position[0][6] == 0):
                            king_destinations.append([0, 6])
                    if not self.black_queen_rook_moved:
                        if (self.position[0][3] == 0) and (self.position[0][2] == 0) and (self.position[0][1] == 0):
                            king_destinations.append([0, 2])
                
                if king_destinations != []: # if the king can move to at least one square
                    for destination in king_destinations:
                        legal_moves.append([square, destination])
            
            elif self.position[square[0]][square[1]] == 'White Pawn':
                pawn_destinations = []
                if square[0] == 6: # can move two
                    if self.position[square[0] - 1][square[1]] == 0: #if next square empty
                        pawn_destinations.append([square[0] - 1, square[1]])
                        if self.position[square[0] - 2][square[1]] == 0: #if the square after is also empty
                            pawn_destinations.append([square[0] - 2, square[1]])
                else: #can only move 1
                    if self.position[square[0] - 1][square[1]] == 0: #if next square empty
                        pawn_destinations.append([square[0] - 1, square[1]])
                        
                #capturing up and left
                if square[1] != 0: #if not the a pawn
                    if self.position[square[0] - 1][square[1] - 1] != 0:
                        if self.position[square[0] - 1][square[1] - 1][ : 5] != self.turn_player: #if there is a black piece up and to the left
                            pawn_destinations.append([square[0] - 1, square[1] - 1])
                    else: #maybe we can take en passant
                        if self.pawn_just_moved_two != False: #we're in business
                            if self.pawn_just_moved_two[0] == square [0]: #if we're on the same row
                                if self.pawn_just_moved_two[1] + 1 == square [1]: #we are right next to it
                                    pawn_destinations.append([square[0] - 1, square[1] - 1])
                                    
                #capturing up and right
                if square[1] != 7: #if not the h pawn
                    if self.position[square[0] - 1][square[1] + 1] != 0:
                        if self.position[square[0] - 1][square[1] + 1][ : 5] != self.turn_player: #if there is a black piece up and to the right
                            pawn_destinations.append([square[0] - 1, square[1] + 1])
                    else: #maybe we can take en passant
                        if self.pawn_just_moved_two != False: #we're in business
                            if self.pawn_just_moved_two[0] == square [0]: #if we're on the same row
                                if self.pawn_just_moved_two[1] - 1 == square [1]: #we are right next to it
                                    pawn_destinations.append([square[0] - 1, square[1] + 1])    
                
                if pawn_destinations != []: # if the pawn can move to at least one square
                    for destination in pawn_destinations:
                        if destination[0] == 0: #promote
                            legal_moves.append([square, destination, 'Knight'])
                            legal_moves.append([square, destination, 'Rook'])
                            legal_moves.append([square, destination, 'Queen'])
                            legal_moves.append([square, destination, 'Bishop'])
                        else:
                            legal_moves.append([square, destination])

            elif self.position[square[0]][square[1]] == 'Black Pawn':
                pawn_destinations = []
                if square[0] == 1: # can move two
                    if self.position[square[0] + 1][square[1]] == 0: #if next square empty
                        pawn_destinations.append([square[0] + 1, square[1]])
                        if self.position[square[0] + 2][square[1]] == 0: #if the square after is also empty
                            pawn_destinations.append([square[0] + 2, square[1]])
                else: #can only move 1
                    if self.position[square[0] + 1][square[1]] == 0: #if next square empty
                        pawn_destinations.append([square[0] + 1, square[1]])
                        
                #capturing down and left
                if square[1] != 0: #if not the a pawn
                    if self.position[square[0] + 1][square[1] - 1] != 0:
                        if self.position[square[0] + 1][square[1] - 1][ : 5] != self.turn_player: #if there is a white piece up and to the left
                            pawn_destinations.append([square[0] + 1, square[1] - 1])
                    else: #maybe we can take en passant
                        if self.pawn_just_moved_two != False: #we're in business
                            if self.pawn_just_moved_two[0] == square [0]: #if we're on the same row
                                if self.pawn_just_moved_two[1] + 1 == square [1]: #we are right next to it
                                    pawn_destinations.append([square[0] + 1, square[1] - 1])
                                    
                    #capturing down and right
                if square[1] != 7: #if not the h pawn
                    if self.position[square[0] + 1][square[1] + 1] != 0:
                        if self.position[square[0] + 1][square[1] + 1][ : 5] != self.turn_player: #if there is a black piece up and to the right
                            pawn_destinations.append([square[0] + 1, square[1] + 1])
                        else: #maybe we can take en passant
                            if self.pawn_just_moved_two != False: #we're in business
                                if self.pawn_just_moved_two[0] == square [0]: #if we're on the same row
                                    if self.pawn_just_moved_two[1] - 1 == square [1]: #we are right next to it
                                        pawn_destinations.append([square[0] + 1, square[1] + 1])
                                        
                if pawn_destinations != []: # if the pawn can move to at least one square
                    for destination in pawn_destinations:
                        if destination[0] == 7: #promote
                            legal_moves.append([square, destination, 'Knight'])
                            legal_moves.append([square, destination, 'Rook'])
                            legal_moves.append([square, destination, 'Queen'])
                            legal_moves.append([square, destination, 'Bishop'])
                        else:
                            legal_moves.append([square, destination])

        if checks_and_captures_only: # gets rid of most moves that aren't checks or captures. Useful for pruning the search tree
            checks_and_captures = []
            for move in legal_moves:
                if move_attacks_king(move, self) or move_is_capture(move, self):
                    checks_and_captures.append(move)
            if legal_moves != []: #if there are legal moves to append. If not, we may return an empty list of moves. If there are no moves to be made, I'm in trouble. I've made a temporary fix for this, but I think it's a small edge case, so I'm ok getting it a bit wrong for now
                while len(checks_and_captures) < 3: # add some moves in to give a more balanced look at the position. E.g. if you only check your opponents checks and captures, but your opponent has no checks or captures, you might think your position is better than it really is
                    checks_and_captures.append(random.choice(legal_moves))
                checks_and_captures.append(random.choice(legal_moves))
            return checks_and_captures

        return legal_moves

class Random_Player: #For testing, and for fun!
    def choose_move(self, current_board, possible_moves): #current board does nothing, just there to match the number of arguments of Player
        return random.choice(possible_moves)

class GameTree(): #this is the tree through which I will search to find the best move
    def __init__(self, board, checks_and_captures_only = False, given_moves = False, last_generation = False): #board is a Board(). #Given moves is passed at the first creation of the class to dictate what moves it can consider. Makes sure that, if it tries to castle through check etc., we can remove that move from possible moves and have it try again. last_generation stops me creating the next lot of legal moves if I'm not going to use them here
        self.parent_board = copy.deepcopy(board)
        if not last_generation:
            if not given_moves:
                self.moves_to_choose_from = self.parent_board.generate_all_legal_moves(checks_and_captures_only = checks_and_captures_only)
            else: # we have been told which moves to consider
                self.moves_to_choose_from = given_moves
        self.children = None # Will be a list of Game_Trees
        self.evaluated_children = [] #will be a list of values of the above game trees

    def create_next_layer(self, checks_and_captures_only = False, last_generation = False):
        self.children = [] #list of GameTrees
        for move in self.moves_to_choose_from:
            child_board = copy.deepcopy(self.parent_board) #will this create a seperate board every time?
            if len(move) == 3: #promotion moves have 3 arguments
                child_board.make_move(move[0], move[1], move[2])
            else:
                child_board.make_move(move[0], move[1])
            self.children.append(GameTree(child_board, checks_and_captures_only = checks_and_captures_only, last_generation = last_generation))

class Player:
    def __init__(self, pawn_value, rook_value, knight_value, bishop_value, queen_value, move_value, undeveloped_minor_cost, early_queen_move_cost, castled_value, centre_pawn_value, early_king_move_cost, early_king_rook_move_cost, early_queen_rook_move_cost, depth, checks_and_captures_only = False): #add more arguments later
        #these things are parameters that determine how the Player evaluates a position. 
        self.pawn_value = pawn_value
        self.rook_value = rook_value
        self.knight_value = knight_value
        self.bishop_value = bishop_value
        self.queen_value = queen_value
        self.move_value = move_value
        self.undeveloped_minor_cost = undeveloped_minor_cost
        self.early_queen_move_cost = early_queen_move_cost
        self.castled_value = castled_value
        self.centre_pawn_value = centre_pawn_value
        self.early_king_move_cost = early_king_move_cost
        self.early_king_rook_move_cost = early_king_rook_move_cost
        self.early_queen_rook_move_cost = early_queen_rook_move_cost
        self.depth = depth # in ply (2 ply is one pair of moves, white and black)
        self.checks_and_captures_only = checks_and_captures_only #Boolean. Only consider checks and captures for moves after your move.

    def select_best(self, parent): #parent is a parent tree node with evaluated board beneath it
        #this function decides whether to take the max or the min in the minimax algorithm
        if parent.evaluated_children == []:
            return 0 #bodge. There are a few things that could be happening for a tree node to have no children, returning 0 just so my code doen't crash. I'm approaching my deadline for this project. I've added this to the future plan section
        if parent.parent_board.turn_player == 'White':
            return max(parent.evaluated_children)
        else:
            return min(parent.evaluated_children)
    
    def get_index_of_move(self, origin):# this is a helper function to get the best move given the evaluations of their children. #origin is the original decision tree in choose_move. Its children are reduced to evaluations at this stage
        best_value = self.select_best(origin)
        for i in range(len(origin.evaluated_children)):
            if origin.evaluated_children[i] == best_value:
                return i #don't care about breaking ties

    def evaluate_position(self, board):
        score = 0
        #count material
        for row in board.position:
            for occupant in row: #name of piece occupying a particular square
                if occupant == 0:
                    score += 0 #don't change the score if there isn't a piece
                else:
                    if occupant[:5] == 'White':
                        colour_multiplier = 1
                    else:
                        colour_multiplier = -1 #black pieces are worth -1 times white pieces

                    if occupant[6:] == 'Pawn':
                        score += self.pawn_value * colour_multiplier
                    elif occupant[6:] == 'Rook':
                        score += self.rook_value * colour_multiplier
                    elif occupant[6:] == 'Knight':
                        score += self.knight_value * colour_multiplier
                    elif occupant[6:] == 'Bishop':
                        score += self.bishop_value * colour_multiplier
                    elif occupant[6:] == 'Queen':
                        score += self.queen_value * colour_multiplier
                    elif occupant[6:] == 'King':
                        score += 1000 * colour_multiplier #king is really valuable
                    else:
                        print('I dont know what is on this square')

        #count possible moves for each side, ignoring issues like checks. The more the better
        if board.move_count < 15: #this becomes more expensive and less useful as the game goes on
            temp_board = copy.deepcopy(board)
            temp_board.turn_player = 'White' 
            #count white's moves
            white_count = len(temp_board.generate_all_legal_moves())
            #count black's moves
            temp_board.turn_player = 'Black'
            black_count = len(temp_board.generate_all_legal_moves())
            score += self.move_value * (white_count - black_count)

        #punish undeveloped minor pieces. Additional penalty for the queen having moved before a given minor
        for piece in board.position[0]:
            if piece == 'Black Knight' or piece == 'Black Bishop':
                score += self.undeveloped_minor_cost #undeveloped black minor pieces are good for white
                if board.position[0][3] != 'Black Queen':
                    score += self.early_queen_move_cost
        for piece in board.position[7]:
            if piece == 'White Knight' or piece == 'White Bishop':
                score -= self.undeveloped_minor_cost #undeveloped black minor pieces are bad for white
                if board.position[7][3] != 'White Queen':
                    score -= self.early_queen_move_cost

        #reward castling, punish going uncastled
        if board.white_king_castled:
            score += self.castled_value
        else:
            if board.white_king_moved:
                score -= self.early_king_move_cost
            if board.white_king_rook_moved:
                score -= self.early_king_rook_move_cost
            if board.white_queen_rook_moved:
                score -= self.early_queen_rook_move_cost

        if board.black_king_castled:
            score -= self.castled_value
        else:
            if board.black_king_moved:
                score += self.early_king_move_cost
            if board.black_king_rook_moved:
                score += self.early_king_rook_move_cost
            if board.black_queen_rook_moved:
                score += self.early_queen_rook_move_cost

        #reward having pawns in the centre
        if board.position[3][3] == 'White Pawn':
            score += self.centre_pawn_value
        if board.position[3][4] == 'White Pawn':
            score += self.centre_pawn_value
        if board.position[4][3] == 'White Pawn':
            score += self.centre_pawn_value
        if board.position[4][4] == 'White Pawn':
            score += self.centre_pawn_value
        if board.position[3][3] == 'Black Pawn':
            score -= self.centre_pawn_value
        if board.position[3][4] == 'Black Pawn':
            score -= self.centre_pawn_value
        if board.position[4][3] == 'Black Pawn':
            score -= self.centre_pawn_value
        if board.position[4][4] == 'Black Pawn':
            score -= self.centre_pawn_value

        return score

    def choose_move(self, given_board, possible_moves): #returns move
        #first, create the tree that we're going to search through
        decision_tree = GameTree(given_board, given_moves = possible_moves)
        if self.depth >= 2:
            print('making gen 1')
            decision_tree.create_next_layer(checks_and_captures_only = self.checks_and_captures_only) #creates children 1st layer with 0 indexing
            print('making gen 2')
            for child in decision_tree.children:
                child.create_next_layer(checks_and_captures_only = self.checks_and_captures_only, last_generation = self.depth == 2)#last argument makes sure that we don't generate a lot of legal moves that we never consider
        if self.depth >= 3:
            print('making gen 3')
            for child in decision_tree.children:
                for grandchild in child.children:
                    grandchild.create_next_layer(checks_and_captures_only = self.checks_and_captures_only, last_generation = self.depth == 3) #last argument makes sure that we don't generate a lot of legal moves that we never consider
        if self.depth >= 4:
            print('making gen 4')
            for child in decision_tree.children:
                for grandchild in child.children:
                    for greatgrandchild in grandchild.children:
                        greatgrandchild.create_next_layer(checks_and_captures_only = self.checks_and_captures_only, last_generation = self.depth == 4) #last argument makes sure that we don't generate a lot of legal moves that we never consider
        if self.depth >= 5:
            print('making gen 5')
            for child in decision_tree.children:
                for grandchild in child.children:
                    for greatgrandchild in grandchild.children:
                        for g2grandchild in greatgrandchild.children:
                            g2grandchild.create_next_layer(checks_and_captures_only = self.checks_and_captures_only, last_generation = self.depth == 5) #last argument makes sure that we don't generate a lot of legal moves that we never consider
        if self.depth >= 6:
            print('Sorry, I have not built depth >= 6 yet. My laptop could never handle it')
        print('tree made')
        #now to go to the bottom layer and evaluate all the positions
        if self.depth == 5:
            for child in decision_tree.children:
                for grandchild in child.children:
                    for greatgrandchild in grandchild.children:
                        for g2grandchild in greatgrandchild.children:
                            for g3grandchild in g2grandchild.children:
                                g2grandchild.evaluated_children.append(self.evaluate_position(g3grandchild.parent_board))# replace g3 grandchild with its evaluation
                            greatgrandchild.evaluated_children.append(self.select_best(g2grandchild)) #selects the best g3grandchild
                        grandchild.evaluated_children.append(self.select_best(greatgrandchild))
                    child.evaluated_children.append(self.select_best(grandchild))
                decision_tree.evaluated_children.append(self.select_best(child))
            return possible_moves[self.get_index_of_move(decision_tree)]
        
        elif self.depth == 4:
            for child in decision_tree.children:
                for grandchild in child.children:
                    for greatgrandchild in grandchild.children:
                        for g2grandchild in greatgrandchild.children:
                            greatgrandchild.evaluated_children.append(self.evaluate_position(g2grandchild.parent_board))
                        grandchild.evaluated_children.append(self.select_best(greatgrandchild))
                    child.evaluated_children.append(self.select_best(grandchild))
                decision_tree.evaluated_children.append(self.select_best(child))
            return possible_moves[self.get_index_of_move(decision_tree)]

        elif self.depth == 3:
            for child in decision_tree.children:
                for grandchild in child.children:
                    for greatgrandchild in grandchild.children:
                        grandchild.evaluated_children.append(self.evaluate_position(greatgrandchild.parent_board))
                    child.evaluated_children.append(self.select_best(grandchild))
                decision_tree.evaluated_children.append(self.select_best(child))
            return possible_moves[self.get_index_of_move(decision_tree)]

        elif self.depth == 2:
            for child in decision_tree.children:
                for grandchild in child.children:
                        child.evaluated_children.append(self.evaluate_position(grandchild.parent_board))
                decision_tree.evaluated_children.append(self.select_best(child))
            return possible_moves[self.get_index_of_move(decision_tree)]

            #code below was to check poisitions that led to bizzare evaluations. I may need it again one day
           # for i in range(len(decision_tree.children)):
                #if abs(decision_tree.evaluated_children[i]) > 500:
                 #   print('position:')
                #    decision_tree.children[i].parent_board.print_position()
               #     print('eval of position above:')
              #      print(decision_tree.evaluated_children[i])
             #       print('evals of its children:')
            #        print(decision_tree.children[i].evaluated_children)
           #         for j in range(len(decision_tree.children[i].evaluated_children)):
          #              if abs((decision_tree.children[i].evaluated_children[j])) > 500:
         #                   print('evals of weird grandchild', j)
        #                    print(decision_tree.children[i].children[j].evaluated_children)
       #                     for k in range(len(decision_tree.children[i].children[j].evaluated_children)):
      #                          if abs((decision_tree.children[i].children[j].evaluated_children[k])) > 500:
     #                               print('evals of weird greatgrandchild', k)
    #                                print(decision_tree.children[i].children[j].children[k].evaluated_children)
   #                                 for l in range(len(decision_tree.children[i].children[j].children[k].evaluated_children)):
  #                                      if abs((decision_tree.children[i].children[j].children[k].evaluated_children[l])) > 500:
 #                                           print('position that is so bad')
#                                            decision_tree.children[i].children[j].children[k].children[l].parent_board.print_position()

def is_the_king_hanging(board, opposition): #useful both for checking if checkmate and if a potential move hangs the king
    #board is just the Board, opposition is the colour of the player who could take the king
    test_board = copy.deepcopy(board) # dont want to actually change the board
    test_board.turn_player = opposition #check if the attacking side can take the king
    #now to find the king
    kings_square = None
    if opposition == 'White':
        for i in range (8):
            for j in range (8):
                if test_board.position[i][j] == 'Black King':
                    kings_square = [i, j]
    else:
        for i in range(8):
            for j in range(8):
                if test_board.position[i][j] == 'White King':
                    kings_square = [i, j]
    #bodge: this function is called when evaluating positions which don't actually forbid the king to be taken. If the king has been taken, I'm going to say it is 'hanging'
    if kings_square == None:
        return True
    for move in test_board.generate_all_legal_moves():
        if move[1] == kings_square:
            return True
    return False

def repeated_position(board1, board2): # Used to check for 3-fold repetitions
    #specificalaly, this function checks if 2 positions are the same. the show_game() function will call this helper function when checking for repetitions.
    #For two boards to be the same, they must have the same position, with the same player to move, with all the same legal moves available for both sides (en passant and castling).
    #This rule doesn't seem to be the same everywhere and everytime, so, to make things easier, I'm going to insist that a 3-fold repetition is a draw (as chess.com does), rather than asking the turn player to call over the arbiter and explain the situation.
    if board1.position != board2.position:
        return False
    if board1.turn_player != board2.turn_player:
        return False #almost all checks should finish by here
    elif has_castling_rights(board1, 'White', 'Kingside') != has_castling_rights(board2, 'White', 'Kingside'): #if white has since surrendered kingside castling rights
        return False
    elif has_castling_rights(board1, 'Black', 'Kingside') != has_castling_rights(board2, 'Black', 'Kingside'): #if black has since surrendered kingside castling rights
        return False
    elif has_castling_rights(board1, 'White', 'Queenside') != has_castling_rights(board2, 'White', 'Queenside'): #if white has since surrendered queenside castling rights
        return False
    elif has_castling_rights(board1, 'Black', 'Queenside') != has_castling_rights(board2, 'Black', 'Queenside'): #if black has since surrendered queenside castling rights
        return False
    elif a_pawn_can_be_taken_en_passant(board1):
        return False
    elif a_pawn_can_be_taken_en_passant(board2):
        return False
    return True
    
def a_pawn_can_be_taken_en_passant(board): #This function will rarely be used. It is to check whether two positions really are the same for 3-fold repetition.
    #if a pawn can be taken en passant in a position, it cannot be counted as the same as any other postion, because that option is there for only 1 move
    if board.pawn_just_moved_two != False: #when a pawn has moved 2, this attribute is set to the position of said pawn
        if board.pawn_just_moved_two[1] == 0: #if it is an a pawn
            if board.turn_player == 'White':
                return board.position[3][1] == 'White Pawn'
            else:
                return board.position[4][1] == 'Black Pawn'
        elif board.pawn_just_moved_two[1] == 7: #if it is an h pawn
            if board.turn_player == 'White':
                return board.position[3][6] == 'White Pawn'
            else:
                return board.position[4][6] == 'Black Pawn'
        else: #it is not a rook pawn, so could be captured either side
            file = board.pawn_just_moved_two[1] #what file is this pawn on?
            if board.turn_player == 'White':
                return (board.position[3][file + 1] == 'White Pawn') or (board.position[3][file - 1] == 'White Pawn')
            else:
                return (board.position[4][file + 1] == 'Black Pawn') or (board.position[4][file - 1] == 'Black Pawn')    

def has_castling_rights(board, player, side): #e.g. Board(), white, queenside. Returns True if player has castling rights on side etc. used by repeated_position()
    if player == 'White':
        if side == 'Queenside':
            if board.white_king_moved:
                return False
            elif board.white_queen_rook_moved:
                return False
            return True
        else: #kingside
            if board.white_king_moved:
                return False
            elif board.white_king_rook_moved:
                return False
            return True
    else: #black
        if side == 'Queenside':
            if board.black_king_moved:
                return False
            elif board.black_queen_rook_moved:
                return False
            return True
        else: #kingside
            if board.black_king_moved:
                return False
            elif board.black_king_rook_moved:
                return False
            return True

def is_that_move_legal(candidate_move, board): #board is before move is made
    move_is_legal = True
    #first, make sure you don't castle out of check
    if is_the_king_hanging(board, board.not_turn_player): #if you're starting the move in check
        if candidate_move == [[7, 4], [7, 6]] and board.position[7][4] == 'White King': #white castles kingside
            move_is_legal = False
        elif candidate_move == [[7, 4], [7, 2]] and board.position[7][4] == 'White King': #white castles queenside
            move_is_legal = False
        elif candidate_move == [[0, 4], [0, 6]] and board.position[0][4] == 'Black King': #black castles kingside
            move_is_legal = False
        elif candidate_move == [[0, 4], [0, 2]] and board.position[0][4] == 'Black King': #black castles queenside
            move_is_legal = False

    position_to_check = copy.deepcopy(board) # look to take the king or land on an intermediate castling square
    if len(candidate_move) == 3: #bit of a bodge, might want to help make_move unpack lists as arguments if this causes a problem often
        position_to_check.make_move(candidate_move[0], candidate_move[1], candidate_move[2])
    else:
        position_to_check.make_move(candidate_move[0], candidate_move[1]) #make the move on a temporary board
    if candidate_move == [[7, 4], [7, 6]] and position_to_check.position[7][6] == 'White King': #if the move was white 0-0
        for move in position_to_check.generate_all_legal_moves(): #for each move black can make
            if move[1] == [7, 5]: #if a piece can move to the interim square
                move_is_legal = False
                break
    elif candidate_move == [[7, 4], [7, 2]] and position_to_check.position[7][2] == 'White King': #if the move was white 0-0-0
        for move in position_to_check.generate_all_legal_moves():
            if move[1] == [7, 3]:
                move_is_legal = False
                break
    elif candidate_move == [[0, 4], [0, 6]] and position_to_check.position[0][6] == 'Black King':#if the move was black 0-0
        for move in position_to_check.generate_all_legal_moves(): #for each move white can make
            if move[1] == [0, 5]: #if a piece can move to the interim square
                move_is_legal = False
                break    
    elif candidate_move == [[0, 4], [0, 2]] and position_to_check.position[0][2] == 'Black King': #if the move was black 0-0-0
        for move in position_to_check.generate_all_legal_moves():
            if move[1] == [0, 3]:
                move_is_legal = False
                break
    #now to check if the king is hanging. The move has already been made on the temporary board.
    if is_the_king_hanging(position_to_check, position_to_check.turn_player):
        move_is_legal = False

    return move_is_legal

def move_attacks_king(move, board): #does not count discovered checks for the sake of computational efficiency
    temporary_board = copy.deepcopy(board)
    if len(move) == 3:
        temporary_board.make_move(move[0], move[1], move[2])
    else:
        temporary_board.make_move(move[0], move[1])
    temporary_board.change_turn_player() #make it the attacker's move again
    return is_the_king_hanging(temporary_board, temporary_board.turn_player)

def move_is_capture(move, board):
    return board.position[move[1][0]][move[1][1]] != 0

class GameGUI():
    def __init__(self, position):
        self.position = position

        self.root = tk.Tk()
        self.root.title('Chess')
        self.root.geometry('1000x700')

        self.human_move = [None, None] #update this with clicked squares when the human clicks.

        #the following are the images needed to show a chess board

        self.empty_white = tk.PhotoImage(file = "ew.png")
        self.empty_black = tk.PhotoImage(file = "eb.png")
        self.white_pawn_white = tk.PhotoImage(file = "wpw.png")
        self.white_pawn_black = tk.PhotoImage(file = "wpb.png")
        self.white_rook_white = tk.PhotoImage(file = "wrw.png")
        self.white_rook_black = tk.PhotoImage(file = "wrb.png")
        self.white_knight_white = tk.PhotoImage(file = "wnw.png")
        self.white_knight_black = tk.PhotoImage(file = "wnb.png")
        self.white_bishop_white = tk.PhotoImage(file = "wbw.png")
        self.white_bishop_black = tk.PhotoImage(file = "wbb.png")
        self.white_queen_white = tk.PhotoImage(file = "wqw.png")
        self.white_queen_black = tk.PhotoImage(file = "wqb.png")
        self.white_king_white = tk.PhotoImage(file = "wkw.png")
        self.white_king_black = tk.PhotoImage(file = "wkb.png")
        
        self.black_pawn_white = tk.PhotoImage(file = "bpw.png")
        self.black_pawn_black = tk.PhotoImage(file = "bpb.png")
        self.black_rook_white = tk.PhotoImage(file = "brw.png")
        self.black_rook_black = tk.PhotoImage(file = "brb.png")
        self.black_knight_white = tk.PhotoImage(file = "bnw.png")
        self.black_knight_black = tk.PhotoImage(file = "bnb.png")
        self.black_bishop_white = tk.PhotoImage(file = "bbw.png")
        self.black_bishop_black = tk.PhotoImage(file = "bbb.png")
        self.black_queen_white = tk.PhotoImage(file = "bqw.png")
        self.black_queen_black = tk.PhotoImage(file = "bqb.png")
        self.black_king_white = tk.PhotoImage(file = "bkw.png")
        self.black_king_black = tk.PhotoImage(file = "bkb.png")

        self.button_frame = tk.Frame(self.root)

        self.button_frame.columnconfigure(0, weight = 1) #a file
        self.button_frame.columnconfigure(1, weight = 1) #b file
        self.button_frame.columnconfigure(2, weight = 1) #c
        self.button_frame.columnconfigure(3, weight = 1) #d
        self.button_frame.columnconfigure(4, weight = 1) #e
        self.button_frame.columnconfigure(5, weight = 1) #f
        self.button_frame.columnconfigure(6, weight = 1) #g
        self.button_frame.columnconfigure(7, weight = 1) #h

        #I don't get why I need to put lambda in here, but it works
        self.a8 = tk.Button(self.button_frame, image = self.get_image(self.position, [0, 0]), command = lambda : self.return_square([0, 0]))
        self.a8.grid(row = 0, column = 0)
        self.a7 = tk.Button(self.button_frame, image = self.get_image(self.position, [1, 0]), command = lambda : self.return_square([1, 0]))
        self.a7.grid(row = 1, column = 0)
        self.a6 = tk.Button(self.button_frame, image = self.get_image(self.position, [2, 0]), command = lambda : self.return_square([2, 0]))
        self.a6.grid(row = 2, column = 0)
        self.a5 = tk.Button(self.button_frame, image = self.get_image(self.position, [3, 0]), command = lambda : self.return_square([3, 0]))
        self.a5.grid(row = 3, column = 0)
        self.a4 = tk.Button(self.button_frame, image = self.get_image(self.position, [4, 0]), command = lambda : self.return_square([4, 0]))
        self.a4.grid(row = 4, column = 0)
        self.a3 = tk.Button(self.button_frame, image = self.get_image(self.position, [5, 0]), command = lambda : self.return_square([5, 0]))
        self.a3.grid(row = 5, column = 0)
        self.a2 = tk.Button(self.button_frame, image = self.get_image(self.position, [6, 0]), command = lambda : self.return_square([6, 0]))
        self.a2.grid(row = 6, column = 0)
        self.a1 = tk.Button(self.button_frame, image = self.get_image(self.position, [7, 0]), command = lambda : self.return_square([7, 0]))
        self.a1.grid(row = 7, column = 0)

        self.b8 = tk.Button(self.button_frame, image = self.get_image(self.position, [0, 1]), command = lambda : self.return_square([0, 1]))
        self.b8.grid(row = 0, column = 1)
        self.b7 = tk.Button(self.button_frame, image = self.get_image(self.position, [1, 1]), command = lambda : self.return_square([1, 1]))
        self.b7.grid(row = 1, column = 1)
        self.b6 = tk.Button(self.button_frame, image = self.get_image(self.position, [2, 1]), command = lambda : self.return_square([2, 1]))
        self.b6.grid(row = 2, column = 1)
        self.b5 = tk.Button(self.button_frame, image = self.get_image(self.position, [3, 1]), command = lambda : self.return_square([3, 1]))
        self.b5.grid(row = 3, column = 1)
        self.b4 = tk.Button(self.button_frame, image = self.get_image(self.position, [4, 1]), command = lambda : self.return_square([4, 1]))
        self.b4.grid(row = 4, column = 1)
        self.b3 = tk.Button(self.button_frame, image = self.get_image(self.position, [5, 1]), command = lambda : self.return_square([5, 1]))
        self.b3.grid(row = 5, column = 1)
        self.b2 = tk.Button(self.button_frame, image = self.get_image(self.position, [6, 1]), command = lambda : self.return_square([6, 1]))
        self.b2.grid(row = 6, column = 1)
        self.b1 = tk.Button(self.button_frame, image = self.get_image(self.position, [7, 1]), command = lambda : self.return_square([7, 1]))
        self.b1.grid(row = 7, column = 1)

        self.c8 = tk.Button(self.button_frame, image = self.get_image(self.position, [0, 2]), command = lambda : self.return_square([0, 2]))
        self.c8.grid(row = 0, column = 2)
        self.c7 = tk.Button(self.button_frame, image = self.get_image(self.position, [1, 2]), command = lambda : self.return_square([1, 2]))
        self.c7.grid(row = 1, column = 2)
        self.c6 = tk.Button(self.button_frame, image = self.get_image(self.position, [2, 2]), command = lambda : self.return_square([2, 2]))
        self.c6.grid(row = 2, column = 2)
        self.c5 = tk.Button(self.button_frame, image = self.get_image(self.position, [3, 2]), command = lambda : self.return_square([3, 2]))
        self.c5.grid(row = 3, column = 2)
        self.c4 = tk.Button(self.button_frame, image = self.get_image(self.position, [4, 2]), command = lambda : self.return_square([4, 2]))
        self.c4.grid(row = 4, column = 2)
        self.c3 = tk.Button(self.button_frame, image = self.get_image(self.position, [5, 2]), command = lambda : self.return_square([5, 2]))
        self.c3.grid(row = 5, column = 2)
        self.c2 = tk.Button(self.button_frame, image = self.get_image(self.position, [6, 2]), command = lambda : self.return_square([6, 2]))
        self.c2.grid(row = 6, column = 2)
        self.c1 = tk.Button(self.button_frame, image = self.get_image(self.position, [7, 2]), command = lambda : self.return_square([7, 2]))
        self.c1.grid(row = 7, column = 2)

        self.d8 = tk.Button(self.button_frame, image = self.get_image(self.position, [0, 3]), command = lambda : self.return_square([0, 3]))
        self.d8.grid(row = 0, column = 3)
        self.d7 = tk.Button(self.button_frame, image = self.get_image(self.position, [1, 3]), command = lambda : self.return_square([1, 3]))
        self.d7.grid(row = 1, column = 3)
        self.d6 = tk.Button(self.button_frame, image = self.get_image(self.position, [2, 3]), command = lambda : self.return_square([2, 3]))
        self.d6.grid(row = 2, column = 3)
        self.d5 = tk.Button(self.button_frame, image = self.get_image(self.position, [3, 3]), command = lambda : self.return_square([3, 3]))
        self.d5.grid(row = 3, column = 3)
        self.d4 = tk.Button(self.button_frame, image = self.get_image(self.position, [4, 3]), command = lambda : self.return_square([4, 3]))
        self.d4.grid(row = 4, column = 3)
        self.d3 = tk.Button(self.button_frame, image = self.get_image(self.position, [5, 3]), command = lambda : self.return_square([5, 3]))
        self.d3.grid(row = 5, column = 3)
        self.d2 = tk.Button(self.button_frame, image = self.get_image(self.position, [6, 3]), command = lambda : self.return_square([6, 3]))
        self.d2.grid(row = 6, column = 3)
        self.d1 = tk.Button(self.button_frame, image = self.get_image(self.position, [7, 3]), command = lambda : self.return_square([7, 3]))
        self.d1.grid(row = 7, column = 3)

        self.e8 = tk.Button(self.button_frame, image = self.get_image(self.position, [0, 4]), command = lambda : self.return_square([0, 4]))
        self.e8.grid(row = 0, column = 4)
        self.e7 = tk.Button(self.button_frame, image = self.get_image(self.position, [1, 4]), command = lambda : self.return_square([1, 4]))
        self.e7.grid(row = 1, column = 4)
        self.e6 = tk.Button(self.button_frame, image = self.get_image(self.position, [2, 4]), command = lambda : self.return_square([2, 4]))
        self.e6.grid(row = 2, column = 4)
        self.e5 = tk.Button(self.button_frame, image = self.get_image(self.position, [3, 4]), command = lambda : self.return_square([3, 4]))
        self.e5.grid(row = 3, column = 4)
        self.e4 = tk.Button(self.button_frame, image = self.get_image(self.position, [4, 4]), command = lambda : self.return_square([4, 4]))
        self.e4.grid(row = 4, column = 4)
        self.e3 = tk.Button(self.button_frame, image = self.get_image(self.position, [5, 4]), command = lambda : self.return_square([5, 4]))
        self.e3.grid(row = 5, column = 4)
        self.e2 = tk.Button(self.button_frame, image = self.get_image(self.position, [6, 4]), command = lambda : self.return_square([6, 4]))
        self.e2.grid(row = 6, column = 4)
        self.e1 = tk.Button(self.button_frame, image = self.get_image(self.position, [7, 4]), command = lambda : self.return_square([7, 4]))
        self.e1.grid(row = 7, column = 4)
        
        self.f8 = tk.Button(self.button_frame, image = self.get_image(self.position, [0, 5]), command = lambda : self.return_square([0, 5]))
        self.f8.grid(row = 0, column = 5)
        self.f7 = tk.Button(self.button_frame, image = self.get_image(self.position, [1, 5]), command = lambda : self.return_square([1, 5]))
        self.f7.grid(row = 1, column = 5)
        self.f6 = tk.Button(self.button_frame, image = self.get_image(self.position, [2, 5]), command = lambda : self.return_square([2, 5]))
        self.f6.grid(row = 2, column = 5)
        self.f5 = tk.Button(self.button_frame, image = self.get_image(self.position, [3, 5]), command = lambda : self.return_square([3, 5]))
        self.f5.grid(row = 3, column = 5)
        self.f4 = tk.Button(self.button_frame, image = self.get_image(self.position, [4, 5]), command = lambda : self.return_square([4, 5]))
        self.f4.grid(row = 4, column = 5)
        self.f3 = tk.Button(self.button_frame, image = self.get_image(self.position, [5, 5]), command = lambda : self.return_square([5, 5]))
        self.f3.grid(row = 5, column = 5)
        self.f2 = tk.Button(self.button_frame, image = self.get_image(self.position, [6, 5]), command = lambda : self.return_square([6, 5]))
        self.f2.grid(row = 6, column = 5)
        self.f1 = tk.Button(self.button_frame, image = self.get_image(self.position, [7, 5]), command = lambda : self.return_square([7, 5]))
        self.f1.grid(row = 7, column = 5)

        self.g8 = tk.Button(self.button_frame, image = self.get_image(self.position, [0, 6]), command = lambda : self.return_square([0, 6]))
        self.g8.grid(row = 0, column = 6)
        self.g7 = tk.Button(self.button_frame, image = self.get_image(self.position, [1, 6]), command = lambda : self.return_square([1, 6]))
        self.g7.grid(row = 1, column = 6)
        self.g6 = tk.Button(self.button_frame, image = self.get_image(self.position, [2, 6]), command = lambda : self.return_square([2, 6]))
        self.g6.grid(row = 2, column = 6)
        self.g5 = tk.Button(self.button_frame, image = self.get_image(self.position, [3, 6]), command = lambda : self.return_square([3, 6]))
        self.g5.grid(row = 3, column = 6)
        self.g4 = tk.Button(self.button_frame, image = self.get_image(self.position, [4, 6]), command = lambda : self.return_square([4, 6]))
        self.g4.grid(row = 4, column = 6)
        self.g3 = tk.Button(self.button_frame, image = self.get_image(self.position, [5, 6]), command = lambda : self.return_square([5, 6]))
        self.g3.grid(row = 5, column = 6)
        self.g2 = tk.Button(self.button_frame, image = self.get_image(self.position, [6, 6]), command = lambda : self.return_square([6, 6]))
        self.g2.grid(row = 6, column = 6)
        self.g1 = tk.Button(self.button_frame, image = self.get_image(self.position, [7, 6]), command = lambda : self.return_square([7, 6]))
        self.g1.grid(row = 7, column = 6)

        self.h8 = tk.Button(self.button_frame, image = self.get_image(self.position, [0, 7]), command = lambda : self.return_square([0, 7]))
        self.h8.grid(row = 0, column = 7)
        self.h7 = tk.Button(self.button_frame, image = self.get_image(self.position, [1, 7]), command = lambda : self.return_square([1, 7]))
        self.h7.grid(row = 1, column = 7)
        self.h6 = tk.Button(self.button_frame, image = self.get_image(self.position, [2, 7]), command = lambda : self.return_square([2, 7]))
        self.h6.grid(row = 2, column = 7)
        self.h5 = tk.Button(self.button_frame, image = self.get_image(self.position, [3, 7]), command = lambda : self.return_square([3, 7]))
        self.h5.grid(row = 3, column = 7)
        self.h4 = tk.Button(self.button_frame, image = self.get_image(self.position, [4, 7]), command = lambda : self.return_square([4, 7]))
        self.h4.grid(row = 4, column = 7)
        self.h3 = tk.Button(self.button_frame, image = self.get_image(self.position, [5, 7]), command = lambda : self.return_square([5, 7]))
        self.h3.grid(row = 5, column = 7)
        self.h2 = tk.Button(self.button_frame, image = self.get_image(self.position, [6, 7]), command = lambda : self.return_square([6, 7]))
        self.h2.grid(row = 6, column = 7)
        self.h1 = tk.Button(self.button_frame, image = self.get_image(self.position, [7, 7]), command = lambda : self.return_square([7, 7]))
        self.h1.grid(row = 7, column = 7)

        self.button_frame.pack()
        self.button_frame.place(anchor = 'nw')

        self.reset_move_button = tk.Button(text = 'Reset Move', command = self.reset_move)
        self.reset_move_button.pack()
        self.reset_move_button.place(height = 100, width = 100, x = 800, y = 0)

        self.next_move_button = tk.Button(text = 'Next Move', command = self.close)
        self.next_move_button.pack()
        self.next_move_button.place(height = 100, width = 100, x = 800, y = 100)

        self.submit_move_button = tk.Button(text = 'Submit Move', command = self.submit_move)
        self.submit_move_button.pack()
        self.submit_move_button.place(height = 100, width = 100, x = 800, y = 200)

        self.promote_to_knight_button = tk.Button(text = 'Promote to a Knight', command = lambda : self.return_promotion('Knight'))
        self.promote_to_knight_button.pack()
        self.promote_to_knight_button.place(height = 100, width = 150, x = 620, y = 350)

        self.promote_to_knight_button = tk.Button(text = 'Promote to a Bishop', command = lambda : self.return_promotion('Bishop'))
        self.promote_to_knight_button.pack()
        self.promote_to_knight_button.place(height = 100, width = 150, x = 800, y = 350)

        self.promote_to_knight_button = tk.Button(text = 'Promote to a Rook', command = lambda : self.return_promotion('Rook'))
        self.promote_to_knight_button.pack()
        self.promote_to_knight_button.place(height = 100, width = 150, x = 620, y = 500)

        self.promote_to_knight_button = tk.Button(text = 'Promote to a Queen', command = lambda : self.return_promotion('Queen'))
        self.promote_to_knight_button.pack()
        self.promote_to_knight_button.place(height = 100, width = 150, x = 800, y = 500)

    def open(self):
        self.root.mainloop()

    def close(self):
        self.root.destroy()

    def get_image(self, position, square): #takes a position and requested square, returns an image of the piece (or lack thereof) on that square
        if sum(square) % 2 == 0: #the piece is on a white square, since 0, 0 is white

            if position[square[0]][square[1]] == 0: #square is empty
                return self.empty_white
            
            elif position[square[0]][square[1]] == 'White Pawn':
                return self.white_pawn_white
            elif position[square[0]][square[1]] == 'White Rook':
                return self.white_rook_white
            elif position[square[0]][square[1]] == 'White Knight':
                return self.white_knight_white
            elif position[square[0]][square[1]] == 'White Bishop':
                return self.white_bishop_white
            elif position[square[0]][square[1]] == 'White Queen':
                return self.white_queen_white
            elif position[square[0]][square[1]] == 'White King':
                return self.white_king_white
            
            elif position[square[0]][square[1]] == 'Black Pawn':
                return self.black_pawn_white
            elif position[square[0]][square[1]] == 'Black Rook':
                return self.black_rook_white
            elif position[square[0]][square[1]] == 'Black Knight':
                return self.black_knight_white
            elif position[square[0]][square[1]] == 'Black Bishop':
                return self.black_bishop_white
            elif position[square[0]][square[1]] == 'Black Queen':
                return self.black_queen_white
            elif position[square[0]][square[1]] == 'Black King':
                return self.black_king_white

        else: #we're on a black square

            if position[square[0]][square[1]] == 0: #square is empty
                return self.empty_black
            
            elif position[square[0]][square[1]] == 'White Pawn':
                return self.white_pawn_black
            elif position[square[0]][square[1]] == 'White Rook':
                return self.white_rook_black
            elif position[square[0]][square[1]] == 'White Knight':
                return self.white_knight_black
            elif position[square[0]][square[1]] == 'White Bishop':
                return self.white_bishop_black
            elif position[square[0]][square[1]] == 'White Queen':
                return self.white_queen_black
            elif position[square[0]][square[1]] == 'White King':
                return self.white_king_black
            
            elif position[square[0]][square[1]] == 'Black Pawn':
                return self.black_pawn_black
            elif position[square[0]][square[1]] == 'Black Rook':
                return self.black_rook_black
            elif position[square[0]][square[1]] == 'Black Knight':
                return self.black_knight_black
            elif position[square[0]][square[1]] == 'Black Bishop':
                return self.black_bishop_black
            elif position[square[0]][square[1]] == 'Black Queen':
                return self.black_queen_black
            elif position[square[0]][square[1]] == 'Black King':
                return self.black_king_black

    def return_square(self, square): # stores squares the human clicks on
        if self.human_move[0] == None:
            self.human_move[0] = square
        else:
            self.human_move[1] == None #not sure why I wrote this, but it ain't broke, so I'm not fixing it
            self.human_move[1] = square

    def return_promotion(self, piece): #adds the 'promote_to' argument if the human ever promotes to something
        self.human_move.append(piece)

    def reset_move(self): #resets move, in case human misclicks
        self.human_move = [None, None]

    def submit_move(self):
        if None not in self.human_move[:2]:
            #it could be that we have forgotten to promote
            if (self.position[self.human_move[0][0]][self.human_move[0][1]][6:] == 'Pawn') and (self.human_move[1][0] % 7 == 0): #hopefully this says 'if the piece we're trying to move is a pawn and it's destination is the back rank:'
                if self.human_move[2] == None:
                    print('you have not told me what to promote to')
                else:
                    self.close()
            else:
                self.close() #closing the window has the same effect as submitting the move, in this case
        else:
            print('you havent given me a move')

def show_game(player1, player2):
    current_board = Board() #generate the starting board
    previous_boards = [copy.deepcopy(current_board)]
    possible_moves = current_board.generate_all_legal_moves() #possible moves is also the name of the argument that player's "choose a move" function accepts. I wonder if this will cause a problem
    result = None #flip this when the game is over
    while result == None: #while the game is still going

        # In positions like check, stalemate and checkmate, many moves in possible_moves won't actually be legal. I think it would be quite inefficient to check that all my proposed moves are really legal, because usually they will be.
        # I'll ask if a randomly selected move is legal, if it isn't, check them all.
        candidate_move = random.choice(possible_moves)
        if not is_that_move_legal(candidate_move, current_board): #a randomly selected move is illegal, let's check them all
            to_remove = []
            for move in possible_moves:
                if not is_that_move_legal(move, current_board):
                    to_remove.append(move)
            for move in to_remove:
                possible_moves.remove(move)

        if possible_moves == []: #there are no legal moves, the game is about to end just have to figure out why
            print('I think the game is over')
            the_board_gui.open()
            #check for mate. Your king must be hanging
            if current_board.turn_player == 'White': #if white might be getting mated
                if is_the_king_hanging(current_board, 'Black'): #if it's check, it's mate, since we only got to this check bc there are no legal moves
                    result = 'Black Wins!'
                else: #no legal moves and not check means stalemate
                    result = 'Stalemate!'
            else:
                if is_the_king_hanging(current_board, 'White'):
                    result = 'White Wins!'
                else:
                    result = 'Stalemate'

        else: #get a move from the turn player
            the_board_gui = GameGUI(current_board.position) #the board gui is the gui, current position is the postion. Very different things
            if ((current_board.turn_player == 'White') and (player1 == 'Human')) or ((current_board.turn_player == 'Black' and player2 == 'Human')): #if the turn player is human
                print('I think it is humans turn')
                human_gave_a_legal_move = False # expect the worst
                while not human_gave_a_legal_move:
                    the_board_gui.open() # when closed, should have given a move
                    candidate_move = the_board_gui.human_move
                    if None in candidate_move:
                        the_board_gui = GameGUI(current_board.position) #create the board again bc I destroyed it
                        pass #remind user to click 2 buttons                   
                    elif candidate_move not in possible_moves:
                        the_board_gui = GameGUI(current_board.position) #create the board again bc I destroyed it
                        print('illegal') #moved the piece wrongly
                    elif not is_that_move_legal(candidate_move, current_board):
                        the_board_gui = GameGUI(current_board.position) #create the board again bc I destroyed it
                        #move was illegal, tell the user so
                        pass
                    else: # move was legal!
                        human_gave_a_legal_move = True

            else: #player is not a human
                print('I think it is the cpus turn')
                the_board_gui.open()

                computer_gave_a_legal_move = False #expect the worst
                while not computer_gave_a_legal_move:      
                    #get the move             
                    if current_board.turn_player == 'White':
                        candidate_move = player1.choose_move(current_board, possible_moves)
                    else:
                        candidate_move = player2.choose_move(current_board, possible_moves)
                    #check the move
                    if not is_that_move_legal(candidate_move, current_board):
                        possible_moves.remove(candidate_move)
                    else:
                        computer_gave_a_legal_move = True
                    
            #promotions are lists of length 3, the following makes the move. Bodge, but works.
            if len(candidate_move) == 3:
                current_board.make_move(candidate_move[0], candidate_move[1], candidate_move[2])
            else:
                current_board.make_move(candidate_move[0], candidate_move[1])
            previous_boards.append(copy.deepcopy(current_board))
            if current_board.consecutive_boring_moves == 100:
                result = '50 Move Draw!'
            possible_moves = current_board.generate_all_legal_moves() # get all the legal moves for the next position 

            #the following handles 3-fold repetition
            if len(previous_boards) > 1:
                test_board = previous_boards[-1]
                count = 0
                for board in previous_boards[:-1]:
                    if repeated_position(test_board, board):
                        count += 1
                if count == 2:
                    result = 'Draw by 3-fold Repetition!'

    print(result)

my_player = Player(pawn_value = 1, rook_value = 5, knight_value = 3, bishop_value = 3, queen_value = 9, move_value = 0.05, undeveloped_minor_cost = 0.2, early_queen_move_cost = 0.5, castled_value = 0.5, centre_pawn_value = 0.35, early_king_move_cost = 1, early_king_rook_move_cost = 1, early_queen_rook_move_cost = 0.1, depth = 4, checks_and_captures_only = True)
show_game('Human', my_player)
#show_game(my_player, 'Human')

#Future Plans
#game against pepper: missed mate in 1. How?
#it is still playing some surprsingly weak moves. I think it is related to the fact that I'm only checking checks and captures. Why take a free piece next move if you can just take it next move (you will stil be able to, because moves that defend it are not being considered)
#easier UI
#for now, if there are no plausible moves in a position, I just try to evaluate it as 0. This should be quite an edge case 
# make it show the checkmate position, just says 'such and such wins' now.
#create game() that doesn't show the board, or modify show_game so that it only shows the board if you ask it to do so
#use game to have the cpu play against itself, adjusting its hyperparameters to improve.
#implement alpha beta pruning.
