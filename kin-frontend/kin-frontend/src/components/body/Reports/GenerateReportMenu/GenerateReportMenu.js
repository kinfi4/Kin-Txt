import React, {useEffect, useState} from "react";
import statsCss from "../Statistics.module.css";
import mainPageCss from "../../MainPage.module.css";
import {DateRangePicker} from "react-date-range";
import {connect} from "react-redux";
import {hideModalWindow, showModalWindow} from "../../../../redux/reducers/modalWindowReducer";
import {generateReport, setChannelsListForGeneration} from "../../../../redux/reducers/reportsReducer";
import {fetchChannels} from "../../../../redux/reducers/channelsReducer";
import {NEWS_SERVICE_URL, STATISTICAL_REPORT, STATISTICS_SERVICE_URL, WORD_CLOUD_REPORT} from "../../../../config";
import BackOnStatsPageLink from "../Common/BackOnStatsPageLink";
import Select from "react-select";
import {showMessage} from "../../../../utils/messages";
import axios from "axios";
import Creatable from 'react-select/creatable';
import InputModalWindow from "../../../common/inputModalWindow/InputModalWindow";
import SelectTemplateModalWindow from "./ModalWindows/SelectTemplateModalWindow";


const ACTION_CREATE_OPTION = "create-option";
const ACTION_REMOVE_OPTION = "remove-value";
const initialGenerateReportState = {
    startDate: new Date(),
    endDate: new Date(),
    reportType: STATISTICAL_REPORT,
}

