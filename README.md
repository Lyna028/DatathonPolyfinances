# DatathonPolyfinances
## Rose Lizé, Zoé Paradis, Lyna Kettani, Maxence Lhuisset
Ce github présente le projet du Datathon de Polyfinance 2023 de notre équipe. L'objectif étant d'optimiser un portefeuille sur le S&P500 sur la période de 2000 à 2015
## Fonctionnement
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

L'algorithme de prédiction est fait pour recevoir une date et retourner un dataset normalisé du type :

| **Stock** | **Secteur** | **Rendement** |
|-----------|-------------|---------------|
|  ADP      | Finance     | 0.3           |
| PFI       | Santé       | 1.1           |
| MMM       | Industriel  | -0.5          |
| ...       | ...         | ...           |

Il crée un part un les arbre de chaques secteur, prédit la valeur de rendement pour J = dateDonnée pour chaque stock du secteur et enfin ajoute les données au dataFrame. le tout en prenant bien en compte de supprimer les valeurs NaN qui pourraient casser notre algorithme et représente de toute façon un stock à oublié tant qu'il est NaN.

### Optimisation du portefeuille

Maintenant que nous avons nos estimations de rendement nous devons les utiliser pour optimiser notre portefeuille sur le principe de long-only tout en gardant en tête les critères du portefeuille comme le minimum de 5% des pondération pour chaque secteur.

Pour ce faire nous avons le script Optimisation qui est notre script principal et qui appelle la fonction d'optimisation du portefeuille de façon répété tous les Y jours (ici 150 pour le long-only).
Le script modifie donc le csv de "submission" pour mettre les pondérations trouvé sur les 150 prochains jours (nous gardons nos pondération pour limiter le taux de renouvellement annuel). Les actions n'étant pas dans les 130 séléctionné ont leur poid à 0.
#### Fonction d'optimisation des pondérations
Cette fonction **optimizeWallet()** dans le [optimisation.py](optimisation.py) reçoit un jour et appel la fonction de prédiction. Il récupère ensuite les 130 meilleurs rendements prédis, les stocks correspondants et leurs secteurs. 
Il vérifie ensuite le pourcentage des rendements totaux pour chaques secteur.
Ayans des valeurs de prédictions très précises et en quantité nous avons fait une optimisation simple:
- *Poids de chaque secteur* : On prend une partie de la pondérations des secteurs les plus représenté dans les 130 meilleurs rendements pour les distribuer aux secteurs sous 5%.
- *Poids des stock dans leur secteur* : On calcul les taux par rapport au rendement total d'un secteur de tous ses stock
- *Poid global de chaque stock* : le poid total d'un stock dans le secteur multiplié par le poids du secteur donne le poids global d'un stock.

## Utilisation de la solution 
Cette solution génère le CSV de notre portefeuilles avec pondérations journalières du 2000-01-03(premier jour ouvert de 2000) au 2015-01-01. Ce CSV est généré (15 min environ) à l'éxécution de :
[optimisation.py](optimisation.py)
les fonctions et variables utilisé sont répartis dans :
- [filter.py](filter.py)
- [predict.py](predict.py)

Elles utilisent les données des *.csv dans [series](series)

