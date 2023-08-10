import React, {useState} from 'react';
import WordCloud from 'react-d3-cloud';
import {connect} from "react-redux";
import {FiFilter} from "react-icons/fi"

import visualizationCss from "../../ReportsVisualization.module.css";

import {transformLargeNumberToReadable} from "../../../../../../utils/utils";
import {transformReportToWordsList} from "../../helpers/DataTransformers";
import FilteringBlock from "../../helpers/FilteringBlock";
import {calcFontSize, calcPadding} from "../../helpers/WordCloudHelpers";
import {showModalWindow} from "../../../../../../redux/reducers/modalWindowReducer";
import SelectFilteredWords from "../../helpers/SelectFilteredWords";
import ChoseReportToCompare from "../../Comparison/ChoseReportToCompare";
import {WORD_CLOUD_REPORT} from "../../../../../../config";
import BackOnStatsPageLink from "../../../Common/BackOnStatsPageLink";


const WordCloudReport = ({showComparisonButton=true, report, wordsList, showModal, reportsIdentifiers}) => {
    const colors = ['#408f5e', '#2F6B9A', '#82a6c2', '#BA97B4', '#2CA884', '#E39E21', '#00C6B5', '#BF8520'];
    const [filters, setFilters] = useState({channelFilter: "All Channels", categoryFilter: "All"});

    let words = transformReportToWordsList(report, filters.channelFilter, filters.categoryFilter, wordsList);
    let theBiggestWordValue = Math.max(...words.map(el => el.value));
    let theSmallestWordValue = Math.min(...words.map(el => el.value));

    return (
        <>
            <BackOnStatsPageLink top={"120px"} left={"25px"} />

            <div className={visualizationCss.visualizationContainer}>

                <div className={visualizationCss.header}>
                    <span>
                        {report.name}
                        <span
                            style={{
                                fontSize: "20px",
                                marginLeft: "20px",
                                color: "#24B382",
                            }}
                        >
                            [{transformLargeNumberToReadable(report.totalWords)} words processed]
                        </span>
                    </span>

                    {
                        showComparisonButton ?
                            <div
                                className={visualizationCss.exportButton}
                                onClick={() => {
                                    showModal(
                                        <ChoseReportToCompare
                                            reportType={WORD_CLOUD_REPORT}
                                            reportsIdentifiers={reportsIdentifiers}
                                            currentReportId={report.reportId}
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

                <div className={visualizationCss.wordCloudFilters}>
                    <div style={{position: "relative"}}>
                        <FilteringBlock
                            currentOption={filters.categoryFilter}
                            options={[
                                {label: "All", onClick: () => setFilters({...filters, categoryFilter: "All"})},
                                ...report.postsCategories.map(el => {
                                    return {label: el, onClick: () => setFilters({...filters, categoryFilter: el})}
                                })
                            ]}
                        />
                    </div>

                    <div style={{position: "relative"}}>
                        <FilteringBlock
                            currentOption={filters.channelFilter}
                            options={[
                                {label: "All Channels", onClick: () => setFilters({...filters, channelFilter: "All Channels"})},
                                ...Object.keys(report.dataByChannel).map(el => {
                                    return {
                                        label: el,
                                        onClick: () => setFilters({...filters, channelFilter: el})
                                    }
                                })
                            ]}
                        />
                    </div>

                    <div style={{position: "relative"}}>
                        <div
                            className={visualizationCss.filterOutWordsButton}
                            onClick={() => showModal(
                                <SelectFilteredWords />,
                                500,
                                800,
                            )}
                        >
                            <div><FiFilter style={{marginRight: "5px"}} /> Filter out words</div>
                        </div>
                    </div>

                </div>

                <div className={visualizationCss.wordCloudContainer}>
                    <WordCloud
                        data={words}
                        width={1500}
                        height={1500}
                        random={() => 0.5}
                        padding={calcPadding(words.length)}
                        fontSize={(word) => calcFontSize(word, words, theBiggestWordValue, theSmallestWordValue)}
                        fill={(w, i) => colors[i % colors.length]}
                        rotate={() => 0}
                    />
                </div>
            </div>
        </>
    );
};

let mapStateToProps = (state) => {
    return {
        wordsList: state.wordsCloudReducer.wordsList,
        reportsIdentifiers: state.reportsReducer.reports,
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        showModal: (content, width, height) => dispatch(showModalWindow(content, width, height)),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(WordCloudReport);