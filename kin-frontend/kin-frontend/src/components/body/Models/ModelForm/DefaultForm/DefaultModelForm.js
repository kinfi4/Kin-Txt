import React, {useEffect} from "react";

import formStyles from "./../ModelFormStyles.module.css";
import statsStyles from "../../../Reports/Statistics.module.css";
import commonStyles from "../../../../../common/CommonStyles.module.css";
import statsCss from "../../../Reports/Statistics.module.css";

import {
    GENERIC_REPORTS_BUILDER_URL, ModelStatuses,
    ModelTypes,
    SupportedLanguages,
} from "../../../../../config";
import InsertModelFiles from "../common/InsertModelFiles";
import FormInput from "../../../../../common/formInputName/FormInput";
import MappingForm from "../common/MappingForm/MappingForm";
import ModelValidationMessageBlock from "./ModelValidationMessageBlock/ModelValidationMessageBlock";
import BackLink from "../../../../../common/backLink/BackLink";
import {ModelBinariesUploadService} from "../../../../../domain/uploadModelBinaries/ModelBinariesUploadService";
import {showMessage} from "../../../../../utils/messages";
import SettingsToggle from "./AdvancedSettings/SettingsToggle";
import AdvancedSettingsForm from "./AdvancedSettings/AdvancedSettingsForm";
import SelectItem from "../../../../../common/select/SelectItem";
import NotReadyModelForm from "./NotReadyModelForm/NotReadyModelForm";
import {ModelValidator} from "../../../../../domain/ModelValidator";

