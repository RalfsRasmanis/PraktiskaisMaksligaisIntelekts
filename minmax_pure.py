#memo{} ir koplietojama vārdnīca starp visiem izsaukumiem
#Tā saglabā jau aprēķinātos stāvokļus, lai tos neaprēķinātu atkārtoti.
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

