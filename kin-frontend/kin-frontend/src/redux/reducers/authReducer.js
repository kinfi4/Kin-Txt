import {STATISTICS_SERVICE_URL} from "../../config";
import {showMessage} from "../../utils/messages";
import APIRequester from "../../domain/apiCalls/APIRequester";

const AUTH_ERROR = "AUTH_ERROR";
const LOGIN_SUCCESS = "LOGIN_SUCCESS";
const LOGIN_FAIL = "LOGIN_FAIL";
const REGISTRATION_ERROR = "REGISTRATION_ERROR";
export const FETCH_ERROR = "FETCH_ERROR";


export const LOGOUT = "LOGOUT";

const initialState = {
    token: localStorage.getItem("token"),
    isAuthenticated: null,
    user: null,
};


export const loadUser = () => async (dispatch, getState) => {
    const apiRequester = new APIRequester(STATISTICS_SERVICE_URL, null, true);

    try {
        const response = await apiRequester.get("/accounts/me");

        if (response.status !== 200) {
            dispatch({type: AUTH_ERROR});
        } else {
            dispatch({type: LOGIN_SUCCESS, token: getState().auth.token});
        }
    } catch (error) {
        dispatch({type: AUTH_ERROR});
    }
};

export const login = (username, password) => async (dispatch) => {
    const apiRequester = new APIRequester(STATISTICS_SERVICE_URL, null, true);

    const body = JSON.stringify({
        username,
        password,
    });

    try {
        const response = await apiRequester.post("/accounts/login", body);

        if (response.status !== 200) {
            dispatch({type: LOGIN_FAIL});
        } else {
            dispatch({type: LOGIN_SUCCESS, token: response.data.token});
        }
    } catch (error) {
        dispatch({type: LOGIN_FAIL});
    }
};

export const logout = (dispatch) => {
    dispatch({type: LOGOUT});
};

export const register = (username, password1, password2) => async (dispatch) => {
    if (!username || !password1 || !password2) {
        dispatch({type: REGISTRATION_ERROR, errors: "Please, fill all fields"});
        return;
    }

    if (password1 !== password2) {
        dispatch({type: REGISTRATION_ERROR, errors: "Passwords don't match"});
        return;
    }

    const apiRequester = new APIRequester(STATISTICS_SERVICE_URL, null, true);

    const body = {
        username,
        password: password1,
        passwordRepeated: password2,
    };

    try {
        const response = await apiRequester.post("/accounts/register", body);
        dispatch({type: LOGIN_SUCCESS, token: response.data.token});
    } catch (error) {
        if (error.response.data.detail) {  // that's Pydantic errors
            dispatch({type: REGISTRATION_ERROR, errors: error.response.data.detail.map(err => err.msg)});
        } else if (error.response.data.errors) {
            dispatch({type: REGISTRATION_ERROR, errors: error.response.data.errors});
        } else {
            dispatch({type: REGISTRATION_ERROR, errors: "Something went wrong"});
        }
    }
};


export function auth(state = initialState, action) {
    switch (action.type) {
        case LOGIN_SUCCESS:
            localStorage.setItem("token", action.token);
            if (window.location.pathname === "/sign-in" || window.location.pathname === "/sign-up") {
                window.location.replace("/reports");
            }

            return {
                ...state,
                token: action.token,
                isAuthenticated: true,
            };
        case REGISTRATION_ERROR:
        case FETCH_ERROR:
            if (Array.isArray(action.errors)) {
                showMessage(
                    action.errors.map((err) => {
                        return {message: err, type: "danger"};
                    })
                );
            } else {
                showMessage([{message: action.errors, type: "danger"}]);
            }

            return {
                isAuthenticated: false,
                token: null,
                user: null,
            };
        case LOGIN_FAIL:
            showMessage([
                {message: "Username or password is incorrect", type: "danger"},
            ]);
            return {
                isAuthenticated: false,
                token: null,
                user: null,
            };
        case AUTH_ERROR:
        case LOGOUT:
            localStorage.removeItem("token");

            if (window.location.pathname !== "/sign-in" && window.location.pathname !== "/sign-up") {
                window.location.replace("/sign-in");
            }

            return {
                ...state,
                token: null,
                user: null,
                isAuthenticated: false,
            };
        default:
            return state;
    }
}
