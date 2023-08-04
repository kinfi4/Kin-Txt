import React from 'react';
import styles from "../InsertModel.module.css";
import statsCss from "../../../../Reports/Statistics.module.css";
import Spinner from "../FileLoadingSpinner/Spinner";
import {fi} from "date-fns/locale";

const SkLearnInputBinariesForm = ({modelName, tokenizerName, onModelFileChange, onTokenizerFileChange}) => {
    modelName = modelName ? modelName : "Choose a file with scikit-learn model";
    tokenizerName = tokenizerName ? tokenizerName : "Choose a file with scikit-learn tokenizer";

    const [loading, setLoading] = React.useState(false);

    const handleFileChange = (fileHandler) => async (event) => {
        setLoading(true);
        try {
            await fileHandler(event.target.files[0]);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className={styles.inputFilesContainer} >
            <div className={styles.inputFileContainer}>
                <label
                    id="file"
                    className={statsCss.generateReportFormLabel}
                >
                    Model File:
                </label>
                <input type="file" id="file" className={styles.fileInput} onChange={handleFileChange(onModelFileChange)} />
                <label htmlFor="file" className={styles.fileLabel}>
                    {loading ? <Spinner /> : modelName}
                </label>
            </div>
            <div className={styles.inputFileContainer}>
                <label
                    id="file"
                    className={statsCss.generateReportFormLabel}
                >
                    Tokenizer File:
                </label>

                <input type="file" id="file" className={styles.fileInput} onChange={handleFileChange(onTokenizerFileChange)} />
                <label htmlFor="file" className={styles.fileLabel}>
                    {loading ? <Spinner /> : tokenizerName}
                </label>
            </div>
        </div>
    );
};

export default SkLearnInputBinariesForm;