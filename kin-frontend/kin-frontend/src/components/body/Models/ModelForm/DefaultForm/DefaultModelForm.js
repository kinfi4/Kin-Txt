import React from "react";
import Select from "react-select";

import formStyles from "./../ModelFormStyles.module.css";
import statsStyles from "../../../Reports/Statistics.module.css";
import commonStyles from "../../../../common/CommonStyles.module.css";
import statsCss from "../../../Reports/Statistics.module.css";

import {ModelTypes} from "../../../../../config";
import InsertModelBinaries from "../common/InsertModelBinaries";
import FormInput from "../../../../common/formInputName/FormInput";
import MappingForm from "../common/MappingForm/MappingForm";
import ModelValidationMessageBlock from "./ModelValidationMessageBlock/ModelValidationMessageBlock";
import {selectStyles} from "../../../Reports/GenerateReportMenu/styles/formStyles";
import BackLink from "../../../../common/backLink/BackLink";

const DefaultModelForm = ({data, setData, onModelSavingCallback, isUpdateForm=false}) => {
    return (
        <div className={statsStyles.statsContainer}>
            <BackLink url={"/models"} />

            <h2 className={commonStyles.pageTitle}>{isUpdateForm ? "Update Model" : "Create Model"}</h2>

            <ModelValidationMessageBlock
                validationStatus={data.modelStatus}
                validationMessage={data.validationMessage}
            />

            <div className={formStyles.modelFormContainer}>
                <div
                    className={formStyles.blockOfForms}
                    style={{width: "15%"}}
                >
                    {/*Select model type*/}
                    <div className={formStyles.formInputContainer}>
                        <label
                            id="modelType"
                            className={statsCss.generateReportFormLabel}
                        >
                            Model Type:
                        </label>

                        <Select
                            defaultValue={{value: ModelTypes.SKLEARN_MODEL, label: ModelTypes.SKLEARN_MODEL}}
                            isSearchable={true}
                            name="modelType"
                            value={{value: data.modelType, label: data.modelType}}
                            onChange={newValue => setData({...data, modelType: newValue.value})}
                            options={Object.entries(ModelTypes).map(([key, value]) => ({value: value, label: value}))}
                            styles={{
                                ...selectStyles,
                                control: (styles) => ({
                                    ...styles,
                                    backgroundColor: "#1d2c3b",
                                    border: '1px solid #2CA884',
                                    '&:hover': {
                                        border: '1px solid #2CA884',
                                    },
                                    width: "100%",
                                    cursor: "pointer"
                                }),
                            }}
                        />
                    </div>
                    {/*Input model*/}
                    <div className={formStyles.formInputContainer}>
                        <InsertModelBinaries
                            modelType={data.modelType}
                            onModelFileChange={(file) => setData({...data, modelFile: file})}
                            onTokenizerFileChange={(file) => setData({...data, tokenizerFile: file})}
                            modelName={data.modelFile ? data.modelFile.name : null}
                            tokenizerName={data.tokenizerFile ? data.tokenizerFile.name : null}
                        />
                    </div>
                    {/*Select model name*/}
                    <div className={formStyles.formInputContainer}>
                        <label
                            id="modelName"
                            className={statsCss.generateReportFormLabel}
                        >
                            Give your model a name:
                        </label>

                        <FormInput
                            placeholder={"Model name"}
                            id={"modelName"}
                            value={data.name}
                            onChange={(event) => setData({...data, name: event.target.value})}
                        />
                    </div>
                    {!isUpdateForm && (
                        <div className={formStyles.formInputContainer}>
                            <label
                                id="modelName"
                                className={statsCss.generateReportFormLabel}
                            >
                                Enter the model code:
                            </label>

                            <FormInput
                                placeholder="Model code"
                                id="modelCode"
                                value={data.code}
                                onChange={(event) => setData({...data, code: event.target.value})}
                            />
                        </div>
                    )}
                    {/*Generate model button*/}
                    <div className={formStyles.formInputContainer}>
                        <div
                            onClick={onModelSavingCallback}
                            className={formStyles.createModelButton}
                        >
                            Validate and Save
                        </div>
                    </div>
                </div>
                <div
                    className={formStyles.blockOfForms}
                    style={{width: "85%"}}
                >
                    <div className={formStyles.formInputContainer}>
                        <label
                            id="modelMappings"
                            className={statsCss.generateReportFormLabel}
                        >
                            Enter model mappings:
                        </label>

                        <MappingForm data={data} setData={setData} id={"modelMappings"} />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DefaultModelForm;