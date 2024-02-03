import React, {useEffect} from "react";
import {connect} from "react-redux";
import commonStyles from "../../../common/CommonStyles.module.css";
import selectReportMenuCss from "../Reports/SelectReport/SelectReportMenu.module.css";
import mainPageCss from "../MainPage.module.css";
import statisticsCss from "../Reports/Statistics.module.css";
import {Link} from "react-router-dom";
import {useRouteMatch} from "react-router-dom/cjs/react-router-dom";
import modelsCss from "./styles/ModelsList.module.css";
import {AiFillDelete, AiFillEdit} from "react-icons/ai";
import {
    deleteModel,
    loadUserModels,
} from "../../../redux/reducers/modelsReducer";
import {
    ModelStatuses,
    ModelTypes,
    VisualizationPossibleModelTypes,
} from "../../../config";

let modelStatusToStatusClass = {
    [ModelStatuses.VALIDATED]: selectReportMenuCss.statusCellCompleted,
    [ModelStatuses.VALIDATING]: selectReportMenuCss.statusCellProcessing,
    [ModelStatuses.VALIDATION_FAILED]: selectReportMenuCss.statusCellFailed,
    [ModelStatuses.CREATED]: selectReportMenuCss.statusCellProcessing,
};

const ModelsList = ({modelsList, deleteModel, loadUserModels}) => {
    useEffect(() => {
        loadUserModels();
    }, []);

    let {path, _} = useRouteMatch();

    const ModelCell = ({name, code, status, modelType, deleteModel}) => {
        const onDeleteClick = () => {
            let userConfirm = window.confirm(
                "Are you sure to delete this model?"
            );
            if (userConfirm) {
                deleteModel(code);
            }
        };

        return (
            <tr>
                <td>
                    {modelType === VisualizationPossibleModelTypes.BUILTIN ? (
                        name
                    ) : (
                        <Link
                            className={modelsCss.modelLink}
                            to={`${path}/edit/${code}`}
                        >
                            {name}
                        </Link>
                    )}
                </td>
                <td
                    className={`${selectReportMenuCss.statusCell} ${modelStatusToStatusClass[status]} ${selectReportMenuCss.reportRowCell}`}
                >
                    <div className={selectReportMenuCss.circle}></div>
                    {status}
                </td>
                <td>
                    <b>{modelType}</b>
                </td>
                <td className={modelsCss.controlsContainer}>
                    {modelType === VisualizationPossibleModelTypes.BUILTIN ? (
                        ""
                    ) : (
                        <Link
                            className={modelsCss.modelLink}
                            to={`${path}/edit/${code}`}
                        >
                            <AiFillEdit />
                        </Link>
                    )}
                    <span onClick={onDeleteClick}>
                        <AiFillDelete />
                    </span>
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
                                    <th width={"320px"}>Name</th>
                                    <th width={"180px"}>Status</th>
                                    <th width={"200px"}>Model Type</th>
                                    <th>
                                        <Link to={`${path}/create`}>
                                            <span
                                                className={
                                                    selectReportMenuCss.generateNewItemButton
                                                }
                                            >
                                                Create New Model
                                            </span>
                                        </Link>
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                {modelsList.map((model, index) => (
                                    <ModelCell
                                        code={model.code}
                                        name={model.name}
                                        status={model.modelStatus}
                                        modelType={model.modelType}
                                        deleteModel={deleteModel}
                                        key={index}
                                    />
                                ))}
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
        modelsList: state.modelsReducer.models,
    };
};
let mapDispatchToProps = (dispatch) => {
    return {
        loadUserModels: () => dispatch(loadUserModels()),
        deleteModel: (modelId) => dispatch(deleteModel(modelId)),
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(ModelsList);
