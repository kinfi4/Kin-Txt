import axios from "axios";

import {FETCH_ERROR} from "./channelsReducer";
import {MODEL_TYPES_URL} from "../../config";
import {showMessage} from "../../utils/messages";

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

let initialState = {
    models: [],
};

const MODELS_LOADED = "MODELS_LOADED";


export const loadUserModels = () => (dispatch) => {
    const token = localStorage.getItem("token")

    axios.get(MODEL_TYPES_URL + "/models", {
        headers: {
            "Authorization": `Token ${token}`,
        }
    }).then(res => {
        dispatch({type: MODELS_LOADED, models: res.data})
    }).catch(err => {
        console.log(err.response.data.errors)
        dispatch({type: FETCH_ERROR, errors: err.response.data.errors})
    });
};

export const deleteModel = (modelId) => (dispatch) => {
    const token = localStorage.getItem("token")

    axios.delete(MODEL_TYPES_URL + "/models/" + modelId, {
        headers: {
            "Authorization": `Token ${token}`,
        }
    }).then(res => {
        dispatch(loadUserModels())
    }).catch(err => {
        console.log(err.response.data.errors)
        dispatch({type: FETCH_ERROR, errors: err.response.data.errors})
    });
};

export const validateAndSaveModel = (model, updating=false) => (dispatch) => {
    const token = localStorage.getItem("token");

    const formData = new FormData();
    formData.append("modelType", model.modelType);
    formData.append("name", model.name);
    formData.append("code", model.code);

    if (updating && (model.modelFile || model.tokenizerFile)) {
        formData.append("modelsHasChanged", "true");
    }

    if (model.modelFile) {
        formData.append("modelData", model.modelFile);
    }
    if (model.tokenizerFile) {
        formData.append("tokenizerData", model.tokenizerFile);
    }

    const categoryMappingsAsDict = model.categoryMapping.reduce((acc, curr) => {
        acc[curr.value] = curr.categoryName;
        return acc;
    }, {});
    formData.append("categoryMapping", JSON.stringify(categoryMappingsAsDict));

    let resultUrl = "/models";
    let resultMethod = "POST";

    if (updating) {
        resultUrl = "/models/" + model.code;
        resultMethod = "PUT";
    }

    axios({
        method: resultMethod,
        url: MODEL_TYPES_URL + resultUrl,
        data: formData,
        headers: {
            "Authorization": `Token ${token}`,
            "Content-Type": "multipart/form-data",
        }
    }).then(res => {
        window.location.replace("/models");
        showMessage([{message: "Model validation has started...", type: "success"}]);
    }).catch(err => {
        console.log(err.response.data.errors);
        dispatch({type: FETCH_ERROR, errors: err.response.data.errors});
    });
}

export default function modelsReducer(state = initialState, action) {
    switch (action.type) {
        case MODELS_LOADED:
            return {
                ...state,
                models: action.models
            }
        default:
            return state;
    }
}




