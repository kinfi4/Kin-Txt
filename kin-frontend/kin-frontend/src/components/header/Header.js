import React from "react";
import {NavLink} from "react-router-dom";
import {logout} from "../../redux/reducers/authReducer";
import {connect} from "react-redux";
import logoImg from "../../images/image-logo.png";

import headerCss from "./Header.module.css";

function Header(props) {
    return (
        <>
            <header className={headerCss.header} id="header">
                <NavLink to={"/reports"}>
                    <div className={headerCss.logo}>
                        <img src={logoImg} alt="Logo" width={"90px"} />
                        Kin-TXT
                    </div>
                </NavLink>
                <nav>
                    <h3>
                        <NavLink to={"/reports"}>REPORTS</NavLink>
                    </h3>
                    <h3>
                        <NavLink to={"/models"}>MODELS</NavLink>
                    </h3>
                    <h3>
                        <NavLink to={"/templates"}>TEMPLATES</NavLink>
                    </h3>

                    <h3 onClick={(e) => props.logout()}>LOG OUT</h3>
                </nav>
            </header>
        </>
    );
}

let mapStateToProps = (state) => {
    return {};
};

let mapDispatchToProps = (dispatch) => {
    return {
        logout: () => dispatch(logout),
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(Header);
