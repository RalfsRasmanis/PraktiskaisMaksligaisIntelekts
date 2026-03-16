import random
import csv
import os


class Stats:
    def __init__(self):
        self.generated_nodes = 0
        self.evaluated_nodes = 0

    def reset(self):
        self.generated_nodes = 0
        self.evaluated_nodes = 0


def save_game_stats_to_csv(filename, algorithm, winner, scores, stats, avg_move_time_ms):
    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        if not file_exists:
            writer.writerow([
                "algorithm",
                "winner",
                "human_score",
                "computer_score",
                "generated_nodes",
                "evaluated_nodes",
                "avg_move_time_ms"
            ])

        writer.writerow([
            algorithm,
            winner,
            scores["Cilvēks"],
            scores["Dators"],
            stats.generated_nodes,
            stats.evaluated_nodes,
            f"{avg_move_time_ms:.6f}"
        ])


# ===================
# IESTATĪJUMI
# ===================


# Statistika algoritmiem
minimax_stats = Stats()
alphabeta_stats = Stats()


# ===================
# PAMATLOĢIKA
# ===================

def generate_random_numbers(randomnumbers):
    return [random.choice([0, 1]) for _ in range(randomnumbers)]


def game_rules(x, y):
    if (x, y) == (0, 0):
        return 1, +1, 0
    elif (x, y) == (0, 1):
        return 0, 0, +1
    elif (x, y) == (1, 0):
        return 1, 0, -1
    elif (x, y) == (1, 1):
        return 0, -1, 0


def apply_move_multiplayer(numlist, index, current_player, scores):
    other_player = change_player(current_player)

    x, y = numlist[index], numlist[index + 1]
    new_value, current_player_pts, other_player_pts = game_rules(x, y)

    scores[current_player] += current_player_pts
    scores[other_player] += other_player_pts

    numlist[index] = new_value
    del numlist[index + 1]


def apply_move_players_immutable(numlist, index, current_player, scores):
    new_list = numlist.copy()
    new_scores = scores.copy()

    other_player = change_player(current_player)

    x, y = numlist[index], numlist[index + 1]
    new_value, current_player_pts, other_player_pts = game_rules(x, y)

    new_scores[current_player] += current_player_pts
    new_scores[other_player] += other_player_pts

    new_list[index] = new_value
    del new_list[index + 1]

    return new_list, new_scores


def game_end(numlist):
    return len(numlist) < 2


def change_player(current_player):
    return "Dators" if current_player == "Cilvēks" else "Cilvēks"


# ===================
# MINIMAX
# ===================

def apply_move(sequence, index, current_player, scores):
    score_dict = {"Cilvēks": scores[0], "Dators": scores[1]}
    player = "Cilvēks" if current_player == 0 else "Dators"

    new_seq, new_scores_dict = apply_move_players_immutable(sequence, index, player, score_dict)
    new_scores = [new_scores_dict["Cilvēks"], new_scores_dict["Dators"]]

    return new_seq, new_scores


def heuristic_minimax(sequence, scores):
    return scores[0] - scores[1]


def generate_children_minimax(sequence, scores, current_player):
    children = []
    for i in range(len(sequence) - 1):
        new_seq, new_scores = apply_move(sequence, i, current_player, scores)
        children.append((i, new_seq, new_scores))
    return children


def minimax(sequence, scores, current_player, stats, memo=None):
    if memo is None:
        memo = {}

    if len(sequence) == 1:
        stats.evaluated_nodes += 1
        return heuristic_minimax(sequence, scores)

    state = (tuple(sequence), tuple(scores), current_player)

    if state in memo:
        return memo[state]

    stats.evaluated_nodes += 1

    children = generate_children_minimax(sequence, scores, current_player)
    stats.generated_nodes += len(children)

    if current_player == 0:
        best = float("-inf")
        for i, new_seq, new_scores in children:
            val = minimax(new_seq, new_scores, 1, stats, memo)
            best = max(best, val)
    else:
        best = float("inf")
        for i, new_seq, new_scores in children:
            val = minimax(new_seq, new_scores, 0, stats, memo)
            best = min(best, val)

    memo[state] = best
    return best


def best_move(sequence, scores, current_player, stats):
    memo = {}
    best_val = float("-inf") if current_player == 0 else float("inf")
    best_idx = 0

    children = generate_children_minimax(sequence, scores, current_player)
    stats.generated_nodes += len(children)

    for i, new_seq, new_scores in children:
        val = minimax(new_seq, new_scores, 1 - current_player, stats, memo)

        if current_player == 0 and val > best_val:
            best_val = val
            best_idx = i
        elif current_player == 1 and val < best_val:
            best_val = val
            best_idx = i

    return best_idx, best_val


# ===================
# ALPHA-BETA
# ===================

def heuristic_alphabeta(s):
    return s["Cilvēks"] - s["Dators"]


def generate_children_alphabeta(v, s, gajejs):
    children = []
    for i in range(len(v) - 1):
        nv, ns = apply_move_players_immutable(v, i, gajejs, s)
        children.append((i, nv, ns))
    return children


def alpha_beta(v, s, gajejs, alpha, beta, dzilums, stats):
    if len(v) == 1 or dzilums == 0:
        stats.evaluated_nodes += 1
        return heuristic_alphabeta(s)

    children = generate_children_alphabeta(v, s, gajejs)
    stats.generated_nodes += len(children)

    if gajejs == "Cilvēks":
        best_val = float("-inf")
        for i, nv, ns in children:
            res = alpha_beta(nv, ns, "Dators", alpha, beta, dzilums - 1, stats)
            best_val = max(best_val, res)

            alpha = max(alpha, best_val)
            if beta <= alpha:
                break

        return best_val
    else:
        best_val = float("inf")
        for i, nv, ns in children:
            res = alpha_beta(nv, ns, "Cilvēks", alpha, beta, dzilums - 1, stats)
            best_val = min(best_val, res)

            beta = min(beta, best_val)
            if beta <= alpha:
                break

        return best_val


def get_ai_move(v, s, stats):
    best_idx = 0
    best_v = float("inf")

    children = generate_children_alphabeta(v, s, "Dators")
    stats.generated_nodes += len(children)

    for i, nv, ns in children:
        val = alpha_beta(nv, ns, "Cilvēks", float("-inf"), float("inf"), 4, stats)
        if val < best_v:
            best_v = val
            best_idx = i

    return best_idx