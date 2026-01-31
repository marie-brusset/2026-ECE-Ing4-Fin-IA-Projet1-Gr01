from collections import Counter, defaultdict

def solve_wordle_csp(possible_words, constraints):

    green = {}
    yellow_forbidden = defaultdict(set)
    gray_letters = defaultdict(set)
    min_count = defaultdict(int)

    for letter, pos, fb in constraints:
        letter = letter.upper()

        if fb == "green":
            green[pos] = letter
            min_count[letter] += 1

        elif fb == "yellow":
            yellow_forbidden[pos].add(letter)
            min_count[letter] += 1

        elif fb == "gray":
            gray_letters[letter].add(pos)

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

        # jaunes (interdits à la position)
        for pos, letters in yellow_forbidden.items():
            if word[pos] in letters:
                valid = False
                break

        if not valid:
            continue

        # jaunes doivent exister ailleurs
        for letter in min_count:
            if counts[letter] < min_count[letter]:
                valid = False
                break

        if not valid:
            continue

        # gris positionnels
        for letter, positions in gray_letters.items():
            for pos in positions:
                if word[pos] == letter:
                    valid = False
                    break

        if valid:
            solutions.append(word)

    return solutions
