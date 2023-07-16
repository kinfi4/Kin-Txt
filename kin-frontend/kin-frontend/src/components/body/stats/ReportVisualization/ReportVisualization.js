import React, {useEffect} from 'react';
import {connect} from "react-redux";
import {REPORT_STATUS_POSTPONED, REPORT_STATUS_PROCESSING, WORD_CLOUD_REPORT} from "../../../../config";
import PostponedReport from "./PostponedReport";
import StatisticalReport from "./StatisticalReport";
import ProcessingReport from "./ProcessingReport";
import WordCloudReport from "./WordCloudReport";
import {removeCurrentReportFromState} from "../../../../redux/reducers/reportsReducer";
import LoadingSpinner from "../../../common/spiner/LoadingSpinner";
import BackOnStatsPageLink from "../Common/BackOnStatsPageLink";

const ReportVisualization = ({setCurrentReportNull, reportIsLoading, report}) => {
    useEffect(() => {
        return () => {
            setCurrentReportNull();
        }
    }, []);

    if(reportIsLoading === true) {
        return <LoadingSpinner width={100} height={100} marginTop={"15%"} />
    }

    if(report === null || report === undefined) {
        return (
            <div
                style={{color: "#f3f3f3", display: "flex", justifyContent: "center", alignItems: "center", fontSize: "30px"}}
            >
                <BackOnStatsPageLink />
                NO REPORT FOUND
            </div>
        )
    }

    if (report.processingStatus === REPORT_STATUS_POSTPONED) {
        return <PostponedReport report={report} />;
    }
    if (report.processingStatus === REPORT_STATUS_PROCESSING) {
        return <ProcessingReport report={report} />;
    }

    if (report.reportType === WORD_CLOUD_REPORT) {
        return <WordCloudReport report={report} />;
    }

    return <StatisticalReport report={report} />;
};

let mapStateToProps = (state) => {
    return {
        report: state.reportsReducer.detailedReport,
        reportIsLoading: state.reportsReducer.loading,
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        setCurrentReportNull: () => dispatch(removeCurrentReportFromState())
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(ReportVisualization);