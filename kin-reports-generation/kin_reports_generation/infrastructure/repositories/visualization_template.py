import logging

from pymongo import MongoClient


class VisualizationTemplateRepository:
    def __init__(self, mongo_client: MongoClient):
        self._mongo_client = mongo_client
        self._reports_generation_db = mongo_client["reports_generation_service"]
        self._templates_collection = self._reports_generation_db["templates"]

        self._logger = logging.getLogger(self.__class__.__name__)
