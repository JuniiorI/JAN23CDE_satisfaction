from elasticsearch import Elasticsearch, helpers
import csv
import time

# Connexion au cluster Elasticsearch
es = Elasticsearch(hosts="http://localhost:9200")

# Nom de l'index
index_name = "reviews"

# Mapping pour l'index
mapping = {
    "mappings": {
        "_meta": {
            "created_by": "yaya"
        },
        "properties": {
            "Company": {"type": "keyword"},
            "Customer": {"type": "keyword"},
            "Date_experience": {"type": "date", "format": "yyyy-MM-dd"},
            "Date_reply": {"type": "date", "format": "yyyy-MM-dd"},
            "Date_review": {"type": "date", "format": "yyyy-MM-dd"},
            "Response_time":{"type": "long"},
            "Experience": {"type": "keyword"},
            "Language": {"type": "keyword"},
            "Number_review": {"type": "long"},
            "Rating": {"type": "long"},
            "Reply": {"type": "keyword"},
            "Status": {"type": "keyword"},
            "Title": {"type": "keyword"},
            "document_id": {"type": "keyword"}
        }
    }
}


def create_elasticsearch_index():
    es = Elasticsearch(hosts="http://localhost:9200")

    # Index des avis clients
    index_name = "reviews"
    # Créer l'index avec le mapping (you can skip this if the index already exists)
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=mapping)

    # Lecture du fichier CSV et correction des champs vides
    with open("../data/processed/reviews.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        documents = []
        for idx, row in enumerate(reader):
            if "" in row:
                row["document_id"] = str(idx)  # Ajout de l'ID du document
                for key in list(row.keys()):
                    if key == "":
                        row.pop(key)  # Suppression des champs avec des clés vides
            documents.append(row)

    # Insérer les documents en vrac dans Elasticsearch
    if documents:
        try:
            response = helpers.bulk(es, documents, index=index_name)
            print("Documents insérés avec succès :", response)
        except helpers.BulkIndexError as e:
            print("Erreur lors de l'insertion des documents :")
            for err in e.errors:
                print("Erreur :", err)

    # Vérification des documents insérés
    result = es.search(index=index_name, size=5)  # Récupère les 5 premiers documents

    # Afficher les résultats
    for hit in result["hits"]["hits"]:
        print(hit["_source"])

    # Insérer les documents en vrac dans Elasticsearch
    if documents:
        try:
            response = helpers.bulk(es, documents, index=index_name)
            print("Documents insérés avec succès :", response)
        except helpers.BulkIndexError as e:
            print("Erreur lors de l'insertion des documents :")
            for err in e.errors:
                print("Erreur :", err)

    # Vérification des documents insérés
    result = es.search(index=index_name, size=5)  # Récupère les 5 premiers documents

    # Afficher les résultats
    for hit in result["hits"]["hits"]:
        print(hit["_source"])

    response = es.search(index="reviews")
    # Récupération du template
    template = es.indices.get_mapping()

    # recherche de tous les documents
    es = Elasticsearch(hosts="http://localhost:9200")

    # Index des avis clients
    index_name = "reviews"
    
    query = {
        "query": {
            "match_all": {}
        }
    }

    # Exécuter la requête
    result = es.search(index="reviews", body=query)

    # Afficher les résultats
    for hit in result["hits"]["hits"]:
        print(hit["_source"])


    # Requête pour obtenir les 5 mots clés positifs
    es = Elasticsearch(hosts="http://localhost:9200")

    # Index des avis clients
    index_name = "reviews"
    query = {
        "query": {
            "match_all": {}
        },
        "aggs": {
            "positive_words": {
                "terms": {
                    "field": "Experience",
                    "size": 5,
                    "min_doc_count": 5
                },
                "aggs": {
                    "rating_filter": {
                        "filter": {
                            "range": {
                                "Rating": {
                                    "gte": 5,
                                    "lte": 5
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    # Exécution de la requête
    result = es.search(index=index_name, body = query)

    # Récupération des résultats
    positive_words = result["aggregations"]["positive_words"]["buckets"]

    for positive_word in positive_words:
        print(f"Mot clé positif : {positive_word['key']} - Nombre d'occurrences : {positive_word['doc_count']}")

    # Recherche des mots les plus récurrents dans les commentaires négatifs
    es = Elasticsearch(hosts="http://localhost:9200")

    # Index des avis clients
    index_name = "reviews"
    query = {
        "query": {
            "match_all": {}
        },
        "aggs": {
            "negative_words": {
                "terms": {
                    "field": "Title",
                    "size": 3,
                    "min_doc_count": 10
                },
                "aggs": {
                    "rating_filter": {
                        "filter": {
                            "range": {
                                "Rating": {
                                    "gte": 1,
                                    "lte": 1
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    # Exécution de la requête
    result = es.search(index=index_name, body=query)

    # Récupération des résultats
    negative_words = result["aggregations"]["negative_words"]["buckets"]

    # Affichage des résultats
    for negative_word in negative_words:
        print(f"Mot clé négatif : {negative_word['key']} - Nombre d'occurrences : {negative_word['doc_count']}")
    
    # Ordonner la sortie du plus petit au plus grand nombre d'occurrences
    negative_words_sorted = sorted(negative_words, key=lambda x: x["doc_count"])

    # Affichage des résultats ordonnés
    for negative_word in negative_words_sorted:
        print(f"Mot clé négatif : {negative_word['key']} - Nombre d'occurrences : {negative_word['doc_count']}")


    # Requête d'agrégation pour obtenir des statistiques sur le champ "Rating"
    es = Elasticsearch(hosts="http://localhost:9200")

    # Index des avis clients
    index_name = "reviews"
    query = {
        "size": 0,
        "aggs": {
            "value_count": {
                "value_count": {
                    "field": "Rating"
                }
            },
            "rating_stats": {
                "stats": {
                    "field": "Rating"
                }
            },
            "extended_ratings_stats": {
                "extended_stats": {
                    "field": "Rating"
                }
            }
        }
    }

    # Exécuter la requête
    result = es.search(index="reviews", body=query)

    # Afficher les résultats de l'agrégation
    aggregations = result.get("aggregations", {})
    value_count = aggregations.get("value_count", {})
    rating_stats = aggregations.get("rating_stats", {})
    extended_ratings_stats = aggregations.get("extended_ratings_stats", {})

    print("Nombre total de valeurs de rating:", value_count.get("value", 0))
    print("Statistiques de rating:")
    print("    Minimum:", rating_stats.get("min", 0))
    print("    Maximum:", rating_stats.get("max", 0))
    print("    Moyenne:", rating_stats.get("avg", 0))
    print("    Somme:", rating_stats.get("sum", 0))
    print("    Écart-type:", extended_ratings_stats.get("std_deviation", 0))
        
    # Liste des entreprises avec le plus de commentaires négatifs
    es = Elasticsearch(hosts="http://localhost:9200")

    # Index des avis clients
    index_name = "reviews"
    query = {
        "query": {
            "match_all": {}
        },
        "sort": [
            {
                "Rating": {
                    "order": "asc"  # Tri ascendant (du plus bas au plus haut)
                }
            }
        ]
    }

    # Exécution de la requête pour récupérer les commentaires triés par note
    result = es.search(index=index_name, body=query)

    # Analyse des commentaires triés pour identifier les entreprises avec le plus de commentaires négatifs
    from collections import Counter

    negative_reviews = []
    for hit in result["hits"]["hits"]:
        rating = int(hit["_source"]["Rating"])  # Convertir la note en entier
        if rating < 3:  # Supposons que 1 à 2 sont considérés comme des notes négatives
            negative_reviews.append(hit["_source"]["Company"])

    # Utilisation de Counter pour compter le nombre de commentaires négatifs par entreprise
    company_count = Counter(negative_reviews)

    # Triez les entreprises par le nombre de commentaires négatifs (du plus au moins)
    sorted_companies = sorted(company_count.items(), key=lambda x: x[1], reverse=True)

    # Afficher les entreprises avec le plus de commentaires négatifs
    for company, count in sorted_companies[:6]:  # Affiche les 5 premières entreprises avec le plus de commentaires négatifs
        print(f"Entreprise : {company}, Nombre de commentaires négatifs : {count}")

    # Le nombre de commentaires non répondues par les entreprises
    # Exécution de la requête
    result = es.search(index=index_name, 
    body={
        "query": {
            "match": {
                "Reply": {
                    "query": "No Reply"
                }
            }
        },
        "aggs": {
            "companies": {
                "terms": {
                    "field": "Company",
                    "size": 10
                }
            }
        }
    })

    # Récupération des résultats
    companies = result["aggregations"]["companies"]["buckets"]

    # Affichage des résultats
    for company in companies:
        print(f"Entreprise : {company['key']} - Nombre de No Reply : {company['doc_count']}")

    # Exécution de la requête pour obtenir le classement des entreprises selon leur note moyenne
    es = Elasticsearch(hosts="http://localhost:9200")

    # Index des avis clients
    index_name = "reviews"
    query = {
        "aggs": {
            "companies": {
                "terms": {
                    "field": "Company"
                },
                "aggs": {
                    "average_rating": {
                        "avg": {
                            "field": "Rating"
                        }
                    }
                }
            }
        }
    }

    result = es.search(index=index_name, body=query)

    # Récupération des résultats
    companies = result["aggregations"]["companies"]["buckets"]

    # Tri des entreprises par leur note moyenne
    companies.sort(key=lambda company: company["average_rating"]["value"], reverse=False)

    # Affichage des résultats
    for company in companies:
        average_ratings = round(company['average_rating']['value'], 2)
        print(f"Entreprise : {company['key']} - Note moyenne : {average_ratings}")

    # Exécution de la requête pour obtenir les différents statuts des commentateurs
    es = Elasticsearch(hosts="http://localhost:9200")

    # Index des avis clients
    index_name = "reviews"
    query = {
        "aggs": {
            "statuses": {
                "terms": {
                    "field": "Status"
                }
            }
        }
    }

    result = es.search(index=index_name, body=query)

    # Récupération des résultats
    statuses = result["aggregations"]["statuses"]["buckets"]

    # Affichage des résultats
    for status in statuses:
        print(f"Status : {status['key']} - Nombre de commentateurs : {status['doc_count']}")

    # Exécution de la requête pour obtenir le délai de réponse des entreprises sur les avis ayant obtenu une réponse.
    es = Elasticsearch(hosts="http://localhost:9200")

    # Index des avis clients
    index_name = "reviews"
    query = {
        "aggs": {
            "companies": {
                "terms": {
                    "field": "Company"
                },
                "aggs": {
                    "average_day": {
                        "avg": {
                            "field": "Response_time"
                        }
                    }
                }
            }
        }
    }

    result = es.search(index=index_name, body=query)

    # Récupération des résultats
    companies = result["aggregations"]["companies"]["buckets"]

    # Tri des entreprises par leur note moyenne
    companies.sort(key=lambda company: company["average_day"]["value"], reverse=False)

    # Affichage des résultats
    for company in companies:
        average_days = round(company['average_day']['value'], 2)
        print(f"Entreprise : {company['key']} - Délai de réponse moyen : {average_days}")
    
    # Nombre et Pourcentage de commentaires non répondus par entreprise
    query = {
        "query": {
            "match": {
                "Reply": "No Reply"
            }
        },
        "aggs": {
            "total_no_reply": {
                "value_count": {
                    "field": "Reply"
                }
            },
            "companies": {
                "terms": {
                    "field": "Company"
                },
                "aggs": {
                    "number_of_no_reply": {
                        "value_count": {
                            "field": "Reply"
                        }
                    }
                }
            }
        }
    }

    result = es.search(index=index_name, body=query)
    # Récupération des résultats
    total_no_reply = result["aggregations"]["total_no_reply"]["value"]
    companies = result["aggregations"]["companies"]["buckets"]

    # Affichage des résultats
    for company in companies:
        number_of_no_reply = company["number_of_no_reply"]["value"]
        percentage = (number_of_no_reply / total_no_reply) * 100
        print(f"Entreprise : {company['key']} - Nombre de No Reply : {number_of_no_reply} - Taux de No Reply : {percentage:.2f}%")

if __name__ == "__main__":
    create_elasticsearch_index()
