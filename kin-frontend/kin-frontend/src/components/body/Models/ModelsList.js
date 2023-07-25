import React, {useEffect, useState} from "react";
import {connect} from "react-redux";
import axios from "axios";


const ModelsList = ({}) => {
    useEffect(() => {

    }, []);

    return (
        <div>
            <h2>Your Models</h2>
        </div>
    );
};


let mapStateToProps = (state) => {
    return {};
}
let mapDispatchToProps = (dispatch) => {
    return {};
}

export default connect(mapStateToProps, mapDispatchToProps)(ModelsList);