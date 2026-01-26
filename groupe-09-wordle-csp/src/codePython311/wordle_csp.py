class WordleCSP:
    """
    Solveur Wordle par CSP (version rapide et robuste)

    - Les contraintes sont stockées explicitement
    - Le dictionnaire est filtré directement
    - Aucune utilisation interne dangereuse de python-constraint
    """

    def __init__(self, longueur=5):
        self.longueur = longueur
        self.contraintes = []   # liste de fonctions (mot -> bool)

    def ajouter_contraintes(self, mot, feedback):
        mot = mot.lower()
        feedback = feedback.upper()

        lettres_presentes = set(
            mot[i] for i in range(self.longueur)
            if feedback[i] in ("G", "Y")
        )

        for i in range(self.longueur):
            lettre = mot[i]

            # 🟩 Vert
            if feedback[i] == "G":
                self.contraintes.append(
                    lambda m, i=i, l=lettre: m[i] == l
                )

            # 🟨 Jaune
            elif feedback[i] == "Y":
                self.contraintes.append(
                    lambda m, i=i, l=lettre: l in m and m[i] != l
                )

            # ⬜ Gris
            elif feedback[i] == "X":
                if lettre not in lettres_presentes:
                    self.contraintes.append(
                        lambda m, l=lettre: l not in m
                    )

    def solutions(self, dictionnaire):
        solutions = []
        for mot in dictionnaire:
            if all(c(mot) for c in self.contraintes):
                solutions.append(mot)
        return solutions
