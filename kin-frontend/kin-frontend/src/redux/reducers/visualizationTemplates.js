import {MODEL_TYPES_URL} from "../../config";
import APIRequester from "../../domain/apiCalls/APIRequester";
import {VisualizationTemplateValidator} from "../../domain/VisualizationTemplateValidator";
import {showMessage} from "../../utils/messages";

let initialState = {
    templates: [],
};

const TEMPLATES_LOADED = "TEMPLATES_LOADED";

export const loadUserTemplates = () => async (dispatch) => {
    const apiRequester = new APIRequester(MODEL_TYPES_URL, dispatch);

    const response = await apiRequester.get(`/visualization-template`);
    dispatch({type: TEMPLATES_LOADED, templates: response.data});
};

export const deleteTemplate = (templateId) => async (dispatch) => {
    const apiRequester = new APIRequester(MODEL_TYPES_URL, dispatch);

    const response = await apiRequester.delete(
        `/visualization-template/${templateId}`
    );

    if (response.status === 204) {
        dispatch(loadUserTemplates());
    }
};

export const createTemplate = (templateData) => async (dispatch) => {
    const validator = new VisualizationTemplateValidator(templateData);
    const [isValid, errorMessages] = validator.validate();
    if(!isValid) {
        showMessage(errorMessages.map(message => {return {message, type: "danger"}}));
        return;
    }

    const apiRequester = new APIRequester(MODEL_TYPES_URL, dispatch);

    const response = await apiRequester.post(
        `/visualization-template`,
        templateData
    );

    if (response.status === 201) {
        window.location.href = "/templates";
        dispatch(loadUserTemplates());
    }
};

export const updateTemplate =
    (templateId, templateData) => async (dispatch) => {
        const validator = new VisualizationTemplateValidator(templateData);
        const [isValid, errorMessages] = validator.validate();
        if(!isValid) {
            showMessage(errorMessages.map(message => {return {message, type: "danger"}}));
            return;
        }

        const apiRequester = new APIRequester(MODEL_TYPES_URL, dispatch);

        const response = await apiRequester.put(
            `/visualization-template/${templateId}`,
            templateData
        );

        if (response.status === 200) {
            window.location.href = "/templates";
            dispatch(loadUserTemplates());
        }
    };

export default function visualizationTemplatesReducer(
    state = initialState,
    action
) {
    switch (action.type) {
        case TEMPLATES_LOADED:
            return {
                ...state,
                templates: action.templates,
            };
        default:
            return state;
    }
}
