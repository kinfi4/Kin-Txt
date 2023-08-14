import React from 'react';
import TapeCss from "../../../Tape/Tape.module.css";
import ComparisonCss from "./ChoseComparisonReport.module.css"
import {connect} from "react-redux";
import {setComparisonReports} from "../../../../../redux/reducers/comparisonReducer";
import {NavLink} from "react-router-dom";
import {hideModalWindow} from "../../../../../redux/reducers/modalWindowReducer";


const ChoseReport = ({reportsIdentifiers, reportType, currentReportId, setComparisonReports, hideModalWindow}) => {
    function onChoseReport (reportId) {
        hideModalWindow();
        setComparisonReports(currentReportId, reportId);
    }

    return (
        <div className={TapeCss.enterLinkContainer}>
            <h3 style={{textAlign: "center", marginBottom: "40px"}}>CHOSE REPORT TO COMPARE WITH</h3>
            <>
                {
                    reportsIdentifiers.map((reportIdentifier, idx) => {
                        if (reportIdentifier.reportId !== currentReportId && reportIdentifier.processingStatus === "Ready" && reportIdentifier.reportType === reportType) {
                            return (
                                <NavLink to={"/reports/compare"}>
                                    <div
                                        key={idx}
                                        className={`${ComparisonCss.comparisonReportBlock}`}
                                        onClick={() => onChoseReport(reportIdentifier.reportId)}
                                    >
                                        {reportIdentifier.name}
                                    </div>
                                </NavLink>
                            )
                        }
                    })
                }
            </>

        </div>
    );
};


let mapStateToProps = (state) => {
    return {}
}

let mapDispatchToProps = (dispatch) => {
    return {
        setComparisonReports: (firstReportId, secondReportId) => dispatch(setComparisonReports(firstReportId, secondReportId)),
        hideModalWindow: () => dispatch(hideModalWindow),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(ChoseReport);