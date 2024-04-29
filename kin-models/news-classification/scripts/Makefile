PRETRAINED_MODELS_DIR := /home/kinfi4/python/Kin-News/kin-models/news-classification/trained-models/bert-models/train-case-1

predict:
	python -m predict-labels predict here.csv -m ${PRETRAINED_MODELS_DIR}/bert-news-classification-model -t ${PRETRAINED_MODELS_DIR}/bert-news-tokenizer -l ${PRETRAINED_MODELS_DIR}/news-label-encoder.pkl
