import axios from "axios";
import {NEWS_SERVICE_URL, MS_IN_MINUTE} from "../../config";
import {FETCH_ERROR} from "./channelsReducer";

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

let initialState = {
    posts: [],
    loading: false,
    postsOffset: null,
    userHasPosts: true,
};

const POSTS_LOADED = "POSTS_LOADED";
const POSTS_LOADING = "POSTS_LOADING";
const POSTS_STOP_LOADING = "POSTS_STOP_LOADING";
const USER_HAS_NO_POSTS = "USER_HAS_NO_POSTS";


export let fetchNextPosts = () => (dispatch, getState) => {
    const token = localStorage.getItem("token");
    const alreadyLoading = getState().postsReducer.loading;

    if (alreadyLoading) {
        return;
    }

    let endTimeTimestamp = getState().postsReducer.postsOffset;
    if(!endTimeTimestamp) {
        endTimeTimestamp = Date.parse(new Date().toString());
    }

    let startTimeTimestamp = endTimeTimestamp - 60 * MS_IN_MINUTE

    let startTime = new Date(startTimeTimestamp);
    let endTime = new Date(endTimeTimestamp);
    console.log(`Getting data from ${startTime} to ${endTime}`)

    dispatch({type: POSTS_LOADING})

    axios.get(NEWS_SERVICE_URL + `/api/v1/messages?start_time=${startTimeTimestamp}&end_time=${endTimeTimestamp}`, {
        headers: {
            'Authorization': `Token ${token}`,
        }
    }).then(res => {
           dispatch({type: POSTS_LOADED, posts: res.data.messages, newOffset: startTimeTimestamp})
       }).catch(err => {
            if(err.response.status === 404) {  // that means user has no subscriptions
                dispatch({type: USER_HAS_NO_POSTS})
                return;
            }

            dispatch({type: FETCH_ERROR, errors: err.response.data.errors})
            dispatch({type: POSTS_STOP_LOADING})
       })
}


export let postsReducer = (state=initialState, action) => {
    switch (action.type){
        case POSTS_LOADED:
            return {loading: false, posts: state.posts.concat(action.posts), postsOffset: action.newOffset, userHasPosts: true}
        case POSTS_LOADING:
            return {...state, loading: true}
        case POSTS_STOP_LOADING:
            return {...state, loading: false}
        case USER_HAS_NO_POSTS:
            return {...state, userHasPosts: false}
        default:
            return state
    }
}
