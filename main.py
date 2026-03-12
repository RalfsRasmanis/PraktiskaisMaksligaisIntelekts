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
#===================
#MINMAX
#===================
def apply_move(sequence, index, current_player, scores):

    score_dict = {"Player1": scores[0], "Player2": scores[1]}

    player = "Player1" if current_player == 0 else "Player2"

    new_seq, new_scores_dict = apply_move_players_immutable(sequence, index, player, score_dict)

    new_scores = [new_scores_dict["Player1"], new_scores_dict["Player2"]]

    return new_seq, new_scores
def minimax(sequence, scores, current_player, memo={}):
    # ja virknē ir tikai viens skaitlis, spēle ir beigusies. Atgriež punktu starpību
    if len(sequence) == 1:
        return scores[0] - scores[1]
    #Izveido stāvokļa aprakstu
    state = (sequence, scores, current_player)
    #Ja šis stāvoklis jau ir aprēķināts, atgriež saglabāto vērtību 
    if state in memo:
        return memo[state]
    #Pārbauda, vai šobrīd spēlē Player 0.
    # Player 0 ir maksimizētājs 
    # viņš vēlas, lai punktu starpība (score[0] - score[1]) būtu pēc iespējas lielāka.
    if current_player == 0:
        #Iestata mainīgo best uz mīnus bezgalību kā sākuma vērtību. 
        # Tas garantē, ka jebkurš reāls gājiens būs labāks par sākuma vērtību 
        # Tādējādi pirmais atrasts gājiens automātiski kļūst par labāko, un katrs nākamais to var tikai uzlabot.
        best = float('-inf')
        #Iziet cauri visiem iespējamajiem gājienu indeksiem. 
        for i in range(len(sequence) - 1):
            #simulē gājienu pie konkrētā indeksa
            #Tiek iegūta jauna virkne un jauni punkti(nemainot oriģiālu)
            #apraksta, kā izskatītos spēle pēc šī gājiena.
            new_seq, new_scores = apply_move(sequence, i, current_player, scores)
            #Rekursīvi izsauc minimax no jaunā stāvokļa, nododot kārtu Player 1 
            #Šī izsaukuma rezultāts val ir labākais rezultāts, ko Player 1 var sasniegt no šī stāvokļa 
            val = minimax(new_seq, new_scores, 1, memo)
            #Salīdzina jauniegūto vērtību val ar līdzšinējo labāko best. 
            #Tā kā Player 0 ir maksimizētājs, saglabā lielāko no abām vērtībām
            #Pēc cikla beigām "best" glabās iespējamo labāko gala rezu;tātu, ko var sasniegt Player 0
            best = max(best, val)
   
    else:  #Player 1 ir minimizētājs — meklē gājienu, kas dod vismazāko punktu starpību. 
        # Sākuma vērtība tiek iestatīta uz pluss bezgalību
        # Tātad jebkurš izdarītais gājiens būs sliktāks par sākuma gājienu
        best = float('inf')
        for i in range(len(sequence) - 1):
            #Tiek iegūta jauna virkne un jauni punkti(nemainot oriģiālu)
            #apraksta, kā izskatītos spēle pēc šī gājiena.
            new_seq, new_scores = apply_move(sequence, i, current_player, scores)
            ##Rekursīvi izsauc minimax no jaunā stāvokļa, nododot kārtu Player 1 
            #Šī izsaukuma rezultāts val ir labākais rezultāts, ko Player 0 var sasniegt no šī stāvokļa 
            val = minimax(new_seq, new_scores, 0, memo)
            #Tiek iegūts sliktākais gājiens
            best = min(best, val)
    #Saglabā aprēķināto vērtību atmiņā un to atgriež
    memo[state] = best
    return best

#Definē funkciju, kas atrod labākā gājiena indeksu un vērtību
def best_move(sequence, scores, current_player):
    #Izveido tukšu atmiņu šim izsaukumam
    memo = {}
    #Iestata sākuma vērtības spēlētājiem
    best_val = float('-inf') if current_player == 0 else float('inf')
    #best_idx sākas ar 0.
    best_idx = 0
    #Pārbauda katru iespējamo gājienu, pielieto to, un izsauc minimax no pretinieka perspektīvas.
    for i in range(len(sequence) - 1):
        new_seq, new_scores = apply_move(sequence, i, current_player, scores)
        val = minimax(new_seq, new_scores, 1 - current_player, memo)
        #Atjaunina labāko indeksu, ja atrasta labāka vērtība. 
        # Player 0 meklē lielāku, Player 1 — mazāku.
        if current_player == 0 and val > best_val:
            best_val = val
            best_idx = i
        elif current_player == 1 and val < best_val:
            best_val = val
            best_idx = i
    #Atgriež labākā gājiena indeksu un tā vērtību.
    return best_idx, best_val

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


