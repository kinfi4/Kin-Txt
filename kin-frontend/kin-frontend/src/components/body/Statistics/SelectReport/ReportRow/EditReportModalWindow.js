import React, {useState} from "react";
import TapeCss from "../../../Tape/Tape.module.css";
import Input from "../../../../common/input/Input";
import Button from "../../../../common/button/Button";

const EditReportModalWindow = (props) => {
    let [data, setData] = useState({reportName: props.reportName});

    return (
        <div className={TapeCss.enterLinkContainer}>
            <h2 style={{marginBottom: "40px"}}>ENTER NEW NAME</h2>
            <Input
                value={data.reportName}
                onChange={(event) => setData({reportName: event.target.value})}
                placeholder={"Report Name"}
            />

            <Button
                text={"Edit"}
                onClick={(event) => props.updateReportName(props.reportId, data.reportName)}
            />
        </div>
    );
}


export default EditReportModalWindow;