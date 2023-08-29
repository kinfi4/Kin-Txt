import React from 'react';
import {ModelTypes} from "../../../../../config";
import InputBinariesForm from "./InsertBinariesForms/InputBinariesForm";

const InsertModelBinaries = ({
    modelType,
    onModelFileChange,
    onTokenizerFileChange,
    modelName=null,
    tokenizerName=null
}) => {
    if (modelType === ModelTypes.SKLEARN_MODEL) {
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

export default InsertModelBinaries;