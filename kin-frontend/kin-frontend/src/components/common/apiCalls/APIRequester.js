import axios from "axios";
import {LOGOUT} from "../../../redux/reducers/authReducer";


export default class APIRequester {
    constructor(url, dispatch=null) {
        this.url = url;
        this.dispatch = dispatch;
    }

    async get(path) {
        const token = localStorage.getItem("token");

        try {
            const response = await axios.get(this.url + path, {
                headers: {
                    Authorization: `Token ${token}`
                }
            });

            return response.data;
        } catch (error) {
            if (error.response.status === 401 && this.dispatch) {
                this.dispatch({ type: LOGOUT })
            }

            throw error;
        }
    }
}