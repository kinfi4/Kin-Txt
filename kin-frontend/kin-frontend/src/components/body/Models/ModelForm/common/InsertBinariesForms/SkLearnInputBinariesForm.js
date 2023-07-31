import React from 'react';
import styles from "../InsertModel.module.css";
import statsCss from "../../../../Statistics/Statistics.module.css";

const SkLearnInputBinariesForm = ({modelName, tokenizerName, onModelFileChange, onTokenizerFileChange}) => {
    modelName = modelName ? modelName : "Choose a file with scikit-learn model";
    tokenizerName = tokenizerName ? tokenizerName : "Choose a file with scikit-learn tokenizer";

    return (
        <div className={styles.inputFilesContainer} >
            <div className={styles.inputFileContainer}>
                <label
                    id="file"
                    className={statsCss.generateReportFormLabel}
                >
                    Model File:
                </label>
                <input type="file" id="file" className={styles.fileInput} onChange={(event) => onModelFileChange(event.target.files[0])} />
                <label htmlFor="file" className={styles.fileLabel}>{modelName}</label>
            </div>
            <div className={styles.inputFileContainer}>
                <label
                    id="file"
                    className={statsCss.generateReportFormLabel}
                >
                    Tokenizer File:
                </label>

                <input type="file" id="file" className={styles.fileInput} onChange={(event) => onTokenizerFileChange(event.target.files[0])} />
                <label htmlFor="file" className={styles.fileLabel}>{tokenizerName}</label>
            </div>
        </div>
    );
};

export default SkLearnInputBinariesForm;