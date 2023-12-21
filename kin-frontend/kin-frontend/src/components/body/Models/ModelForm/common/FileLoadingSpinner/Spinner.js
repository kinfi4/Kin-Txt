import React from "react";
import spinnerStyles from "./SpinnerStyles.module.css";

const Spinner = () => {
    return (
        <div className={spinnerStyles.spinnerContainer}>
            <div className={spinnerStyles.firstBounce}></div>
            <div className={spinnerStyles.secondBounce}></div>
        </div>
    );
};

export default Spinner;
