import React, {useEffect} from "react";
import {connect} from "react-redux";

import APIRequester from "../../../../../common/apiCalls/APIRequester";
import {ModelTypes, MODEL_TYPES_URL} from "../../../../../config";
import {showMessage} from "../../../../../utils/messages";
import DefaultModelForm from "../DefaultForm/DefaultModelForm";
import {validateAndSaveModel} from "../../../../../redux/reducers/modelsReducer";
import {validateFormData} from "../common/FormDataValidation";

const ModelUpdateForm = ({modelCode, onModelSavingCallback}) => {
    const [data, setData] = React.useState({
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
    });

    useEffect(() => {
        const requester = new APIRequester(MODEL_TYPES_URL);

        requester.get(`/models/${modelCode}`).then((response) => {
            setData({
                ...data,
                modelType: response.data.modelType,
                modelFile: null,
                tokenizerFile: null,
                name: response.data.name,
                modelStatus: response.data.modelStatus,
                categoryMapping: Object.entries(response.data.categoryMapping).map(
                    (value, categoryName) => ({
                        value: Number(value[0]), categoryName: value[1]
                    })
                ),
                modelName: response.data.modelName,
                tokenizerName: response.data.tokenizerName,
                validationMessage: response.data.validationMessage,
                code: response.data.code,
            });
        }).catch((error) => {
            if(error.response && error.response.status === 404) {
                showMessage([{message: "Model not found", type: 'danger'}]);
                return;
            }

            console.log(error)

            showMessage([{message: "Something went wrong during model loading.", type: 'danger'}]);
        });
    }, []);

    const onUpdateButtonClick = () => {
        const validationResult = validateFormData(data, true);

        if (!validationResult) {
            return;
        }

        onModelSavingCallback(data);
    }


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
        onModelSavingCallback: (model) => dispatch(validateAndSaveModel(model, true)),
    };
}

export default connect(() => {return{};}, mapDispatchToProp)(ModelUpdateForm);