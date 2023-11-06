# DatathonPolyfinances
## Rose Lizé, Zoé Paradis, Lyna Kettani, Maxence Lhuisset
Ce github présente le projet du Datathon de Polyfinance 2023 de notre équipe. L'objectif étant d'optimiser un portefeuille sur le S&P500 sur la période de 2000 à 2015
## Méthodologie
### Clean DataSet
Nous avons commencé par lire les donnée récupéré depuis les CSV du sujet puis par néttoyer nos DataFrame dans filter.py. Nous avons pris uniquements les valeurs intéréssantes dans notre cas puis avons normalisé les valeurs si cela est pertinant
### Calculate indexs
Nous calculons différents index intéréssants graces à nos données pour un stock donnée à une date donné. 
Nous avons fait :
- ***AtrStock*** : L'ATR (Average True Rage) est un indicateur financier sur la volatilité moyenne de notre stock sur les X derniers jours
- ***longTermReturn*** : Cette valeur correspond au taux de rendement qu'on aurait eu à notre date si on avait investi sur notre stock il y a X jours
- ***
