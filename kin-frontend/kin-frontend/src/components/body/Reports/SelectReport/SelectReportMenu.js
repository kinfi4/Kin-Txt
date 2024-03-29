import React, {useEffect} from "react";
import {connect} from "react-redux";

import selectReportMenuCss from "./SelectReportMenu.module.css";
import commonStyles from "../../../../common/CommonStyles.module.css";

import {
    deleteReport,
    fetchUserReports,
    updateReportName,
    updateReportsPage,
} from "../../../../redux/reducers/reportsReducer";
import {showModalWindow} from "../../../../redux/reducers/modalWindowReducer";
import ReportBlock from "./ReportRow/ReportBlock";
import ReportFilters from "./ReportFilters/ReportFilters";
import Pagination from "../../../../common/pagination/Pagination";

const SelectReportMenu = ({
    reportNames,
    fetchUserReports,
    currentPage,
    updatePage,
    totalPages,
    ...props
}) => {
    useEffect(() => {
        fetchUserReports();
    }, []);

    return (
        <>
            <h2 className={commonStyles.pageTitle}>Your Reports</h2>

            <div className={selectReportMenuCss.reportsListContainer}>
                <table className={selectReportMenuCss.reportTable}>
                    <thead>
                        <ReportFilters />
                    </thead>
                    <tbody>
                        {reportNames.map((el, idx) => (
                            <ReportBlock
                                name={el.name}
                                reportId={el.reportId}
                                reportStatus={el.processingStatus}
                                updateReportName={props.updateReportName}
                                deleteReport={props.deleteReport}
                                showModal={props.showModal}
                                reportProcessingDate={el.generationDate}
                                key={idx}
                            />
                        ))}
                    </tbody>
                </table>

                <Pagination
                    currentPageIndex={currentPage}
                    setPageIndex={updatePage}
                    totalPages={totalPages}
                />
            </div>
        </>
    );
};

let mapStateToProps = (state) => {
    return {
        currentPage: state.reportsReducer.reportsFilters.page,
        totalPages: state.reportsReducer.totalPages,
        reportNames: state.reportsReducer.reports,
    };
};
let mapDispatchToProps = (dispatch) => {
    return {
        updatePage: (page) => dispatch(updateReportsPage(page)),
        fetchUserReports: () => dispatch(fetchUserReports()),
        updateReportName: (reportId, reportName) => dispatch(updateReportName(reportId, reportName)),
        deleteReport: (reportId) => dispatch(deleteReport(reportId)),
        showModal: (content, width, height) => dispatch(showModalWindow(content, width, height)),
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(SelectReportMenu);
