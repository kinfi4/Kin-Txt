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
                border: "1px solid #dcc1a6",
                padding: "10px 20px",
                color: "#dcc1a6",
                fontSize: "18px",
            }}
        >
            <p
                style={{
                    fontWeight: "bold",
                }}
            >
                Pay attention! <br/>
                The report was generated with warnings :
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