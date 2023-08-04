import React from "react";
import styles from "./ValidationMessageStyles.module.css";
import {ModelStatuses} from "../../../../../../config";
import {IoMdDoneAll} from "react-icons/io";
import {MdSmsFailed} from "react-icons/md";

const validationResultToMessageMapping = {
    [ModelStatuses.VALIDATION_FAILED]: {
        styleClass: styles.validationFailed,
        text: "Model validation failed.",
        icon: <MdSmsFailed />
    },
    [ModelStatuses.VALIDATED]: {
        styleClass: styles.validationPassed,
        text: "Model validation passed.",
        icon: <IoMdDoneAll />
    }
}


const ModelValidationMessageBlock = ({validationStatus, validationMessage}) => {
    if(!validationStatus) {
        return <></>
    }
    
    const valResult = validationResultToMessageMapping[validationStatus];

    return (
        <div className={styles.validationResultsContainer}>
            <div className={`${styles.validationResult} ${valResult.styleClass}`}>
                {valResult.icon} {valResult.text}
            </div>
            {
                validationMessage ? <div><b>Details:</b> <i>{validationMessage}</i></div> : <></>
            }
        </div>
    );
};

export default ModelValidationMessageBlock;