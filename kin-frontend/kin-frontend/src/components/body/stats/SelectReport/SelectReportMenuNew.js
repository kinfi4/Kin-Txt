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
        <div
            className={selectReportMenuCss.reportBlock}
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
                {props.name}
            </Link>
            <div className={selectReportMenuCss.reportControls}>
                <span onClick={onEditClick}><AiFillEdit /></span>
                <span onClick={onDeleteClick}><AiFillDelete /></span>
            </div>
        </div>
    )
}

const SelectReportMenu = (props) => {
    let {path, url} = useRouteMatch();
    useEffect(() => {
        props.fetchUserReports();
    }, []);

    return (
        <>
            <div className={selectReportMenuCss.reportsListContainer}>
                <div className={selectReportMenuCss.reportsFiltersContainer}>
                    <div className={selectReportMenuCss.reportsFiltersBlock}>
                        <div><input type="text"/></div>
                        <div>Status</div>
                        <div>Date</div>
                    </div>

                    <h2><Link to={`${path}/generate`}><span className={selectReportMenuCss.generateNewReportButton}>Generate new</span></Link></h2>
                </div>
                <div className={selectReportMenuCss.reportsList}>
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
                                key={idx}
                            />
                        )
                    }
                </div>
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