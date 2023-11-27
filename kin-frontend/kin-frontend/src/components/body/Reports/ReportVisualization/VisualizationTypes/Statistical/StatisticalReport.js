import React, {useState} from 'react';
import {connect} from "react-redux";
import {FaFileCsv} from "react-icons/fa";
import {VscJson} from "react-icons/vsc";

import visualizationCss from "../../ReportsVisualization.module.css"

import {STATISTICAL_REPORT, STATISTICS_SERVICE_URL} from "../../../../../../config";
import {downloadFile, transformLargeNumberToReadable} from "../../../../../../utils/utils";
import ChoseReportToCompare from "../../Comparison/ChoseReportToCompare";
import {showModalWindow} from "../../../../../../redux/reducers/modalWindowReducer";
import BackLink from "../../../../../../common/backLink/BackLink";
import {ReportBuilder} from "./Charts/ReportBuilder";


const StatisticalReport = ({showComparisonButton=true, report, ...props}) => {
    const [exportOptions, setExportOptions] = useState({activeExportOptions: false});
    const reportBuilder = new ReportBuilder(report);

    function renderExportOptions() {
        if(exportOptions.activeExportOptions) {
            return (
                <div
                    className={visualizationCss.exportOptions}
                >
                    <div
                        onClick={() => {
                            downloadFile(STATISTICS_SERVICE_URL + `/reports-data/${report.reportId}?export_type=csv`, 'csv')
                        }}
                    >
                       <FaFileCsv style={{marginRight: "5px"}}/> CSV
                    </div>
                    <div
                        onClick={() => {
                            downloadFile(STATISTICS_SERVICE_URL + `/reports-data/${report.reportId}?export_type=json`, 'json')
                        }}
                    >
                       <VscJson style={{marginRight: "5px"}} /> <span style={{fontSize: "15px"}}>JSON</span>
                    </div>
                </div>
            )
        }

        return <></>
    }

    return (
        <>
            <BackLink url={"/reports"} top={"120px"} left={"25px"}/>

            <div className={visualizationCss.visualizationContainer}>
                <div className={visualizationCss.header}>
                <span>
                    {report.name}
                    <div className={visualizationCss.totalMessagesCountLabel}>
                        [{transformLargeNumberToReadable(report.totalMessagesCount)} messages processed]
                    </div>
                </span>

                    <div className={visualizationCss.reportOptions}>
                        <div
                            className={visualizationCss.exportButton}
                            onMouseEnter={() => setExportOptions({activeExportOptions: true})}
                            onMouseLeave={() => setExportOptions({activeExportOptions: false})}
                            style={{marginLeft: "30px"}}
                        >
                            EXPORT
                            {renderExportOptions()}
                        </div>
                        {
                            showComparisonButton ?
                                <div
                                    className={visualizationCss.exportButton}
                                    onClick={() => {
                                        props.showModal(
                                            <ChoseReportToCompare
                                                reportType={STATISTICAL_REPORT}
                                                currentReportId={report.reportId}
                                            />,
                                            500,
                                            800,
                                        )
                                    }}
                                >
                                    COMPARE
                                </div>
                                :
                                <></>
                        }
                    </div>
                </div>

                <div className={visualizationCss.chartsContainer}>
                    {
                        reportBuilder
                        .generateChartRenderers()
                        .organizeChartsOrder()
                        .build()
                    }
                </div>
            </div>
        </>
    );
};


const mapDispatchToProps = (dispatch) => {
    return {
        showModal: (content, width, height) => dispatch(showModalWindow(content, width, height)),
    }
}

export default connect(() => new Object(), mapDispatchToProps)(StatisticalReport);
