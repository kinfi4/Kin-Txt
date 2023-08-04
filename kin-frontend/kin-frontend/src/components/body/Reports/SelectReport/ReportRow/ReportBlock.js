import selectReportMenuCss from "../SelectReportMenu.module.css";
import {Link} from "react-router-dom";
import {REPORT_STATUS_POSTPONED, REPORT_STATUS_PROCESSING} from "../../../../../config";
import {AiFillDelete, AiFillEdit} from "react-icons/ai";
import React from "react";
import EditReportModalWindow from "./EditReportModalWindow";

const reportStatusToStatusClass = {
    "Processing": selectReportMenuCss.statusCellProcessing,
    "Postponed": selectReportMenuCss.statusCellFailed,
    "Ready": selectReportMenuCss.statusCellCompleted,
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
        <tr>
            <td
                className={selectReportMenuCss.reportRowCell}
                width={"500px"}
            >
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
            <td
                className={`${selectReportMenuCss.statusCell} ${reportStatusToStatusClass[props.reportStatus]} ${selectReportMenuCss.reportRowCell}`}
                width={"95px"}
            >
                <div className={selectReportMenuCss.circle}></div> {props.reportStatus}
            </td>
            <td
                className={selectReportMenuCss.reportRowCell}
                width={"80px"}
            >
                {props.reportProcessingDate}
            </td>
            <td className={selectReportMenuCss.reportRowCell}>
                <div className={selectReportMenuCss.reportControls}>
                    <span onClick={onEditClick}><AiFillEdit /></span>
                    <span onClick={onDeleteClick}><AiFillDelete /></span>
                </div>
            </td>
        </tr>
    )
}


export default ReportBlock;