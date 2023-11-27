import React from 'react';
import {Link} from "react-router-dom";
import selectReportMenuCss from "../SelectReportMenu.module.css";
import {useRouteMatch} from "react-router-dom/cjs/react-router-dom";
import Input from "../../../../../common/input/Input";
import reportFiltersCss from "./ReportFilters.module.css";
import {updateFilters} from "../../../../../redux/reducers/reportsReducer";
import {connect} from "react-redux";

const ReportFilters = ({page, updateFilters, reportNameFilter, dateFromFilter, dateToFilter, statusFilter}) => {
    const onReportNameFilterChange = (event) => {
        const reportName = event.target.value;
        updateFilters(page, reportName, dateFromFilter, dateToFilter, statusFilter);
    }

    let {path, url} = useRouteMatch();
    
    return (
        <tr className={reportFiltersCss.filtersContainer}>
            <th width={"500px"}>
                <Input placeholder={"Report name"} onChange={onReportNameFilterChange} id={"reportNameFilter"} value={reportNameFilter} />
            </th>

            <th width={"95px"}>
                Status
            </th>

            <th width={"80px"}>
                Date
            </th>

            <th>
                <h2>
                    <Link to={`${path}/generate`}><span className={selectReportMenuCss.generateNewItemButton}>Generate New Report</span></Link>
                </h2>
            </th>
        </tr>
    );
};


const mapStateToProps = (state) => {
    return {
        page: state.reportsReducer.page,
        reportNameFilter: state.reportsReducer.reportsFilters.name,
        dateFromFilter: state.reportsReducer.reportsFilters.dateFrom,
        dateToFilter: state.reportsReducer.reportsFilters.dateTo,
        statusFilter: state.reportsReducer.reportsFilters.processingStatus,
    }
};
const mapDispatchToProps = (dispatch) => {
    return {
        updateFilters: (name, dateFrom, dateTo, status) => dispatch(updateFilters(name, dateFrom, dateTo, status))
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ReportFilters);