const GenerateReportMenu = ({channels, initialChannels, setChannels, sendGenerationRequest, showModalWindow, hideModalWindow, ...props}) => {
    useEffect(() => {
        props.fetchChannels();
    }, []);
    useEffect(() => {
        setChannels(initialChannels.map(el => el.link));
    }, [initialChannels]);

    const [data, setData] = useState(initialGenerateReportState);

    const handleChannelsListChange = (selectedOptions, action) => {
        if(action.action === ACTION_CREATE_OPTION) {
            addNewChannel(action.option.value);
        } else if (action.action === ACTION_REMOVE_OPTION) {
            removeChannelFromList(action.removedValue.value);
        }
    }
    const addNewChannel = (channelLink) => {
        if(!channelLink) {
            showMessage([{message: "Sorry, but you have to specify the link.", type: "danger"}]);
            return;
        }
        if(channels.includes(channelLink)) {
            showMessage([{message: "Sorry but the specified Channel already in the list", type: "danger"}]);
            return;
        }

        const token = localStorage.getItem("token");
        axios.get(NEWS_SERVICE_URL + `/channels/exists/${channelLink}`, {
            headers: {
                'Authorization': `Token ${token}`,
            }
        }).then(res => {
            if(res.data.exists) {
                channelLink = channelLink.replace("https://t.me/", "");
                const newList = [...channels, channelLink];

                setChannels(newList);
            } else {
                showMessage([{message: "Channel with provided link does not exists!", type: "danger"}]);
            }
        })
    }
    const removeChannelFromList = (channelLink) => {
        const newList = channels.filter(link => link !== channelLink);
        setChannels(newList);
    }
    const saveTemplate = (templateName) => {
        if (!templateName) {
            showMessage([{message: "You have to specify the template name.", type: "danger"}]);
            return;
        }

        const token = localStorage.getItem("token");

        const postData = {
            name: templateName,
            reportType: data.reportType,
            channelList: channels,
            fromDate: data.startDate.toISOString(),
            toDate: data.endDate.toISOString(),
        };
        axios.post(STATISTICS_SERVICE_URL + "/templates", postData, {
            headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json',
            }
        }).then(res => {
            if(res.status === 201) {
                showMessage([{message: "Template has been saved successfully", type: "success"}]);
                hideModalWindow();
            } else {
                showMessage([{message: "Something went wrong during template saving.", type: "danger"}]);
            }
        }).catch(err => {
            showMessage([{message: "Something went wrong during template saving.", type: "danger"}]);
        })
    }
    const loadTemplate = (templateId) => {
        const token = localStorage.getItem("token");
        axios.get(STATISTICS_SERVICE_URL + `/templates/${templateId}`, {headers: {'Authorization': `Token ${token}`}})
        .then(res => {
            setData({
                startDate: new Date(res.data.fromDate),
                endDate: new Date(res.data.toDate),
                reportType: res.data.reportType,
            });

            setChannels(res.data.channelList);
        })
        .catch(err => {
            showMessage([{message: "Something went wrong during template loading.", type: "danger"}]);
        });
    }

    return (
        <>
            <BackOnStatsPageLink />

            <div className={statsCss.generateReportForm}>
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
                            styles={{
                                control: (styles) => ({
                                    ...styles,
                                    backgroundColor: "#1d2c3b",
                                    border: '1px solid #2CA884',
                                    '&:hover': {
                                        border: '1px solid #2CA884',
                                    },
                                    minWidth: "360px",
                                    maxWidth: "360px",
                                    cursor: "pointer"
                                }),
                                singleValue: (styles) => ({ ...styles, color: "#cecece" }),
                                option: (styles) => ({ ...styles, cursor: "pointer" }),
                            }}
                        />
                    </div>

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
                            defaultValue={initialChannels.map(el => ({value: el.link, label: el.link}))}
                            name="channels"
                            value={channels.map(el => ({value: el, label: el}))}
                            components={{ DropdownIndicator: () => null, IndicatorSeparator: () => null, Menu: () => null}}
                            onChange={handleChannelsListChange}
                            styles={{
                                control: (styles) => ({
                                    ...styles,
                                    cursor: "text",
                                    backgroundColor: "#1d2c3b",
                                    border: '1px solid #2CA884',
                                    '&:hover': {
                                        border: '1px solid #2CA884',
                                    },
                                    minHeight: '150px',
                                    maxHeight: "250px",
                                    minWidth: "360px",
                                    maxWidth: "360px",
                                }),
                                input: (styles) => ({ ...styles, color: "#cecece" }),
                                placeholder: (styles) => ({ ...styles, color: "#bdbdbd" }),
                                menu: (provided, state) => ({
                                    ...provided,
                                    width: 'fit-content',
                                    marginLeft: 0,
                                    marginTop: 0,
                                }),
                                multiValue: (base, state) => ({
                                    ...base,
                                    backgroundColor: '#64617E',
                                    color: 'white',
                                    borderRadius: '3px',
                                    padding: '5px',
                                }),
                                multiValueLabel: (base, state) => ({
                                    ...base,
                                    color: "#cecece",
                                    fontWeight: "bold",
                                }),
                                multiValueRemove: (base, state) => ({
                                    ...base,
                                    cursor: 'pointer',
                                }),
                            }}
                        />
                    </div>

                    <div className={statsCss.generateReportFormFieldContainer}>
                        <div className={statsCss.templateButtonsContainer}>
                            <div onClick={() => showModalWindow(
                                <InputModalWindow
                                    actionCallback={saveTemplate}
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
                                    choseTemplate={loadTemplate}
                                />,
                                450,
                                800,
                            )}>
                                LOAD BLUEPRINT
                            </div>
                        </div>
                    </div>

                    <div className={statsCss.generateReportsControlsContainer}>
                        <div
                            className={mainPageCss.controlButton}
                            onClick={() => {
                                sendGenerationRequest(data.startDate, data.endDate, channels, data.reportType);
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

let mapStateToProps = (state) => {
    return {
        initialChannels: state.channels.channels,
        channels: state.reportsReducer.channelListForGeneration,
    }
}
let mapDispatchToProps = (dispatch) => {
    return {
        sendGenerationRequest: (startDate, endDate, channels, reportType) => dispatch(generateReport(startDate, endDate, channels, reportType)),
        setChannels: (channels) => dispatch(setChannelsListForGeneration(channels)),
        fetchChannels: () => dispatch(fetchChannels()),
        showModalWindow: (content, width, height) => dispatch(showModalWindow(content, width, height)),
        hideModalWindow: () => dispatch(hideModalWindow),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(GenerateReportMenu);