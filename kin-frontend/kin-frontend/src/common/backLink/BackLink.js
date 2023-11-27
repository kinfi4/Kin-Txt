import React from "react";
import statsCss from "../../components/body/Reports/Statistics.module.css";
import {IoIosArrowRoundBack} from "react-icons/io"
import {Link} from "react-router-dom";

function BackLink ({url, top = "120px", left = "20px"}) {
    return (
        <div className={statsCss.choseReportLink} style={{top: top, left: left}}>
            <Link to={url}>
                <IoIosArrowRoundBack style={{marginRight: "5px", fontSize: "40px"}}/> <span style={{fontSize: "25px"}}>BACK</span>
            </Link>
        </div>
    );
}

export default BackLink;
