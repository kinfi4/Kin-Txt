import logging

import spacy

_logger = logging.getLogger(__name__)


class SpacyModelLoaderMixin:
    def load_spacy_model(self, model_name: str) -> spacy.language.Language:
        try:
            nlp = spacy.load(model_name)
        except OSError:
            _logger.info(f"[SpacyModelLoaderMixin] Model {model_name} not found. Downloading...")

            spacy.cli.download(model_name)
            nlp = spacy.load(model_name)

        return nlp
