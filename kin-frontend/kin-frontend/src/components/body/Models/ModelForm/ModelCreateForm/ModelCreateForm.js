import React from "react";
import {connect} from "react-redux";

import {ModelTypes, SupportedLanguages} from "../../../../../config";
import {validateFormData} from "../common/FormDataValidation";
import {validateAndSaveModel} from "../../../../../redux/reducers/modelsReducer";
import DefaultModelForm from "../DefaultForm/DefaultModelForm";

const initialState = {
    modelType: ModelTypes.SKLEARN_MODEL,
    modelFile: null,
    tokenizerFile: null,
    categoryMapping: [
        {value: 0, categoryName: "First Category"},
        {value: 1, categoryName: "Second Category"},
    ],
    name: "",
    code: "",
    preprocessingConfig: {
        removeLinks: true,
        removeEmoji: false,
        removePunctuation: true,
        removeExtraSpaces: true,
        removeHtmlTags: true,
        lowercase: true,
        stopWordsFile: null,
        language: SupportedLanguages.ENGLISH,
        lemmatize: false,
    },
};

const ModelCreateForm = ({createModel}) => {
    const [data, setData] = React.useState(initialState);
    const setInitialState = () => setData(initialState);

    const onCreateButtonClick = () => {
        const validationResult = validateFormData(data);

        if (!validationResult) {
            return;
        }

        createModel(data, setInitialState);
    };

    return (
        <DefaultModelForm
            data={data}
            setData={setData}
            onModelSavingCallback={onCreateButtonClick}
        />
    );
};

const mapDispatchToProps = (dispatch) => {
    return {
        createModel: (model, setInitialState) =>
            dispatch(validateAndSaveModel(model, setInitialState)),
    };
};

export default connect(() => new Object(), mapDispatchToProps)(ModelCreateForm);
