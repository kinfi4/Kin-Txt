import React, {useState} from 'react';
import {connect} from "react-redux";
import {FaFileCsv} from "react-icons/fa";
import {VscJson} from "react-icons/vsc";

import visualizationCss from "../../ReportsVisualization.module.css"

import {STATISTICAL_REPORT, STATISTICS_SERVICE_URL} from "../../../../../../config";
import {downloadFile, transformLargeNumberToReadable} from "../../../../../../utils/utils";
import ChoseReportToCompare from "../../Comparison/ChoseReportToCompare";
import {showModalWindow} from "../../../../../../redux/reducers/modalWindowReducer";
import BackOnStatsPageLink from "../../../Common/BackOnStatsPageLink";
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
            <BackOnStatsPageLink top={"120px"} left={"25px"}/>

            <div className={visualizationCss.visualizationContainer}>
                <div className={visualizationCss.header}>
                <span>
                    {report.name}
                    <span
                        style={{
                            fontSize: "20px",
                            marginLeft: "20px",
                            color: "#7b6991",
                        }}
                    >
                        [{transformLargeNumberToReadable(report.totalMessagesCount)} messages processed]
                    </span>
                </span>

                    <div className={visualizationCss.reportOptions}>
                        <div
                            className={visualizationCss.exportButton}
                            onMouseEnter={() => setExportOptions({activeExportOptions: true})}
                            onMouseLeave={() => setExportOptions({activeExportOptions: false})}
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
                                                reportsIdentifiers={props.reportsIdentifiers}
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

let mapStateToProps = (state) => {
    return {
        reportsIdentifiers: state.reportsReducer.reports,
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        showModal: (content, width, height) => dispatch(showModalWindow(content, width, height)),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(StatisticalReport);














































// {
//     "reportId": 11,
//     "name": "Another Success",
//     "reportType": "Statistical",
//     "processingStatus": "Ready",
//     "generationDate": "09/08/2023 06:06",
//     "reportFailedReason": null,
//     "totalMessagesCount": 211,
//     "postsCategories": [
//     "Economical",
//     "Political",
//     "Shelling",
//     "Humanitarian"
// ],
//     "visualizationDiagramsList": [
//     "ByCategory__Pie",
//     "ByChannel__Pie",
//     "ByCategory__Bar",
//     "ByChannel__Bar",
//     "ByHour__Bar",
//     "ByDate__Line"
// ],
//     "data": {
//     "ByHour": {
//         "0": 1,
//             "1": 0,
//             "2": 0,
//             "3": 0,
//             "4": 3,
//             "5": 15,
//             "6": 12,
//             "7": 11,
//             "8": 11,
//             "9": 5,
//             "10": 9,
//             "11": 13,
//             "12": 12,
//             "13": 13,
//             "14": 8,
//             "15": 15,
//             "16": 22,
//             "17": 14,
//             "18": 10,
//             "19": 14,
//             "20": 9,
//             "21": 7,
//             "22": 4,
//             "23": 3
//     },
//     "ByCategory": {
//         "Economical": 2,
//             "Political": 146,
//             "Shelling": 49,
//             "Humanitarian": 14
//     },
//     "ByDate": {
//         "01/08/2023": 29,
//             "02/08/2023": 27,
//             "03/08/2023": 22,
//             "04/08/2023": 29,
//             "05/08/2023": 50,
//             "06/08/2023": 22,
//             "07/08/2023": 32
//     },
//     "ByChannel": {
//         "novinach": 211
//     }
// }
// }