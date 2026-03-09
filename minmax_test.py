#Funkcija apply_move pieņem 4 parametrus
#sequence - pašreizējā skaitļu virkne
#index - vieta, kur tiek veikts gājiens
#current_player - spēlētājs, kurš veic gājienu
#score - punktu skaits
def apply_move(sequence, index, current_player, scores):
    #Izlasa 2 blakus esošus ciparus attiecīgajā pozīcijā
    a, b = sequence[index], sequence[index + 1]
    # Izveido mainīgo sarakstu kopiju no score, lai varētu mainīt punktus neiietekmējot oriģinālu
    new_scores = list(scores)
    #Aprēķina pretinieka numuru. Ja current_player=0, tad opponent=1, un otrādi.
    opponent = 1 - current_player
    #Speles noteikumu definīcija
    if a == 0 and b == 0:
        result = 1
        new_scores[current_player] += 1
    elif a == 0 and b == 1:
        result = 0
        new_scores[opponent] += 1
    elif a == 1 and b == 0:
        result = 1
        new_scores[opponent] -= 1
    else:
        result = 0
        new_scores[current_player] -= 1
    # izveido jaunu virkni:
    #viss pirms indeksa + jaunais rezultāta skaitlis + viss pēc otrā skaitļa.
    new_sequence = sequence[:index] + (result,) + sequence[index + 2:]
    #Atgriež jauno virkni un jaunos punktus
    return new_sequence, tuple(new_scores)

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


def human_move(sequence, scores):
    print("\nAvailable pairs:")
    for i in range(len(sequence) - 1):
        print(f"  Index {i}: ({sequence[i]}, {sequence[i+1]})")

    while True:
        try:
            idx = int(input(f"Your move — enter index (0 to {len(sequence) - 2}): "))
            if 0 <= idx <= len(sequence) - 2:
                return idx
            else:
                print(f"  Please enter a number between 0 and {len(sequence) - 2}.")
        except ValueError:
            print("  Invalid input. Please enter an integer.")


def play_game(initial_sequence):
    sequence = tuple(initial_sequence)
    scores = (0, 0)
    current_player = 1          # ← Computer goes first
    move_number = 1

    print("=" * 50)
    print("       WELCOME TO THE NUMBER SEQUENCE GAME")
    print("=" * 50)
    print(f"Initial sequence: {list(sequence)}")
    print(f"You are Player 0 (maximizer). Computer is Player 1 (minimizer).")
    print(f"Computer goes first!")
    print(f"Scores: Player 0 = {scores[0]}, Player 1 = {scores[1]}\n")

    while len(sequence) > 1:
        print(f"--- Move {move_number} | Sequence: {list(sequence)} | "
              f"Scores: P0={scores[0]}, P1={scores[1]} ---")

        if current_player == 0:
            idx = human_move(sequence, scores)
        else:
            idx, projected = best_move(sequence, scores, current_player)
            print(f"\nComputer's turn — analysing all pairs...")
            print(f"  Best pair found: ({sequence[idx]}, {sequence[idx+1]}) "
                  f"at index {idx} (projected score diff: {projected})")

        pair = (sequence[idx], sequence[idx + 1])
        sequence, scores = apply_move(sequence, idx, current_player, scores)

        print(f"  {'You' if current_player == 0 else 'Computer'} "
              f"replaced pair {pair} at index {idx} → "
              f"new sequence: {list(sequence)}, "
              f"Scores: P0={scores[0]}, P1={scores[1]}")

        current_player = 1 - current_player
        move_number += 1

    print("\n" + "=" * 50)
    print(f"Final sequence: {list(sequence)}")
    print(f"Final scores: Player 0 = {scores[0]}, Player 1 = {scores[1]}")

    if scores[0] > scores[1]:
        print("You win! 🎉")
    elif scores[1] > scores[0]:
        print("Computer wins!")
    else:
        print("It's a draw!")
    print("=" * 50)


# --- Start the game ---
play_game([1, 0, 1])


