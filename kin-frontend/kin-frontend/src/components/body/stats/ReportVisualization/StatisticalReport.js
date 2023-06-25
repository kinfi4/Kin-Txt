import React, {useState} from 'react';
import {
    BarChart,
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    Legend,
    Bar,
    PieChart,
    Pie,
    AreaChart,
    Area,
    Cell,
    ResponsiveContainer,
} from "recharts";
import {
    getDataPercentage,
    toPercent,
    transformObjectToArray
} from "./helpers/DataTransformers";
import visualizationCss from "./ReportsVisualization.module.css"
import {STATISTICAL_REPORT, STATISTICS_SERVICE_URL} from "../../../../config";
import {capitalizeFirstLetter, downloadFile, transformLargeNumberToReadable} from "../../../../utils/utils";
import FilteringBlock from "./helpers/FilteringBlock";
import {FaFileCsv} from "react-icons/fa";
import {VscJson} from "react-icons/vsc";
import {getColor} from "./helpers/Colors";
import ChoseReportToCompare from "./Comparison/ChoseReportToCompare";
import {showModalWindow} from "../../../../redux/reducers/modalWindowReducer";
import {connect} from "react-redux";
import BackOnStatsPageLink from "../Common/BackOnStatsPageLink";


const StatisticalReport = ({showComparisonButton=true, ...props}) => {
    const [filteringState, setFilteringState] = useState({currentCategory: "Shelling", currentSentiment: "negative"});
    const [exportOptions, setExportOptions] = useState({activeExportOptions: false});
    function renderExportOptions() {
        if(exportOptions.activeExportOptions) {
            return (
                <div
                    className={visualizationCss.exportOptions}
                >
                    <div
                        onClick={() => {
                            downloadFile(STATISTICS_SERVICE_URL + `/api/v1/reports-data/${props.report.reportId}?export_type=csv`, 'csv')
                        }}
                    >
                       <FaFileCsv style={{marginRight: "5px"}}/> CSV
                    </div>
                    <div
                        onClick={() => {
                            downloadFile(STATISTICS_SERVICE_URL + `/api/v1/reports-data/${props.report.reportId}?export_type=json`, 'json')
                        }}
                    >
                       <VscJson style={{marginRight: "5px"}} /> <span style={{fontSize: "15px"}}>JSON</span>
                    </div>
                </div>
            )
        }

        return <></>
    }

    const messagesByHourCount = transformObjectToArray(props.report.messagesCountByDayHour, "hour", "messagesCount");
    const messagesByChannelCount = transformObjectToArray(props.report.messagesCountByChannel, "channel", "messagesCount");
    const messagesCountByCategory = transformObjectToArray(props.report.messagesCountByCategory, "category", "messagesCount");
    const messagesCountBySentimentType = transformObjectToArray(props.report.messagesCountBySentimentType, "sentiment", "messagesCount");
    const messagesCountByDate = transformObjectToArray(props.report.messagesCountByDate, "date", "messagesCount");
    const messagesCountByDateByCategory = transformObjectToArray(props.report.messagesCountByDateByCategory, "date", "categories");
    const messagesCountByDateBySentimentType = transformObjectToArray(props.report.messagesCountByDateBySentimentType, "date", "sentiment");
    const messagesCountByChannelBySentimentType = transformObjectToArray(props.report.messagesCountByChannelBySentimentType, "channel", "sentiment");
    const messagesCountByChannelByCategory = transformObjectToArray(props.report.messagesCountByChannelByCategory, "channel", "category");

    return (
        <div className={visualizationCss.visualizationContainer}>
            <BackOnStatsPageLink top={"0px"} left={"10px"}/>
            <div className={visualizationCss.header}>
                <span>
                    {props.report.name}
                    <span
                        style={{
                            fontSize: "20px",
                            marginLeft: "20px",
                            color: "#7b6991",
                        }}
                    >
                        [{transformLargeNumberToReadable(props.report.totalMessagesCount)} messages processed]
                    </span>
                </span>

                <div className={visualizationCss.reportOptions}>
                    <div
                        className={visualizationCss.exportButton}
                        onMouseEnter={() => setExportOptions({activeExportOptions: true})}
                        onMouseLeave={() => setExportOptions({activeExportOptions: false})}
                    >
                        EXPORT
                        {renderExportOptions()}
                    </div>
                    {
                        showComparisonButton ?
                            <div
                                className={visualizationCss.exportButton}
                                onClick={() => {
                                    props.showModal(
                                        <ChoseReportToCompare
                                            reportType={STATISTICAL_REPORT}
                                            reportsIdentifiers={props.reportsIdentifiers}
                                            currentReportId={props.report.reportId}
                                        />,
                                        500,
                                        800,
                                    )
                                }}
                            >
                                COMPARE
                            </div>
                            :
                            <></>
                    }
                </div>
            </div>

            <div
                className={visualizationCss.chartContainer}
                style={{
                    height: "450px",
                    width: "47.4%",
                    minWidth: "250px",
                }}
            >
                <h2>Number of messages distributed by hours</h2>

                <ResponsiveContainer width={"100%"} height={"80%"}>
                    <BarChart
                        data={messagesByHourCount}
                    >
                        <XAxis dataKey="hour" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="messagesCount" fill={getColor("count")} name={"Number of messages"} />
                    </BarChart>
                </ResponsiveContainer>
            </div>

            <div
                className={visualizationCss.chartContainer}
                style={{
                    height: "450px",
                    width: "46%",
                    minWidth: "250px",
                }}
            >
                <h2>Number of messages distributed by channels</h2>

                <ResponsiveContainer width={"100%"} height={"80%"}>
                    <BarChart
                        width={550}
                        height={300}
                        data={messagesByChannelCount}>
                        <XAxis dataKey="channel" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="messagesCount" fill={getColor("count")} name={"Number of messages"} />
                    </BarChart>
                </ResponsiveContainer>
            </div>

            <div
                className={visualizationCss.chartContainer}
                style={{
                    height: "400px",
                    width: "96.5%",
                    minWidth: "800px",
                }}
            >
                <h2>Dependence of news number on dates</h2>


                <ResponsiveContainer width={"100%"} height={"80%"}>
                    <AreaChart
                        data={messagesCountByDate}
                    >
                        <XAxis dataKey="date" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Area type="monotone" dataKey="messagesCount" stroke={"#fff"} fill={getColor("count")} name={"Number of messages"} />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
            <div
                className={visualizationCss.chartContainer}
                style={{
                    height: "440px",
                    width: "58.2%",
                    minWidth: "250px",
                }}
            >
                <h2>Sentiment distribution by channels</h2>

                <ResponsiveContainer width={"100%"} height={"80%"}>
                    <BarChart
                        data={messagesCountByChannelBySentimentType}
                        stackOffset="expand"
                    >
                        <XAxis dataKey="channel" />
                        <YAxis tickFormatter={toPercent} />
                        <Tooltip />
                        <Legend />
                            <Bar dataKey="sentiment.negative" name="Negative" fill={getColor("negative")} type="monotone" stackId="1" />
                            <Bar dataKey="sentiment.positive" name="Positive" fill={getColor("Positive")} type="monotone" stackId="1" />
                            <Bar dataKey="sentiment.neutral" name="Neutral" fill={getColor("Neutral")} type="monotone" stackId="1" />
                    </BarChart>
                </ResponsiveContainer>
            </div>

            <div
                className={visualizationCss.chartContainer}
                style={{
                    height: "440px",
                    width: "35%",
                    minWidth: "300pxx",
                }}
            >
                <h2>Sentiment Distribution</h2>

                <ResponsiveContainer width={"100%"} height={"80%"}>
                    <PieChart>
                        <Pie
                            data={messagesCountBySentimentType}
                            labelLine={false}
                            outerRadius={150}
                            dataKey="messagesCount"
                        >

                            {
                                messagesCountBySentimentType.map((entry, index) => {
                                    return <Cell fill={getColor(entry.sentiment)} name={entry.sentiment} />
                                })
                            }
                        </Pie>
                        <Tooltip />
                        <Legend />
                    </PieChart>
                </ResponsiveContainer>
            </div>

            <div
                className={visualizationCss.chartContainer}
                style={{
                    height: "400px",
                    width: "96.5%",
                }}
            >
                <h2>Dependence sentiment color by date</h2>

                <ResponsiveContainer width={"100%"} height={"80%"}>
                    <AreaChart
                        data={messagesCountByDateBySentimentType}
                        stackOffset="expand"
                    >

                        <XAxis dataKey="date" />
                        <YAxis tickFormatter={toPercent} />
                        <Legend />
                        <Tooltip />
                        <Area type="monotone" dataKey="sentiment.positive" stackId="1" stroke={getColor("Positive")} fill={getColor("Positive")} name={"Positive"} />
                        <Area type="monotone" dataKey="sentiment.negative" stackId="1" stroke={getColor("Negative")} fill={getColor("Negative")} name={"Negative"} />
                        <Area type="monotone" dataKey="sentiment.neutral" stackId="1" stroke={getColor("Neutral")} fill={getColor("Neutral")} name={"Neutral"} />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
            <div
                className={visualizationCss.chartContainer}
                style={{
                    height: "400px",
                    width: "96.5%",
                }}
            >
                <FilteringBlock
                    currentOption={filteringState.currentSentiment}
                    options={[
                        {label: "Negative", onClick: () => setFilteringState({...filteringState, currentSentiment: "negative"})},
                        {label: "Positive", onClick: () => setFilteringState({...filteringState, currentSentiment: "positive"})},
                        {label: "Neutral", onClick: () => setFilteringState({...filteringState, currentSentiment: "neutral"})},
                    ]}
                />
                <h2>{capitalizeFirstLetter(filteringState.currentSentiment)} news during time</h2>

                <ResponsiveContainer width={"100%"} height={"80%"}>
                    <AreaChart
                        data={messagesCountByDateBySentimentType}
                    >

                        <XAxis dataKey="date" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Area
                            type="monotone"
                            dataKey={`sentiment.${filteringState.currentSentiment}`}
                            stroke={getColor(filteringState.currentSentiment)}
                            fill={getColor(filteringState.currentSentiment)}
                            name={capitalizeFirstLetter(filteringState.currentSentiment)}
                        />
                    </AreaChart>
                    </ResponsiveContainer>
            </div>
            <div
                className={visualizationCss.chartContainer}
                style={{
                    height: "400px",
                    width: "96.5%",
                }}
            >
                <h2>{capitalizeFirstLetter(filteringState.currentSentiment)} news percentage during time</h2>

                <ResponsiveContainer width={"100%"} height={"80%"}>
                    <AreaChart
                        data={getDataPercentage(messagesCountByDateBySentimentType, "date", "sentiment", filteringState.currentSentiment)}
                    >

                        <XAxis dataKey="date" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Area
                            type="monotone"
                            dataKey={filteringState.currentSentiment}
                            stroke={getColor(filteringState.currentSentiment)}
                            fill={getColor(filteringState.currentSentiment)}
                            name={capitalizeFirstLetter(filteringState.currentSentiment)}
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
            <div
                className={visualizationCss.chartContainer}
                style={{
                    height: "700px",
                    width: "47.2%",
                }}
            >
                <h2>Message categories distribution by channels</h2>

                <ResponsiveContainer width={"100%"} height={"80%"}>
                    <BarChart
                        data={messagesCountByChannelByCategory}
                        stackOffset="expand"
                        layout="vertical"
                    >
                        <XAxis type="number" />
                        <YAxis dataKey="channel" type="category" />
                        <Tooltip />
                        <Legend />

                        <Bar dataKey="category.Shelling" name="Shelling" fill={getColor("Shelling")} stackId={'a'} />
                        <Bar dataKey="category.Political" name="Political" fill={getColor("Political")} stackId={'a'}/>
                        <Bar dataKey="category.Humanitarian" name="Humanitarian" fill={getColor("Humanitarian")} stackId={'a'} />
                        <Bar dataKey="category.Economical" name="Economical" fill={getColor("Economical")} stackId={'a'} />
                    </BarChart>
                </ResponsiveContainer>
            </div>

            <div
                className={visualizationCss.chartContainer}
                style={{
                    height: "700px",
                    width: "46%",
                }}
            >
                <h2>News Categories</h2>

                <div className={visualizationCss.categoriesCounters}>
                    <div>
                        Shelling news total:  {props.report.messagesCountByCategory.Shelling}
                    </div>
                    <div>
                        Political news total:  {props.report.messagesCountByCategory.Political}
                    </div>
                    <div>
                        Economical news total:  {props.report.messagesCountByCategory.Economical}
                    </div>
                    <div>
                        Humanitarian news total:  {props.report.messagesCountByCategory.Humanitarian}
                    </div>
                </div>

                <ResponsiveContainer width={"100%"} height={"55%"}>
                    <PieChart>
                        <Pie
                            data={messagesCountByCategory}
                            labelLine={false}
                            outerRadius={160}
                            dataKey="messagesCount"
                            fill={getColor("count")}
                        >

                            {
                                messagesCountByCategory.map((entry, index) => {
                                    return <Cell fill={getColor(entry.category)} name={entry.category} />
                                })
                            }
                        </Pie>
                        <Tooltip />
                        <Legend />
                    </PieChart>
                </ResponsiveContainer>
            </div>

            <div
                className={visualizationCss.chartContainer}
                style={{
                    height: "400px",
                    width: "96.5%",
                }}
            >
                <h2>Dependence of news number on dates by categories</h2>

                <ResponsiveContainer width={"100%"} height={"80%"}>
                    <LineChart
                        data={messagesCountByDateByCategory}
                    >
                        <XAxis dataKey="date" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey={"categories.Shelling"} stroke={getColor("shelling")} name={"Shelling"} dot={false} />
                        <Line type="monotone" dataKey={"categories.Political"} stroke={getColor("Political")} name={"Political"} dot={false} />
                        <Line type="monotone" dataKey={"categories.Humanitarian"} stroke={getColor("Humanitarian")} name={"Humanitarian"} dot={false} />
                        <Line type="monotone" dataKey={"categories.Economical"} stroke={getColor("Economical")} name={"Economical"} dot={false} />
                    </LineChart>
                </ResponsiveContainer>
            </div>

            <div
                className={visualizationCss.chartContainer}
                style={{
                    height: "400px",
                    width: "96.5%",
                }}
            >
                <h2>{filteringState.currentCategory} news during time</h2>

                <FilteringBlock
                    currentOption={filteringState.currentCategory}
                    options={[
                        {label: "Shelling", onClick: () => setFilteringState({...filteringState, currentCategory: "Shelling"})},
                        {label: "Economical", onClick: () => setFilteringState({...filteringState, currentCategory: "Economical"})},
                        {label: "Humanitarian", onClick: () => setFilteringState({...filteringState, currentCategory: "Humanitarian"})},
                        {label: "Political", onClick: () => setFilteringState({...filteringState, currentCategory: "Political"})},
                    ]}
                />

                <ResponsiveContainer width={"100%"} height={"80%"}>
                    <AreaChart
                        data={messagesCountByDateByCategory}
                    >

                        <XAxis dataKey="date" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Area
                            type="monotone"
                            dataKey={`categories.${filteringState.currentCategory}`}
                            stroke={getColor(filteringState.currentCategory)}
                            fill={getColor(filteringState.currentCategory)}
                            name={filteringState.currentCategory}
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
            <div
                className={visualizationCss.chartContainer}
                style={{
                    height: "400px",
                    width: "96.5%",
                }}
            >
                <h2>{filteringState.currentCategory} news percentage during time</h2>

                <ResponsiveContainer width={"100%"} height={"80%"}>
                    <AreaChart
                        width={1210}
                        height={400}
                        data={getDataPercentage(messagesCountByDateByCategory, "date", "categories", filteringState.currentCategory)}
                    >

                        <XAxis dataKey="date" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Area
                            type="monotone"
                            dataKey={filteringState.currentCategory}
                            stroke={getColor(filteringState.currentCategory)}
                            fill={getColor(filteringState.currentCategory)}
                            name={filteringState.currentCategory}
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>

        </div>
    );
};

let mapStateToProps = (state) => {
    return {
        reportsIdentifiers: state.reportsReducer.reports,
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        showModal: (content, width, height) => dispatch(showModalWindow(content, width, height)),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(StatisticalReport);
