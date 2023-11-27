import React from 'react';
import processingIcon from "../../../../../../images/processing-icon.png";
import BackLink from "../../../../../../common/backLink/BackLink";

const ProcessingReport = () => {
    return (
        <>
            <BackLink url={"/reports"} />
            <div
                style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "40px",
                    alignItems: "center",
                    justifyContent: "center",
                    color: "#edf2fc",
                    fontSize: "25px",
                    marginTop: "200px"
                }}
            >
                <img src={processingIcon} alt="Processing Icon" width={"250px"} />
                <h3>Your report is being processing!</h3>
            </div>
        </>
    );
};

export default ProcessingReport;