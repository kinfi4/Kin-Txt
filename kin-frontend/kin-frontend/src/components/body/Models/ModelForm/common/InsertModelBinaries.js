import React from 'react';
import {ModelTypes} from "../../../../../config";
import SkLearnInputBinariesForm from "./InsertBinariesForms/SkLearnInputBinariesForm";

const InsertModelBinaries = ({
    modelType,
    onModelFileChange,
    onTokenizerFileChange,
    modelName=null,
    tokenizerName=null
}) => {
    if (modelType === ModelTypes.SKLEARN_MODEL) {
        return <SkLearnInputBinariesForm
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