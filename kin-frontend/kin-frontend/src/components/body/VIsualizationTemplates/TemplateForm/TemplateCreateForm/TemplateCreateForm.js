import React from "react";
import TemplateDefaultForm from "../TemplateDefaultForm/TemplateDefaultForm";
import {createTemplate} from "../../../../../redux/reducers/visualizationTemplates";
import {connect} from "react-redux";


const TemplateCreateForm = ({createTemplate}) => {
    const [data, setData] = React.useState({
        name: "",
        charts: [],
    });

    return <TemplateDefaultForm
        data={data}
        setData={setData}
        onCreationCallback={() => createTemplate({
            name: data.name,
            visualizationDiagramTypes: data.charts,
        })}
    />;
};


const mapDispatchToProps = (dispatch) => {
    return {
        createTemplate: (data) => dispatch(createTemplate(data)),
    };
}

export default connect(null, mapDispatchToProps)(TemplateCreateForm);
