import React, {useEffect} from 'react';
import {connect} from "react-redux";

import selectReportMenuCss from "./SelectReportMenu.module.css"
import {
    deleteReport,
    fetchReportDetails,
    fetchUserReports,
    updateReportName
} from "../../../../redux/reducers/reportsReducer";
import {showModalWindow} from "../../../../redux/reducers/modalWindowReducer";
import ReportBlock from "./ReportRow/ReportBlock";
import ReportFilters from "./ReportFilters/ReportFilters";
import commonStyles from "../../../common/CommonStyles.module.css";


const SelectReportMenu = (props) => {
    useEffect(() => {
        props.fetchUserReports();
    }, []);

    const names = [
        {name: "Report 1", reportId: 1, processingStatus: "Processing", generationDate: "2021-05-05"},
        {name: "Report 2", reportId: 2, processingStatus: "Processing", generationDate: "2021-05-05"},
        {name: "Report 3", reportId: 3, processingStatus: "Ready", generationDate: "2021-05-05"},
        {name: "Report 4", reportId: 4, processingStatus: "Postponed", generationDate: "2021-05-05"},
    ]

    return (
        <>
            <h2 className={commonStyles.pageTitle}>Your Reports</h2>

            <div className={selectReportMenuCss.reportsListContainer}>

                <table className={selectReportMenuCss.reportTable}>
                    <thead>
                        <ReportFilters />
                    </thead>
                    <tbody>
                    {
                        names.map((el, idx) =>
                            <ReportBlock
                                name={el.name}
                                reportId={el.reportId}
                                reportStatus={el.processingStatus}
                                updateReportName={props.updateReportName}
                                deleteReport={props.deleteReport}
                                fetchReportDetails={props.fetchReportDetails}
                                showModal={props.showModal}
                                reportProcessingDate={el.generationDate}
                                key={idx}
                            />
                        )
                    }
                    </tbody>
                </table>
            </div>
        </>
    );
};

let mapStateToProps = (state) => {
    return {
        reportNames: state.reportsReducer.reports,
    }
}
let mapDispatchToProps = (dispatch) => {
    return {
        fetchUserReports: () => dispatch(fetchUserReports()),
        updateReportName: (reportId, reportName) => dispatch(updateReportName(reportId, reportName)),
        deleteReport: (reportId) => dispatch(deleteReport(reportId)),
        fetchReportDetails: (reportId) => dispatch(fetchReportDetails(reportId)),
        showModal: (content, width, height) => dispatch(showModalWindow(content, width, height)),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(SelectReportMenu);