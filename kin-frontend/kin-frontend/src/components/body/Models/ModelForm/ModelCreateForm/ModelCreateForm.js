import React from "react";
import formStyles from "../ModelFormStyles.module.css";
import statsStyles from "../../../Statistics/Statistics.module.css";
import commonStyles from "../../../../common/CommonStyles.module.css";
import Select from "react-select";
import {ModelTypes, STATISTICAL_REPORT, WORD_CLOUD_REPORT} from "../../../../../config";
import statsCss from "../../../Statistics/Statistics.module.css";
import InsertModelBinaries from "../common/InsertModelBinaries";
import FormInput from "../../../../common/formInputName/FormInput";

const ModelCreateForm = () => {
    const [data, setData] = React.useState({
        modelType: ModelTypes.SKLEARN_MODEL,
        modelFile: null,
        tokenizerFile: null,
        categoryMapping: {0: "First Category", 1: "Second Category"},
        name: "",
    });

    return (
        <div className={statsStyles.statsContainer}>
            <h2 className={commonStyles.pageTitle}>Create Model</h2>

            <div className={formStyles.modelFormContainer}>
                <div className={formStyles.blockOfForms}>
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
                                singleValue: (styles) => ({ ...styles, color: "#cecece" }),
                                option: (styles) => ({ ...styles, cursor: "pointer" }),
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
                    {/*Generate model button*/}
                    <div className={formStyles.formInputContainer}>
                        <div className={formStyles.createModelButton}>Create Model</div>
                    </div>
                </div>
                <div>
                    <div className={formStyles.formInputContainer}>
                        INPUT MAPPINGS
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ModelCreateForm;