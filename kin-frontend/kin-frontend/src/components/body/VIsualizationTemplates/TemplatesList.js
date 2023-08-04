import React, {useEffect} from "react";
import {connect} from "react-redux";
import {Link} from "react-router-dom";
import {useRouteMatch} from "react-router-dom/cjs/react-router-dom";
import {AiFillDelete, AiFillEdit} from "react-icons/ai";

import commonStyles from "../../common/CommonStyles.module.css";
import selectReportMenuCss from "../Reports/SelectReport/SelectReportMenu.module.css";
import mainPageCss from "../MainPage.module.css";
import statisticsCss from "../Reports/Statistics.module.css";
import modelsCss from "./../Models/styles/ModelsList.module.css";

import {ModelStatuses} from "../../../config";
import {loadUserTemplates} from "../../../redux/reducers/visualizationTemplates";

let modelStatusToStatusClass = {
    [ModelStatuses.VALIDATED]: selectReportMenuCss.statusCellCompleted,
    [ModelStatuses.VALIDATING]: selectReportMenuCss.statusCellProcessing,
    [ModelStatuses.VALIDATION_FAILED]: selectReportMenuCss.statusCellFailed,
    [ModelStatuses.CREATED]: selectReportMenuCss.statusCellProcessing,
}


const TemplatesList = ({templatesList, deleteTemplate, loadUserTemplates}) => {
    useEffect(() => {
        loadUserTemplates();
    }, []);

    let {path, _} = useRouteMatch();

    const TemplateCell = ({name, id, deleteTemplate}) => {
        const onDeleteClick = () => {
            let userConfirm = window.confirm("Are you sure to delete this template?");
            if (userConfirm) {
                deleteTemplate(id);
            }
        }

        return (
            <tr>
                <td>{name}</td>
                <td className={modelsCss.controlsContainer}>
                    <span><AiFillEdit /></span>
                    <span onClick={onDeleteClick}><AiFillDelete /></span>
                </td>
            </tr>
        );
    };

    return (
        <>
            <div className={mainPageCss.container}>
                <div className={statisticsCss.statsContainer}>
                    <h2 className={commonStyles.pageTitle}>Your Visualization Templates</h2>

                    <div className={selectReportMenuCss.reportsListContainer}>
                        <table className={selectReportMenuCss.reportTable}>
                            <thead>
                            <tr className={modelsCss.filtersBlock}>
                                <th width={"500px"}>Name</th>
                                <th>
                                    <Link to={`${path}/create`}><span className={selectReportMenuCss.generateNewItemButton}>New Template</span></Link>
                                </th>
                            </tr>
                            </thead>
                            <tbody>
                            {
                                templatesList.map((model, index) =>
                                    <TemplateCell
                                        id={model.id}
                                        name={model.name}
                                        deleteTemplate={deleteTemplate}
                                        key={index}
                                    />
                                )
                            }
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </>
    );
};


let mapStateToProps = (state) => {
    return {
        templatesList: state.visualizationTemplatesReducer.templates,
    };
}
let mapDispatchToProps = (dispatch) => {
    return {
        loadUserTemplates: () => dispatch(loadUserTemplates()),
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(TemplatesList);