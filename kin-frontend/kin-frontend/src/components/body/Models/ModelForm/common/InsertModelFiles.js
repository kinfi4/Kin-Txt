import React from "react";

import {ModelTypes} from "../../../../../config";
import InputBinariesForm from "./InsertBinariesForms/InputBinariesForm";

const InsertModelFiles = ({
    modelType,
    onModelFileChange,
    onTokenizerFileChange,
    modelName=null,
    tokenizerName=null
}) => {
    if (modelType === ModelTypes.SKLEARN_MODEL || modelType === ModelTypes.KERAS) {
        return <InputBinariesForm
            modelName={modelName}
            tokenizerName={tokenizerName}
            onModelFileChange={onModelFileChange}
            onTokenizerFileChange={onTokenizerFileChange}
        />
    }

    return (
        <div>

        </div>
    );
};

export default InsertModelFiles;