# DatathonPolyfinances
## Rose Lizé, Zoé Paradis, Lyna Kettani, Maxence Lhuisset
Ce github présente le projet du Datathon de Polyfinance 2023 de notre équipe. L'objectif étant d'optimiser un portefeuille sur le S&P500 sur la période de 2000 à 2015
## Méthodologie
### Clean DataSet
Nous avons commencé par lire les donnée récupéré depuis les CSV du sujet puis par néttoyer nos DataFrame dans filter.py. Nous avons pris uniquements les valeurs intéréssantes dans notre cas puis avons normalisé les valeurs si cela est pertinant
### Calcul des métriques
Nous calculons différentes métriques intéréssants graces à nos données pour un stock donnée à une date donné. Toutes les fonctions sont dans le filter.Elles sont toutes appelé par la fonction getTreeX() qui formate nos résultats pour la suite du processus
Nous avons fait :
- ***AtrStock*** : L'ATR (Average True Rage) est un indicateur financier sur la volatilité moyenne de notre stock sur les X derniers jours
- ***longTermReturn*** : Correspond au taux de rendement qu'on aurait eu à notre date si on avait investi sur notre stock il y a X jours
- ***gapValue*** : C'est l'ecart type du prix de l'action sur les X derniers jours
- ***AverageVolume*** : Donne la moyenne du nombre transactions journalières sur l'action sur les X derniers jours
- ***positiveReturn*** : C'est le taux de rendement journaliers qui sont positifs sur les X derniers jours
- ***returnAverage*** : C'est la moyenne des rendements journaliers sur les X derniers jours
- ***lowestClose*** : C'est la valeur la plus basse qu'a pris notre action à sa fermeture lors des X derniers jours
- ***highestClose*** : C'est la valeur la plus haute qu'a pris notre action à sa fermeture lors des X derniers jours

### Prédiction des rendements futurs

Notre solution est basé sur une prédiction des rendements et des risques à long terme pour nos stock. 
Le Fonctionement général consiste à prédire à un jour J la valeur du rendement obtenue au jour J2 (J2 = J +x) à partir des métriques calculé sur j.
Pour cela on utilise une **RandomForest** que l'on entraine en lui donnant des listes (x1, x2, ..., x8), liste des métrique à un jour J dans le passé et en lui donnant la valeur du rendement au jour J2 que l'on connait puisqu'on entraine notre algorithme sur des données du marché dans le passé.
#### Optimisation des prédictions
Pour s'assurer que nos prédictions soient les plus précises, nous avons dans un premier temps choisi un découpage de nos ensembles d'entrainement optimal. 
Ensuite nous allons faire une **RandomForest** par secteur d'activité (Santé, Finance...). 
Ainsi nous avons plus de données que si l'on prenait seulements les anciennent valeurs de notre action uniquement et nous gardons une certaine cohérence des données puisque les actions de même secteurs ont de nombreux points commun dans leur évolutions.

#### Retour des prédictions

L'algorithme de prédiction est fait pour recevoir une date et retourner un dataset du type :

| **Stock** | **Secteur** | **Rendement** |
|-----------|-------------|---------------|
|  ADP      | Finance     | 2             |
| PFI       | Santé       | 1.5           |
| MMM       | Industriel  | -2.4          |
| ...       | ...         | ...           |

Il crée un part un les arbre de chaques secteur, prédit la valeur de rendement pour J = dateDonnée pour chaque stock du secteur et enfin ajoute les données au dataFrame. le tout en prenant bien en compte de supprimer les valeurs NaN qui pourraient casser notre algorithme et représente de toute façon un stock à oublié tant qu'il est NaN.

### Optimisation du portefeuille
