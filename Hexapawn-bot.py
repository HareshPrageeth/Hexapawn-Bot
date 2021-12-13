
import random

#Global variables
board = [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]

###############################################

#Returns True if there is a move, player = -1 for user and +1 for computer
def anymove(player):
    li = []
    moves = []
    for row in range(3):
        for column in range(3):
            if board[column][row] == player:
                if valid(row, column)!= []:
                    moves.append(valid(row, column))
    if moves == []:
        return (False)
    else:
        return (True)

##############################################################################

#computer's move, makes a random move from all of the computer's possible moves
#call function when it's computer's turn
def compmove():
    li = []
    allmoves = []
    for row in range(3):
        for column in range(3):
            if board[column][row] == 1:
                li.append([row,column])
    for pawn in li:
        for place in valid(pawn[0],pawn[1]):
            allmoves.append([pawn, place])
    if len(allmoves) != 0:
        #move = allmoves[random.randint(0,len(allmoves))]
        ##haresh
        move = allmoves[random.randint(0,len(allmoves)-1)]
        #updateboard(board, move[0][0], move[0][1], move[1][0], move[1][1])
        #return (board)
        updateboard( move[0][0], move[0][1], move[1][0], move[1][1])
    else:
        print("No moves possible.")
        #return(board)

###############################################################################

#input coordinate of pawn and obtain possible places to move to
#if [place_x, place_y] in valid(pawn_x, pawn_y), the move is valid
def valid(pawn_x, pawn_y):
    direc = board[pawn_y][pawn_x]
    possible_moves = []
    if pawn_y + direc in range(3):
        for i in (-1,1):
            if pawn_x + i in range(3) and board[pawn_y + direc][pawn_x + i] == -(board[pawn_y][pawn_x]):
                possible_moves.append([pawn_x + i, pawn_y + direc])
        if board[pawn_y + direc][pawn_x] == 0:
            possible_moves.append([pawn_x, pawn_y + direc])
    return(possible_moves)

#####################################################

#general board updation
def updateboard(pawn_x, pawn_y, place_x, place_y):
    board[place_y][place_x] = board[pawn_y][pawn_x]
    board[pawn_y][pawn_x]=0
    return board

################################################################################
#Returns 1 if the human won, -1 if the computer won and 0 if the game is still running
def gameover(board,turn):
    # checking if the human pawns are not there
    if -1 not in board[0] and -1 not in board[1] and -1 not in board[2]:
        return 1

    # checking if the comp pawns are not there
    elif 1 not in board[0] and 1 not in board[1] and 1 not in board[2]:
        return -1

    # checking if the human pawn reached the end
    elif -1 in board[0]:
        return -1

    # checking if the comp pawn reached the end
    elif 1 in board[2]:
        return 1

    # checking if the comp has no valid move to play
    elif not anymove(1) and turn == 1:
        return -1

    # checking if the human has no valid move to play
    elif not anymove(-1) and turn == -1:
        return 1

    else:
        return 0

####################################################################################


def displayboard(board):
  print(" {:^3} {:^3} {:^3}".format("0","1","2"))
  for row in range(3):
      for col in range(3):
          if board[row][col]==1:
              print("| x ",end='')
          elif board[row][col]==0:
              print("|   ",end='')
          elif board[row][col]==-1:
              print("| o ",end='')
      print("|{:^3}".format(str(row)))

#########################################################################################

def displayboard(board):
  print(" {:^3} {:^3} {:^3}".format("0","1","2"))
  for row in range(3):
      for col in range(3):
          if board[row][col]==1:
              print("| x ",end='')
          elif board[row][col]==0:
              print("|   ",end='')
          elif board[row][col]==-1:
              print("| o ",end='')
      print("|{:^3}".format(str(row)))

#########################################################################################

def userInput():
    valid_co = [0,1,2]
    invalid_inp = True
    while (invalid_inp):
        inp = input("Enter coordinates of pawn to move in the format (x,y):")
        invalid_inp = ("," not in inp) and inp.endswith(")") and inp.startswith("(")
        if not invalid_inp:
            pawn_x, pawn_y = inp[1:-1].split(",")
            pawn_x, pawn_y = pawn_x.strip(), pawn_y.strip()
            if pawn_x.isdigit() and pawn_y.isdigit():
                pawn_x = int(pawn_x)
                pawn_y = int(pawn_y)
                if pawn_x in valid_co and pawn_y in valid_co and board[pawn_y][pawn_x] == -1:
                    invalid_inp = False
                else:
                    print("Invalid input.\n")
                    invalid_inp = True
                    continue
            else:
                print("Invalid input.\n")
                invalid_inp = True
                continue
        else:
            print("Invalid input.\n")
            invalid_inp = True
            continue

    invalid_inp = True
    while (invalid_inp):
        inp = input("Enter coordinates of the postion to which you wish to move the pawn in the format (x,y):")
        invalid_inp = ("," not in inp) and inp.endswith(")") and inp.startswith("(")
        if not invalid_inp:
            place_x, place_y = inp[1:-1].split(",")
            place_x, place_y = place_x.strip(), place_y.strip()
            if place_x.isdigit() and place_y.isdigit():
                place_x = int(place_x)
                place_y = int(place_y)
                if place_x in valid_co and place_y in valid_co:
                    invalid_inp = False
                else:
                    print("Invalid input.\n")
                    invalid_inp = True
                    continue
            else:
                print("Invalid input.\n")
                invalid_inp = True
                continue
        else:
            print("Invalid input.\n")
            invalid_inp = True
            continue
    
    return [pawn_x,pawn_y,place_x,place_y]

#############################################################################
#                          Main method
############################################################################

if __name__ == '__main__':
    displayboard(board)
    while True:
        print("Your move:")
        pawn_x, pawn_y, place_x, place_y = userInput()
        if [place_x, place_y] in valid(pawn_x, pawn_y):
            updateboard(pawn_x, pawn_y, place_x, place_y)
            displayboard(board)
            winner=gameover(board,1)
            if winner == -1 :
                print("Human wins")
                break
            elif winner == 1:
                print("Computer wins")
                break


            compmove()
            print("\nComputer Move:")
            displayboard(board)
            winner=gameover(board,-1)
            if winner == -1 :
                print("Human wins")
                break
            elif winner == 1:
                print("Computer wins")
                break


        else:
            print("Invalid Input\n")

<<<<<<< HEAD
=======


>>>>>>> 6965fd0d14b3f2917e5e1394aee6e1f3255aed4a
