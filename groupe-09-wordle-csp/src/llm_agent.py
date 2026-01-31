import ollama
import json
from csp_solver import solve_wordle_csp

# ----------------------------
# Chargement du dictionnaire
# ----------------------------
def load_dictionary(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip().upper() for line in f if len(line.strip()) == 5]
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

DICTIONARY = load_dictionary("wordle.txt")

# ----------------------------
# Interface CSP locale
# ----------------------------
def solveur_csp_local(lettres_vertes="", lettres_jaunes="", lettres_grises=""):
    """
    lettres_vertes  : "P0,R3"
    lettres_jaunes  : "O1,E4"
    lettres_grises  : "L2,A3,K4"
    """

    constraints = []

    if lettres_vertes:
        for item in lettres_vertes.split(","):
            item = item.strip()
            if len(item) >= 2:
                letter = item[0].upper()
                pos = int(item[1])
                constraints.append((letter, pos, "green"))

    if lettres_jaunes:
        for item in lettres_jaunes.split(","):
            item = item.strip()
            if len(item) >= 2:
                letter = item[0].upper()
                pos = int(item[1])
                constraints.append((letter, pos, "yellow"))

    if lettres_grises:
        for item in lettres_grises.split(","):
            item = item.strip()
            if len(item) >= 2:
                letter = item[0].upper()
                pos = int(item[1])
                constraints.append((letter, pos, "gray"))

    return solve_wordle_csp(DICTIONARY, constraints)

# ----------------------------
# Agent Wordle complet
# ----------------------------
def interroger_agent_wordle(prompt_utilisateur):

    # Extraction des contraintes Wordle
    response = ollama.chat(
        model="llama3.1",
        messages=[
            {
                "role": "user",
                "content": (
                    "You are a Wordle assistant.\n"
                    "Extract the Wordle feedback and call the function.\n"
                    "Return ONLY a function call.\n\n"
                    f"{prompt_utilisateur}"
                ),
            }
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "solveur_csp_local",
                    "description": "Filters Wordle words using feedback constraints",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lettres_vertes": {
                                "type": "string",
                                "description": "Green letters with position, e.g. P0,R3",
                            },
                            "lettres_jaunes": {
                                "type": "string",
                                "description": "Yellow letters with position, e.g. O1,E4",
                            },
                            "lettres_grises": {
                                "type": "string",
                                "description": "Gray letters with position, e.g. L2,A3,K4",
                            },
                        },
                        "required": [],
                    },
                },
            }
        ],
    )

    if not response["message"].get("tool_calls"):
        return response["message"]["content"]

    tool_call = response["message"]["tool_calls"][0]
    args = tool_call["function"]["arguments"]

    if isinstance(args, str):
        args = json.loads(args)

    # CSP strict
    mots_possibles = solveur_csp_local(**args)

    if not mots_possibles:
        return "Aucun mot Wordle valide ne respecte les contraintes données."

    # Prompt ranking amélioré
    prompt_final = f"""
You are an expert Wordle solver.

You are given a list of valid 5-letter ENGLISH words.
You MUST choose words ONLY from this list.
It is strictly forbidden to invent or modify any word.

Selection criteria:
1. Common usage in English
2. High letter frequency
3. Prefer words with 5 unique letters
4. Avoid rare or obscure words

List of possible words:
{mots_possibles}

Instructions:
- Rank the words from most promising to least promising.
- If there are 3 or more words, return the TOP 3.
- If there are fewer than 3 words, return all of them.
- The first word in the ranking is the chosen word.

Answer STRICTLY using this format:

Mot choisi: <WORD>
Raison: <maximum 2 sentences>

Ranking:
1. <WORD>
2. <WORD>
3. <WORD>
"""

    final_response = ollama.chat(
        model="llama3.1",
        messages=[{"role": "user", "content": prompt_final}],
    )

    content = final_response["message"]["content"]

    # ----------------------------
    # Validation stricte
    # ----------------------------

    chosen_word = None
    ranking_words = []

    for line in content.splitlines():
        line = line.strip()

        if line.lower().startswith("chosen word"):
            chosen_word = line.split(":")[1].strip().upper()

        if line and line[0].isdigit() and "." in line:
            word = line.split(".", 1)[1].strip().upper()
            ranking_words.append(word)

    # Vérification chosen
    if chosen_word not in mots_possibles:
        return "Le LLM a proposé un mot choisi invalide."

    # Vérification ranking
    for w in ranking_words:
        if w not in mots_possibles:
            return "Le LLM a proposé un ranking invalide."

    return (
        f"\nMOTS POSSIBLES ({len(mots_possibles)}):\n"
        f"{', '.join(mots_possibles[:30])}"
        + ("..." if len(mots_possibles) > 30 else "")
        + "\n\nDECISION DE L'IA:\n"
        + content
    )
