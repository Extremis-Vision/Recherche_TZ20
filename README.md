# 🚀 Function Calling Project

## 🌟 Overview
The goal of this project is to evaluate the performance of models, specific techniques, and the quality of responses provided and adapt this technics to retrive knowledge from different sources ( Web, Document). The project is divided into several parts:

1. **[Keyword Generation for Search](1_generation_words_search_basic/1_generation_words_search_basic.md)**: Contained in the `1_generation_words_search_basic` folder. 🔍
2. **[Function Calling](2_function_calling/2_Function_calling.md)**: Details can be found in the `2_function_calling` folder. 📞
3. **[Analysis of Results](3_analyse_result/3_analyse_result.md)**: Analysis of parts 1 and 2, located in the `3_analyse_result` folder. 📊
4. **[Information Retrieval](4_Retrived_Information/4_Retrived_Information.md)**: Techniques such as RAG, KAG, CAG, etc., detailed in the `4_Retrived_Information` folder. 🔄
5. **[Internet Search](5_recherche_internet/5_recherche_internet.md)**: Contained in the `5_recherche_internet` folder. 🌍

## 🛠️ Supplementary

6. **[Agent](6_Agent/6_Agent.md)**: Additional information in the `6_Agent` folder. 🤖
7. **[Finetuning](7_Finetunning/7_Finetunning.md)**: Details can be found in the `7_Finetunning` folder. 🛠️



# Checklist des Tâches à Aborder

## Tâches Urgentes

Problème Base de Chunk et  chunl recupération 
1. **Modification du Système de Recherche**
   - Améliorer la recherche si la réponse ne convient pas.
   - Ajouter un bouton pour refaire la recherche avec DeepSearch ou ExtremeSearch.

2. **Bot Auto avec Deadlines et Autres**
   - Implémenter un bot automatique pour rajouter des données et informations automatiquement en fonction de ce qui est renvoyé.

3. **Description Appuyée sur le Noeud**
   - Afficher une description appuyée sur le nœud dans les résultats de recherche.

4. **Rajout Potentiel d'un Système de Retrieve avec GraphRAG**
   - Intégrer GraphRAG et ajouter des metadata (liens du site, catégorie et sujet principal) dans le RAG.

5. **Bouton Création dans le Graph**
   - Ajouter un bouton pour créer de nouvelles entités ou relations dans le graph.

6. **Zoomer et Zoom Auto**
   - Implémenter les fonctionnalités de zoom et zoom automatique, avec mode plein écran pendant l'ajout d'entités.

7. **Vérification LOAD RELATION**
   - Vérifier la relation de chargement (LOAD RELATION) pour s'assurer qu'elle fonctionne correctement.

8. **Simplification du Code React**
   - Rendre le code React plus simple et lisible.

## Tâches Importantes

9. **Choix du Type de Recherche et du Modèle par Défaut**
   - Permettre à l'utilisateur de choisir entre différents types de recherche et modèles, avec un modèle par défaut (Ministral).

10. **Modifications du Prompt de Génération des Mots Clés**
    - Adapter le prompt pour qu'il mette en avant les mots les plus importants.

11. **Tests avec Gemma 4b et Granite 8b**
    - Tester le système avec différents modèles comme Gemma 4b et Granite 8b.

12. **Bouton de Création de Graphique**
    - Ajouter un bouton pour créer des graphiques.
    - Permettre aux utilisateurs d'activer ou désactiver la création de graphiques par défaut, avec le choix du nombre de sites à crawler.

13. **Table Paramètre Relier à la BDD**
    - Créer une table paramètre relier à la base de données pour stocker les paramètres de recherche.

14. **Modification du Crawler et Autres**
    - Mettre à jour le crawler pour qu'il cherche de nouveaux mots ou outils chaque fois qu'ils sont découverts.

15. **Capacité de Recherche des Images**
    - Ajouter la capacité de rechercher des images dans les résultats.

16. **Citations des Sources Correctes**
    - Afficher les citations des sources correctement dans les résultats de recherche.

17. **Affichage des Sources Ajoutées pour une Requête de Recherche**
    - Afficher les sources ajoutées pour chaque requête de recherche.

18. **Utilisation de Farfalle ou SearXNG**
    - Utiliser Farfalle pour reprendre le sys prompt ou implémenter la recherche avec SearXNG.

## Tâches Moins Urgentes mais Importantes

19. **Rendre le Code Plus Lisible et Ajouter des Commentaires**
    - Remettre en ordre le repo, ajouter des explications du code et citations correctes.






















Finir modification de relation pour qu'il fonctionne correctement (penser à modifier noeud aussi car id normal ne fonctionnera plus dans le futur avec neo4j)

- MODIFIER SYSTÈME DE RECHERCHE POUR L'AMÉLIORER SI LA RÉPONSE NE CONVIENT PAS IL RENVOIE ALORS UN BOUTON POUR REFAIRE LA RECHERCHE AVEC DEEPSEARCH OU EXTREME SEARCH 
- BOT AUTO AVEC DES DEADLINE ET AUTRE POUR AUTOMATIQUEMENT RAJOUTER DES DONNÉES ET DES INFORMATIONS EN FONCTION DE CE QUI EST RENVOYER 
- DESCIPTION APPUIS SUR LE NOEUD
- Rajout potentielle u système de retrive avec GraphRAG combiné et aussi metadata dans le RAG (rajouter le liens du site catégorie et sujet principale en méta data du chunk )
- Bouton création de dans le graph 
- Bouton zoom et zoom auto, laisse le mode plein écran lors des ajout et autres 
- Vérifier LOAD RELATION 
- RENDRE LE CODE REACT PLUS SIMPLE ET LISSIBLE 
- Choix du type de recherche et du modèle avec par défaut ministral 
- Modifications du prompt de génération des mots clées (pour qu'il mette les mots les plus important dans un pompt)
- Tester avec Gemma 4b, Granite 8b
- Rajout du bouton de création de graphique / Choix dans les paramètre par défaut activation ou pas (choix du nombre de site à crawler)
- rajout potentiellement d'une table paramètre relier à la bdd 
-Modification du crawler et autre pour qu'il cherche de nouveau mot et autre a chaque fois qu'il en découvre ou nom d'outils 
- Rajout de la capacité de recherche et autre des images 
- Citations des sources correctes 
- Affichage des sources ajouté pour une requ^ete de recherche
- Choix du type préférer de recherche 
- Utilisation de Farfalle pour reprendre sys prompt ou implémentation de la recherche surtout avec SearXNG
- Remise en ordre du repo explication du code et autre ainsi que citation correcte. 

Idée rajout possible : 
- mettre tous les noeuds comme fonds de la page d'acceille
- rajouté les types / catégorie à un noeuds / rajouter la possibilité de mettre du json et l'interpréter par la lecture
