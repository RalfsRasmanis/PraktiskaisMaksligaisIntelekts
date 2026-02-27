import random


# Randomā ģenerēti skaitļi 
randomnumbers = int(input("Enter the number of random numbers to generate: "))
numlist = [random.choice([0, 1]) for _ in range(randomnumbers)]

current_player = "Player1"

# Spēlētāju punkti
scores = {"Player1": 0, "Player2": 0}


def game_rules (x,y):
    if (x, y)== (0, 0):
        return 1, +1, 0 # new value - 1, current_player dabu 1 punktu, other_player 0
    elif (x, y) == (0, 1):
        return 0, 0, +1 # value 0, utt
    elif (x, y) == (1, 0):
        return 1, 0, -1  #other player -1pt
    elif (x, y) == (1, 1):
        return 0, -1, 0 #curent -1pt

def apply_move_multiplayer(numlist, index, current_player, scores):
    
    # Kurš spēlētājs pašlaik spēlē
    other_player = "Player2" if current_player == "Player1" else "Player1"
    # Pāru skaitļu pārbaude un punktu piešķiršana vai noņemšana
    x, y = numlist[index], numlist[index + 1]
    new_value, current_player_pts, other_player_pts = game_rules(x, y)
    scores[current_player] += current_player_pts
    scores[other_player] += other_player_pts

    # nomainīt numlist
    numlist[index] = new_value # Change the value of the first element in the pair
    del numlist[index + 1] # Remove the second element in the pair




def apply_move_players_immutable(numlist, index, current_player, scores): #Prieks minimax algoritma, lai saglabātu nemainīgumu
    
    new_list = numlist.copy() # Create a copy of the original list to maintain immutability
    new_scores = scores.copy() # Create a copy of the scores to maintain immutability

    # Kurš spēlētājs pašlaik spēlē
    other_player = change_player(current_player)
    # Pāru skaitļu pārbaude un punktu piešķiršana vai noņemšana
    x, y = numlist[index], numlist[index + 1]
    new_value, current_player_pts, other_player_pts = game_rules(x, y)
    new_scores[current_player] += current_player_pts
    new_scores[other_player] += other_player_pts
    
    # nomainīt numlist, ka immutable
    new_list[index] = new_value 
    del new_list[index + 1] 
    return new_list, new_scores

def game_end(numlist):
        return len(numlist) < 2
    
def change_player(current_player):
        return "Player2" if current_player == "Player1" else "Player1"

    # Pati spēles gaita
while not game_end(numlist):
    print("Current list:", numlist)
    print("Scores:", scores)
    
    try:
        index = int(input(f"{current_player}, enter index of pair to play: "))
        if index < 0 or index >= len(numlist) - 1:
            print("Invalid index, try again.")
            continue
    except ValueError:
        print("Please enter a valid integer index.")
        continue

    apply_move_multiplayer(numlist, index, current_player, scores)
    current_player = change_player(current_player)

print("Game over!")
print("Final scores:", scores)
print("Winner:", max(scores, key=scores.get))

