import axios from "axios";
import {NEWS_SERVICE_URL} from "../../config"
import {showMessage} from "../../utils/messages";
import {FETCH_ERROR} from "./channelsReducer";


axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

const AUTH_ERROR = 'AUTH_ERROR'
const LOGIN_SUCCESS = 'LOGIN_SUCCESS'
const LOGIN_FAIL = 'LOGIN_FAIL'
const REGISTRATION_ERROR = 'REGISTRATION_ERROR'

export const LOGOUT = 'LOGOUT'

const initialState = {
    token: localStorage.getItem('token'),
    isAuthenticated: null,
    user: null,
}

// CHECK THE TOKEN AND LOAD THE USER
export const loadUser = () => (dispatch, getState) => {
    const headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    const token = getState().auth.token;
    if(token){
        headers['Authorization'] = `Token ${token}`
    }

    axios.get(NEWS_SERVICE_URL + '/api/v1/me', {
        headers: headers
    }).then(res => {
        if(res.status !== 200) {
            dispatch({type: AUTH_ERROR})
        } else {
            dispatch({type: LOGIN_SUCCESS, token: token})
        }
    }).catch(
        er => {
            dispatch({type: AUTH_ERROR})
        }
    )
}

// LOGIN
export const login = (username, password) => (dispatch) => {
    const headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    // REQUEST BODY
    const body = JSON.stringify({
        username,
        password,
    })

    axios.post(NEWS_SERVICE_URL + '/api/v1/login', body, {
        headers: headers,
    }).then(res => {
        dispatch({ type: LOGIN_SUCCESS, token: res.data.token })
    }).catch(
        err => dispatch({type: LOGIN_FAIL})
    )
}

// LOGOUT
export const logout = (dispatch) => {
    dispatch({ type: LOGOUT })
}

// REGISTER
export const register = (username, password1, password2) => (dispatch) => {
    const body = {
        username,
        password: password1,
        passwordRepeated: password2
    }

    axios.post(NEWS_SERVICE_URL + '/api/v1/register', JSON.stringify(body), {
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(res => {
            dispatch({ type: LOGIN_SUCCESS, token: res.data.token })
      }).catch(err => {
          console.log(err.response.data.errors)
          dispatch({ type: REGISTRATION_ERROR, errors: err.response.data.errors })
      })
}


// REDUCER
export function auth (state=initialState, action){
    switch (action.type) {
        case LOGIN_SUCCESS:
            localStorage.setItem('token', action.token)
            if(window.location.pathname === '/sign-in' || window.location.pathname === '/sign-up') {
                window.location.replace('/')
            }

            return {
                ...state,
                token: action.token,
                isAuthenticated: true
            }
        case REGISTRATION_ERROR:
        case FETCH_ERROR:
            if(Array.isArray(action.errors)) {
                showMessage(action.errors.map((err) => {
                    return {message: err, type: 'danger'}
                }))
            } else {
                showMessage([{message: action.errors, type: 'danger'}])
            }

            return {
                isAuthenticated: false,
                token: null,
                user: null
            }
        case LOGIN_FAIL:
            showMessage([{message: 'Username or password is incorrect', type: 'danger'}])
            return {
                isAuthenticated: false,
                token: null,
                user: null
            }
        case AUTH_ERROR:
        case LOGOUT:
            localStorage.removeItem('token')
            if(window.location.pathname !== '/sign-in' && window.location.pathname !== '/sign-up') {
                window.location.replace('/sign-in')
            }

            return {
                ...state,
                token: null,
                user: null,
                isAuthenticated: false
            }
        default:
            return state
    }
}