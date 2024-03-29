import React from "react";
import {connect} from "react-redux";

import {ModelTypes, PossibleTruncatePaddingTypes, SupportedLanguages} from "../../../../../config";
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
        padding: PossibleTruncatePaddingTypes.Pre,
        truncating: PossibleTruncatePaddingTypes.Pre,
        maxlen: null,
    },
};

const ModelCreateForm = ({createModel}) => {
    const [data, setData] = React.useState(initialState);
    const setInitialState = () => setData(initialState);

    return (
        <DefaultModelForm
            data={data}
            setData={setData}
            onModelSavingCallback={() => createModel(data, setInitialState)}
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
