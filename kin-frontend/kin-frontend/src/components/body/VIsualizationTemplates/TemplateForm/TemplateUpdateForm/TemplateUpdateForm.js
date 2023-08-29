import React, {useEffect} from "react";
import TemplateDefaultForm from "../TemplateDefaultForm/TemplateDefaultForm";
import {updateTemplate} from "../../../../../redux/reducers/visualizationTemplates";
import {connect} from "react-redux";
import APIRequester from "../../../../common/apiCalls/APIRequester";
import {MODEL_TYPES_URL} from "../../../../../config";
import {showMessage} from "../../../../../utils/messages";


const TemplateUpdateForm = ({templateId, updateTemplate}) => {
    const [data, setData] = React.useState({name: "", charts: []});

    useEffect(() => {
        const requester = new APIRequester(MODEL_TYPES_URL);

        requester.get(`/visualization-template/${templateId}`).then((response) => {
            setData({
                ...data,
                name: response.data.name,
                charts: response.data.visualizationDiagramTypes,
            });
        }).catch((error) => {
            if(error.response && error.response.status === 404) {
                showMessage([{message: "Template not found", type: 'danger'}]);
                return;
            }

            showMessage([{message: "Something went wrong during model loading.", type: 'danger'}]);
        });
    }, []);

    return <TemplateDefaultForm
        data={data}
        setData={setData}
        onCreationCallback={() => updateTemplate(
            templateId,
            {name: data.name, visualizationDiagramTypes: data.charts}
        )}
        isUpdateForm={true}
    />;
};


const mapDispatchToProps = (dispatch) => {
    return {
        updateTemplate: (id, data) => dispatch(updateTemplate(id, data)),
    };
}

export default connect(null, mapDispatchToProps)(TemplateUpdateForm);
