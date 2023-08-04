import React from "react";
import statsCss from "../Statistics.module.css";
import {IoIosArrowRoundBack} from "react-icons/io"
import {Link} from "react-router-dom";

function BackOnStatsPageLink ({top = "120px", left = "20px"}) {
    return (
        <div className={statsCss.choseReportLink} style={{top: top, left: left}}>
            <Link to={`/statistics`}>
                <IoIosArrowRoundBack style={{marginRight: "5px", fontSize: "40px"}}/> <span style={{fontSize: "25px"}}>BACK</span>
            </Link>
        </div>
    );
}

export default BackOnStatsPageLink;
