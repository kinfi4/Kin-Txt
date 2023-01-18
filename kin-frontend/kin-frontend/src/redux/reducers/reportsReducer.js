import axios from "axios";
import {NEWS_SERVICE_URL, REPORT_STATUS_POSTPONED, STATISTICS_SERVICE_URL} from "../../config";
import {FETCH_ERROR} from "./channelsReducer";
import {showMessage} from "../../utils/messages";
import {translateDateToString} from "../../utils/utils";

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

let initialState = {
    reports: [],
    loading: false,
    detailedReport: null,
    channelListForGeneration: [],
}

const REPORTS_LOADED = "REPORTS_LOADED";
const REPORTS_LOADING = "REPORTS_LOADING";
const REPORTS_STOP_LOADING = "REPORTS_STOP_LOADING";
const REPORT_DETAILS_LOADED = "REPORT_DETAILS_LOADED";
const SET_CHANNELS = "SET_CHANNELS";
const SET_NULL_DETAILED_REPORT = "SET_NULL_DETAILED_REPORT";


export let fetchUserReports = () => (dispatch) => {
    const token = localStorage.getItem("token");

    axios.get(STATISTICS_SERVICE_URL + `/api/v1/reports`, {
        headers: {
            'Authorization': `Token ${token}`,
        }
    }).then(res => {
           dispatch({type: REPORTS_LOADED, reports: res.data.reports})
       }).catch(err => {
           dispatch({type: FETCH_ERROR, errors: err.response.data.errors})
           dispatch({type: REPORTS_STOP_LOADING})
       })
}

export let fetchReportDetails = (reportId) => (dispatch) => {
    const token = localStorage.getItem("token");

    dispatch({type: REPORTS_LOADING})

    axios.get(STATISTICS_SERVICE_URL + `/api/v1/reports/${reportId}`, {
        headers: {
            'Authorization': `Token ${token}`,
        }
    }).then(res => {
        dispatch({type: REPORT_DETAILS_LOADED, detailedReport: res.data})
    }).catch(err => {
        dispatch({type: FETCH_ERROR, errors: err.response.data.errors})
        dispatch({type: REPORTS_STOP_LOADING})
    })
}

export let generateReport = (startDate, endDate, channels, reportType) => (dispatch) => {
    if(!channels.length) {
        showMessage([{message: "You didn't specify any channel!", type: "danger"}])
        return;
    }

    const token = localStorage.getItem("token");

    const startDateString = translateDateToString(startDate);
    const endDateString = translateDateToString(endDate);

    console.log(`Sending generate report request for dates: ${startDateString} : ${endDateString}`)

    const body = {
        startDate: startDateString,
        endDate: endDateString,
        channels: channels,
        reportType: reportType,
    }

    axios.post(STATISTICS_SERVICE_URL + `/api/v1/reports`, body, {
        headers: {
            'Authorization': `Token ${token}`,
        }
    }).then(res => {
        showMessage([{message: 'Report generation started!', type: 'success'}])
    }).catch(err => {
        dispatch({type: FETCH_ERROR, errors: err.response.data.errors})
    })
}

export let updateReportName = (reportId, reportName) => (dispatch) => {
    const token = localStorage.getItem("token");
    const body = {name: reportName}

    axios.put(STATISTICS_SERVICE_URL + `/api/v1/reports/${reportId}`, body, {
        headers: {
            'Authorization': `Token ${token}`,
        }
    }).then(res => {
        window.location.replace('/statistics')
        showMessage([{message: 'Report renamed', type: 'success'}])
    }).catch(err => {
        dispatch({type: FETCH_ERROR, errors: err.response.data.errors})
    })

}

export let deleteReport = (reportId) => (dispatch) => {
    const token = localStorage.getItem("token");

    axios.delete(STATISTICS_SERVICE_URL + `/api/v1/reports/${reportId}`, {
        headers: {
            'Authorization': `Token ${token}`,
        }
    }).then(res => {
        window.location.replace('/statistics')
        showMessage([{message: 'Report deleted!', type: 'success'}])
    }).catch(err => {
        dispatch({type: FETCH_ERROR, errors: err.response.data.errors})
    })
}

export let setChannelsListForGeneration = (channels) => (dispatch) => {
    dispatch({type: SET_CHANNELS, channels: channels})
}

export let removeCurrentReportFromState = () => (dispatch) => {
    dispatch({type: SET_NULL_DETAILED_REPORT})
}


export let reportsReducer = (state=initialState, action) => {
    switch (action.type){
        case REPORT_DETAILS_LOADED:
            return {...state, detailedReport: action.detailedReport, loading: false}
        case SET_CHANNELS:
            return {...state, channelListForGeneration: action.channels}
        case REPORTS_LOADED:
            return {reports: action.reports}
        case REPORTS_LOADING:
            return {...state, loading: true}
        case REPORTS_STOP_LOADING:
            return {...state, loading: false}
        case SET_NULL_DETAILED_REPORT:
            return {...state, detailedReport: null, loading: false}
        default:
            return state
    }
}
