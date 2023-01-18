import axios from "axios";
import {NEWS_SERVICE_URL, MS_IN_MINUTE} from "../../config";
import {FETCH_ERROR} from "./channelsReducer";

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

let initialState = {
    myRate: null,
    averageRating: null,
    currentRating: 0,
    ratesCount: 0,
    loading: false,
}

const RATING_LOADED = "RATING_LOADED"
const START_LOADING_RATING = "START_LOADING_RATING"
const STOP_LOADING_RATING = "STOP_LOADING_RATING"
const CURRENT_MARK_CHANGED = "CURRENT_MARK_CHANGED"


export let fetchChannelRating = (channelLink) => (dispatch) => {
    const token = localStorage.getItem("token")

    dispatch({type: START_LOADING_RATING})
    axios.get(NEWS_SERVICE_URL + `/api/v1/channels/rates?channel=${channelLink}`, {
        headers: {
            'Authorization': `Token ${token}`,
        }
    }).then(res => {
            dispatch({
            type: RATING_LOADED,
            myRate: res.data.myRate,
            totalRates: res.data.totalRates,
            averageRating: res.data.averageRating,
            })
       }).catch(err => {
            dispatch({type: FETCH_ERROR, errors: err.response.data.errors})
            dispatch({type: STOP_LOADING_RATING})
       })
}

export let changeCurrentRating = (rating) => (dispatch) => {
    dispatch({type: CURRENT_MARK_CHANGED, rating: rating})
}

export let rateChannel = (channelLink, rate) => (dispatch) => {
    const token = localStorage.getItem("token")
    const body = {
        channelLink: channelLink,
        rating: rate,
    }

    dispatch({type: START_LOADING_RATING})

    axios.post(NEWS_SERVICE_URL + '/api/v1/channels/rates', body, {
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': `Token ${token}`,
        }
    }).then(res => {
        dispatch({
            type: RATING_LOADED,
            myRate: res.data.myRate,
            totalRates: res.data.totalRates,
            averageRating: res.data.averageRating,
        })
    }).catch(err => {
        dispatch({type: FETCH_ERROR, errors: err.response.data.errors})
        dispatch({type: STOP_LOADING_RATING})
    })
}


export let ratingReducer = (state=initialState, action) => {
    switch (action.type){
        case CURRENT_MARK_CHANGED:
            return {...state, currentRating: action.rating}
        case STOP_LOADING_RATING:
            return {...state, loading: false}
        case START_LOADING_RATING:
            return {...state, loading: true}
        case RATING_LOADED:
            return {
                loading: false,
                myRate: action.myRate,
                ratesCount: action.totalRates,
                averageRating: action.averageRating,
            }
        default:
            return state
    }
}
