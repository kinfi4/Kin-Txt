import axios from "axios";
import {NEWS_SERVICE_URL, REPORT_STATUS_POSTPONED, STATISTICS_SERVICE_URL} from "../../config";
import {FETCH_ERROR} from "./channelsReducer";
import {showMessage} from "../../utils/messages";
import {translateDateToString} from "../../utils/utils";
import APIRequester from "../../components/common/apiCalls/APIRequester";
import {hideModalWindow} from "./modalWindowReducer";


const reportsFilters = {
    page: 0,
    name: "",
    dateFrom: null,
    dateTo: null,
    processingStatus: null,
};
const initialState = {
    reports: [],
    totalPages: 1,
    loading: false,
    reportsFilters: reportsFilters,
};

const REPORTS_LOADED = "REPORTS_LOADED";
const REPORTS_LOADING = "REPORTS_LOADING";
const REPORTS_STOP_LOADING = "REPORTS_STOP_LOADING";
const UPDATE_FILTERS = "UPDATE_FILTERS";
const UPDATE_REPORTS_PAGE = "UPDATE_REPORTS_PAGE";


const reportFiltersToQueryParams = (filters) => {
    if(!filters) {
        return "";
    }

    let queryParams = "";

    if (filters.name) {
        queryParams += `&name=${filters.name}`;
    }
    if (filters.dateFrom) {
        queryParams += `&dateFrom=${filters.dateFrom}`;
    }
    if (filters.dateTo) {
        queryParams += `&dateTo=${filters.dateTo}`;
    }
    if (filters.processingStatus) {
        queryParams += `&processingStatus=${filters.processingStatus}`;
    }
    if (filters.page) {
        queryParams += `&page=${filters.page}`;
    }

    return queryParams;
}


export const updateFilters = (page, name, dateFrom, dateTo, processingStatus) => (dispatch, getState) => {
    dispatch({type: UPDATE_FILTERS, page, name, dateFrom, dateTo, processingStatus});

    dispatch(fetchUserReports());
};

export const updateReportsPage = (page) => (dispatch, getState) => {
    dispatch({type: UPDATE_REPORTS_PAGE, page});
    dispatch(fetchUserReports());
}

export const fetchUserReports = () => async (dispatch, getState) => {
    const filters = getState().reportsReducer.reportsFilters;

    let queryParams = reportFiltersToQueryParams(filters);
    queryParams = queryParams ? `?${queryParams.substring(1)}` : "";

    const apiRequester = new APIRequester(STATISTICS_SERVICE_URL, dispatch, true);

    try {
        const response = await apiRequester.get(`/reports${queryParams}`);
        dispatch({type: REPORTS_LOADED, reports: response.data.data, totalPages: response.data.totalPages});
    } catch (error) {
        dispatch({type: REPORTS_STOP_LOADING})
    }
}

export const generateReport = (data) => async (dispatch) => {
    if(!data.channels.length) {
        showMessage([{message: "You didn't specify any channel!", type: "danger"}])
        return;
    }

    const startDateString = translateDateToString(data.startDate);
    const endDateString = translateDateToString(data.endDate);

    console.log(`Sending generate report request for dates: ${startDateString} : ${endDateString}`)

    const body = {
        ...data,
        startDate: startDateString,
        endDate: endDateString,
    }

    const apiRequester = new APIRequester(STATISTICS_SERVICE_URL, dispatch);

    const response = await apiRequester.post(`/reports`, body);

    if(response) {
        showMessage([{message: "Report generation started!", type: "success"}])
    }
}

export const updateReportName = (reportId, reportName) => async (dispatch) => {
    const apiRequester = new APIRequester(STATISTICS_SERVICE_URL, dispatch);

    const response = await apiRequester.put(`/reports/${reportId}`, {name: reportName});

    if(response) {
        showMessage([{message: "Report renamed", type: "success"}])
        dispatch(hideModalWindow);
        dispatch(fetchUserReports());
    }
}

export const deleteReport = (reportId) => async (dispatch) => {
    const apiRequester = new APIRequester(STATISTICS_SERVICE_URL, dispatch);
    const response = await apiRequester.delete(`/reports/${reportId}`);

    if (response) {
        showMessage([{message: "Report deleted!", type: "success"}])
        dispatch(fetchUserReports());
    }
}
export const startLoading = () => (dispatch) => {
    dispatch({type: REPORTS_LOADING})
}

export const stopLoading = () => (dispatch) => {
    dispatch({type: REPORTS_STOP_LOADING})
}


export let reportsReducer = (state=initialState, action) => {
    switch (action.type){
        case REPORTS_LOADED:
            return {...state, reports: action.reports, totalPages: action.totalPages}
        case REPORTS_LOADING:
            return {...state, loading: true}
        case REPORTS_STOP_LOADING:
            return {...state, loading: false}
        case UPDATE_FILTERS:
            return {
                ...state,
                reportsFilters: {
                    ...state.reportsFilters,
                    page: action.page,
                    name: action.name,
                    dateFrom: action.dateFrom,
                    dateTo: action.dateTo,
                    processingStatus: action.processingStatus,
                }
            }
        case UPDATE_REPORTS_PAGE:
            return {
                ...state,
                reportsFilters: {
                    ...state.reportsFilters,
                    page: action.page,
                }
            }
        default:
            return state
    }
}
