import React from "react";

import BackLink from "../../../../../../common/backLink/BackLink";

import processingIcon from "../../../../../../images/processing-icon.png";


const NotReadyModelForm = () => {
    return (
        <>
            <BackLink url={"/models"} />
            <div
                style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "40px",
                    alignItems: "center",
                    justifyContent: "center",
                    color: "#edf2fc",
                    fontSize: "25px",
                    paddingTop: "250px"
                }}
            >
                <img
                    src={processingIcon}
                    alt="Processing Icon"
                    width={"250px"}
                />
                <h3>Your model is not ready yet...</h3>
            </div>
        </>
    );
};

export default NotReadyModelForm;