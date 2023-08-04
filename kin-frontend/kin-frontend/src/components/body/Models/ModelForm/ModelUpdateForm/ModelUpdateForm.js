import React, {useEffect} from "react";
import basicStyles from "../ModelFormStyles.module.css";
import APIRequester from "../../../../common/apiCalls/APIRequester";
import {ModelTypes, REPORTS_BUILDER_URL} from "../../../../../config";
import {showMessage} from "../../../../../utils/messages";
import DefaultModelForm from "../DefaultForm/DefaultModelForm";

const ModelUpdateForm = ({modelId}) => {
    const [data, setData] = React.useState({
        modelType: ModelTypes.SKLEARN_MODEL,
        modelFile: null,
        tokenizerFile: null,
        categoryMapping: [],
        name: "",
        modelStatus: null,
        modelName: null,
        tokenizerName: null,
        validationFailedMessage: null,
        modelsHasChanged: false,
    });


    useEffect(() => {
        const requester = new APIRequester(REPORTS_BUILDER_URL);

        requester.get(`/models/${modelId}`).then((response) => {
            setData({
                ...data,
                modelType: response.modelType,
                modelFile: null,
                tokenizerFile: null,
                name: response.name,
                modelStatus: response.modelStatus,
                categoryMapping: Object.entries(response.categoryMapping).map(
                    (value, categoryName) => ({
                        value: Number(value[0]), categoryName: value[1]
                    })
                ),
                modelName: response.modelPath.split("/").pop(),
                tokenizerName: response.tokenizerPath.split("/").pop(),
                validationFailedMessage: response.validationFailedMessage,
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


    return (
        <DefaultModelForm
            data={data}
            setData={setData}
            onModelSavingCallback={() => {}}
            isUpdateForm={true}
        />
    );
};

export default ModelUpdateForm;