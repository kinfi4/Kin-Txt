import React, {useEffect, useState} from "react";
import {connect} from "react-redux";
import {DateRangePicker} from "react-date-range";
import Creatable from 'react-select/creatable';
import Select from "react-select";

import statsCss from "../Statistics.module.css";
import mainPageCss from "../../MainPage.module.css";

import {hideModalWindow, showModalWindow} from "../../../../redux/reducers/modalWindowReducer";
import {generateReport} from "../../../../redux/reducers/reportsReducer";
import {
    NEWS_SERVICE_URL,
    STATISTICAL_REPORT,
    STATISTICS_SERVICE_URL,
    WORD_CLOUD_REPORT
} from "../../../../config";
import BackLink from "../../../common/backLink/BackLink";
import {showMessage} from "../../../../utils/messages";
import InputModalWindow from "../../../common/inputModalWindow/InputModalWindow";
import SelectTemplateModalWindow from "./ModalWindows/SelectTemplateModalWindow";
import {loadUserTemplates} from "../../../../redux/reducers/visualizationTemplates";
import {loadUserModels} from "../../../../redux/reducers/modelsReducer";
import APIRequester from "../../../common/apiCalls/APIRequester";
import {selectStyles, multiSelectStyles} from "./styles/formStyles";
import FormInput from "../../../common/formInputName/FormInput";


