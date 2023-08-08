import React, {useEffect} from "react";
import APIRequester from "../../../../common/apiCalls/APIRequester";
import {ModelTypes, REPORTS_BUILDER_URL} from "../../../../../config";
import {showMessage} from "../../../../../utils/messages";
import DefaultModelForm from "../DefaultForm/DefaultModelForm";
import {validateAndSaveModel} from "../../../../../redux/reducers/modelsReducer";
import {validateFormData} from "../common/FormDataValidation";
import {connect} from "react-redux";

const ModelUpdateForm = ({modelId, onModelSavingCallback}) => {
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
        id: modelId,
    });

    useEffect(() => {
        const requester = new APIRequester(REPORTS_BUILDER_URL);

        requester.get(`/models/${modelId}`).then((response) => {
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
                modelName: response.data.modelPath.split("/").pop(),
                tokenizerName: response.data.tokenizerPath.split("/").pop(),
                validationMessage: response.data.validationMessage,
                id: modelId,
            });
        }).catch((error) => {
            console.log(error);
            if(error.response && error.response.status === 404) {
                showMessage([{message: "Model not found", type: 'danger'}]);
                return;
            }

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