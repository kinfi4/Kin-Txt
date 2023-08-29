import React from "react";
import {connect} from "react-redux";

import {ModelTypes} from "../../../../../config";
import {validateFormData} from "../common/FormDataValidation";
import {validateAndSaveModel} from "../../../../../redux/reducers/modelsReducer";
import DefaultModelForm from "../DefaultForm/DefaultModelForm";

const ModelCreateForm = ({createModel}) => {
    const [data, setData] = React.useState({
        modelType: ModelTypes.SKLEARN_MODEL,
        modelFile: null,
        tokenizerFile: null,
        categoryMapping: [{value: 0, categoryName: "First Category"}, {value: 1, categoryName: "Second Category"}],
        name: "",
        code: "",
    });

    const onCreateButtonClick = () => {
        const validationResult = validateFormData(data);

        if (!validationResult) {
            return;
        }

        createModel(data);
    }

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
        createModel: (model) => dispatch(validateAndSaveModel(model))
    }
}

export default connect(() => new Object(), mapDispatchToProps)(ModelCreateForm);
