import React from "react";

import notFound from "../../../images/not-found.png"

const ResourceNotFound = () => {
    return (
        <div
            style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                color: "white",
                flexDirection: "column",
                paddingTop: "250px",
            }}
        >
            <img
                src={notFound}
                alt="Not-Found"
                width="250px"
            />
            <h2>Sorry, seems like resource your are looking for does not exist.</h2>
        </div>
    );
};

export default ResourceNotFound;