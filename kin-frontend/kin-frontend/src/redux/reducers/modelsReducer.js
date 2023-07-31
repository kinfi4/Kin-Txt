import axios from "axios";
import {FETCH_ERROR} from "./channelsReducer";
import {REPORTS_BUILDER_URL} from "../../config";
import {showMessage} from "../../utils/messages";

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

let initialState = {
    models: [],
}


const MODELS_LOADED = "MODELS_LOADED";


export const loadUserModels = () => (dispatch) => {
    const token = localStorage.getItem("token")

    axios.get(REPORTS_BUILDER_URL + "/models", {
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

    axios.delete(REPORTS_BUILDER_URL + "/models/" + modelId, {
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

export const createModel = (model) => (dispatch) => {
    const token = localStorage.getItem("token");

    const formData = new FormData();
    formData.append("modelType", model.modelType);
    formData.append("modelData", model.modelFile);
    formData.append("tokenizerData", model.tokenizerFile);
    formData.append("name", model.name);

    const categoryMappingsAsDict = model.categoryMapping.reduce((acc, curr) => {
        acc[curr.value] = curr.categoryName;
        return acc;
    }, {});
    formData.append("categoryMapping", JSON.stringify(categoryMappingsAsDict));

    axios.post(REPORTS_BUILDER_URL + "/models", formData, {
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




