import authCss from './auth.module.css'
import {connect} from "react-redux";
import {login} from "../../redux/reducers/authReducer";
import Input from "../common/input/Input";
import {useState} from "react";
import {NavLink} from "react-router-dom";
import Button from "../common/button/Button";

function Login(props) {
    const [details, setDetails] = useState({username: '', password: ''})
    let onLoginSubmit = () => {
        props.login(details.username, details.password)
    }

    return (
        <>
            <div className={authCss.authContainer}>
                <div className={authCss.authForm}>
                    <h2>LOGIN</h2>

                    <Input
                        type={"text"}
                        onChange={(element) => setDetails({...details, username: element.target.value})}
                        value={details.username}
                        placeholder={"Username"}
                        id={"username"}
                    />
                    <Input
                        type={"password"}
                        onChange={(element) => setDetails({...details, password: element.target.value})}
                        value={details.password}
                        placeholder={"Password"}
                        id={"password"}
                    />

                    <Button
                        onClick={(event) => onLoginSubmit()}
                        text={'Sign In'}
                        styles={{
                            marginTop: "15px"
                        }}
                    />

                    <NavLink to={'/sign-up'} className={authCss.formLink}>New to the Kin-News? <br/>Register</NavLink>
                </div>
            </div>
        </>
    );
}


let mapStateToProps = (state) => {
    return {}
}

let mapDispatchToProps = (dispatch) => {
    return {
        login: (username, password) => dispatch(login(username, password))
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(Login);
