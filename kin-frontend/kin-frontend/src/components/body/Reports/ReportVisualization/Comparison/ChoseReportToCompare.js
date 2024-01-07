import React, {useEffect} from "react";
import {connect} from "react-redux";
import {NavLink} from "react-router-dom";

import TapeCss from "../../../Tape/Tape.module.css";
import ComparisonCss from "./ChoseComparisonReport.module.css";

import {setComparisonReports} from "../../../../../redux/reducers/comparisonReducer";
import {hideModalWindow} from "../../../../../redux/reducers/modalWindowReducer";
import {STATISTICS_SERVICE_URL} from "../../../../../config";
import APIRequester from "../../../../../common/apiCalls/APIRequester";

const ChoseReport = ({
    reportType,
    currentReportId,
    setComparisonReports,
    hideModalWindow,
}) => {
    const [reportsIdentifiers, setReports] = React.useState([]);

    useEffect(() => {
        const requestReports = async () => {
            const apiRequester = new APIRequester(STATISTICS_SERVICE_URL);
            const response = await apiRequester.get(
                `/reports?reportType=${reportType}&processingStatus=Ready`
            );
            return response.data.data;
        };

        requestReports().then((r) => setReports(r));
    }, []);

    function onChoseReport(reportId) {
        hideModalWindow();
        setComparisonReports(currentReportId, reportId);
    }

    return (
        <div className={TapeCss.enterLinkContainer}>
            <h3 style={{textAlign: "center", marginBottom: "40px"}}>
                CHOSE REPORT TO COMPARE WITH
            </h3>
            <>
                {reportsIdentifiers.map((reportIdentifier, idx) => {
                    if (reportIdentifier.reportId !== currentReportId) {
                        return (
                            <NavLink to={"/reports/compare"} key={idx}>
                                <div
                                    key={idx}
                                    className={`${ComparisonCss.comparisonReportBlock}`}
                                    onClick={() =>
                                        onChoseReport(reportIdentifier.reportId)
                                    }
                                >
                                    {reportIdentifier.name}
                                </div>
                            </NavLink>
                        );
                    }
                })}
            </>
        </div>
    );
};

const mapDispatchToProps = (dispatch) => {
    return {
        setComparisonReports: (firstReportId, secondReportId) =>
            dispatch(setComparisonReports(firstReportId, secondReportId)),
        hideModalWindow: () => dispatch(hideModalWindow),
    };
};

export default connect(() => new Object(), mapDispatchToProps)(ChoseReport);
