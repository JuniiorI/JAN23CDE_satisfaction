# Etude de la satisfaction clients.
  
1. Aperçu:

Imaginez que vous êtes une entreprise cherchant à obtenir une vue d'ensemble de la satisfaction de vos clients. Ce projet a pour objectif de vous fournir une analyse approfondie des avis des consommateurs afin de répondre à plusieurs problématiques business cruciales :

    Nombre de commentaires non répondus par les entreprises.

    Le délai de réponse des commentaires des clients.

    Les tendances des mots clés les plus utilisés par les commentateurs.

    Note moyenne des avis clients.

2. Problématiques business:

- Commentaires non répondus
Le projet vise à déterminer le nombre de commentaires non répondus par les entreprises. Ceci offre un aperçu crucial de la communication avec les clients.

- Délai de réponse
L'analyse inclut le délai moyen de réponse des entreprises aux commentaires des clients, fournissant des informations sur la réactivité de chaque entreprise.

- Mots clés populaires
L'identification des tendances des mots clés les plus utilisés par les commentateurs permet de comprendre les préoccupations récurrentes des clients.

- Note moyenne
La note moyenne des avis clients est un indicateur clé de la satisfaction globale des clients. Cela peut aider à évaluer la perception générale de chaque entreprise.

3. Entreprises Sélectionnées

Pour ce projet, nous avons choisi de nous concentrer sur six entreprises du secteur bancaire :

    Orange Bank

    Younited Credit

    Boursorama Banque

    Anytime

    Cofidis

    Floabank  

Les données sont extraites du site Trustpilot.com, et le dataframe principal new_df est composé de 13 colonnes.

4. Détails Techniques

    Langage de programmation : Python 3.12.0
    Librairies utilisées : BeautifulSoup, Pandas, dateparser, Elasticsearch
    Environnement de scraping : Visual Studio Code

5. Objectifs du Projet

    Comprendre le ressenti des clients à l'égard des entreprises sélectionnées.
    Identifier les causes de mécontentement des clients et proposer des pistes de solution.


6. Technologies Utilisées
  
	Windows
	Visual Studio Code:
    Scraping : BeautifulSoup avec Python.
    Base de données : Elasticsearch-8.8.2.
    Visualisation : Kibana-8.7.1.

7. Dashboard

Un tableau de bord interactif sera créé à l'aide de Kibana, représentant les KPI essentiels pour une compréhension approfondie de la satisfaction des clients

8. Choix de BDD en rapport avec la problématique:

Meme si MongoDB est plus populaire, polyvalent et peut etre utilisé dans plusieurs cas d'utilisation(app web, app mobile, gestion de contenus etc).

Nous avons opté pour Elasticsearch car on veut utiliser la recherche, l'exploration et l'analyse de texte intégral.

Pour notre projet, ELasticsearch reste le meilleur choix.

- Justification du mapping de données --> par rapport aux types de requêtes associées aux questions business.

Le mapping est essentiel pour permettre à elasticsearch de connaitre et spécifier le format de nos données.

Pour nos données, le mapping a été fait de telle sorte que les dates ont été converties convenablement sur elasticsearch.

le type keyword: utilisé pour le stockage de chaines de caractères brutes qui ne nécessitent pas d'analyse textuelle.

comme Customer, Company, document_id.

le type text est utilisé pour les champs qui necessitent une analyse textuelle. les données textuelles sont analysées (tokenisées) en mots individuels lors de l'indexation.

le texte est divisé en mots et chaque mot est traité indépendamment

- L'organisation des données au sein de l'index "reviews" a été pensée en fonction de nos besoins métier. Les champs tels que "Company", "Customer", "Date_experience", "Date_reply", "Date_review", "Language", "Number_review", "Rating", "Reply", "Status", "Title", "Experience", "Date_Experience", "Response_time" ont été inclus pour capturer toutes les informations pertinentes des avis clients. En structurant les données de cette manière, nous facilitons l'exécution de requêtes spécifiques et l'analyse des sentiments des clients. Les conversions appropriées des types de données, telles que les dates en "datetime64" et les entiers en "int64", sont effectuées pour garantir une manipulation efficace des données.

  

9. Explication des Statuts:

- Verified: Avis vérifiés Les entreprises peuvent utiliser l'une des méthodes d'invitation automatique de Trustpilot pour automatiser l'envoi d'un e-mail d'invitation à laisser un avis à la suite d'un achat ou d'une expérience de service.

- Invited: Vous avez peut-être reçu un e-mail de la part d'une entreprise vous demandant de laisser un avis sur Trustpilot. Toutes les entreprises, indépendamment de si elles utilisent nos services gratuits ou payants, peuvent envoyer des invitations à laisser un avis à leurs clients.

- Redirected: Certaines entreprises partagent un lien sur leur site web qui dirige les utilisateurs vers leur page de profil sur Trustpilot. Si vous cliquez sur ce lien et écrivez un avis, il sera automatiquement accompagné du statut « Redirigé » sur Trustpilot.

- Merged: Quand le profil d'une entreprise ou un avis est accompagné du statut « Fusionné » sur Trustpilot, cela indique que l'entreprise avait plusieurs profils sur Trustpilot avant de les fusionner en un profil unique.

10. Structure du projet
JAN23CDE_satisfaction/
│
├── src/
│   ├── scraping_trustpilot.py
│   ├── bdd_trustpilot.py
│   ├── cronjobs/
│   │   └── scraping_cronjob.py
│   │   └── cronjob_scraping.yaml
│   ├── Dockerfile_scraping
│   ├── Dockerfile_elasticsearch
│   ├── Dockerfile_kibana
│   ├── requirements.txt
│   └── .github/
│       └── workflows/
│           └── tests.yml
│
├── data/
│   ├── raw/
│   └── processed/
│
├── report/
│   └── Readme.txt
│
├── notebook/
│
├── config/
│   ├── elasticsearch.yml
│   └── kibana.yml
│
├── Docker-compose.yml
│
└── .git/
    └── ... (configuration git)

12. Liens Utiles  

    Dépôt GitHub : https://github.com/JuniiorI/JAN23CDE_satisfaction/tree/YACI01-yaya

    Présentation du Projet: https://app.presentations.ai/#/docs/edit/3031234/

    [Tableau de Bord Kibana]: http://localhost:5601/app/dashboards#/view/a667cdf0-8b1c-11ee-a1fb-9304b3c5a830?_g=(refreshInterval:(pause:!t,value:60000),time:(from:now-15m,to:now))&_a=()

  

Ce projet vise à fournir des informations précieuses pour orienter les décisions commerciales et améliorer la satisfaction globale des clients.