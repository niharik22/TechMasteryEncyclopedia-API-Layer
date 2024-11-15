from pymongo import MongoClient
import logging
from typing import List, Dict


class MongoDBClient:
    def __init__(self, uri: str, database_name: str, collection_name: str, test_mode: bool):
        try:
            self.client = MongoClient(uri)
            self.test_mode = test_mode
            if test_mode:
                self.db = self.client['test_db']  # Use test database if in test mode
            else:
                self.db = self.client[database_name]  # Use production database
            self.collection = self.db[collection_name]
            logging.info(f"Connected to MongoDB database: {self.db.name}, collection: {self.collection.name}")
        except Exception as e:
            logging.error(f"Error connecting to MongoDB: {e}")
            raise


    def make_index(self, index_fields) -> None:
        """
        Creates an index on the specified fields in the collection.

        Args:
            index_fields (str or list): Field(s) for the index. Can be a single field as a string or multiple fields as a list of tuples.
        """
        try:
            # If a single string is passed, create a single field index
            if isinstance(index_fields, str):
                self.collection.create_index(index_fields, unique=True)
                logging.info(f"Index created on {index_fields}")
            # If a list of tuples is passed, create a compound index
            elif isinstance(index_fields, list) and all(isinstance(field, tuple) for field in index_fields):
                self.collection.create_index(index_fields, unique=True)
                logging.info(f"Compound index created on {index_fields}")
            else:
                logging.error("Invalid index format. Provide a string or list of tuples for compound indexes.")
        except Exception as e:
            logging.error(f"Error creating index: {e}")


    def insert_document(self, doc: dict, col_name: str = None) -> bool:
        """Inserts a document into the collection."""
        collection = self.collection if col_name is None else self.db[col_name]
        try:
            collection.insert_one(doc)
            logging.info(f"Document inserted into {collection.name}")
            return True
        except Exception as e:
            logging.error(f"Error inserting document: {e}")
            return False

    def update_document(self, query: dict, update: dict, upsert: bool = True, col_name: str = None):
        """Updates or inserts a document based on the query."""
        collection = self.collection if col_name is None else self.db[col_name]
        try:
            collection.update_one(query, {'$set': update}, upsert=upsert)
            logging.debug(f"Document updated or inserted in {collection.name}")
        except Exception as e:
            logging.error(f"Error updating document: {e}")

    def insert_documents(self, docs: List[Dict], col_name: str) -> bool:
        """Performs bulk insertion of documents into the specified collection."""
        collection = self.db[col_name]
        if docs:
            try:
                collection.insert_many(docs)
                logging.info(f"Inserted {len(docs)} documents into {collection.name} in bulk.")
                return True
            except Exception as e:
                logging.error(f"Error during bulk insertion into {collection.name}: {e}")
                return False
        else:
            logging.info("No documents to insert.")
            return False

    def update_many_documents(self, query: dict, update: dict, col_name: str):
        """Updates multiple documents in the specified collection."""
        collection = self.db[col_name]
        try:
            result = collection.update_many(query, {'$set': update})
            logging.info(f"Updated {result.modified_count} documents in {collection.name}")
        except Exception as e:
            logging.error(f"Error updating documents in {collection.name}: {e}")

    def query_documents(self, query: dict, projection: dict = None, col_name: str = None):
        """Queries documents from the collection."""
        collection = self.collection if col_name is None else self.db[col_name]
        try:
            results = collection.find(query, projection)
            logging.debug(f"Queried documents from {collection.name}")
            return results
        except Exception as e:
            logging.error(f"Error querying documents: {e}")
            return None

    def change_database_and_collection(self, new_database_name: str = None, new_collection_name: str = None) -> None:
        """Changes the database and/or collection to new specified names."""
        try:
            # If test_mode is False, allow changing the database
            if not self.test_mode and new_database_name:
                self.db = self.client[new_database_name]
                logging.info(f"Database changed to: {self.db.name}")

            # Change collection if new_collection_name is provided
            if new_collection_name:
                self.collection = self.db[new_collection_name]
                logging.info(f"Collection changed to: {self.collection.name}")
        except Exception as e:
            logging.error(f"Error changing database and/or collection: {e}")

    def close_connection(self) -> None:
        """Closes the connection to MongoDB."""
        try:
            self.client.close()
            logging.info("MongoDB connection closed.")
        except Exception as e:
            logging.error(f"Error closing MongoDB connection: {e}")