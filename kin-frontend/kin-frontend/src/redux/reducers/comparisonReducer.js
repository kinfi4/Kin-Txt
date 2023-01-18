import axios from "axios";
import {STATISTICS_SERVICE_URL} from "../../config";

const initialState = {
    firstReport: null,
    secondReport: null,
    reportsAreLoading: false,
}

const SET_COMPARISON_REPORTS = "SET_COMPARISON_REPORTS";
const SET_NULL_COMPARISON_REPORTS = "SET_NULL_COMPARISON_REPORTS";
const SET_LOADING_REPORTS = "SET_LOADING_REPORTS";


const fetchReport = (reportId) => {
    const token = localStorage.getItem("token");

    return axios.get(STATISTICS_SERVICE_URL + `/api/v1/reports/${reportId}`, {
        headers: {
            'Authorization': `Token ${token}`
        }
    }).then(response => response.data);
}


export const setComparisonReports = (firstReportId, secondReportId) => (dispatch) => {
    dispatch({type: SET_LOADING_REPORTS});

    const fetchFirstReportPromise = fetchReport(firstReportId);

    fetchFirstReportPromise.then(firstReportData => {
        const fetchSecondReportPromise = fetchReport(secondReportId);

        fetchSecondReportPromise.then(secondReportData => {
            dispatch({type: SET_COMPARISON_REPORTS, firstReport: firstReportData, secondReport: secondReportData});
        });
    });
}


export const setNullComparisonReports = () => (dispatch) => {
    dispatch({type: SET_NULL_COMPARISON_REPORTS});
}


export let comparisonReducer = (state=initialState, action) => {
    switch (action.type){
        case SET_LOADING_REPORTS:
            return {...state, reportsAreLoading: true}
        case SET_COMPARISON_REPORTS:
            return {firstReport: action.firstReport, secondReport: action.secondReport, reportsAreLoading: false};
        case SET_NULL_COMPARISON_REPORTS:
            return {firstReport: null, secondReport: null, reportsAreLoading: false};
        default:
            return state
    }
}