const ACTION_CREATE_OPTION = "create-option";
const ACTION_REMOVE_OPTION = "remove-value";
const initialGenerateReportState = {
    startDate: new Date(),
    endDate: new Date(),
    reportType: STATISTICAL_REPORT,
    channels: [],
    templateId: "",
    modelId: "",
    name: "",
}

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

    useEffect(() => {
        loadUserTemplates();
        loadUserModels();
    }, []);

    const handleChannelsListChange = async (selectedOptions, action) => {
        if(action.action === ACTION_CREATE_OPTION) {
            await addNewChannel(action.option.value);
        } else if (action.action === ACTION_REMOVE_OPTION) {
            await removeChannelFromList(action.removedValue.value);
        }
    }
    const addNewChannel = async (channelLink) => {
        if(!channelLink) {
            showMessage([{message: "Sorry, but you have to specify the link.", type: "danger"}]);
            return;
        }
        if(data.channels.includes(channelLink)) {
            showMessage([{message: "Sorry but the specified Channel already in the list", type: "danger"}]);
            return;
        }

        const apiRequester = new APIRequester(NEWS_SERVICE_URL);

        const response = await apiRequester.get(`/channels/exists/${channelLink}`);

        if(response.data.exists) {
            channelLink = channelLink.replace("https://t.me/", "");
            const newList = [...data.channels, channelLink];

            setData({...data, channels: newList});
        } else {
            showMessage([{message: "Channel with provided link does not exists!", type: "danger"}]);
        }
    }

    const removeChannelFromList = async (channelLink) => {
        const newList = data.channels.filter(link => link !== channelLink);
        setData({...data, channels: newList});
    }

    const saveBlueprint = async (blueprintName) => {
        if (!blueprintName) {
            showMessage([{message: "You have to specify the blueprint name.", type: "danger"}]);
            return;
        }

        const postData = {
            name: blueprintName,
            reportType: data.reportType,
            channelList: data.channels,
            fromDate: data.startDate.toISOString(),
            toDate: data.endDate.toISOString(),
            modelId: data.modelId,
            templateId: data.templateId,
            reportName: data.name,
        };

        const apiRequester = new APIRequester(STATISTICS_SERVICE_URL, null, true);

        try {
            const response = await apiRequester.post("/templates", postData)
            if (response.status === 201) {
                showMessage([{message: "Blueprint has been saved successfully", type: "success"}]);
                hideModalWindow();
            } else {
                showMessage([{message: "Something went wrong during blueprint saving.", type: "danger"}]);
            }
        } catch (error) {
            showMessage([{message: "Something went wrong during blueprint saving.", type: "danger"}]);
        }
    }
    const loadBlueprint = async (blueprintId) => {
        const apiRequester = new APIRequester(STATISTICS_SERVICE_URL);

        const response = await apiRequester.get(`/templates/${blueprintId}`);

        if(!response.data) {
            showMessage([{message: "Something went wrong during template loading.", type: "danger"}]);
            return;
        }

        setData({
            startDate: new Date(response.data.fromDate),
            endDate: new Date(response.data.toDate),
            reportType: response.data.reportType,
            channels: response.data.channelList,
            templateId: response.data.templateId,
            modelId: response.data.modelId,
            name: response.data.reportName,
        });
    }

    return (
        <>
            <BackLink url={"/reports"} />

            <div className={statsCss.generateReportForm}>
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
                            onChange={(event) => setData({...data, name: event.target.value})}
                            style={{width: "95%"}}
                        />
                    </div>

                    <DateRangePicker
                        rangeColors={["#2CA884"]}
                        ranges={[{
                            startDate: data.startDate,
                            endDate: data.endDate,
                            key: 'selection',
                        }]}
                        onChange={
                            (range) => setData({
                                ...data,
                                startDate: range.selection.startDate,
                                endDate: range.selection.endDate,
                            })
                        }
                    />

                    <div className={statsCss.generateReportFormFieldContainer}>
                        <div className={statsCss.templateButtonsContainer}>
                            <div onClick={() => showModalWindow(
                                <InputModalWindow
                                    actionCallback={saveBlueprint}
                                    title={"NAME YOUR TEMPLATE"}
                                    inputPlaceholder={"Template name"}
                                    submitPlaceholder={"SAVE"}
                                />,
                                450,
                                300,
                            )}>
                                SAVE AS BLUEPRINT
                            </div>
                            <div onClick={() => showModalWindow(
                                <SelectTemplateModalWindow
                                    choseTemplate={loadBlueprint}
                                />,
                                450,
                                800,
                            )}>
                                LOAD BLUEPRINT
                            </div>
                        </div>
                    </div>
                </div>

                <div className={statsCss.controls}>
                    <div className={statsCss.generateReportFormFieldContainer}>
                        <label
                            id="reportType"
                            className={statsCss.generateReportFormLabel}
                        >
                            Report Type:
                        </label>

                        <Select
                            defaultValue={{value: STATISTICAL_REPORT, label: "Statistical report"}}
                            isSearchable={true}
                            name="reportType"
                            value={{value: data.reportType, label: data.reportType}}
                            onChange={newValue => setData({...data, reportType: newValue.value})}
                            options={[
                                {value: STATISTICAL_REPORT, label: "Statistical report"},
                                {value: WORD_CLOUD_REPORT, label: "Word cloud"},
                            ]}
                            styles={selectStyles}
                        />
                    </div>

                    <div className={statsCss.generateReportFormFieldContainer}>
                        <label
                            id="modelId"
                            className={statsCss.generateReportFormLabel}
                        >
                            Model:
                        </label>

                        <Select
                            isSearchable={true}
                            name="modelId"
                            value={{value: data.modelId, label: userModels.find(model => model.id === data.modelId)?.name}}
                            onChange={newValue => setData({...data, modelId: newValue.value})}
                            options={[...userModels.map(model => ({value: model.id, label: model.name}))]}
                            styles={selectStyles}
                        />
                    </div>

                    {
                        data.reportType === STATISTICAL_REPORT &&
                        <div className={statsCss.generateReportFormFieldContainer}>
                            <label
                                id="templateId"
                                className={statsCss.generateReportFormLabel}
                            >
                                Visualization template:
                            </label>

                            <Select
                                isSearchable={true}
                                name="templateId"
                                value={{value: data.templateId, label: userTemplates.find(t => t.id === data.templateId)?.name}}
                                onChange={newValue => setData({...data, templateId: newValue.value})}
                                options={[...userTemplates.map(template => ({value: template.id, label: template.name}))]}
                                styles={selectStyles}
                            />
                        </div>
                    }

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
                            value={data.channels.map(el => ({value: el, label: el}))}
                            components={{ DropdownIndicator: () => null, IndicatorSeparator: () => null, Menu: () => null}}
                            onChange={handleChannelsListChange}
                            styles={multiSelectStyles}
                        />
                    </div>

                    <div className={statsCss.generateReportsControlsContainer}>
                        <div
                            className={mainPageCss.controlButton}
                            onClick={() => {
                                sendGenerationRequest(data);
                                setData(initialGenerateReportState);
                            }}
                            style={{backgroundColor: "#2CA884", fontSize: "22px", width: "310px"}}
                        >
                            GENERATE REPORT
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}


const mapStateToProps = (state) => {
    return {
        userModels: state.modelsReducer.models,
        userTemplates: state.visualizationTemplatesReducer.templates,
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        sendGenerationRequest: (data) => dispatch(generateReport(data)),
        showModalWindow: (content, width, height) => dispatch(showModalWindow(content, width, height)),
        hideModalWindow: () => dispatch(hideModalWindow),
        loadUserModels: () => dispatch(loadUserModels()),
        loadUserTemplates: () => dispatch(loadUserTemplates()),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(GenerateReportMenu);