# Documentation technique – Solveur Wordle CSP + LLM

## 1. Objectif du projet
Ce projet a pour objectif de résoudre le jeu **Wordle** en combinant :
- une approche algorithmique basée sur un **CSP (Constraint Satisfaction Problem)**,
- une approche assistée par un **LLM** (Large Language Model) exécuté localement via **Ollama**.

Le système ne simule pas le jeu Wordle lui-même, mais modélise le **raisonnement logique** du jeu afin de retrouver les mots compatibles avec les retours fournis par l’utilisateur.

---

## 2. Organisation générale du projet
Le projet est structuré de la manière suivante :

- `src/`
  - `main.py` : interface console pour utiliser le solveur
  - `app.py` : interface web développée avec Streamlit
  - `csp_solver.py` : implémentation du solveur Wordle par contraintes
  - `llm_agent.py` : agent combinant CSP et LLM
  - `wordle.txt` : dictionnaire de plus de 20 000 mots
- `docs/`
  - `DOCUMENTATION_TECHNIQUE.md` : documentation technique du projet

---

## 3. Représentation du problème (CSP)
Le problème Wordle est modélisé comme un problème de satisfaction de contraintes :

- Chaque mot est une chaîne de **5 lettres**
- Les retours du jeu sont codés sous forme :
  - `V` : lettre bien placée (vert)
  - `J` : lettre présente mais mal placée (jaune)
  - `G` : lettre absente (gris)

Chaque tentative ajoute une **nouvelle contrainte** sur le mot secret.

---

## 4. Solveur CSP (`csp_solver.py`)
Le solveur repose sur une implémentation fidèle des règles de Wordle, y compris la gestion des doublons.

### 4.1 Calcul du feedback
La fonction `wordle_feedback_vjg(secret, guess)` :
- compare un mot candidat (`secret`) avec une tentative (`guess`)
- retourne un feedback exact en `V / J / G`
- respecte les règles officielles de Wordle

### 4.2 Filtrage du dictionnaire
La fonction `solve_wordle_csp(possible_words, attempts)` :
- parcourt l’ensemble du dictionnaire
- conserve uniquement les mots compatibles avec **toutes** les tentatives précédentes
- retourne la liste des mots encore possibles

Cette approche est :
- déterministe
- explicable
- très rapide même avec un grand dictionnaire

---

## 5. Agent LLM (`llm_agent.py`)
L’agent combine le CSP avec un LLM exécuté localement via **Ollama**.

### 5.1 Entrées utilisateur
Deux types d’entrées sont acceptés :
- entrée structurée : `ORATE GVVJG` ou `ORATE -> GVVJG`
- texte libre (extrait via le LLM)

Une extraction automatique est réalisée si le format n’est pas directement reconnu.

### 5.2 Rôle du LLM
Le LLM n’est **pas utilisé pour résoudre les contraintes**.  
Son rôle est :
- d’extraire une tentative depuis un texte libre
- de classer les mots proposés par le CSP
- de suggérer des mots pertinents parmi les solutions valides

Le LLM ne peut choisir **que parmi les mots validés par le CSP**.

---

## 6. Limitation et contrôle du LLM
Pour éviter des appels trop coûteux ou inutiles :
- le nombre de candidats envoyés au LLM est limité
- si trop de solutions existent, seules les plus informatives sont conservées
- le CSP reste toujours la source de vérité

---

## 7. Interfaces utilisateur

### 7.1 Interface console (`main.py`)
- interaction en ligne de commande
- historique conservé pendant la session
- affichage des mots possibles et de la décision du LLM

### 7.2 Interface web (`app.py`)
Développée avec **Streamlit**, elle permet :
- une saisie structurée (mot + feedback)
- une saisie en texte libre
- l’affichage de l’historique des tentatives
- la visualisation des résultats en temps réel

---

## 8. Exécution du projet

### Prérequis
- Python 3.11
- Ollama installé localement
- modèle LLM disponible (ex. `llama3.1`)

### Lancement console
```bash
python main.py