const DefaultModelForm = ({
    data,
    setData,
    onModelSavingCallback,
    isUpdateForm = false,
}) => {
    const [modelFileUploadProgress, setModelFileUploadProgress] =
        React.useState({progress: 0, isValidating: false});
    const [tokenizerFileUploadProgress, setTokenizerFileUploadProgress] =
        React.useState({progress: 0, isValidating: false});

    useEffect(() => {
        const handleBeforeUnload = (e) => {
            if (!data.preventPageReload) {
                return;
            }

            // Standard for most browsers
            e.preventDefault();
            // For some older browsers
            e.returnValue = "";
        };

        window.addEventListener("beforeunload", handleBeforeUnload);

        return () => {
            window.removeEventListener("beforeunload", handleBeforeUnload);
        };
    }, [data.preventPageReload]);

    // If the model is not ready, we show a different form
    if(data.modelStatus === ModelStatuses.CREATED || data.modelStatus === ModelStatuses.VALIDATING) {
        return <NotReadyModelForm />
    }

    let modelBlobName = null;
    if (data.modelFile) {
        modelBlobName = data.modelFile.name;
    } else if (data.modelName) {
        modelBlobName = data.modelName;
    }

    let tokenizerBlobName = null;
    if (data.tokenizerFile) {
        tokenizerBlobName = data.tokenizerFile.name;
    } else if (data.tokenizerName) {
        tokenizerBlobName = data.tokenizerName;
    }

    const blobsAreUploading = modelFileUploadProgress.progress > 0 || tokenizerFileUploadProgress.progress > 0;

    const handleModelValidationStart = async () => {
        if (blobsAreUploading) {
            return;
        }

        const modelValidator = new ModelValidator(data);
        const [isValid, errors] = modelValidator.validate(isUpdateForm);
        if(!isValid) {
            showMessage(errors.map((error) => ({message: error, type: "danger"})));
            return;
        }

        const binariesUploadService = new ModelBinariesUploadService(
            GENERIC_REPORTS_BUILDER_URL,
            1024 * 1024 * 5, // 5MB
            data.code // we need to pass the code of the future model as well, so the server knows where to save the files
        );

        await binariesUploadService.uploadModelData(
            data,
            setModelFileUploadProgress,
            setTokenizerFileUploadProgress,
        );

        onModelSavingCallback();
        setModelFileUploadProgress({progress: 0, isValidating: false});
        setTokenizerFileUploadProgress({progress: 0, isValidating: false});
    };

    return (
        <div className={statsStyles.statsContainer}>
            <BackLink url={"/models"} />

            <h2 className={commonStyles.formPageTitle}>
                {isUpdateForm ? "Update Model" : "Create Model"}
            </h2>

            <ModelValidationMessageBlock
                validationStatus={data.modelStatus}
                validationMessage={data.validationMessage}
            />

            <div className={formStyles.modelFormContainer}>
                <div className={formStyles.basicSettingsContainer}>
                    <div className={formStyles.blockOfForms} style={{width: "40%"}}>
                        {/*Select model type*/}
                        <div className={formStyles.formInputContainer}>
                            <label
                                id="modelType"
                                className={statsCss.generateReportFormLabel}
                            >
                                Model Type:
                            </label>

                            <SelectItem
                                defaultValue={{
                                    value: ModelTypes.SKLEARN_MODEL,
                                    label: ModelTypes.SKLEARN_MODEL,
                                }}
                                name="modelType"
                                value={{
                                    value: data.modelType,
                                    label: data.modelType,
                                }}
                                onChange={(newValue) =>
                                    setData({...data, modelType: newValue.value})
                                }
                                options={Object.entries(ModelTypes).map(
                                    ([key, value]) => ({value: value, label: value})
                                )}
                                width={"100%"}
                            />
                        </div>
                        {/*Input model*/}
                        <div className={formStyles.formInputContainer}>
                            <InsertModelFiles
                                modelType={data.modelType}
                                onModelFileChange={(file) =>
                                    setData({...data, modelFile: file})
                                }
                                onTokenizerFileChange={(file) =>
                                    setData({...data, tokenizerFile: file})
                                }
                                modelName={modelBlobName}
                                tokenizerName={tokenizerBlobName}
                                modelFileUploadProgress={modelFileUploadProgress}
                                tokenizerFileUploadProgress={tokenizerFileUploadProgress}
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
                                onChange={(event) =>
                                    setData({...data, name: event.target.value})
                                }
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
                                    onChange={(event) =>
                                        setData({...data, code: event.target.value})
                                    }
                                />
                            </div>
                        )}
                        {/*Generate model button*/}
                        <div className={formStyles.formInputContainer}>
                            <div
                                onClick={handleModelValidationStart}
                                className={formStyles.createModelButton}
                            >
                                Validate and Save
                            </div>
                        </div>
                    </div>
                    <div className={formStyles.blockOfForms} style={{width: "70%"}}>
                        <div className={formStyles.formInputContainer}>
                            <label
                                id="modelMappings"
                                className={statsCss.generateReportFormLabel}
                            >
                                Enter model mappings:
                            </label>

                            <MappingForm
                                data={data}
                                setData={setData}
                                id={"modelMappings"}
                            />
                        </div>
                        <div className={formStyles.formInputContainer}>
                            <label
                                id="language"
                                className={statsCss.generateReportFormLabel}
                            >
                                Select model language:
                            </label>

                            <SelectItem
                                defaultValue={{
                                    value: SupportedLanguages.ENGLISH.value,
                                    label: SupportedLanguages.ENGLISH.label,
                                }}
                                isSearchable={true}
                                name="language"
                                value={{
                                    value: data.preprocessingConfig.language.value,
                                    label: data.preprocessingConfig.language.label,
                                }}
                                onChange={(newValue) =>
                                    setData({
                                        ...data,
                                        preprocessingConfig: {
                                            ...data.preprocessingConfig,
                                            language: SupportedLanguages.getLanguageByValue(newValue.value)
                                        }
                                    })
                                }
                                options={
                                    Object.entries(SupportedLanguages)
                                        .filter(([key, element]) => element.value !== undefined)
                                        .map(
                                            ([key, lang]) =>
                                            ({value: lang.value, label: lang.label})
                                        )
                                }
                                width={"100%"}
                            />
                        </div>
                    </div>
                </div>
                <div className={formStyles.advancedSettingsContainer}>
                    <SettingsToggle settingsForm={<AdvancedSettingsForm settingsData={data} setData={setData} />} />
                </div>
            </div>
        </div>
    );
};

export default DefaultModelForm;
