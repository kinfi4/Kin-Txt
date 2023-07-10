import React, {useEffect, useState} from 'react';
import axios from "axios";
import {STATISTICS_SERVICE_URL} from "../../../../../config";
import {hideModalWindow} from "../../../../../redux/reducers/modalWindowReducer";
import {connect} from "react-redux";
import TapeCss from "../../../tape/Tape.module.css";
import {NavLink} from "react-router-dom";
import ComparisonCss from "../../ReportVisualization/Comparison/ChoseComparisonReport.module.css";
import {showMessage} from "../../../../../utils/messages";

const SelectTemplateModalWindow = ({choseTemplate, hideModalWindow, ...props}) => {
    const [templates, setTemplates] = useState([]);

    const onChoseTemplate = (templateId) => {
        choseTemplate(templateId);
        hideModalWindow();
    }

    const loadTemplates = () => {
        const token = localStorage.getItem("token");
        axios.get(STATISTICS_SERVICE_URL + "/templates", {headers: {"Authorization": `Token ${token}`}})
        .then(res => {
            setTemplates(res.data.templates.map(template => {
                return {name: template.name, id: template.id};
            }));
        })
        .catch(err => {
            showMessage([{message: "Something went wrong during templates loading.", type: "danger"}]);
        });
    }

    useEffect(() => {
        loadTemplates();
    }, []);

    return (
        <div className={TapeCss.enterLinkContainer}>
            <h2 style={{textAlign: "center", marginBottom: "40px"}}>CHOSE YOUR TEMPLATE</h2>
            <>
                {
                    templates.map((template, idx) => (
                            <div
                                key={idx}
                                className={`${ComparisonCss.comparisonReportBlock}`}
                                onClick={() => onChoseTemplate(template.id)}
                            >
                                {template.name}
                            </div>
                        )
                    )
                }
            </>

        </div>
    );
};

let mapStateToProps = (state) => {
    return {}
}

let mapDispatchToProps = (dispatch) => {
    return {
        hideModalWindow: () => dispatch(hideModalWindow),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(SelectTemplateModalWindow);