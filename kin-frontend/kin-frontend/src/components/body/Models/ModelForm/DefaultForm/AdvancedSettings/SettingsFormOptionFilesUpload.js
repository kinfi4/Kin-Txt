import React from "react";
import styles from "./styles/SettingsOptionsStyles.module.css"
import inputFilesStyles from "../../common/InsertModel.module.css";


const SettingsFormOptionFilesUpload = ({data, setData, optionName, title, inputFileMessage, originalFileNameField=null}) => {
    const fileIsSet = data.preprocessingConfig[optionName] !== null;

    let inputLabelClassName = inputFilesStyles.fileLabel;
    if(fileIsSet) {
        inputLabelClassName = `${inputFilesStyles.fileLabel} ${inputFilesStyles.inputFileSelected}`;
    }

    let inputFileTitle = inputFileMessage;
    if(fileIsSet) {
        inputFileTitle = data.preprocessingConfig[optionName].name;
    } else if (data.preprocessingConfig[originalFileNameField]) {
        inputFileTitle = data.preprocessingConfig[originalFileNameField];
    }

    return (
        <div>
            <div className={styles.inputFileContainer}>
                <label className={styles.label}>
                    {title}
                </label>
                <label
                    id={optionName}
                    className={inputLabelClassName}
                >
                    {inputFileTitle}
                </label>
                <input
                    type="file"
                    id={optionName}
                    className={inputFilesStyles.fileInput}
                    style={{width: "100%"}}
                    onChange={(event) =>
                        setData({
                            ...data,
                            preprocessingConfig: {
                                ...data.preprocessingConfig,
                                [optionName]: event.target.files[0],
                            },
                        })
                    }
                />
            </div>
        </div>
    );
};

export default SettingsFormOptionFilesUpload;