import React, {useEffect, useState} from "react";
import statsCss from "../Statistics.module.css";
import mainPageCss from "../../MainPage.module.css";
import {DateRangePicker} from "react-date-range";
import {connect} from "react-redux";
import {Link} from "react-router-dom";
import {showModalWindow} from "../../../../redux/reducers/modalWindowReducer";
import SelectChannelsWindow from "./SelectChannels";
import {generateReport, setChannelsListForGeneration} from "../../../../redux/reducers/reportsReducer";
import {fetchChannels} from "../../../../redux/reducers/channelsReducer";
import {IoIosArrowRoundBack} from "react-icons/io"
import {STATISTICAL_REPORT, WORD_CLOUD_REPORT} from "../../../../config";


const GenerateReportMenu = (props) => {
    useEffect(() => {
        props.fetchChannels();
    }, []);
    useEffect(() => {
        props.setChannels(props.initialChannels.map(el => el.link));
    }, [props.initialChannels]);

    const [data, setData] = useState({startDate: new Date(), endDate: new Date()});

    return (
        <>
            <div className={statsCss.choseReportLink}>
                <Link to={`/statistics`}>
                   <IoIosArrowRoundBack style={{marginRight: "5px", fontSize: "40px"}}/> <span style={{fontSize: "25px"}}>BACK</span>
                </Link>
            </div>

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
                            startDate: range.selection.startDate,
                            endDate: range.selection.endDate,
                        })
                    }
                />
                <div className={statsCss.controls}>
                    <div
                        className={mainPageCss.controlButton}
                        onClick={() => props.showModal(
                            <SelectChannelsWindow />,
                            500,
                            800,
                        )}
                    >
                        SELECT CHANNELS
                    </div>

                    <div className={statsCss.generateReportsControlsContainer}>
                        <div
                            className={mainPageCss.controlButton}
                            onClick={() => props.sendGenerationRequest(data.startDate, data.endDate, props.channels, STATISTICAL_REPORT)}
                            style={{backgroundColor: "#2CA884", fontSize: "22px"}}
                        >
                            GENERATE STATISTICAL REPORT
                        </div>
                        <div
                            className={mainPageCss.controlButton}
                            onClick={() => props.sendGenerationRequest(data.startDate, data.endDate, props.channels, WORD_CLOUD_REPORT)}
                            style={{backgroundColor: "#2CA884", fontSize: "22px"}}
                        >
                            GENERATE WORD CLOUD
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
        showModal: (content, width, height) => dispatch(showModalWindow(content, width, height)),
        sendGenerationRequest: (startDate, endDate, channels, reportType) => dispatch(generateReport(startDate, endDate, channels, reportType)),
        setChannels: (channels) => dispatch(setChannelsListForGeneration(channels)),
        fetchChannels: () => dispatch(fetchChannels()),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(GenerateReportMenu);