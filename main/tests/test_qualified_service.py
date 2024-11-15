import unittest
from unittest.mock import MagicMock
from main.services.qualified_service import QualifiedService
from main.mongodb.MongoHelper import MongoDBClient


class TestQualifiedService(unittest.TestCase):
    def setUp(self):
        # Create a mock instance of MongoDBClient
        self.mock_mdb_client = MagicMock(spec=MongoDBClient)

        # Mock the collection attribute of MongoDBClient
        self.mock_mdb_client.collection = MagicMock()

        # Initialize QualifiedService with the mock MongoDB client
        self.qualified_service = QualifiedService(self.mock_mdb_client)

    def test_get_place_of_work_count_grouped_by_role_and_state(self):
        # Setup mock response
        self.mock_mdb_client.collection.aggregate.return_value = [
            {"_id": "On-site", "count": 5},
            {"_id": "Remote", "count": 3}
        ]

        # Call the method
        result = self.qualified_service.get_place_of_work_count_grouped_by_role_and_state(
            "United States", "NY", "Data Analyst"
        )

        # Assert the result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["_id"], "On-site")
        self.assertEqual(result[0]["count"], 5)

    def test_get_bigram_data_by_country_state_role(self):
        # Setup mock response
        self.mock_mdb_client.query_documents.return_value = iter([{
            "tools": [{"bigram": ["tool1", "tool2"], "score": 2}],
            "libraries": [{"bigram": ["lib1", "lib2"], "score": 3}],
            "skills": [{"bigram": ["skill1", "skill2"], "score": 5}],
            "languages": [{"bigram": ["lang1", "lang2"], "score": 4}]
        }])

        # Call the method
        result = self.qualified_service.get_bigram_data_by_country_state_role(
            "United States", "NY", "Data Analyst"
        )

        # Assert the result
        self.assertIn("tools", result)
        self.assertIn("libraries", result)
        self.assertIn("skills", result)
        self.assertIn("languages", result)
        self.assertEqual(len(result["tools"]), 1)
        self.assertEqual(result["tools"][0]["bigram"], ["tool1", "tool2"])

    def test_get_education_data_by_country_state_role(self):
        # Setup mock response
        self.mock_mdb_client.query_documents.return_value = iter([{
            "education": ["Bachelor's Degree", "Master's Degree"]
        }])

        # Call the method
        result = self.qualified_service.get_education_data_by_country_state_role(
            "United States", "NY", "Data Analyst"
        )

        # Assert the result
        self.assertEqual(len(result), 2)
        self.assertIn("Bachelor's Degree", result)
        self.assertIn("Master's Degree", result)

    def test_get_freq_grouped_by_state(self):
        # Setup mock response
        self.mock_mdb_client.collection.aggregate.return_value = [
            {"_id": "NY", "count": 10},
            {"_id": "CA", "count": 8}
        ]

        # Call the method
        result = self.qualified_service.get_freq_grouped_by_state("United States")

        # Assert the result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["state"], "NY")
        self.assertEqual(result[0]["count"], 10)


if __name__ == '__main__':
    unittest.main()
