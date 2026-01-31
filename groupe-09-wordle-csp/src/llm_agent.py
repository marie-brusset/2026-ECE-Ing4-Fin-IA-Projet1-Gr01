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
# Agent Wordle (LLM + CSP)
# ----------------------------
def interroger_agent_wordle(prompt_utilisateur):

    # LLM : extraction des contraintes Wordle
    response = ollama.chat(
        model="llama3.1",
        messages=[
            {
                "role": "user",
                "content": (
                    "You are a Wordle assistant.\n"
                    "From the following description, extract Wordle feedback.\n"
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

    # Sécurité : Ollama renvoie parfois une string JSON
    if isinstance(args, str):
        args = json.loads(args)

    # CSP strict Wordle
    mots_possibles = solveur_csp_local(**args)

    if not mots_possibles:
        return "Aucun mot Wordle valide ne respecte les contraintes données."

    # PROMPT STRICT POUR LE CHOIX DU MOT (ANGLAIS)
    prompt_final = f"""
You are an expert Wordle solver.

You are given a list of valid 5-letter ENGLISH words.
You MUST choose exactly ONE word from the list.
It is strictly forbidden to invent a word or alter spelling.

Selection criteria:
1. Common usage in English
2. High letter frequency
3. Prefer fewer repeated letters when possible

List of possible words:
{mots_possibles}

Answer strictly using this format:
Chosen word: <WORD>
Reason: <maximum 2 sentences>
"""

    final_response = ollama.chat(
        model="llama3.1",
        messages=[{"role": "user", "content": prompt_final}],
    )

    # Validation stricte du mot choisi
    content = final_response["message"]["content"]
    chosen_word = None

    for line in content.splitlines():
        if line.lower().startswith("chosen word"):
            chosen_word = line.split(":")[1].strip().upper()

    if chosen_word not in mots_possibles:
        return (
            "LLM proposed an invalid word.\n\n"
            f"LLM output:\n{content}"
        )

    return (
        f"MOTS POSSIBLES ({len(mots_possibles)}):\n"
        f"{', '.join(mots_possibles[:30])}"
        + ("..." if len(mots_possibles) > 30 else "")
        + "\n\nDECISION DE L'IA:\n"
        + content
    )
