import axios from "axios";
import {LOGOUT} from "../../redux/reducers/authReducer";
import {FETCH_ERROR} from "../../redux/reducers/channelsReducer";


export default class APIRequester {
    constructor(url, dispatch=null, reRaiseErrors=false) {
        this.url = url;
        this.dispatch = dispatch;
        this.reRaiseErrors = reRaiseErrors;

        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
        axios.defaults.xsrfCookieName = "csrftoken";
    }

    async get(path, params=null) {
        try {
            let url = this.url + path;

            const urlParams = "?" + new URLSearchParams(params).toString();
            if(urlParams.length > 1) {
                url += urlParams;
            }

            return await axios.get(
                url,
                {headers: this._buildHeaders()},
            );
        } catch (error) {
            await this._handleErrors(error);
        }
    }

    async delete(path) {
        try {
            return await axios.delete(
                this.url + path,
                {headers: this._buildHeaders()},
            );
        } catch (error) {
            await this._handleErrors(error);
        }
    }

    async post(path, data, contentType="application/json") {
        try {
            return await axios.post(
                this.url + path,
                data,
                {headers: this._buildHeaders({"Content-Type": contentType})},
            );
        } catch (error) {
            await this._handleErrors(error);
        }
    }

    async put(path, data, contentType="application/json") {
        try {
            return await axios.put(
                this.url + path,
                data,
                {headers: this._buildHeaders({"Content-Type": contentType})},
            );
        } catch (error) {
            await this._handleErrors(error);
        }
    }

    async _handleErrors(error) {
        if (error.response.status === 401 && this.dispatch) {
            this.dispatch({ type: LOGOUT })
        } else if (this.dispatch) {
            this.dispatch({type: FETCH_ERROR, errors: error.response.data.errors})
        }

        if (this.reRaiseErrors) {
            throw error;
        }
    }

    _buildHeaders(additionalHeaders={}) {
        const token = localStorage.getItem("token");

        return {
            ...additionalHeaders,
            "Authorization": `Token ${token}`,
        };
    }
}