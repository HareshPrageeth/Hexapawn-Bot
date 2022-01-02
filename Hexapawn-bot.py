import random
###############################################################################

def returnnestedtuple(board1):
    board1=board1.copy()
    for x in range(3):
        board1[x]=tuple(board1[x])
    board1=tuple(board1)
    return board1

###############################################################################


#Global variables for each game

board = [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]
branch={}

#Global variable for the enitre program
finaldict={returnnestedtuple(board):{}}


###############################################################################

#Removes the moves which led to the loss
#It removes all the moves up to the point in the game where there was a choice
def removebadmove(thisgame2):
    global board,branch,finaldict
    for end_ind in range(len(thisgame2)):
        end_ind=end_ind*-1
        innerdict=finaldict
        for i in thisgame2[:end_ind]:
            innerdict=innerdict[i]
        if len(innerdict)>1:
            innerdict2=finaldict
            end_ind=end_ind-1
            for i in thisgame2[:end_ind]:
                innerdict2=innerdict2[i]
            bad=innerdict2[thisgame2[end_ind]].pop(thisgame2[end_ind+1])
            break
        elif len(innerdict[thisgame2[end_ind]])==0:
            innerdict.clear()

###############################################################################

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
        return False
    else:
        return True

###############################################################################

#Method to generate all possible moves and update it in the tree
#this is function is called only if the moves are not already there
def genmoves():
    global branch,finaldict
    li = []
    allmoves = []
    for row in range(3):
        for column in range(3):
            if board[column][row] == 1:
                li.append([row,column])
    for pawn in li:
        for place in valid(pawn[0],pawn[1]):
            allmoves.append([pawn, place])
    
    newboards=[]
    for el in allmoves:
        pawn_x=el[0][0]
        pawn_y=el[0][1]
        place_x=el[1][0]
        place_y=el[1][1]
        newboards.append(returnnestedtuple(returnupdatedboard(board,pawn_x,pawn_y,place_x,place_y)))
    branch.update(dict.fromkeys(newboards))
    for key in branch:
      branch[key]={}.copy()

###############################################################################

#Computer's move, makes a random move from all of the computer's possible moves
#Call function when it's computer's turn
def compmove():
    global board,branch,finaldict
    if len(branch)==0:
        genmoves()
    move = list(random.choice(list(branch.keys())))
    branch=branch[returnnestedtuple(move)]
    for x in range(3):
        move[x]=list(move[x])
    board=list(move)

###############################################################################

#Input coordinate of pawn and obtain possible places to move to
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

###############################################################################

#Returns updated the board taking original board and coordinates as arguments
def returnupdatedboard(board2,pawn_x, pawn_y, place_x, place_y):
    board2=board2.copy()
    for x in range(3):
        board2[x]=board2[x].copy()
    board2[place_y][place_x] = board2[pawn_y][pawn_x]
    board2[pawn_y][pawn_x]=0
    return board2

###############################################################################

#Returns 1 if the human won, -1 if the computer won and 0 if the game is still running
def gameover(turn):
    
    #Checking if the human pawns are not there
    if -1 not in board[0] and -1 not in board[1] and -1 not in board[2]:
        return 1

    #Checking if the comp pawns are not there
    elif 1 not in board[0] and 1 not in board[1] and 1 not in board[2]:
        return -1

    #Checking if a human pawn reached the end
    elif -1 in board[0]:
        return -1

    #Checking if a computer pawn reached the end
    elif 1 in board[2]:
        return 1

    #Checking if the computer has no valid move to play
    elif not anymove(1) and turn == 1:
        return -1

    #Checking if the human has no valid move to play
    elif not anymove(-1) and turn == -1:
        return 1

    else:
        return 0

###############################################################################

