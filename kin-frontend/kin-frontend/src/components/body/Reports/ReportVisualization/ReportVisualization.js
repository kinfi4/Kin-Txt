import React, {useEffect} from 'react';
import {connect} from "react-redux";

import {
    REPORT_STATUS_POSTPONED,
    REPORT_STATUS_PROCESSING,
    STATISTICS_SERVICE_URL,
    WORD_CLOUD_REPORT
} from "../../../../config";
import PostponedReport from "./VisualizationTypes/Postponed/PostponedReport";
import StatisticalReport from "./VisualizationTypes/Statistical/StatisticalReport";
import ProcessingReport from "./VisualizationTypes/Prosessing/ProcessingReport";
import WordCloudReport from "./VisualizationTypes/WordCloud/WordCloudReport";
import LoadingSpinner from "../../../common/spiner/LoadingSpinner";
import BackLink from "../../../common/backLink/BackLink";
import {startLoading, stopLoading} from "../../../../redux/reducers/reportsReducer";
import APIRequester from "../../../common/apiCalls/APIRequester";
import {showMessage} from "../../../../utils/messages";

const ReportVisualization = ({reportId, reportIsLoading, startReportLoading, endReportLoading}) => {
    const [report, setReport] = React.useState(null);

    const loadReport = async () => {
        const apiRequester = new APIRequester(STATISTICS_SERVICE_URL);
        const response = await apiRequester.get(`/reports/${reportId}`);

        if(response.status === 404) {
            showMessage([{message: 'Report not found', type: 'danger'}]);
            return null;
        }

        if(response.status !== 200) {
            showMessage([{message: 'Error loading report', type: 'danger'}]);
            return null;
        }

        return response.data;
    }

    useEffect(() => {
        startReportLoading();

        loadReport().then((report) => {
            setReport(report);
            endReportLoading();
        });
    }, []);


    if(reportIsLoading === true) {
        return <LoadingSpinner width={100} height={100} marginTop={"15%"} />
    }

    if(report === null || report === undefined) {
        return (
            <div
                style={{color: "#f3f3f3", display: "flex", justifyContent: "center", alignItems: "center", fontSize: "30px"}}
            >
                <BackLink url={"/reports"} />
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
        reportIsLoading: state.reportsReducer.loading,
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        startReportLoading: () => dispatch(startLoading()),
        endReportLoading: () => dispatch(stopLoading()),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(ReportVisualization);