import React, {useEffect, useState} from 'react';
import {connect} from "react-redux";

import selectReportMenuCss from "./SelectReportMenu.module.css"
import {
    deleteReport,
    fetchReportDetails,
    fetchUserReports,
    updateReportName
} from "../../../../redux/reducers/reportsReducer";
import {Link} from "react-router-dom";
import {useRouteMatch} from "react-router-dom/cjs/react-router-dom";
import {AiFillDelete, AiFillEdit} from "react-icons/ai";
import {showModalWindow} from "../../../../redux/reducers/modalWindowReducer";
import TapeCss from "../../tape/Tape.module.css";
import Input from "../../../common/input/Input";
import Button from "../../../common/button/Button";
import {REPORT_STATUS_POSTPONED, REPORT_STATUS_PROCESSING} from "../../../../config";

const reportStatusToStatusClass = {
    "Processing": selectReportMenuCss.statusCellProcessing,
    "Postponed": selectReportMenuCss.statusCellFailed,
    "Ready": selectReportMenuCss.statusCellCompleted,
}


const EditReportModalWindow = (props) => {
    let [data, setData] = useState({reportName: props.reportName});

    return (
        <div className={TapeCss.enterLinkContainer}>
            <h2 style={{marginBottom: "40px"}}>ENTER NEW NAME</h2>
            <Input
                value={data.reportName}
                onChange={(event) => setData({reportName: event.target.value})}
                placeholder={"Report Name"}
            />

            <Button
                text={"Edit"}
                onClick={(event) => props.updateReportName(props.reportId, data.reportName)}
            />
        </div>
    );
}

const ReportBlock = (props) => {
    const onEditClick = () => {
        props.showModal(
            <EditReportModalWindow
                reportName={props.name}
                reportId={props.reportId}
                updateReportName={props.updateReportName}
            />,
            400,
            300,
        )
    }
    const onDeleteClick = () => {
        let userConfirm = window.confirm("Are you sure to delete this report?");
        if (userConfirm) {
            props.deleteReport(props.reportId)
        }
    }

    return (
        <tr className={selectReportMenuCss.reportRow}>
            <td>
                <Link
                    className={`
                    ${selectReportMenuCss.reportLink}
                    ${props.reportStatus === REPORT_STATUS_POSTPONED ? selectReportMenuCss.postponed : ""}
                    ${props.reportStatus === REPORT_STATUS_PROCESSING ? selectReportMenuCss.processing : ""}`
                    }
                    onClick={() => props.fetchReportDetails(props.reportId)}
                    to={"/statistics/view"}
                >
                    <span>{props.name}</span>
                </Link>
            </td>
            <td className={`${selectReportMenuCss.statusCell} ${reportStatusToStatusClass[props.reportStatus]}`}>
                <div className={selectReportMenuCss.circle}></div> {props.reportStatus}
            </td>
            <td>
                {props.reportProcessingDate}
            </td>
            <td>
                <div className={selectReportMenuCss.reportControls}>
                    <span onClick={onEditClick}><AiFillEdit /></span>
                    <span onClick={onDeleteClick}><AiFillDelete /></span>
                </div>
            </td>
        </tr>
    )
}

const SelectReportMenu = (props) => {
    console.log(props)
    let {path, url} = useRouteMatch();
    useEffect(() => {
        props.fetchUserReports();
    }, []);

    return (
        <>
            <div className={selectReportMenuCss.reportsListContainer}>
                <table className={selectReportMenuCss.reportTable}>
                    <thead>
                        <tr>
                            <th>Report Name</th>
                            <th>Status</th>
                            <th>Date</th>
                            <th><h2><Link to={`${path}/generate`}><span className={selectReportMenuCss.generateNewReportButton}>Generate new</span></Link></h2></th>
                        </tr>
                    </thead>
                    <tbody>
                    {
                        props.reportNames.map((el, idx) =>
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