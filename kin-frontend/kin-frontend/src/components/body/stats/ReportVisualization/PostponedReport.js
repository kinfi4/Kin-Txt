import React from 'react';
import reportsVisualizationCss from "./ReportsVisualization.module.css"
import processingImageFailedIcon from "../../../../images/processing-failed.png"
import visualizationCss from "./ReportsVisualization.module.css";
import {
    deleteReport,
} from "../../../../redux/reducers/reportsReducer";
import {connect} from "react-redux";

const PostponedReport = (props) => {
    const onDeleteClick = () => {
        const userConfirm = window.confirm("Are you sure to delete this report?");
        if (userConfirm) {
            props.deleteReport(props.report.reportId);
        }
    }

    return (
        <div className={reportsVisualizationCss.postponedContainer}>
            <div className={visualizationCss.header}>
                <span>
                    {props.report.name}
                </span>

                <div
                    className={visualizationCss.exportButton}
                    style={{backgroundColor: "#dc4444"}}
                    onClick={() => onDeleteClick()}
                >
                    DELETE
                </div>
            </div>
            <div>
                <img src={processingImageFailedIcon} alt="Processing Failed"/>
                <div>
                    We are sorry for this! But your report processing failed with error: <br/> <br/>
                    {props.report.reportFailedReason}
                </div>
            </div>
        </div>
    );
};

let mapStateToProps = (state) => {
    return {}
}

let mapDispatchToProps = (dispatch) => {
    return {
        deleteReport: (reportId) => dispatch(deleteReport(reportId)),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(PostponedReport);