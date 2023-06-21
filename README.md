# JAN23CDE_satisfaction

Notre problématique sera de savoir l'avis général des consommateurs surtout le niveau de mécontentement des clients sur l'entreprise Western Union.
Le périmètre du projet:
les technologies utilisées pour le scraping : la librairie BeautifulSoup avec python 3.10.5 sur Jupyter Notebook
Choix du secteur de la finance.
L'analyse des données se fera avec Elasticsearch pour traiter la bdd NoSQL.
objectifs: comprendre les causes de mécontentement des clients et dégager des pistes de solution.
Et à l'aide d'un dashboard on va représenter les avis positifs comme négatifs les plus fréquents.

Recherche d'un site fiable pour la récupération des avis clients
Trustpilot.com est un excellent site pour scraper les commentaires des clients
Pour notre projet, nous avons opté de le délimiter en prenant 6 entreprises évoluant dans le secteur de la finance.
La technologie utilisée est BeautifulSoup pour extraire efficacement les commentaires des clients que l"on stockera dans des dataframes que l'on concaténera dans un grand dataframe.
Il est composé de 11 colonnes ("Company", "Customer", "Number_review", "Language", "Title", "Date_review", "Reply", "Date_reply", "Rating", "Status", "Experience", "Date_experience") et de 2414 lignes
Ce dernier sera nettoyé et analysé: on recherchera les valeurs manquantes, on les traitera convenablement et 
il faudra aussi les colonnes contenant des entier en int64, celles contenant les dates en datetime64.
Avec cette conversion des dates, il risque d'apparaitre de nouvelles valeurs manquantes dans les colonnes de date (NaT) il nous faudrait les transformer pour ne perdre beaucoup d'infos.
Nous ferons une analyse brève de la base de données.

Le 1er Notebook a été transformé en une fonction "extract_reviews()" qui parviendra à scraper rapidement sans retaper tout le code pour chaque compagnie.



