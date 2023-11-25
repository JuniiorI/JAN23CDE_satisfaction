# JAN23CDE_satisfaction
Pour notre projet, nous avons opté de le délimiter en prenant 6 entreprises évoluant dans le secteur de la banque.

Notre problématique sera de savoir l'avis général des consommateurs des clients sur les entreprises Orange Bank, Younited Credit, Boursorama Banque, Anytime, Cofidis, Floabank.

Le périmètre du projet: Les entreprises établies en France dans le domaine bancaire. 
Les entreprises sélectionnées ont minimum 5000 commentaires sur leur page sur trustpilot.

les technologies utilisées pour le scraping : la librairie BeautifulSoup avec python 3.9.7 sur Jupyter Notebook.
L'analyse des données se fera avec Elasticsearch-8.8.2 et kibana-8.7.1 pour traiter la bdd NoSQL.

objectifs: comprendre le ressenti des clients sur les entreprises sélectionnées.
les causes de mécontentement des clients et dégager des pistes de solution.

Et à l'aide d'un dashboard on va représenter les avis positifs comme négatifs les plus fréquents.


Notre dataframe principal est composé de 11 colonnes ("Company", "Customer", "Number_review", "Language", "Title", "Date_review", "Reply", "Date_reply", "Rating", "Status", "Experience", "Date_experience") et de 2414 lignes
Ce dernier sera nettoyé et analysé: on recherchera les valeurs manquantes, on les traitera convenablement et 
il faudra aussi les colonnes contenant des entier en int64, celles contenant les dates en datetime64.
Avec cette conversion des dates, il risque d'apparaitre de nouvelles valeurs manquantes dans les colonnes de date (NaT) il nous faudrait les transformer pour ne perdre beaucoup d'infos.
Nous ferons une analyse brève de la base de données.

Le 1er Notebook Satisfaction_client.ipynb a été transformé en différents scripts python qui parviendront à scraper rapidement sans retaper tout le code pour chaque compagnie.

Liste des questions business: 


- Quels sont les 5 mots clé negatifs et positifs les plus utilisés par les clients ?
- Statistiques sur le champ Rating ?
- Les entreprises  avec le plus de "No Reply" dans la colonne Reply ?
- Quelle est la note moyenne de chaque entreprise ?
- Donnez le groupe des commentateurs selon le "status".
- Temps moyen de reponse de chaque entreprise sur les messages répondus


Choix de BDD en rapport avec la problématique:
Meme si MongoDB est plus populaire, polyvalent et peut etre utilisé dans plusieurs cas d'utilisation(app web, app mobile, gestion de contenus etc).
Nous avons opté pour Elasticsearch car on veut utiliser la recherche, l'exploration et l'analyse de texte intégral.
Pour notre projet, ELasticsearch reste le meilleur choix.
 
- Justification du mapping de données --> par rapport aux types de requêtes associées aux questions business.
Le mapping est essentiel pour permettre à elasticsearch de connaitre et spécifier le format de nos données.
Pour nos données, le mapping a été fait de telle sorte que les datetimes ont été converties convenablement sur elasticsearch.

le type keyword: utilisé pour le stockage de chaines de caractères brutes qui ne nécessitent de d'analyse textuelle.
comme Customer, Company, document_id ...

le type text est utilisé pour les champs qui necessitent une analyse textuelle. les données textuelles sont analysées (tokenisées) en mots individuels lors de l'indexation.
le texte est divisé en mots et chaque mot est traité indépendamment

- L'organisation des données au sein de l'index "reviews" a été pensée en fonction de nos besoins métier. Les champs tels que "Company", "Customer", "Date_experience", "Date_reply", "Date_review", "Language", "Number_review", "Rating", "Reply", "Status", "Title", "Experience" ont été inclus pour capturer toutes les informations pertinentes des avis clients. En structurant les données de cette manière, nous facilitons l'exécution de requêtes spécifiques et l'analyse des sentiments des clients. Les conversions appropriées des types de données, telles que les dates en "datetime64" et les entiers en "int64", sont effectuées pour garantir une manipulation efficace des données.

Explication des Statuts:
- Verified: Avis vérifiés Les entreprises peuvent utiliser l'une des méthodes d'invitation automatique de Trustpilot pour automatiser l'envoi d'un e-mail d'invitation à laisser un avis à la suite d'un achat ou d'une expérience de service.

- Invited: Vous avez peut-être reçu un e-mail de la part d'une entreprise vous demandant de laisser un avis sur Trustpilot. Toutes les entreprises, indépendamment de si elles utilisent nos services gratuits ou payants, peuvent envoyer des invitations à laisser un avis à leurs clients.

- Redirected: Certaines entreprises partagent un lien sur leur site web qui dirige les utilisateurs vers leur page de profil sur Trustpilot. Si vous cliquez sur ce lien et écrivez un avis, il sera automatiquement accompagné du statut « Redirigé » sur Trustpilot.

- Merged: Quand le profil d'une entreprise ou un avis est accompagné du statut « Fusionné » sur Trustpilot, cela indique que l'entreprise avait plusieurs profils sur Trustpilot avant de les fusionner en un profil unique.

1 seul index + mapping associé
tests unitaires 
bdd remplies ? 
compléter le readme ?
