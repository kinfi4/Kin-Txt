import React from "react";
import TemplateDefaultForm from "../TemplateDefaultForm/TemplateDefaultForm";


const TemplateCreateForm = () => {
    const [data, setData] = React.useState({
        name: "",
        charts: [],
    });

    return <TemplateDefaultForm
        data={data}
        setData={setData}
    />;
};


export default TemplateCreateForm;