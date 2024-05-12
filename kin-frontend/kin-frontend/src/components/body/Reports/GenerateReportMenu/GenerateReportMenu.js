import React, {useEffect, useState} from "react";
import {connect} from "react-redux";
import {DateRangePicker} from "react-date-range";
import Creatable from "react-select/creatable";

import statsCss from "../Statistics.module.css";
import mainPageCss from "../../MainPage.module.css";

import {
    hideModalWindow,
    showModalWindow,
} from "../../../../redux/reducers/modalWindowReducer";
import {generateReport} from "../../../../redux/reducers/reportsReducer";
import {
    ClassificationScopes,
    DatasourceTypes,
    STATISTICAL_REPORT,
    STATISTICS_SERVICE_URL,
    VisualizationPossibleModelTypes,
    WORD_CLOUD_REPORT,
} from "../../../../config";
import BackLink from "../../../../common/backLink/BackLink";
import {showMessage} from "../../../../utils/messages";
import InputModalWindow from "../../../../common/inputModalWindow/InputModalWindow";
import SelectTemplateModalWindow from "./ModalWindows/SelectTemplateModalWindow";
import {loadUserTemplates} from "../../../../redux/reducers/visualizationTemplates";
import {loadUserModels} from "../../../../redux/reducers/modelsReducer";
import {multiSelectStyles} from "./styles/formStyles";
import FormInput from "../../../../common/formInputName/FormInput";
import commonStyles from "../../../../common/CommonStyles.module.css";
import SelectItem from "../../../../common/select/SelectItem";
import {GenerationBlueprintController} from "./GenerationBlueprintController";
import {GenerateReportRequestValidator} from "../../../../domain/GenerateReportRequestValidator";

const ACTION_CREATE_OPTION = "create-option";
const ACTION_REMOVE_OPTION = "remove-value";
const initialGenerateReportState = {
    startDate: new Date(),
    endDate: new Date(),
    reportType: STATISTICAL_REPORT,
    channels: [],
    templateId: "",
    modelCode: "",
    name: "",
    datasourceType: DatasourceTypes.TELEGRAM,
    modelType: VisualizationPossibleModelTypes.SKLEARN_MODEL,
    classificationScope: ClassificationScopes.ENTIRE_POST,
};

