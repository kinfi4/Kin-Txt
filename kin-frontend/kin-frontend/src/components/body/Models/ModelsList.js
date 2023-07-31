import React, {useEffect, useState} from "react";
import {connect} from "react-redux";
import commonStyles from "../../common/CommonStyles.module.css";
import selectReportMenuCss from "../Statistics/SelectReport/SelectReportMenu.module.css";
import mainPageCss from "../MainPage.module.css";
import statisticsCss from "../Statistics/Statistics.module.css";
import {Link} from "react-router-dom";
import {useRouteMatch} from "react-router-dom/cjs/react-router-dom";
import modelsCss from "./styles/ModelsList.module.css";
import {AiFillDelete, AiFillEdit} from "react-icons/ai";
import {deleteModel, loadUserModels} from "../../../redux/reducers/modelsReducer";


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
                <td>{name}</td>
                <td>{status}</td>
                <td>
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
                    <h2 className={commonStyles.pageTitle}>Your Models</h2>

                    <div className={selectReportMenuCss.reportsListContainer}>
                        <table className={selectReportMenuCss.reportTable}>
                            <thead>
                                <tr className={modelsCss.filtersBlock}>
                                    <th width={"500px"}>Name</th>
                                    <th width={"200px"}>Status</th>
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