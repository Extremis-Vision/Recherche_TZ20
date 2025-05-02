# Projet de Génération de Mots Clés

## Introduction

Ce projet teste différentes méthodes de génération de mots clés avec une structure définie. Il est décomposé en plusieurs dossiers et fichiers. Cette version basique évalue la capacité des modèles à générer des mots clés en fonction d'un prompt donné.

## Architecture

Les dossiers contiennent des fichiers Python pour générer des fichiers CSV avec des données (temps, score, réponse) pour analyser et comparer les performances des LLMs.

- **benchmark_structured_output** : Utilise un système de prompt pour générer une réponse au format JSON, ensuite traitée avec Python.
- **benchmark_output_parser** : Utilise des outils Python et LangChain pour traiter les réponses des modèles de manière plus fiable.

Les fichiers du dossier principal montrent comment utiliser certaines bibliothèques et LLMs, avec des exemples de génération simple.

## Benchmark

Le benchmark évalue les réponses des modèles en français et en anglais avec 20 prompts ambigus et difficiles. Les métriques incluent le temps de réponse, de chargement, et de génération de la première réponse. Un score est créé pour évaluer la conformité des réponses à la structure demandée.

## Benchmark Avancé

- Vérification du nombre de mots clés et de catégories demandés par l'utilisateur.

## Idées pour le Benchmark

### Advanced Metrics for Semantic and Contextual Analysis

1. Utiliser BERTScore et ROUGE pour l'alignement sémantique et syntaxique.
2. Déployer Perspective API pour filtrer les outputs toxiques/irrelevants.
3. Appliquer BERTopic pour la cohérence des sujets et NLTK pour la diversité des métriques.
4. Valider avec des évaluations humaines crowdsourcées pour l'assurance qualité finale.

### Métriques Supplémentaires

- **SoftKeyScore** : Évalue les similarités partielles et sémantiques.
- **KPEval** : Intéressant pour l'évaluation des mots clés.
- **DeepEval, LlamaIndex** : Évaluent les outputs des LLMs pour la correction, la similarité sémantique et l'utilité contextuelle.
- **Sentence Transformer, BERT, PubMedBERT** : Pour des évaluations précises.
- **GEMBA** : Combine évaluations humaines et modèles de langage pour attribuer des scores.

## Outils de Benchmark

- **Pandas** : Analyse statistique.
- **Matplotlib/Seaborn** : Visualisation.
- **NLTK/SpaCy** : Analyse lexicale.
- **Metrics spécialisées** : BLEU, ROUGE pour la qualité textuelle.
- **IRaMuTeQ, NVivo, ALCESTE, MAXQDA, Qualtrics Text iQ, Lexalytics** : Analyse qualitative.
- **BERTScore, ROUGE-N** : Évaluation sémantique.
- **Human Evaluation via Crowdsourcing** : Évaluation humaine.

## Sites Intéressants

- [LM Arena](https://lmarena.ai/)
- [Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard#/)
- [Vellum AI LLM Leaderboard](https://www.vellum.ai/llm-leaderboard)
