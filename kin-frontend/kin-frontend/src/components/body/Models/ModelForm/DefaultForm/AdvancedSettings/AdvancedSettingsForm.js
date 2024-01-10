import React from "react";
import SettingsFormOptionCheckbox from "./SettingsFormOptionCheckbox";
import styles from "./styles/SettingsOptionsStyles.module.css"
import SettingsFormOptionFilesUpload from "./SettingsFormOptionFilesUpload";
import SettingsFormOptionSelect from "./SettingsFormOptionSelect";
import {PossibleTruncatePaddingTypes} from "../../../../../../config";
import {capitalizeFirstLetter} from "../../../../../../utils/utils";
import SettingsFormOptionNumber from "./SettingsFormOptionNumber";

const AdvancedSettingsForm = ({settingsData, setData}) => {
    return (
        <div>
            <div>
                <h3>Preprocessing settings</h3>
                <div className={styles.settingsContainer}>
                    <div>
                        <SettingsFormOptionCheckbox setData={setData} data={settingsData} optionName={"lowercase"} title={"Lowercase"}/>
                        <SettingsFormOptionCheckbox setData={setData} data={settingsData} optionName={"removeEmoji"} title={"Remove emoji"}/>
                        <SettingsFormOptionCheckbox setData={setData} data={settingsData} optionName={"removeExtraSpaces"} title={"Trim extra spaces"}/>
                        <SettingsFormOptionCheckbox setData={setData} data={settingsData} optionName={"removeHtmlTags"} title={"Remove HTML tags"}/>
                        <SettingsFormOptionCheckbox setData={setData} data={settingsData} optionName={"removeLinks"} title={"Remove hyperlinks"}/>
                        <SettingsFormOptionCheckbox setData={setData} data={settingsData} optionName={"removePunctuation"} title={"Remove punctuation"}/>
                        <SettingsFormOptionCheckbox setData={setData} data={settingsData} optionName={"lemmatize"} title={"Lemmatize text"} />
                    </div>
                    <div>
                        <SettingsFormOptionFilesUpload
                            data={settingsData}
                            setData={setData}
                            optionName={"stopWordsFile"}
                            title={"Set stop words"}
                            inputFileMessage={"Choose a csv, json, txt file with stop words"}
                            originalFileNameField={"stopWordsFileName"}
                        />
                        <SettingsFormOptionNumber
                            setData={setData}
                            data={settingsData}
                            optionName={"maxlen"}
                            title={"Set max length (optional)"}
                        />

                        {
                            settingsData.preprocessingConfig.maxlen &&
                            <>
                                <SettingsFormOptionSelect
                                    setData={setData}
                                    data={settingsData}
                                    optionName={"truncating"}
                                    title={"Truncating option"}
                                    options={PossibleTruncatePaddingTypes.getOptionsForSelect()}
                                    defaultValue={{
                                        value: PossibleTruncatePaddingTypes.Pre,
                                        label: capitalizeFirstLetter(PossibleTruncatePaddingTypes.Pre),
                                    }}
                                />
                                <SettingsFormOptionSelect
                                    setData={setData}
                                    data={settingsData}
                                    optionName={"padding"}
                                    title={"Padding option"}
                                    options={PossibleTruncatePaddingTypes.getOptionsForSelect()}
                                    defaultValue={{
                                        value: PossibleTruncatePaddingTypes.Pre,
                                        label: capitalizeFirstLetter(PossibleTruncatePaddingTypes.Pre),
                                    }}
                                />
                            </>
                        }
                    </div>
                </div>
            </div>


        </div>
    );
};

export default AdvancedSettingsForm;