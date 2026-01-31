# Solveur de Wordle par CSP et LLM

## 1. Introduction

Wordle est un jeu de mots dans lequel un joueur doit deviner un mot secret.
À chaque tentative, le jeu fournit un feedback sous forme de couleurs :
- Vert (G) : lettre bien placée
- Jaune (Y) : lettre présente mais mal placée
- Gris (X) : lettre absente

Ce projet implémente un **solveur de Wordle** basé sur la
**Programmation par Contraintes (CSP)**, assisté par un **agent de type LLM**
pour la stratégie et l’explication des décisions.

L’objectif n’est pas d’implémenter le jeu Wordle lui-même,
mais un **assistant de raisonnement** capable de filtrer les mots possibles
à partir du feedback fourni par l’environnement.

---

## 2. Modélisation du problème (CSP)

Le mot secret est modélisé comme un problème de satisfaction de contraintes :

- Une **variable** par position du mot
- Un **domaine** correspondant aux lettres de l’alphabet
- Des **contraintes logiques** dérivées du feedback Wordle

### Traduction du feedback en contraintes :
- **Vert (G)** : la lettre doit être à cette position
- **Jaune (Y)** : la lettre est présente dans le mot mais pas à cette position
- **Gris (X)** : la lettre est absente du mot (sauf si déjà identifiée comme présente)

Un solveur CSP est utilisé pour réduire progressivement l’espace des solutions
en filtrant un dictionnaire de mots.

---

## 3. Architecture du système

Le projet est structuré en trois couches distinctes :

- **Solveur CSP (`wordle_csp.py`)**  
  Gère les variables, les domaines et les contraintes.
  Il garantit la cohérence logique des solutions.

- **Agent LLM (`llm_agent.py`)**  
  Analyse les solutions produites par le CSP,
  propose un mot à jouer et fournit une explication textuelle.

- **Interface interactive (`main.py`)**  
  Gère l’interaction avec l’utilisateur et orchestre les appels
  entre le CSP et l’agent LLM.

Cette séparation assure une architecture claire et extensible.

---

## Intégration d’une IA (LLM)

Le projet peut intégrer un agent basé sur un modèle de langage (LLM).
Cet agent n’effectue pas le raisonnement par contraintes.
Il exploite les résultats fournis par le solveur CSP afin de proposer un mot
et, éventuellement, fournir une explication du choix.

Cette intégration permet d’explorer une approche hybride combinant
raisonnement symbolique et aide à la décision par IA.


## 4. Intégration du LLM et Function Calling

Le LLM est utilisé comme une **couche décisionnelle et explicative**
au-dessus du solveur CSP.

Dans ce projet, le LLM est **simulé** par une fonction Python.
Il ne résout pas les contraintes lui-même, mais **appelle le solveur CSP**
pour obtenir les solutions valides, ce qui correspond conceptuellement
au mécanisme de **function calling**.

Dans une version avec un LLM réel (ex. API OpenAI),
le solveur CSP pourrait être exposé comme une fonction appelable
via le mécanisme de function calling JSON.

---

## 5. Stratégie de résolution

Lorsque plusieurs solutions sont possibles, une heuristique simple est utilisée :
le mot proposé est celui qui maximise la diversité des lettres,
afin de réduire l’espace de recherche plus efficacement.

Cette stratégie est appliquée par l’agent LLM.

---

## 6. Utilisation

1. Lancer le programme :
```bash
python main.py

---

## 7. Interface web avec Streamlit

Afin de faciliter la démonstration et l’interaction avec le solveur,
une **interface web interactive** a été développée à l’aide de **Streamlit**.

Cette interface permet :
- de saisir un mot proposé et son feedback (G / Y / X),
- de visualiser dynamiquement les mots encore possibles,
- d’afficher l’historique des tentatives,
- d’obtenir une proposition de mot accompagnée d’une explication de l’agent LLM,
- de relancer une nouvelle partie sans redémarrer l’application.

L’interface Streamlit agit uniquement comme une **couche de présentation** :
elle ne modifie pas la logique du solveur CSP ni celle de l’agent LLM.
Toute la logique de raisonnement reste centralisée dans les modules
`wordle_csp.py` et `llm_agent.py`.

### Lancement de l’interface Streamlit

L’interface web peut être lancée avec la commande suivante :

```bash
python -m streamlit run app_streamlit.py

## Documentation technique

La documentation technique du projet est disponible ici :
[DOCUMENTATION_TECHNIQUE.md](./DOCUMENTATION_TECHNIQUE.md)


