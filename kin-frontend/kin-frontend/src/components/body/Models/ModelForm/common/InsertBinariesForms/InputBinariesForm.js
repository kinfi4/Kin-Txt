import React from "react";
import {ProgressBar} from "react-step-progress-bar";

import Spinner from "../FileLoadingSpinner/Spinner";

import "react-step-progress-bar/styles.css";
import styles from "../InsertModel.module.css";
import statsCss from "../../../../Reports/Statistics.module.css";

const InputBinariesForm = ({
    modelName,
    tokenizerName,
    onModelFileChange,
    onTokenizerFileChange,
    modelFileUploadProgress,
    tokenizerFileUploadProgress,
}) => {
    const modelIsSet = modelName !== null;
    const tokenizerIsSet = tokenizerName !== null;

    modelName = modelName ? modelName : "Choose a file with model";
    tokenizerName = tokenizerName
        ? tokenizerName
        : "Choose a file with tokenizer";

    const modelIsLoading = modelFileUploadProgress.progress > 0;
    const tokenizerIsLoading = tokenizerFileUploadProgress.progress > 0;

    let uploadingModelMessage = "Uploading the model";
    if (!modelFileUploadProgress.isValidating && modelFileUploadProgress.progress === 100) {
        uploadingModelMessage = "Model uploaded successfully";
    } else if (modelFileUploadProgress.isValidating) {
        uploadingModelMessage = "Validating files integrity";
    }

    let uploadingTokenizerMessage = "Uploading the tokenizer";
    if (
        !tokenizerFileUploadProgress.isValidating &&
        tokenizerFileUploadProgress.progress === 100
    ) {
        uploadingTokenizerMessage = "Tokenizer uploaded successfully";
    } else if (tokenizerFileUploadProgress.isValidating) {
        uploadingTokenizerMessage = "Validating files integrity";
    }

    const [loadingTheModelFileIntoBrowser, setLoadingModel] =
        React.useState(false);
    const [loadingTheFileIntoBrowser, setLoadingTokenizer] =
        React.useState(false);

    const handleFileChange = (fileHandler, setLoading) => async (event) => {
        setLoading(true);
        try {
            await fileHandler(event.target.files[0]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.inputFilesContainer}>
            <div className={styles.inputFileContainer}>
                <label id="file" className={statsCss.generateReportFormLabel}>
                    Model File:
                </label>
                <input
                    type="file"
                    id="file"
                    className={styles.fileInput}
                    onChange={handleFileChange(
                        onModelFileChange,
                        setLoadingModel
                    )}
                />
                <label
                    htmlFor="file"
                    className={`${styles.fileLabel} ${
                        modelIsSet ? styles.inputFileSelected : ""
                    }`}
                >
                    {loadingTheModelFileIntoBrowser ? (
                        <Spinner />
                    ) : modelIsLoading ? (
                        <>
                            <div
                                style={{
                                    display: "flex",
                                    justifyContent: "space-between",
                                    alignItems: "center",
                                    width: "100%",
                                }}
                            >
                                <span>{uploadingModelMessage}</span>
                                <Spinner />
                            </div>
                        </>
                    ) : (
                        modelName
                    )}
                </label>
                {modelIsLoading ? (
                    <div className={styles.animatedProgressBar}>
                        <ProgressBar
                            percent={modelFileUploadProgress.progress}
                            filledBackground="linear-gradient(to right, #00c6b6, #0f544b)"
                        />
                    </div>
                ) : (
                    <div style={{height: "10px"}}></div>
                )}
            </div>
            <div className={styles.inputFileContainer}>
                <label id="file" className={statsCss.generateReportFormLabel}>
                    Tokenizer File:
                </label>
                <input
                    type="file"
                    id="file"
                    className={styles.fileInput}
                    onChange={handleFileChange(
                        onTokenizerFileChange,
                        setLoadingTokenizer
                    )}
                />
                <label
                    htmlFor="file"
                    className={`${styles.fileLabel} ${
                        tokenizerIsSet ? styles.inputFileSelected : ""
                    }`}
                >
                    {loadingTheFileIntoBrowser ? (
                        <Spinner />
                    ) : tokenizerIsLoading ? (
                        <>
                            <div
                                style={{
                                    display: "flex",
                                    justifyContent: "space-between",
                                    alignItems: "center",
                                    width: "100%",
                                }}
                            >
                                <span>{uploadingTokenizerMessage}</span>
                                <Spinner />
                            </div>
                        </>
                    ) : (
                        tokenizerName
                    )}
                </label>
                {tokenizerIsLoading ? (
                    <div className={styles.animatedProgressBar}>
                        <ProgressBar
                            percent={tokenizerFileUploadProgress.progress}
                            filledBackground="linear-gradient(to right, #00c6b6, #0f544b)"
                        />
                    </div>
                ) : (
                    <div style={{height: "10px"}}></div>
                )}
            </div>
        </div>
    );
};

export default InputBinariesForm;
