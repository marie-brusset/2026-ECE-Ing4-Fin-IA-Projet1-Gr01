def llm_decision(candidats):
    if not candidats:
        return "Aucune solution possible.", None

    def score(mot):
        return len(set(mot))

    meilleur = max(candidats, key=score)

    explication = (
        f"Il reste {len(candidats)} solutions possibles. "
        f"Le mot '{meilleur}' est proposé car il maximise la diversité des lettres."
    )

    return explication, meilleur
