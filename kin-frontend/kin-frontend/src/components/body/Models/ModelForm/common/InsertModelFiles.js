import React from "react";

import {ModelTypes} from "../../../../../config";
import InputBinariesForm from "./InsertBinariesForms/InputBinariesForm";

const InsertModelFiles = ({
    modelType,
    onModelFileChange,
    onTokenizerFileChange,
    modelName=null,
    tokenizerName=null,
    modelFileUploadProgress,
    tokenizerFileUploadProgress,
    validatingUploadedModelFiles=false,
    validatingUploadedTokenizerFiles=false,
}) => {
    if (modelType === ModelTypes.SKLEARN_MODEL || modelType === ModelTypes.KERAS) {
        return <InputBinariesForm
            modelName={modelName}
            tokenizerName={tokenizerName}
            onModelFileChange={onModelFileChange}
            onTokenizerFileChange={onTokenizerFileChange}
            modelFileUploadProgress={modelFileUploadProgress}
            tokenizerFileUploadProgress={tokenizerFileUploadProgress}
            validatingUploadedModelFiles={validatingUploadedModelFiles}
            validatingUploadedTokenizerFiles={validatingUploadedTokenizerFiles}
        />
    }

    return (
        <div>

        </div>
    );
};

export default InsertModelFiles;