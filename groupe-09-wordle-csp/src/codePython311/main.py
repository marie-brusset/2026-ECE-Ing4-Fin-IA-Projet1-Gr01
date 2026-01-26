from wordle_csp import WordleCSP
from llm_agent import llm_decision

def charger_dictionnaire(fichier):
    with open(fichier, "r") as f:
        return [l.strip() for l in f if l.strip()]

# Chargement du dictionnaire
dictionnaire = charger_dictionnaire("dictionary.txt")

print("🟩🟨⬜ Solveur Wordle par CSP + LLM")

premiere_partie = True

while True:  # 🔁 boucle des parties
    csp = WordleCSP(longueur=5)

    # ➜ N'afficher "Nouvelle partie" qu'après la première
    if not premiere_partie:
        print("\n🆕 Nouvelle partie")

    premiere_partie = False
    
    coups = 0
    historique =[]
    
    # 🔁 boucle des essais
    while True:
        essai = input("\nMot proposé : ").lower()
        feedback = input("Feedback (G/Y/X) : ").upper()
        
        coups += 1
        historique.append((essai, feedback))
        
        print(f"🔢 Coup numéro : {coups}")
        print("📜 Historique :", historique)
        

        csp.ajouter_contraintes(essai, feedback)
        candidats = csp.solutions(dictionnaire)

        print("Mots possibles :", candidats)
        print("Nombre de solutions :", len(candidats))

        explication, proposition = llm_decision(candidats)
        print("🤖 LLM :", explication)
        if proposition:
            print("🤖 Mot proposé par le LLM :", proposition)

        # 🎉 Mot trouvé
        if len(candidats) == 1:
            print("🎉 Mot trouvé :", candidats[0])
            break

        # ❌ Aucune solution
        if len(candidats) == 0:
            print("❌ Aucune solution possible")
            break

    # ❓ Question posée UNIQUEMENT après une partie terminée
    rejouer = input("\nVoulez-vous rejouer ? (o/n) : ").lower()
    if rejouer != "o":
        print("👋 Fin du jeu")
        break
