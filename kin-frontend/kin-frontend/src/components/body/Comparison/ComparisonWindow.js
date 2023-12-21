import React, {useEffect} from "react";
import {connect} from "react-redux";
import comparisonCss from "./Comparison.module.css";
import StatisticalReport from "../Reports/ReportVisualization/VisualizationTypes/Statistical/StatisticalReport";
import {WORD_CLOUD_REPORT} from "../../../config";
import WordCloudReport from "../Reports/ReportVisualization/VisualizationTypes/WordCloud/WordCloudReport";
import {setNullComparisonReports} from "../../../redux/reducers/comparisonReducer";
import LoadingSpinner from "../../../common/spiner/LoadingSpinner";

const ComparisonWindow = ({
    firstReport,
    secondReport,
    reportsAreLoading,
    setNullComparisonReports,
}) => {
    useEffect(() => {
        return () => {
            setNullComparisonReports();
        };
    }, []);

    if (reportsAreLoading) {
        return (
            <div className={comparisonCss.comparisonContainer}>
                <div className={comparisonCss.comparisonBlock}>
                    <LoadingSpinner
                        width={100}
                        height={100}
                        marginTop={"30%"}
                    />
                </div>
                <div className={comparisonCss.comparisonBlock}>
                    <LoadingSpinner
                        width={100}
                        height={100}
                        marginTop={"30%"}
                    />
                </div>
            </div>
        );
    }

    if (firstReport === null || secondReport === null) {
        return (
            <div className={comparisonCss.comparisonContainer}>
                <div
                    className={comparisonCss.comparisonBlock}
                    style={{
                        color: "#fff",
                        paddingTop: "300px",
                        fontSize: "25px",
                    }}
                >
                    SORRY BUT COMPARISON REPORT NOT SELECTED
                </div>
                <div
                    className={comparisonCss.comparisonBlock}
                    style={{
                        color: "#fff",
                        paddingTop: "300px",
                        fontSize: "25px",
                    }}
                >
                    SORRY BUT COMPARISON REPORT NOT SELECTED
                </div>
            </div>
        );
    }

    if (firstReport.reportType === WORD_CLOUD_REPORT) {
        return (
            <div className={comparisonCss.comparisonContainer}>
                <div className={comparisonCss.comparisonBlock}>
                    <WordCloudReport
                        report={firstReport}
                        showComparisonButton={false}
                    />
                </div>
                <div className={comparisonCss.comparisonBlock}>
                    <WordCloudReport
                        report={secondReport}
                        showComparisonButton={false}
                    />
                </div>
            </div>
        );
    }

    return (
        <div className={comparisonCss.comparisonContainer}>
            <div className={comparisonCss.comparisonBlock}>
                <StatisticalReport
                    report={firstReport}
                    showComparisonButton={false}
                />
            </div>
            <div className={comparisonCss.comparisonBlock}>
                <StatisticalReport
                    report={secondReport}
                    showComparisonButton={false}
                />
            </div>
        </div>
    );
};

let mapStateToProps = (state) => {
    return {
        firstReport: state.comparisonReducer.firstReport,
        secondReport: state.comparisonReducer.secondReport,
        reportsAreLoading: state.comparisonReducer.reportsAreLoading,
    };
};

let mapDispatchToProps = (dispatch) => {
    return {
        setNullComparisonReports: () => dispatch(setNullComparisonReports()),
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(ComparisonWindow);
