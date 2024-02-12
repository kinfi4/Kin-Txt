import axios from "axios";

import {FETCH_ERROR} from "./authReducer";
import {GENERIC_REPORTS_BUILDER_URL, MODEL_TYPES_URL} from "../../config";
import {showMessage} from "../../utils/messages";
import APIRequester from "../../domain/apiCalls/APIRequester";

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

let initialState = {
    models: [],
};

const MODELS_LOADED = "MODELS_LOADED";
const MODEL_VALIDATION_STARTED = "MODEL_VALIDATION_STARTED";

export const loadUserModels =
    (filters = null) =>
    (dispatch) => {
        const apiRequester = new APIRequester(MODEL_TYPES_URL, dispatch);

        const URL = "/models";

        apiRequester
            .get(URL, filters)
            .then((res) => {
                dispatch({type: MODELS_LOADED, models: res.data});
            })
            .catch((err) => {
                console.log(err.response.data.errors);
                dispatch({type: FETCH_ERROR, errors: err.response.data.errors});
            });
    };

export const deleteModel = (modelId) => (dispatch) => {
    const apiRequester = new APIRequester(MODEL_TYPES_URL, dispatch);

    apiRequester
        .delete("/models/" + modelId)
        .then((res) => {
            dispatch(loadUserModels());
        })
        .catch((err) => {
            console.log(err.response.data.errors);
            dispatch({type: FETCH_ERROR, errors: err.response.data.errors});
        });
};

export const validateAndSaveModel =
    (model, setInitialState, updating = false) => async (dispatch) => {
        const token = localStorage.getItem("token");

        const data = {
            modelType: model.modelType,
            name: model.name,
            code: model.code,
        };

        data["preprocessingConfig"] = {};

        data["preprocessingConfig"]["removeLinks"] = model.preprocessingConfig.removeLinks;
        data["preprocessingConfig"]["removeEmoji"] = model.preprocessingConfig.removeEmoji;
        data["preprocessingConfig"]["removePunctuation"] = model.preprocessingConfig.removePunctuation;
        data["preprocessingConfig"]["lowercase"] = model.preprocessingConfig.lowercase;
        data["preprocessingConfig"]["removeExtraSpaces"] = model.preprocessingConfig.removeExtraSpaces;
        data["preprocessingConfig"]["removeHtmlTags"] = model.preprocessingConfig.removeHtmlTags;
        data["preprocessingConfig"]["removeStopWords"] = model.preprocessingConfig.stopWordsFile !== null;
        data["preprocessingConfig"]["lemmatizeText"] = model.preprocessingConfig.lemmatize;
        data["preprocessingConfig"]["language"] = model.preprocessingConfig.language.value;
        data["preprocessingConfig"]["maxTokens"] = model.preprocessingConfig.maxlen;
        data["preprocessingConfig"]["padding"] = model.preprocessingConfig.padding;
        data["preprocessingConfig"]["truncating"] = model.preprocessingConfig.truncating;

        if (model.preprocessingConfig.stopWordsFile !== null) {
            data["preprocessingConfig"]["stopWordsFileOriginalName"] = model.preprocessingConfig.stopWordsFile.name;
        }

        if(updating && model.preprocessingConfig.stopWordsFileOriginalName !== null) {
            data["preprocessingConfig"]["removeStopWords"] = true;
        }

        if (model.modelFile) {
            data["originalModelFileName"] = model.modelFile.name;
        }
        if (model.tokenizerFile) {
            data["originalTokenizerFileName"] = model.tokenizerFile.name;
        }

        const categoryMappingsAsDict = model.categoryMapping.reduce(
            (acc, curr) => {
                acc[curr.value] = curr.categoryName;
                return acc;
            },
            {}
        );
        data["categoryMapping"] = JSON.stringify(categoryMappingsAsDict);

        let resultUrl = "/models";
        let resultMethod = "POST";

        if (updating) {
            resultUrl = "/models/" + model.code;
            resultMethod = "PUT";
        }

        try {
            const response = await axios({
                method: resultMethod,
                url: MODEL_TYPES_URL + resultUrl,
                data: data,
                headers: {
                    Authorization: `Token ${token}`,
                    "Content-Type": "application/json",
                },
            });

            setInitialState();
            dispatch(loadUserModels());
            showMessage([
                {message: "Model validation has started...", type: "success"},
            ]);
        } catch (error) {
            dispatch(deleteModelBinaries(model.code));
            dispatch({type: FETCH_ERROR, errors: error.response.data.errors});
        }
    };

const deleteModelBinaries = (modelCode) => async (dispatch) => {
    const apiRequester = new APIRequester(
        GENERIC_REPORTS_BUILDER_URL,
        dispatch
    );

    console.log(
        "Sending request to delete model binaries for model code: " + modelCode
    );

    const response = await apiRequester.delete("/blobs/delete/" + modelCode);

    if (response.status !== 204) {
        dispatch({type: FETCH_ERROR, errors: response.data.errors});
    }
};

export default function modelsReducer(state = initialState, action) {
    switch (action.type) {
        case MODELS_LOADED:
            return {
                ...state,
                models: action.models,
            };
        default:
            return state;
    }
}
