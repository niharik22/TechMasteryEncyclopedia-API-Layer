import logging
from typing import Dict, List
from main.mongodb.MongoHelper import MongoDBClient
from pymongo import ASCENDING


class QualifiedService:
    def __init__(self, mdb_client: MongoDBClient):
        """
        Initializes the QualifiedService with a MongoDBClient instance.

        Args:
            mdb_client (MongoDBClient): An instance of MongoDBClient.
        """
        self.mdb_client = mdb_client

    def get_place_of_work_count_grouped_by_role_and_state(
            self, country: str, state: str, role: str
    ) -> List[Dict]:
        """
        Queries the 'qualified' collection to get the count of 'place_of_work' grouped
        for a specific country, state, and role.

        Args:
            country (str): The country to filter by.
            state (str): The state to filter by.
            role (str): The role to filter by.

        Returns:
            List[Dict]: A list of dictionaries containing the count of 'place_of_work' occurrences.
        """
        try:
            self.mdb_client.change_database_and_collection(new_collection_name="qualified")
            match_query = {"country": country, "state": state, "role": role}
            pipeline = [
                {"$match": match_query},
                {"$group": {"_id": "$place_of_work", "count": {"$sum": 1}}},
                {"$sort": {"count": ASCENDING}}
            ]

            results = self.mdb_client.collection.aggregate(pipeline)
            grouped_data = [doc for doc in results]
            logging.info("Successfully queried and grouped data for country: %s, state: %s, role: %s", country, state, role)
            return grouped_data

        except Exception as e:
            logging.exception("Failed to query and group data for country: %s, state: %s, role: %s", country, state, role)
            return []

    def get_bigram_details_by_country_state_role(
            self, country: str, state: str, role: str
    ) -> Dict[str, List[Dict]]:
        """
        Queries the 'bigrams' collection to get tools, libraries, skills, and languages
        for a specific country, state, and role.

        Args:
            country (str): The country to filter by.
            state (str): The state to filter by.
            role (str): The role to filter by.

        Returns:
            Dict[str, List[Dict]]: A dictionary containing tools, libraries, skills, and languages data.
        """
        try:
            self.mdb_client.change_database_and_collection(new_collection_name="bigrams")
            query = {"country": country, "state": state, "role": role}
            projection = {"tools": 1, "libraries": 1, "skills": 1, "languages": 1, "_id": 0}

            result = self.mdb_client.query_documents(query, projection)
            document = next(result, None)

            if document:
                logging.info("Successfully fetched bigrams data for country: %s, state: %s, role: %s", country, state, role)
                return {
                    "tools": document.get("tools", []),
                    "libraries": document.get("libraries", []),
                    "skills": document.get("skills", []),
                    "languages": document.get("languages", [])
                }
            else:
                logging.warning("No bigrams data found for country: %s, state: %s, role: %s", country, state, role)
                return {"tools": [], "libraries": [], "skills": [], "languages": []}

        except Exception as e:
            logging.exception("Error querying bigrams data for country: %s, state: %s, role: %s", country, state, role)
            return {"tools": [], "libraries": [], "skills": [], "languages": []}

    def get_education_data_by_country_state_role(
            self, country: str, state: str, role: str
    ) -> List[Dict]:
        """
        Queries the 'bigrams' collection to get the education data
        for a specific country, state, and role.

        Args:
            country (str): The country to filter by.
            state (str): The state to filter by.
            role (str): The role to filter by.

        Returns:
            List[Dict]: A list containing education data. Returns an empty list if no data is found.
        """
        try:
            self.mdb_client.change_database_and_collection(new_collection_name="bigrams")
            query = {"country": country, "state": state, "role": role}
            projection = {"education": 1, "_id": 0}

            result = self.mdb_client.query_documents(query, projection)
            document = next(result, None)

            if document:
                logging.info("Successfully fetched education data for country: %s, state: %s, role: %s", country, state, role)
                return document.get("education", [])
            else:
                logging.warning("No education data found for country: %s, state: %s, role: %s", country, state, role)
                return []

        except Exception as e:
            logging.exception("Error querying education data for country: %s, state: %s, role: %s", country, state, role)
            return []

    def get_freq_grouped_by_state(self, country: str) -> List[Dict]:
        """
        Queries the 'qualified' collection to count the number of records grouped by state
        for a specific country, excluding the state "ALL".

        Args:
            country (str): The country to filter by.

        Returns:
            List[Dict]: A list of dictionaries containing state and count of records, excluding the state "ALL".
        """
        try:
            self.mdb_client.change_database_and_collection(new_collection_name="qualified")
            match_query = {"country": country, "state": {"$ne": "All"}}
            pipeline = [
                {"$match": match_query},
                {"$group": {"_id": "$state", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]

            results = self.mdb_client.collection.aggregate(pipeline)
            grouped_data = [{"state": doc["_id"], "count": doc["count"]} for doc in results]
            logging.info("Successfully fetched record count grouped by state for country: %s, excluding state: ALL", country)
            return grouped_data

        except Exception as e:
            logging.exception("Error querying record count grouped by state for country: %s", country)
            return []

    def get_roles_by_country_and_state(self, country: str, state: str) -> List[str]:
        """
        Queries the 'qualified' collection to get all distinct roles for a specific country and state.

        Args:
            country (str): The country to filter by.
            state (str): The state to filter by.

        Returns:
            List[str]: A list of distinct roles available in the given country and state.
        """
        try:
            # Switch to the 'qualified' collection
            self.mdb_client.change_database_and_collection(new_collection_name="qualified")

            # Query to filter by country and state
            query = {"country": country, "state": state}

            # Use the distinct method to get unique roles
            roles = self.mdb_client.collection.distinct("role", query)

            logging.info("Successfully fetched distinct roles for country: %s and state: %s", country, state)
            return roles

        except Exception as e:
            logging.exception("Error querying distinct roles for country: %s and state: %s", country, state)
            return []
