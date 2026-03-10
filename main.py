import random


# Randomā ģenerēti skaitļi 
randomnumbers = int(input("Ievieto virknes garumu 15-25: "))
numlist = [random.choice([0, 1]) for _ in range(randomnumbers)]

current_player = "Cilvēks"

# Spēlētāju punkti
scores = {"Cilvēks": 0, "Dators": 0}


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
    other_player = "Dators" if current_player == "Cilvēks" else "Cilvēks"
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
        return "Dators" if current_player == "Cilvēks" else "Cilvēks"


# Alpha-Beta algoritma sākums


def alpha_beta(v, s, gajejs, alpha, beta, dzilums):
    #šī funkcija ir datora spēja skatīties nākotnē v - virkne, s - punkti, dzilums - cik gājienus uz priekšu dators redz
    if len(v) == 1 or dzilums == 0:#ja virknē palicis tikai 1 skaitlis vai arī ir sasniegts dziļuma limits, tiek noskaidrots, kurš pašlaik uzvar
        return s["Cilvēks"] - s["Dators"]#dators cenšas panākt, lai starpība būtu viņam izdevīga

    if gajejs == "Cilvēks":
        best_val = float('-inf') #tiek izvēlēts mīnus bezgalība, lai jebkurš pirmais gājiens ko dators atradīs, uzreiz būtu labāks par to
        for i in range(len(v) - 1):
            #iztēlojamies gājienu
            nv, ns = apply_move_players_immutable(v, i, "Cilvēks", s)#nv, ns ir gājiens, kurš tika izdarīts 'galvā'
            res = alpha_beta(nv, ns, "Dators", alpha, beta, dzilums - 1)#res apskata, kas notiks, ja tiks izdarīts noteiktais gājiens
            best_val = max(best_val, res) #patur labāko variantu
            
            #Alpha-Beta atzarošana
            #ja dators saprot, ka šis ceļš ir sliktāks par to, ko tas atrada iepriekš, tas nepārbauda pārējos variantus šajā zarā
            alpha = max(alpha, best_val)
            if beta <= alpha:
                break #Nogriež liekos gājienus
        return best_val
    else:
        #datora mērķis ir iegūt pēc iespējas mazāku starpības rezultātu, lai tas uzvarētu
        best_val = float('inf')
        for i in range(len(v) - 1):
            nv, ns = apply_move_players_immutable(v, i, "Dators", s)
            res = alpha_beta(nv, ns, "Cilvēks", alpha, beta, dzilums - 1)
            best_val = min(best_val, res)
            
            #atkal atzarošana, ja šis gājiens pretiniekam ir pārāk izdevīgs, dators to neizvēlēsies, jo tas paredz, ka cilvēks to izvēlēsies
            beta = min(beta, best_val)
            if beta <= alpha:
                break
        return best_val

def get_ai_move(v, s):
    #funkcija kura izsauc, lai dators pasaka savu gala lēmumu
    best_idx = 0
    best_v = float('inf') 
    for i in range(len(v) - 1):
        #dators izmēģina katru iespējamo gājienu
        nv, ns = apply_move_players_immutable(v, i, "Dators", s)
        #izsauc Alpha-Beta, lai redzētu, pie kā šis gājiens novedīs pēc 4 soļiem(dziļuma)
        val = alpha_beta(nv, ns, "Cilvēks", float('-inf'), float('inf'), 4)
        if val < best_v:
            best_v = val
            best_idx = i
    return best_idx


# Alpha-Beta algoritma beigas


#spēles gaita starp cilvēku un datoru
while not game_end(numlist):
    print(f"Virkne: {numlist}")
    print(f"Punkti: {scores}")
    
    if current_player == "Cilvēks":
        try:
            index = int(input(f"Tavs gājiens, izvēlies indeksu (0-{len(numlist)-2}): "))
            if index < 0 or index >= len(numlist) - 1:
                print("Nepareizs indekss!")
                continue
        except ValueError:
            print("Ievadi skaitli!")
            continue
    else:
        print("Dators domā...")
        index = get_ai_move(numlist, scores)
        print(f"Dators izvēlējās indeksu: {index}")

    apply_move_multiplayer(numlist, index, current_player, scores)

    current_player = change_player(current_player)
print("\nSPĒLE BEIDZĀS!")
print(f"Gala punkti: {scores}")
if scores["Cilvēks"] > scores["Dators"]:
    print("Uzvarēja Cilvēks!")
elif scores["Dators"] > scores["Cilvēks"]:
    print("Uzvarēja Dators!")
else:
    print("Neizšķirts!")
