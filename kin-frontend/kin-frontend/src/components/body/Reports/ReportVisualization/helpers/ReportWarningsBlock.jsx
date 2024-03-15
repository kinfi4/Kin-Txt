import React from "react";

const ReportWarningsBlock = ({warningsList}) => {
    return (
        <div
            style={{
                display: warningsList.length === 0 ? "none" : "flex",

                justifyContent: "start",
                alignItems: "center",
                width: "100%",
                marginTop: "40px",
                borderRadius: "5px",
                border: "1px solid #d77916",
                padding: "10px 20px",
                color: "#e09636",
                fontSize: "18px",
            }}
        >
            <p>
                <b>Pay attention!</b> <br/>
                The report was generated with warnings:
                <ul>
                    {
                        warningsList.map((warning, index) => (
                            <li key={index}>{warning}</li>
                        ))
                    }
                </ul>
            </p>
        </div>
    );
};

export default ReportWarningsBlock;