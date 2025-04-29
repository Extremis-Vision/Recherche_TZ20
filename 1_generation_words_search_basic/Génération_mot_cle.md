Voici la première partie du code du projet qui sert a testé les différentes manière de générer un output de données avec une structure il est décomposé en plusieurs dossier et fichier. Ceci n'est qu'une version basique de la génération de mots clées. pour obtenir de meilleur je pense que la solution suivante qui va être testé sera l'utilisation d'un modèle de thinking qui permetra de sortir plusieur mots logique en rapport avec la question/ demande de l'utilisateur et qui la divisera à ce moment la aucun nombre de mot ne sera donnée, mais ici le bus est de savoir la capacité de ces modèles à générer des mots clées en fonction d'un prompt donnée. 
Ce qui pourrait potentiellement pour un premier teste de recherche, mais aussi pour augmenté la variété de recherche dans le cas ou l'utilisateur n'est aps satisfait de la réponse. 

1) Architecture : 
Les dossiers continent un fichier python permetant de générer un fichier csv qui contient différente données (temps, score, réponse), ces données seront utilisé pour analyser les performances des llms et les comparés.
- benchmark_structured_output : utilise un système prompt qui lui demande de générer une réponse dans un format spécifique, ici json qui sera ensuite traité avec du python testé.
- benchmark_output_parser :  utilise une idée similaire au précédent, mais en utilisant des outils de pythone et de langchain qui permet de réduire le nombre de ligne de code et le rendre plus fiable pour traité les réponses des modèles qui peuvent être différente en fonction du modèle

Les fichiers à l'intérieur du dossier principale ont pour but de donnée un exemple de comment sont utilisé certaine librairie et les llms, il y a aussi un exemple avec de la génération simple.


Benchmark : 
Il se basera sur plusieur paramètre en premier pour vérifier la différence de réponse entre les prompts en français et anglais il y aura 20 qui auront été choisi pour être ambigu et difficile. 

Tous les modèles seront évalué sur ce cette de prompt et génèreront des réponse qui seront enregistrer ainsi que le temps de réponse, le temps de chargement et de génération de la première réponse. 

Un score est crée ce score représente le nombre d'output que le modèle à généré qui respecte la structure demandé. 

Une fois tous cela pris en compte, un benchmark plus avancé sera appliqué au résultat obtenue lors des précédents tests.

Benchmerk avancé : 
- nombre de mots clées et le nombre de catégorie vérification que ces deux soit le nombre demandé par l'utilisateur.

idée pour le benchmark vrac 



Pandas pour l'analyse statistique
Matplotlib/Seaborn pour la visualisation
NLTK/SpaCy pour l'analyse lexicale
Metrics sp�cialis�es (BLEU, ROUGE) pour la qualit� textuelle


IRaMuTeQ
NVivo
ALCESTE
MAXQDA
Qualtrics Text iQ
Lexalytics



BERTScore
ROUGE-N
Human Evaluation via Crowdsourcing


## Advanced Metrics for Semantic and Contextual Analysis
BERT-based Toxicity Detection
Topic Coherence Scores
Diversity Metrics

VADER Sentiment Analysis
BERTopic for Topic Modeling


F1-Score with Gold Standards


Implementation Recommendations
Step 1: Use BERTScore and ROUGE for baseline semantic and syntactic alignment.
Step 2: Deploy Perspective API to filter toxic/irrelevant outputs.
Step 3: Apply BERTopic for topic coherence and NLTK for diversity metrics.
Step 4: Validate with crowdsourced human ratings for final quality assurance.


semantic relevance comme f1 scores on du mal a capturer les nuances semantic 
il serarit mieux d'utiliser SoftKeyScore metric qui evalue les ressemblance partiel et les similarité sémantique ce qui donne un meilleur système pour générer un score en se basant sur les mots générer. 
A savoir que KPEval serait aussi intéresant. 

il est aussi important de considéré l'utilité du contexte 

DeepEval, LlamaIndex premete d'évaluer les output des llms en vérifiant résultat a quels points cela est correcte, mais aussi les similarité  sémantic et l'utilité de contexte, 
il y aurait aussi sentence transformer et bert ou pubmedbert qui permettrait de faire des evalutaion précise 

des méthode comme GEMBA (Generated Metric-Based Assesment) utilise une combinaison entre humain et modèle de language pour attribuer des scores et notés. 

Il est important de savoir que la génération de mots clées dans le contexte de recherche précise est une partie coplqiué de la recherche en effet il y a plein de chose différente a prendre en compte vue que c'est un système qui utilise a plusieur niveau des mdoèles pour trouver des similarité entre des thèmes et ensuite générer une réponse. 

Les métrics générer serontdonc difficilement capable de représenté les véritables performance, mais il est important de savoir que ses benchmark sont surtout pour comparer les technique d'appel de llm et dans un contexte général les modèle. 

Les systèmes de benchmark seront utile a plusieur niveau pour extimé les résultat obtenue à des recherches et autres. Donc nous les reveront plus tard. Les résultats de ces benchmarks seront comparé au résultat obetune par d'autre learderboard qui compare ces modèles avec des informations sur les différentes méthodes utilisé. 

Les sites intéressant sont : 
- https://lmarena.ai/
- https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard#/
- https://www.vellum.ai/llm-leaderboard