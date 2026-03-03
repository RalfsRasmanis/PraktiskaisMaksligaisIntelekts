import random
def gameStartValues():
    AIScore = 0
    playerScore = 0
    turn = False #player = false AI = tru
    randomAmount= int(input("Enter number between 15-25: "))
    forEnemy = False
  
    return AIScore,playerScore,turn,randomAmount,forEnemy

def createBoard(randomAmount):
    print(randomAmount)
    gameBoard = []
    for i in range(randomAmount):
        gameBoard += [str(random.randint(0,1))]
    return gameBoard

def pointsCase(pair):
    match pair:
        case ['0','0']:
            return 1, False, '1'
        case ['0','1']:
            return 1, True, '0' 
        case ['1','0']:
            return -1, True, '1'
        case ['1','1']:
            return -1, False, '0'  

def gameEnd(gameBoard):
    return len(gameBoard) <= 1

def showBoard(gameBoard):
    print(gameBoard)
    for i in range(len(gameBoard)-1):
        print ("Pair", i)
        print(gameBoard[i:i+2])

def pointGiver(AIScore,playerScore,turn,point,forEnemy):
    if  turn==True:
        if forEnemy == False:
            AIScore+=point
        else:
            playerScore+=point
            
    else:
        if forEnemy == False:
            playerScore+=point
        else:
            AIScore+=point
    
    return playerScore , AIScore

AIScore,playerScore,turn,randomAmount,forEnemy = gameStartValues()
gameBoard = createBoard(randomAmount)

while not gameEnd(gameBoard):

    showBoard(gameBoard)

    print("Player", playerScore)
    print("AI" , AIScore)
    
    if turn:
        print("AI turn")
        pairPosition = random.randint(0,len(gameBoard)-2)
    else:
        print("Player turn")

        pairPosition = -1

        while pairPosition < 0 or pairPosition >= len(gameBoard)-1:
            pairCheck = input("Enter your pair number: ").strip()
            if pairCheck.isdigit() == False:
                continue
            else:
                pairPosition = int(pairCheck)

    pair = gameBoard[pairPosition:pairPosition+2]
    del gameBoard[pairPosition:pairPosition+2]

    point, forEnemy ,insertValue = pointsCase(pair)
    gameBoard.insert(pairPosition,insertValue)

    playerScore, AIScore = pointGiver(AIScore,playerScore,turn,point,forEnemy)

    turn = not turn
    
if playerScore > AIScore:
    print("Player wins", playerScore)
else:
    print("AI wins", AIScore)