# Duran Reddy (2353785), Eric Yuan (2332155), Sani Abdullahi Sani (2770930)
#Imports
import chess
import chess.engine
from reconchess import *
import random
from reconchess.utilities import without_opponent_pieces
from reconchess.utilities import is_illegal_castle
import time
import numpy as np
import math
from collections import Counter


class MyAgentPlayer(Player):

    def printBoard(self):
        print(chess.Board(self.board))

    def getNextMoves(self,board):

        legalMoves = list(board.pseudo_legal_moves)
        legalMoves.append(chess.Move.null())

        return legalMoves

    def getStates(self,board):
        boardObj = chess.Board(board)
        moves = self.getNextMoves(boardObj)

        positions = []

        for move in moves:
            new_board = boardObj.copy()
            new_board.push(move)
            positions.append(new_board.fen())

        return positions

    def statesAfterCapture(self,board, captured):
        boardObj = chess.Board(board)
        moves = self.getNextMoves(boardObj)
        canCapture = []

        for move in moves:
            if boardObj.is_capture(move) and move.to_square == captured:
                nextBoard = boardObj.copy()
                nextBoard.push(move)
                canCapture.append(nextBoard.fen())

        return canCapture

    def statePredictionWithSensingOriginal(self,boards, window):
        potential_states = []

        pairs = window.split(';')
        keyValue = [pair.split(':') for pair in pairs]

        windowDict = {key: (value if value != '?' else None) for key, value in keyValue}

        for fen in boards:
            board = chess.Board(fen)
            flag = True

            for key in windowDict:
                if (str(board.piece_at(chess.parse_square(key))) != str(windowDict[key])):
                    flag = False
                    break

            if flag:
                potential_states.append(fen)

        return potential_states

    def statePredictionWithSensing(self,boards, window):
        potential_states = []

        # Convert the window format to a dictionary
        windowDict = {chess.square_name(square): piece for square, piece in window}

        for fen in boards:
            board = chess.Board(fen)
            flag = True

            for square, piece in windowDict.items():
                if str(board.piece_at(chess.parse_square(square))) != str(piece):
                    flag = False
                    break

            if flag:
                potential_states.append(fen)

        return potential_states

    def makeMove(self,board,timePerMove):
        enemyKing = board.king(not board.turn)

        if enemyKing is not None:
            if board.attacks(enemyKing):
                enemyKingAttackers = board.attackers(board.turn,enemyKing)
                if enemyKingAttackers:
                    # If so, capture the opposing king
                    attacker_square = chess.square_name(enemyKingAttackers.pop())
                    return attacker_square + chess.square_name(enemyKing)

        #Couldnt attack the king so make a stockfish move
        result = self.engine.play(board, chess.engine.Limit(time=timePerMove))  # Adjust the time limit as needed
        return result.move

    def multiMoves(self,boards,timePerMove):
        moves = {}

        for fen in boards:
            board = chess.Board(fen)

            if(board.king(not self.color) is None):
                # We captured the opposing king and the game didnt end so remove the state
                continue
            

            if(board.king(self.color)==None):
                # Our king was captured and game didnt end so remove the state
                continue

            move = self.makeMove(board,timePerMove)
            if move in moves:
                moves[move] += 1
            else:
                moves[move] = 1

        sorted_moves = sorted(moves.items(), key=lambda x: (-x[1], str(x[0])))

        return sorted_moves

    def get_best_sense_for_state(self, state):

        local_best_square = None
        local_best_score = float('-inf')

        board=chess.Board(state)
        available_squares = [chess.square_name(sq) for sq in chess.SQUARES if not (chess.square_file(sq) in [0, 7] or chess.square_rank(sq) in [0, 7])]


        if board.king(self.color) is None:
            return None

        for square in chess.SQUARES:
            
            square_name = chess.square_name(square)
            # Get piece on the current square (consider for potential check reveal)
            score=0
            piece = board.piece_at(square)
            if piece is not None and piece.color != self.color:
                if board.is_attacked_by(self.color, chess.KING):
                    score = 20


            # Define offsets for the 3x3 grid
            offsets = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1), (0, 0), (0, 1),
                    (1, -1), (1, 0), (1, 1)]

            # Iterate over offsets within the 3x3 grid
            for offset in offsets:
                target_x = chess.square_file(square) + offset[0]
                target_y = chess.square_rank(square) + offset[1]

                # Check if target square is within board boundaries
                if 0 <= target_x <= 7 and 0 <= target_y <= 7:
                    target_square = chess.square(target_x, target_y)

                    #Weigh pieces that are closer to the king as stronger positions
                    king_square = board.king(self.color)  # Get the King's square
                    king_file = chess.square_file(king_square)
                    king_rank = chess.square_rank(king_square)

                    squared_distance = (target_x - king_file)**2 + (target_y - king_rank)**2
                    distance = math.sqrt(squared_distance + 1e-6)  # Add epsilon to avoid domain error
                    distMultiplier = (8 * math.sqrt(2)) - distance

                    # Evaluate piece on the target square
                    target_piece = board.piece_at(target_square)
                    if target_piece is not None and target_piece.color != self.color:
                        piece_type = target_piece.piece_type
                        if piece_type == chess.PAWN:
                            score += 1
                        elif piece_type in (chess.KNIGHT, chess.BISHOP):
                            score += 3
                        elif piece_type == chess.ROOK:
                            score += 5
                        elif piece_type == chess.QUEEN:
                            score += 8
                        else:  # King or empty square
                            score += 6
                        
                        score+=distMultiplier
            

            # Update best square for this state based on score
            if score > local_best_score:
                local_best_square = square
                local_best_score = score

        return local_best_square

    def is_adjacent_to_last_sensed(self, square):
        count=0
        for last_square in self.lastSensed:
            if self.is_adjacent(square, last_square):
                count+=1
        return count

    def is_adjacent(self, square1, square2):
        # Check if two squares are adjacent (in the same row/column)
        file_diff = abs(chess.square_file(square1) - chess.square_file(square2))
        rank_diff = abs(chess.square_rank(square1) - chess.square_rank(square2))
        return file_diff <= 1 and rank_diff <= 1

    def update_last_sensed(self, square):
        self.lastSensed.append(square)
        if len(self.lastSensed) > 3:
            self.lastSensed.pop(0)  # Maintain only the last 3 sensed squares

    def __init__(self):
        # setup agent as you see fit
        self.board = None #What we believe the current board to be
        self.color = None
        self.last_piece_captured_square = None
        self.potential_states = set()
        # self.engine = chess.engine.SimpleEngine.popen_uci('./stockfish.exe', setpgrp=True)
        self.engine = chess.engine.SimpleEngine.popen_uci('/opt/stockfish/stockfish', setpgrp=True)
        self.numTurns = 0
        self.lastSensed = []
        self.ourLastCapturedSquare = None
        #Eric
        self.senseResult = None 
        self.openingBranch = 0
        self.openingSenseList = []
        self.openingMovesList = []
        self.squaresICareAbout = []

        randoNo = random.random()
        if(randoNo < 0.3): #30% chance to use horse opening
            self.openingSenseList = [[[""],["e5"],["e7"], [["e7"], [""]]],  #white
                                     [["d3"], [["b4"],[""]], [["c3"],[""]], [["e2"],[""]]]]  #black
            self.openingMovesList = [[["b1c3"], ["c3d5"], ["d5f6"]],  #white
                                      [["b8c6"], ["c6b4"], ["b4d3"]]] #black
            self.squaresICareAbout = [[[""],[["d5-a"]],[["f6-a"]],[["e8-a"]]], #white
                                      [[""],[["b4-a"]],[["d3-a"]],[["e1-K"]]]] #black
        else: #70% chance to use fools opening
            self.openingSenseList = [[[""],["f7"],["e7"], ["f7"],["d7"],[""],["d7"]], #white
                                     [["d3"],[[""],["e2"]], ["c4"], ["c3"],["c3"]]]   #black
            #self.openingMovesList = [[["e2e4"], ["f1c4"],[["d1h5"],["e4d5"]],[["h5f7"],["d1h5"]],[[""],["c4b5"]],[""]], #white
            self.openingMovesList = [[["e2e4"], ["f1c4"],[["d1h5"],["e4d5"]],[["h5f7"],["d1h5"],["c4b5"]],[[""],["c4b5"],["d1h5"]],[""]], #white                          
                                     [["d7d5"], [["c7c6"], ["e7e6"]],[["g8f6"],["e7e6"]],[["d8a5"], [""]]]] #black
            self.squaresICareAbout = [[[""],[""],[["d7.p"],["d6.p"]],[["e7-a"],["g6-a"]], [""]], #white
                                      [[""], [""], [["d5-P"],["c3-a"],["b1-a"]],[["c3-a"],["b1-a"]], [["c3-a"],["b1-a"]]]] #black

        # engine = chess.engine.SimpleEngine.popen_uci('/opt/stockfish/stockfish', setpgrp=True)
        pass

    def handle_game_start(self, color, board, opponent_name):
        # function that is run when the game starts
        self.board = board.fen()
        self.color = color
        self.potential_states.add(board.fen())

        if(self.color): #white
            self.openingSenseList = self.openingSenseList[0]
            self.openingMovesList = self.openingMovesList[0]
            self.squaresICareAbout = self.squaresICareAbout[0]
        else: #black
            self.openingSenseList = self.openingSenseList[1]
            self.openingMovesList = self.openingMovesList[1]
            self.squaresICareAbout = self.squaresICareAbout[1]

        pass

    def handle_opponent_move_result(self, captured_my_piece, capture_square):
        # feedback on whether the opponent captured a piece

        #If its the first turn and we're white, calling this method produces an error, so skip this method in this case
        if(self.color and self.numTurns==0):
            self.numTurns += 1
            return
        
        self.numTurns += 1
        tempStates = set() #will store temp states so we can remove the states as need be

        if(captured_my_piece):

            #A piece was captured so we sort the list of potential states for the
            self.last_piece_captured_square=capture_square
            for state in self.potential_states:

                if chess.Board(state).piece_at(capture_square) is None or chess.Board(state).piece_at(capture_square).color != self.color:
                    #state believed that we didnt have a piece there, or that an opponent had a piece there
                    continue


                newStates = self.statesAfterCapture(state,capture_square)
                if(newStates!=None):
                    #Add the new states to the potential state
                    tempStates.update(newStates)
        else:
            #No piece was captured so just update all the states
            self.last_piece_captured_square=None
            for state in self.potential_states:
                newStates = self.getStates(state)
                tempStates.update(newStates)
        self.potential_states=tempStates
        pass
    
    def openingSense(self): #Eric
        openingSensList = self.openingSenseList
        
        if(self.numTurns <= len(openingSensList)):
            senseSquare = openingSensList[self.numTurns-1]
            if(len(senseSquare) > 1): #more than one sensing
                index = min(len(senseSquare), self.openingBranch) #find closest branch to current
                senseSquare = senseSquare[index]
            return senseSquare[0]
        else:
            return ""

    def query_window(self, location):
        for square_index, piece in self.senseResult:
            if square_index == location:
                return piece
        return None

    def evaluateSenseResult(self):
        squaresICareAbout = self.squaresICareAbout
        
        if(self.numTurns >= len(squaresICareAbout)):
            return
        
        squaresICareAbout = squaresICareAbout[self.numTurns-1]
        window = self.senseResult
        #windowDict = {chess.square: piece for square, piece in window}
        flag = False #check if any conditions have been met to branch
        for squares in squaresICareAbout:
            if(squares == "" and flag == False):
                continue
            else:
                orValid = True
                valid = True
                for s in squares:
                    squareLoc = s[:2]
                    tempPiece = s[-1]

                    numLoc = chess.SQUARE_NAMES.index(squareLoc)
                    actPiece = self.query_window(numLoc)
                    
                    if(s[-2] == "."):
                        if(tempPiece == actPiece or (actPiece != None and tempPiece == "a")):
                            orValid = True
                            continue
                        else:
                            orValid = False
                    elif(s[-2] == "-"):
                        if(actPiece != None and (actPiece == tempPiece or (tempPiece == "a" and actPiece != None))):
                            valid = False

                    elif(s[-2] == "+"):
                        if(actPiece != tempPiece or (actPiece != None and tempPiece == "a")):
                            valid = False
                if(not(orValid and valid)):
                    flag = True
                    self.openingBranch = self.openingBranch + 1
                    break
        
        #check if potential threat is made
        #screw it hard code
        if(self.numTurns == 4 and self.last_piece_captured_square == 35):
            self.openingBranch = self.openingBranch+1
        #if time to add
        if(self.last_piece_captured_square != None):
            openingPieceCaptured = False
            for move in self.openingMovesList:
                m = move
                if(len(move) > 1): #more than one available move
                    index = min(len(move)-1, self.openingBranch) #select closest move to current
                    m = move[index]
                m = m[0]
                if(m == ""):
                    continue
                if(chess.parse_square(m[-2:]) == self.last_piece_captured_square):
                    openingPieceCaptured = True


            if(openingPieceCaptured): #opening sequence ruined
                self.openingMovesList = []
                self.openingSenseList = []
                self.squaresICareAbout = []
    
    def openingMove(self, moveActions):
        openingMoves = self.openingMovesList

        self.evaluateSenseResult()

        #sense calculations stuff
        if(self.numTurns > len(openingMoves)):
            return ""
        move = openingMoves[self.numTurns-1]

        if(len(move) > 1): #more than one available move
            index = min(len(move)-1, self.openingBranch) #select closest move to current
            move = move[index]
        if(move == ""): #throwaway move
            return ""
        if(str(moveActions).find(move[0]) != -1):
            return move[0]
        else:
            self.openingBranch = self.openingBranch +1
        return ""

    def choose_sense(self, sense_actions, move_actions, seconds_left):
        # write code here to select a sensing move
        sense = self.openingSense() #Eric
        if(sense != ""):
            return chess.parse_square(sense)

        #If they captured our piece, sense around it to see if we can capture it
        if(self.last_piece_captured_square!=None):
            return self.last_piece_captured_square
        
        #If we captured their piece, predict their move to attack our piece
        if(self.ourLastCapturedSquare!=None):
            file, rank = chess.square_file(self.ourLastCapturedSquare), chess.square_rank(self.ourLastCapturedSquare)

            # Move the square inwards if it's on the border
            if file == 0:
                file += 1
            elif file == 7:
                file -= 1
            if rank == 0:
                rank += 1
            elif rank == 7:
                rank -= 1

            # Return the updated square
            return chess.square(file, rank)

        sampleStates = 500

        if len(self.potential_states)<500: #Will picj 500 boards to base the sensing on
            sampleStates = len(self.potential_states)

        if len(self.potential_states) ==0:
            available_squares = [chess.square_name(sq) for sq in chess.SQUARES if not (chess.square_file(sq) in [0, 7] or chess.square_rank(sq) in [0, 7])] #Gets all squares that arent on the corners
            choice = chess.parse_square(random.choice(available_squares))
            self.lastSensed = choice
            return choice

        # Iterate over all boards
        squareCounter = Counter()
        #All the senses
        for state in random.sample(self.potential_states, sampleStates):
            if state is None:
                continue
            current_best_square = self.get_best_sense_for_state(state)
            # Update global best square and score if better candidate found
            if current_best_square is not None:
                squareCounter[current_best_square] += 1

        
        sorted_squares = sorted(squareCounter.items(), key=lambda item: item[1], reverse=True)
        for i, (square, count) in enumerate(sorted_squares):
            if self.lastSensed !=None:
                adjacent_square_count = self.is_adjacent_to_last_sensed(square)
                if adjacent_square_count>0:
                    if i < len(sorted_squares) - 1 and random.random() < adjacent_square_count*0.3:
                        continue
                    self.update_last_sensed(square)
                    return square
                self.update_last_sensed(square)
                return square
            else:
                last_square = sorted_squares[0][0]
                self.update_last_sensed(last_square)
                return last_square
                
        last_square = sorted_squares[-1][0]
        self.update_last_sensed(last_square)
        return last_square
    
    def handle_sense_result(self, sense_result):
        # This is where the sensing result returns feedback

        #Remove the states that dont correspond with the sensed window
        if(len(self.potential_states)>1):
            newStates = self.statePredictionWithSensing(self.potential_states,sense_result)
            self.potential_states.clear()
            self.potential_states.update(newStates)
        self.senseResult = sense_result #Eric
        pass

    def choose_move(self, move_actions, seconds_left):
        # execute a chess move
        move = self.openingMove(move_actions)
        if(move != ""):
            return chess.Move.from_uci(move)

        moves = None
        if(len(self.potential_states)>10000):
            #Too many states, thus randomly remove until we have 10000
            random_sample = random.sample(self.potential_states, 10000)
            # self.potential_states = set(random_sample)
            #Find the best move to make from 10000 states
            moves = self.multiMoves(random_sample,0.001)

        #Find the best move to make from all the states
        try:
            moves= self.multiMoves(self.potential_states,10/(len(self.potential_states)))
        except ZeroDivisionError:
            moves = self.multiMoves(self.potential_states,0.001)

        #For some reasons sometimes move is a string and sometimes it is a Move object, so convert it to a Move object if need be
        for potential_move in moves:
            move = potential_move[0]
            if(type(move)==str):
                move = chess.Move.from_uci(move)
            
            #Can make the move so make it
            if move in move_actions:
                return move
        pass

    def handle_move_result(self, requested_move, taken_move, captured_opponent_piece, capture_square):
        # this function is called after your move is executed.

        if(captured_opponent_piece):
            self.ourLastCapturedSquare = capture_square
        else:            
            self.ourLastCapturedSquare = None

        #Proposed method where we remove the states that can make the requested_move if it wasnt taken and states that cant make taken_move
        tempStates = self.potential_states.copy()
        for state in self.potential_states:

            #Check if the requested_move and taken_move are legal in the state
            requested_move_legality = chess.Board(state).is_legal(requested_move)
            taken_move_legality = chess.Board(state).is_legal(taken_move)

            #See if the state captured the enemy king. If they did, then the game would end, so we did not actually do this
            if(chess.Board(state).king(not self.color) is None):
                tempStates.remove(state)
                continue

            if taken_move is None:
                 if requested_move_legality:
                    tempStates.remove(state) #taken_move was None, so no move could have been made, so remove states where requested_move was legal
            elif requested_move.uci()!=taken_move.uci():
                #remove all states where the requested move is legal and all states where taken move is illegal:
                if(requested_move_legality or not taken_move_legality):
                    tempStates.remove(state)
            else: #taken_move=requested_move
                #remove all states where the requested move is illegal
                if(not requested_move_legality):
                    tempStates.remove(state)


        statesAfterMove = []
        for state in tempStates:
            checkState = chess.Board(state)

            if(taken_move is None): #Push null move if taken_move is None
                checkState.push(chess.Move.null())
            else:
                if checkState.king(not checkState.turn) == checkState.piece_at(chess.parse_square(taken_move.uci()[2:4])): #If the resultant move would result in a king capture, game would end, so remove this state
                    continue;
                checkState.push(taken_move)
            statesAfterMove.append(checkState.fen())

        self.potential_states.clear()
        self.potential_states.update(statesAfterMove)

        pass

    def handle_game_end(self, winner_color, win_reason, game_history):
        # shut down everything at the end of the game
        self.engine.quit()
        pass

