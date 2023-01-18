import Input from "../common/input/Input";
import {NavLink} from "react-router-dom";
import authCss from "./auth.module.css";
import {useState} from "react";
import {register} from "../../redux/reducers/authReducer";
import {connect} from "react-redux";
import Button from "../common/button/Button";


function Register(props) {
    const [details, setDetails] = useState({username: '', password1: '', password2: ''})
    let onRegisterSubmit = () => {
        props.register(details.username, details.password1, details.password2)
    }

    return (
        <>
            <div className={authCss.authContainer}>
                <div className={authCss.authForm}>
                    <h2>REGISTER</h2>

                    <Input
                        type={"text"}
                        onChange={(element) => setDetails({...details, username: element.target.value})}
                        value={details.username}
                        placeholder={"Username"}
                        id={"username"}
                    />
                    <Input
                        type={"password"}
                        onChange={(element) => setDetails({...details, password1: element.target.value})}
                        value={details.password1}
                        placeholder={"Password"}
                        id={"password"}
                    />
                    <Input
                        type={"password"}
                        onChange={(element) => setDetails({...details, password2: element.target.value})}
                        value={details.password2}
                        placeholder={"Repeat Password"}
                        id={"repeat-password"}
                    />

                    <Button
                        onClick={(event) => onRegisterSubmit()}
                        text={'Sign Up'}
                        styles={{
                            marginTop: "15px"
                        }}
                    />

                    <NavLink to={'/sign-in'} className={authCss.formLink}>Already have an account? <br/>Login</NavLink>
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
        register: (username, password1, password2) => dispatch(register(username, password1, password2))
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Register);