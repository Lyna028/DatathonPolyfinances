# DatathonPolyfinances
## Rose Lizé, Zoé Paradis, Lyna Kettani, Maxence Lhuisset
Ce github présente le projet du Datathon de Polyfinance 2023 de notre équipe. L'objectif étant d'optimiser un portefeuille sur le S&P500 sur la période de 2000 à 2015
## Méthodologie
### Clean DataSet
Nous avons commencé par lire les donnée récupéré depuis les CSV du sujet puis par néttoyer nos DataFrame dans filter.py. Nous avons pris uniquements les valeurs intéréssantes dans notre cas puis avons normalisé les valeurs si cela est pertinant
### Calcule des métriques
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
