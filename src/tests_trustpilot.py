import unittest
from elasticsearch import Elasticsearch
from bdd_trustpilot import create_elasticsearch_index ,es, index_name, mapping  # Importez les variables nécessaires de votre script principal

class TestElasticsearchOperations(unittest.TestCase):
    def setUp(self):
        # Initialisation : Créez une connexion Elasticsearch pour les tests
        self.es = Elasticsearch(hosts="http://localhost:9200")
        self.index_name = "bdd_review_test"
    
    def test_index_exists(self):
        # Vérifie si l'index existe
        self.assertTrue(es.indices.exists(index=index_name))

    def test_data_inserted(self):
        # Vérifie si des données ont été insérées
        result = es.search(index=index_name, size=5)
        self.assertGreater(result["hits"]["total"]["value"], 0)

if __name__ == '__main__':
    unittest.main()
