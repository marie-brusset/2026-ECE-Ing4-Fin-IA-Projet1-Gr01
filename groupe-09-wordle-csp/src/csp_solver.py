from collections import Counter, defaultdict

def solve_wordle_csp(possible_words, constraints):

    green = {}
    yellow_forbidden = defaultdict(set)
    min_count = defaultdict(int)
    gray_letters = set()

    # Analyse contraintes
    for letter, pos, fb in constraints:
        letter = letter.upper()

        if fb == "green":
            green[pos] = letter
            min_count[letter] += 1

        elif fb == "yellow":
            yellow_forbidden[pos].add(letter)
            min_count[letter] += 1

        elif fb == "gray":
            gray_letters.add(letter)

    solutions = []

    for word in possible_words:
        word = word.upper()
        counts = Counter(word)
        valid = True

        # verts
        for pos, letter in green.items():
            if word[pos] != letter:
                valid = False
                break

        if not valid:
            continue

        # jaunes (pas à cette position)
        for pos, letters in yellow_forbidden.items():
            if word[pos] in letters:
                valid = False
                break

        if not valid:
            continue

        # jaunes doivent exister
        for letter, required in min_count.items():
            if counts[letter] < required:
                valid = False
                break

        if not valid:
            continue

        # gris = absents globalement (sauf si min_count > 0)
        for letter in gray_letters:
            if letter not in min_count and counts[letter] > 0:
                valid = False
                break

        if valid:
            solutions.append(word)

    return solutions