const GenerateReportMenu = ({
    userModels,
    userTemplates,
    sendGenerationRequest,
    showModalWindow,
    hideModalWindow,
    loadUserModels,
    loadUserTemplates,
}) => {
    const [data, setData] = useState(initialGenerateReportState);
    const blueprintController = new GenerationBlueprintController(setData, null, hideModalWindow);

    useEffect(() => {
        loadUserTemplates();
        loadUserModels({modelStatus: "Validated"});
    }, []);

    const handleChannelsListChange = async (selectedOptions, action) => {
        if (action.action === ACTION_CREATE_OPTION) {
            await addNewChannel(action.option.value);
        } else if (action.action === ACTION_REMOVE_OPTION) {
            await removeChannelFromList(action.removedValue.value);
        }
    };
    const addNewChannel = async (channelLink) => {
        if (!channelLink) {
            showMessage([
                {
                    message: "Sorry, but you have to specify the link.",
                    type: "danger",
                },
            ]);
            return;
        }
        if (data.channels.includes(channelLink)) {
            showMessage([
                {
                    message:
                        "Sorry but the specified Channel already in the list",
                    type: "danger",
                },
            ]);
            return;
        }

        channelLink = channelLink.replace("https://t.me/", "");
        const newList = [...data.channels, channelLink];
        setData({...data, channels: newList});
    };
    const removeChannelFromList = async (channelLink) => {
        const newList = data.channels.filter((link) => link !== channelLink);
        setData({...data, channels: newList});
    };
    const onGenerateReport = async () => {
        const validator = new GenerateReportRequestValidator(data);

        const [isValid, messages] = validator.validate();
        if (!isValid) {
            showMessage(messages.map(message => {return {message, type: "danger"}}));
            return;
        }

        sendGenerationRequest(data);
        setData(initialGenerateReportState);
    }

    return (
        <>
            <BackLink url={"/reports"} />

            <h2 className={commonStyles.formPageTitle}>Generate Report</h2>

            <div
                className={statsCss.generateReportForm}
                style={{marginTop: "-50px"}}
            >
                <div className={statsCss.controls}>
                    <div className={statsCss.generateReportFormFieldContainer}>
                        <label
                            id="reportName"
                            className={statsCss.generateReportFormLabel}
                        >
                            Give your report a name:
                        </label>

                        <FormInput
                            placeholder={"Report name"}
                            id={"reportName"}
                            value={data.name}
                            onChange={(event) =>
                                setData({...data, name: event.target.value})
                            }
                            style={{width: "95%"}}
                        />
                    </div>

                    <DateRangePicker
                        rangeColors={["#2CA884"]}
                        ranges={[
                            {
                                startDate: data.startDate,
                                endDate: data.endDate,
                                key: "selection",
                            },
                        ]}
                        onChange={(range) =>
                            setData({
                                ...data,
                                startDate: range.selection.startDate,
                                endDate: range.selection.endDate,
                            })
                        }
                    />

                    {/*<div className={statsCss.generateReportFormFieldContainer}>*/}
                    {/*    <div className={statsCss.templateButtonsContainer}>*/}
                    {/*        <div*/}
                    {/*            onClick={() =>*/}
                    {/*                showModalWindow(*/}
                    {/*                    <InputModalWindow*/}
                    {/*                        actionCallback={(blueprintName => blueprintController.saveBlueprint(blueprintName, data))}*/}
                    {/*                        title={"NAME YOUR TEMPLATE"}*/}
                    {/*                        inputPlaceholder={"Template name"}*/}
                    {/*                        submitPlaceholder={"SAVE"}*/}
                    {/*                    />,*/}
                    {/*                    450,*/}
                    {/*                    300*/}
                    {/*                )*/}
                    {/*            }*/}
                    {/*        >*/}
                    {/*            SAVE AS BLUEPRINT*/}
                    {/*        </div>*/}
                    {/*        <div*/}
                    {/*            onClick={() =>*/}
                    {/*                showModalWindow(*/}
                    {/*                    <SelectTemplateModalWindow*/}
                    {/*                        setReportData={setData}*/}
                    {/*                    />,*/}
                    {/*                    450,*/}
                    {/*                    800*/}
                    {/*                )*/}
                    {/*            }*/}
                    {/*        >*/}
                    {/*            LOAD BLUEPRINT*/}
                    {/*        </div>*/}
                    {/*    </div>*/}
                    {/*</div>*/}
                </div>

                <div className={statsCss.controls}>
                    <div className={statsCss.generateReportFormFieldContainer}>
                        <label
                            id="reportType"
                            className={statsCss.generateReportFormLabel}
                        >
                            Report Type:
                        </label>

                        <SelectItem
                            name="reportType"
                            value={{
                                value: data.reportType,
                                label: data.reportType,
                            }}
                            onChange={(newValue) =>
                                setData({
                                    ...data,
                                    reportType: newValue.value,
                                    classificationScope: ClassificationScopes.ENTIRE_POST,
                                })
                            }
                            options={[
                                {
                                    value: STATISTICAL_REPORT,
                                    label: "Statistical report",
                                },
                                {value: WORD_CLOUD_REPORT, label: "Word cloud"},
                            ]}
                        />
                    </div>

                    <div className={statsCss.generateReportFormFieldContainer}>
                        <label
                            id="modelCode"
                            className={statsCss.generateReportFormLabel}
                        >
                            Model:
                        </label>

                        <SelectItem
                            name="modelCode"
                            value={{
                                value: data.modelCode,
                                label: userModels.find(
                                    (model) => model.code === data.modelCode
                                )?.name,
                            }}
                            onChange={(chosenValue) =>
                                setData({
                                    ...data,
                                    modelCode: chosenValue.value,
                                    modelType: userModels.find(
                                        (model) =>
                                            model.code === chosenValue.value
                                    )?.modelType,
                                })
                            }
                            options={[
                                ...userModels.map((model) => ({
                                    value: model.code,
                                    label: model.name,
                                })),
                            ]}
                        />
                    </div>

                    {
                        data.reportType === STATISTICAL_REPORT && (
                            <div className={statsCss.generateReportFormFieldContainer}
                            >
                                <label
                                    id="templateId"
                                    className={statsCss.generateReportFormLabel}
                                >
                                    Visualization template:
                                </label>

                                <SelectItem
                                    name="templateId"
                                    value={{
                                        value: data.templateId,
                                        label: userTemplates.find(
                                            (t) => t.id === data.templateId
                                        )?.name,
                                    }}
                                    onChange={(newValue) =>
                                        setData({
                                            ...data,
                                            templateId: newValue.value,
                                        })
                                    }
                                    options={[
                                        ...userTemplates.map((template) => ({
                                            value: template.id,
                                            label: template.name,
                                        })),
                                    ]}
                                />
                            </div>
                        )
                    }

                    {/*{*/}
                    {/*    data.reportType === WORD_CLOUD_REPORT && (*/}
                    {/*        <div className={statsCss.generateReportFormFieldContainer}*/}
                    {/*        >*/}
                    {/*            <label*/}
                    {/*                id="classificationScope"*/}
                    {/*                className={statsCss.generateReportFormLabel}*/}
                    {/*            >*/}
                    {/*                Classification scope:*/}
                    {/*            </label>*/}

                    {/*            <SelectItem*/}
                    {/*                name="classificationScope"*/}
                    {/*                value={{*/}
                    {/*                    value: data.classificationScope,*/}
                    {/*                    label: ClassificationScopes.getLabelFromValue(data.classificationScope),*/}
                    {/*                }}*/}
                    {/*                onChange={(selectedItem) =>*/}
                    {/*                    setData({*/}
                    {/*                        ...data,*/}
                    {/*                        classificationScope: selectedItem.value,*/}
                    {/*                    })*/}
                    {/*                }*/}
                    {/*                options={ClassificationScopes.getOptionsForSelect()}*/}
                    {/*            />*/}
                    {/*        </div>*/}

                    {/*    )*/}
                    {/*}*/}

                    {/*<div className={statsCss.generateReportFormFieldContainer}>*/}
                    {/*    <label*/}
                    {/*        id="datasource"*/}
                    {/*        className={statsCss.generateReportFormLabel}*/}
                    {/*    >*/}
                    {/*        Datasource:*/}
                    {/*    </label>*/}

                    {/*    <SelectItem*/}
                    {/*        name="datasource"*/}
                    {/*        value={{*/}
                    {/*            value: data.datasourceType,*/}
                    {/*            label: data.datasourceType,*/}
                    {/*        }}*/}
                    {/*        onChange={(newValue) =>*/}
                    {/*            setData({...data, datasourceType: newValue.value})*/}
                    {/*        }*/}
                    {/*        options={Object.entries(DatasourceTypes).map(*/}
                    {/*            (item) => ({value: item[1], label: item[1]}),*/}
                    {/*        )}*/}
                    {/*    />*/}
                    {/*</div>*/}

                    <div className={statsCss.generateReportFormFieldContainer}>
                        <label
                            id="channels"
                            className={statsCss.generateReportFormLabel}
                        >
                            Channel List:
                        </label>

                        <Creatable
                            isClearable
                            isMulti
                            placeholder={"Enter Channel links..."}
                            name="channels"
                            value={data.channels.map((el) => ({
                                value: el,
                                label: el,
                            }))}
                            components={{
                                DropdownIndicator: () => null,
                                IndicatorSeparator: () => null,
                                Menu: () => null,
                            }}
                            onChange={handleChannelsListChange}
                            styles={multiSelectStyles}
                        />
                    </div>

                    <div className={statsCss.generateReportsControlsContainer}>
                        <div
                            className={mainPageCss.controlButton}
                            onClick={onGenerateReport}
                            style={{
                                backgroundColor: "#2CA884",
                                fontSize: "22px",
                                width: "310px",
                            }}
                        >
                            GENERATE REPORT
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

const mapStateToProps = (state) => {
    return {
        userModels: state.modelsReducer.models,
        userTemplates: state.visualizationTemplatesReducer.templates,
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        sendGenerationRequest: (data) => dispatch(generateReport(data)),
        showModalWindow: (content, width, height) => dispatch(showModalWindow(content, width, height)),
        hideModalWindow: () => dispatch(hideModalWindow),
        loadUserModels: (modelFilters) => dispatch(loadUserModels(modelFilters)),
        loadUserTemplates: () => dispatch(loadUserTemplates()),
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(GenerateReportMenu);
