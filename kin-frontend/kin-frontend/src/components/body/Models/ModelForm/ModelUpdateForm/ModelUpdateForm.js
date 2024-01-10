import React, {useEffect} from "react";
import {connect} from "react-redux";

import APIRequester from "../../../../../common/apiCalls/APIRequester";
import {ModelTypes, MODEL_TYPES_URL, SupportedLanguages, PossibleTruncatePaddingTypes} from "../../../../../config";
import {showMessage} from "../../../../../utils/messages";
import DefaultModelForm from "../DefaultForm/DefaultModelForm";
import {validateAndSaveModel} from "../../../../../redux/reducers/modelsReducer";
import {validateFormData} from "../common/FormDataValidation";

const initialState = {
    modelType: ModelTypes.SKLEARN_MODEL,
    modelFile: null,
    tokenizerFile: null,
    categoryMapping: [],
    name: "",
    modelStatus: null,
    modelName: null,
    tokenizerName: null,
    validationMessage: null,
    code: "",
    preventPageReload: true,
    preprocessingConfig: {
        removeLinks: true,
        removeEmoji: false,
        removePunctuation: true,
        removeExtraSpaces: true,
        removeHtmlTags: true,
        lowercase: true,
        stopWordsFile: null,
        stopWordsFileName: null,
        language: SupportedLanguages.ENGLISH,
        lemmatize: false,
        padding: PossibleTruncatePaddingTypes.Pre,
        truncating: PossibleTruncatePaddingTypes.Pre,
        maxlen: null,
    },
};

const ModelUpdateForm = ({modelCode, onModelSavingCallback}) => {
    const [data, setData] = React.useState(initialState);

    const letPageReload = () => setData({...initialState, preventPageReload: false});

    useEffect(() => {
        const requester = new APIRequester(MODEL_TYPES_URL);

        requester
            .get(`/models/${modelCode}`)
            .then((response) => {
                setData({
                    ...data,
                    modelType: response.data.modelType,
                    modelFile: null,
                    tokenizerFile: null,
                    name: response.data.name,
                    modelStatus: response.data.modelStatus,
                    categoryMapping: Object.entries(
                        response.data.categoryMapping
                    ).map((value, categoryName) => ({
                        value: Number(value[0]),
                        categoryName: value[1],
                    })),
                    modelName: response.data.originalModelFileName,
                    tokenizerName: response.data.originalTokenizerFileName,
                    validationMessage: response.data.validationMessage,
                    code: response.data.code,
                    modelDataHasChanged: false,
                    preprocessingConfig: {
                        removeLinks: response.data.preprocessingConfig.removeLinks,
                        removeEmoji: response.data.preprocessingConfig.removeEmoji,
                        removePunctuation: response.data.preprocessingConfig.removePunctuation,
                        removeExtraSpaces: response.data.preprocessingConfig.removeExtraSpaces,
                        removeHtmlTags: response.data.preprocessingConfig.removeHtmlTags,
                        lowercase: response.data.preprocessingConfig.lowercase,
                        stopWordsFile: null,
                        stopWordsFileName: response.data.preprocessingConfig.stopWordsFileOriginalName,
                        language: SupportedLanguages.getLanguageByValue(
                            response.data.preprocessingConfig.language
                        ),
                        lemmatize: response.data.preprocessingConfig.lemmatizeText,
                        maxlen: response.data.preprocessingConfig.maxTokens,
                        padding: PossibleTruncatePaddingTypes.getPaddingTypeByValue(
                            response.data.preprocessingConfig.padding
                        ),
                        truncating: PossibleTruncatePaddingTypes.getPaddingTypeByValue(
                            response.data.preprocessingConfig.truncating
                        ),
                    }
                });
            })
            .catch((error) => {
                if (error.response && error.response.status === 404) {
                    showMessage([{message: "Model not found", type: "danger"}]);
                    return;
                }

                console.log(error);

                showMessage([
                    {
                        message: "Something went wrong during model loading.",
                        type: "danger",
                    },
                ]);
            });
    }, []);

    const onUpdateButtonClick = () => {
        const validationResult = validateFormData(data, true);

        if (!validationResult) {
            return;
        }

        onModelSavingCallback(data, letPageReload);

        // update after delay in 100ms
        setTimeout(() => {
            window.location.href = "/models";
        }, 100);
    };

    return (
        <DefaultModelForm
            data={data}
            setData={setData}
            onModelSavingCallback={onUpdateButtonClick}
            isUpdateForm={true}
        />
    );
};

const mapDispatchToProp = (dispatch) => {
    return {
        onModelSavingCallback: (model, letPageReload) =>
            dispatch(validateAndSaveModel(model, letPageReload, true)),
    };
};

export default connect(() => {
    return {};
}, mapDispatchToProp)(ModelUpdateForm);
