import axios from "axios";
import {REPORTS_BUILDER_URL} from "../../config";
import {FETCH_ERROR} from "./channelsReducer";

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

let initialState = {
    templates: [],
}

const TEMPLATES_LOADED = "TEMPLATES_LOADED";


export const loadUserTemplates = () => (dispatch) => {
    const token = localStorage.getItem("token")

    axios.get(REPORTS_BUILDER_URL + "/visualization-template", {
        headers: {
            "Authorization": `Token ${token}`,
        }
    }).then(res => {
        dispatch({type: TEMPLATES_LOADED, templates: res.data})
    }).catch(err => {
        console.log(err.response.data.errors)
        dispatch({type: FETCH_ERROR, errors: err.response.data.errors})
    });
}

export const deleteTemplate = (templateId) => (dispatch) => {
    const token = localStorage.getItem("token")

    axios.delete(REPORTS_BUILDER_URL + `/visualization-template/${templateId}`, {
        headers: {
            "Authorization": `Token ${token}`,
        }
    }).then(res => {
        dispatch(loadUserTemplates())
    }).catch(err => {
        console.log(err.response.data.errors)
        dispatch({type: FETCH_ERROR, errors: err.response.data.errors})
    });
}


export default function visualizationTemplatesReducer(state = initialState, action) {
    switch (action.type) {
        case TEMPLATES_LOADED:
            return {
                ...state,
                templates: action.templates,
            }
        default:
            return state;
    }
}