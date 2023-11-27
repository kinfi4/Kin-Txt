import React, {useEffect, useState} from 'react';
import {connect} from "react-redux";
import {AiFillDelete} from "react-icons/ai";

import TapeCss from "../../../Tape/Tape.module.css";
import GenerateReportCss from "../styles/GenerateReport.module.css";

import {STATISTICS_SERVICE_URL} from "../../../../../config";
import {hideModalWindow} from "../../../../../redux/reducers/modalWindowReducer";
import {showMessage} from "../../../../../utils/messages";
import APIRequester from "../../../../../common/apiCalls/APIRequester";

const SelectTemplateModalWindow = ({choseTemplate, hideModalWindow, ...props}) => {
    const [templates, setTemplates] = useState([]);
    const onChoseTemplate = (templateId) => {
        choseTemplate(templateId);
        hideModalWindow();
    }
    const loadTemplates = () => {
        const apiRequester = new APIRequester(STATISTICS_SERVICE_URL);

        apiRequester.get("/templates").then((response) => {
            setTemplates(response.data.templates.map(template => {
                return {name: template.name, id: template.id};
            }));
        }).catch((error) => {
            showMessage([{message: "Something went wrong during blueprint loading.", type: "danger"}]);
        });
    }

    const onDeleteClick = (templateId) => {
        if(!window.confirm("Are you sure you want to delete this blueprint?")) {
            return;
        }

        const apiRequester = new APIRequester(STATISTICS_SERVICE_URL);

        apiRequester.delete(`/templates/${templateId}`).then((response) => {
            showMessage([{message: "Blueprint deleted.", type: "success"}]);
            loadTemplates();
        }).catch((error) => {
            showMessage([{message: "Something went wrong during blueprint deleting.", type: "danger"}]);
        });
    };

    useEffect(() => {
        loadTemplates();
    }, []);


    return (
        <div className={TapeCss.enterLinkContainer}>
            <h2 style={{textAlign: "center", marginBottom: "40px"}}>CHOSE YOUR BLUEPRINT</h2>
            <>
                {
                    templates.map((template, idx) => (
                        <div className={GenerateReportCss.choseTemplateBlock} key={idx}>
                            <span onClick={() => onChoseTemplate(template.id)}>{template.name}</span>
                            <span onClick={() => onDeleteClick(template.id)}><AiFillDelete /></span>
                        </div>
                        )
                    )
                }
            </>
        </div>
    );
};

const mapDispatchToProps = (dispatch) => {
    return {
        hideModalWindow: () => dispatch(hideModalWindow),
    }
}

export default connect(() => null, mapDispatchToProps)(SelectTemplateModalWindow);