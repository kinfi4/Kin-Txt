import React, {useEffect, useState} from "react";
import {connect} from "react-redux";
import commonStyles from "../../common/CommonStyles.module.css";
import selectReportMenuCss from "../Reports/SelectReport/SelectReportMenu.module.css";
import mainPageCss from "../MainPage.module.css";
import statisticsCss from "../Reports/Statistics.module.css";
import {Link, NavLink} from "react-router-dom";
import {useRouteMatch} from "react-router-dom/cjs/react-router-dom";
import modelsCss from "./styles/ModelsList.module.css";
import {AiFillDelete, AiFillEdit} from "react-icons/ai";
import {deleteModel, loadUserModels} from "../../../redux/reducers/modelsReducer";
import {ModelStatuses} from "../../../config";

let modelStatusToStatusClass = {
    [ModelStatuses.VALIDATED]: selectReportMenuCss.statusCellCompleted,
    [ModelStatuses.VALIDATING]: selectReportMenuCss.statusCellProcessing,
    [ModelStatuses.VALIDATION_FAILED]: selectReportMenuCss.statusCellFailed,
    [ModelStatuses.CREATED]: selectReportMenuCss.statusCellProcessing,
}


const ModelsList = ({modelsList, deleteModel, loadUserModels}) => {
    useEffect(() => {
        loadUserModels();
    }, []);


    let {path, _} = useRouteMatch();

    const ModelCell = ({name, id, status, deleteModel}) => {
        const onDeleteClick = () => {
            let userConfirm = window.confirm("Are you sure to delete this model?");
            if (userConfirm) {
                deleteModel(id);
            }
        }

        return (
            <tr>
                <td>
                    <Link className={modelsCss.modelLink} to={`${path}/edit/${id}`}>{name}</Link>
                </td>
                <td
                    className={`${selectReportMenuCss.statusCell} ${modelStatusToStatusClass[status]} ${selectReportMenuCss.reportRowCell}`}
                >
                    <div className={selectReportMenuCss.circle}></div> {status}
                </td>
                <td className={modelsCss.controlsContainer}>
                    <Link className={modelsCss.modelLink} to={`${path}/edit/${id}`}><AiFillEdit /></Link>
                    <span onClick={onDeleteClick}><AiFillDelete /></span>
                </td>
            </tr>
        );
    };

    return (
        <>
            <div className={mainPageCss.container}>
                <div className={statisticsCss.statsContainer}>
                    <h2 className={commonStyles.pageTitle}>Your Models</h2>

                    <div className={selectReportMenuCss.reportsListContainer}>
                        <table className={selectReportMenuCss.reportTable}>
                            <thead>
                                <tr className={modelsCss.filtersBlock}>
                                    <th width={"500px"}>Name</th>
                                    <th width={"250px"}>Status</th>
                                    <th>
                                        <Link to={`${path}/create`}><span className={selectReportMenuCss.generateNewItemButton}>Create New Model</span></Link>
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                {
                                    modelsList.map((model, index) =>
                                        <ModelCell
                                            id={model.id}
                                            name={model.name}
                                            status={model.modelStatus}
                                            deleteModel={deleteModel}
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
        modelsList: state.modelsReducer.models
    };
}
let mapDispatchToProps = (dispatch) => {
    return {
        loadUserModels: () => dispatch(loadUserModels()),
        deleteModel: (modelId) => dispatch(deleteModel(modelId))
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(ModelsList);