def displayboard():
    print(" {:^9} {:^9} {:^9} ".format("0","1","2"))
    print(" _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ ")
    for i in range(3):
        print("|         |         |         |")
        for j in range(3):
          if board[i][j]==-1:
            print("|   (*)   ",end='')
          elif board[i][j]==1:
            print("|   <\">   ",end='')
          else:
            print("|         ",end='')
        print("|")
        for j in range(3):
          if board[i][j]==-1:
            print("|   |:|   ",end='')
          elif board[i][j]==1:
            print("|   /V\\   ",end='')
          else:
            print("|         ",end='')
        print("| ",i)
        for j in range(3):
          if board[i][j]==-1:
            print("|   ===   ",end='')
          elif board[i][j]==1:
            print("|   ---   ",end='')
          else:
            print("|         ",end='')
        print("|")
        print("|_ _ _ _ _|_ _ _ _ _|_ _ _ _ _|")
    print()
###############################################################################

def userInput():
    valid_co = [0,1,2]
    invalid_inp = True
    while (invalid_inp):
        inp = input("Enter coordinates of pawn to move in the format (x,y):")
        invalid_inp = not(("," in inp) and inp.endswith(")") and inp.startswith("("))
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
        invalid_inp = not(("," in inp) and inp.endswith(")") and inp.startswith("("))
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

#Mirrors the board, doesn't change the existing board 
def mirror(board): 
    tboard = list(board)
    for col in range(3): 
        tboard[col]=list(tboard[col])
        for row in range(3): 
            tboard[col][row] = board[col][abs(row - 2)]
    return returnnestedtuple(tboard)

#############################################################################

#Mirrors the game and simulates it
def mirrorsimulation(game):
    global board,branch,finaldict,thisgame
    for i in range(len(game)):
        game[i]=mirror(game[i])
    branch=finaldict[game[0]]
    thisgame=[game[0]]
    for i in range(1,len(game),2):
        mirroredboard=game[i]
        if mirroredboard in branch:
            branch=branch[mirroredboard]
        else:
            branch.update({mirroredboard:{}.copy()})
            branch=branch[mirroredboard]
        thisgame.append(mirroredboard)

        if i==len(game)-1:
            break
        if len(branch)==0:
            board=list(mirroredboard)
            for ind in range(3):
                board[ind]=list(board[ind])
            genmoves()
            
        i=i+1
        mirroredboard=game[i]
        branch=branch[mirroredboard]
        thisgame.append(mirroredboard)
    if len(thisgame)%1==0:
        board=list(mirroredboard)
        for ind in range(3):
            board[ind]=list(board[ind])
        winner=gameover(-1)
        if winner == -1 :
            removebadmove(thisgame)

#############################################################################
#                          Main method
#############################################################################

if __name__ == '__main__':
    global board,branch,finaldict
    ch='y'
    while ch not in "Nn": 
        if ch in "Yy":
            board = [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]
            branch=finaldict[returnnestedtuple(board)]
            thisgame=[returnnestedtuple(board)]
            displayboard()

            while True:
                print("Your move:")
                pawn_x, pawn_y, place_x, place_y = userInput()
                if [place_x, place_y] in valid(pawn_x, pawn_y):
                    board=returnupdatedboard(board,pawn_x, pawn_y, place_x, place_y)
                    displayboard()
                    if returnnestedtuple(board) in branch:
                        branch=branch[returnnestedtuple(board)]
                    else:
                        branch.update({returnnestedtuple(board):{}.copy()})
                        branch=branch[returnnestedtuple(board)]
                    thisgame.append(returnnestedtuple(board))
                    winner=gameover(1)
                    if winner == -1 :
                        print("Human wins")
                        removebadmove(thisgame)
                        mirrorsimulation(thisgame)
                        break
                    
                    compmove()
                    print("\nComputer Move:")
                    displayboard()
                    thisgame.append(returnnestedtuple(board))
                    winner=gameover(-1)
                    if winner == 1:
                        print("Computer wins")
                        mirrorsimulation(thisgame)
                        break

                else:
                    print("Invalid Input\n")

        else:
            print("Invalid choice.\n")
        print("Do you want to run the program agian?[Yes(Y/y) or No(N/n)]")
        ch=input("Enter choice:") 

###############################################################################