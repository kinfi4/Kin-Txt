import React, {useEffect, useState} from "react";
import {connect} from "react-redux";
import {AiFillDelete} from "react-icons/ai";

import commonCss from "../../../../../common/CommonStyles.module.css";
import GenerateReportCss from "../styles/GenerateReport.module.css";

import {hideModalWindow} from "../../../../../redux/reducers/modalWindowReducer";
import {GenerationBlueprintController} from "../GenerationBlueprintController";

const SelectTemplateModalWindow = ({setReportData, hideModalWindow}) => {
    const [templates, setTemplates] = useState([]);
    const blueprintController = new GenerationBlueprintController(setReportData, setTemplates, hideModalWindow);

    useEffect(() => {
        (async () => {
            await blueprintController.loadUserBlueprintsList();
        })();
    }, []);

    return (
        <div className={commonCss.enterLinkContainer}>
            <h2 style={{textAlign: "center", marginBottom: "40px"}}>
                CHOSE YOUR BLUEPRINT
            </h2>
            <>
                {templates.map((template, idx) => (
                    <div
                        className={GenerateReportCss.choseTemplateBlock}
                        key={idx}
                    >
                        <span onClick={() => blueprintController.loadBlueprint(template.id)}>
                            {template.name}
                        </span>
                        <span onClick={() => blueprintController.deleteBlueprint(template.id)}>
                            <AiFillDelete />
                        </span>
                    </div>
                ))}
            </>
        </div>
    );
};

const mapDispatchToProps = (dispatch) => {
    return {
        hideModalWindow: () => dispatch(hideModalWindow),
    };
};

export default connect(() => null, mapDispatchToProps)(SelectTemplateModalWindow);
