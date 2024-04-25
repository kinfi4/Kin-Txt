import React, {useEffect, useState} from "react";
import {connect} from "react-redux";
import {FiFilter} from "react-icons/fi";

import visualizationCss from "../../ReportsVisualization.module.css";

import {transformLargeNumberToReadable} from "../../../../../../utils/utils";
import {transformReportToWordsList} from "../../helpers/DataTransformers";
import FilteringBlock from "../../helpers/FilteringBlock";
import {showModalWindow} from "../../../../../../redux/reducers/modalWindowReducer";
import SelectFilteredWords from "../../helpers/SelectFilteredWords";
import ChoseReportToCompare from "../../Comparison/ChoseReportToCompare";
import {WORD_CLOUD_REPORT} from "../../../../../../config";
import BackLink from "../../../../../../common/backLink/BackLink";
import ReportWarningsBlock from "../../helpers/ReportWarningsBlock";
import {WordCloudBuilder} from "../../../../../../domain/reports/WordCloudBuilder";
import LoadingSpinner from "../../../../../../common/spiner/LoadingSpinner";

const WordCloudReport = ({
    showComparisonButton = true,
    report,
    wordsList,
    showModal,
}) => {
    const [rebuilding, setRebuilding] = useState(false);

    useEffect(() => {
        setTimeout(() => setRebuilding(false), 500);
    }, [rebuilding])

    const [filters, setFilters] = useState({
        channelFilter: "All Channels",
        categoryFilter: "All",
    });

    let words = transformReportToWordsList(
        report,
        filters.channelFilter,
        filters.categoryFilter,
        wordsList
    );

    const reportIsEmpty = report.totalWords === 0;
    const wcBuilder = WordCloudBuilder.fromWordsList(words);

    return (
        <>
            <BackLink url={"/reports"} top={"120px"} left={"25px"} />

            <div className={visualizationCss.visualizationContainer}>
                {
                    report.reportWarnings ?
                        <ReportWarningsBlock warningsList={report.reportWarnings} />
                        :
                        <></>
                }

                <div className={visualizationCss.header}>
                    <span>
                        {report.name}
                        <div
                            className={visualizationCss.totalMessagesCountLabel}
                        >
                            [{transformLargeNumberToReadable(report.totalWords)}{" "}
                            words processed]
                        </div>
                    </span>

                    {
                        showComparisonButton && !reportIsEmpty ? (
                            <div
                                className={visualizationCss.exportButton}
                                onClick={() => {
                                    showModal(
                                        <ChoseReportToCompare
                                            reportType={WORD_CLOUD_REPORT}
                                            currentReportId={report.reportId}
                                        />,
                                        500,
                                        800
                                    );
                                }}
                            >
                                COMPARE
                            </div>
                        ) : <></>
                    }
                </div>

                {
                    reportIsEmpty ?
                        <span className={visualizationCss.emptyReportMessage}>
                            Sorry, but it seems like there's no data found :(( <br />
                            Verify the channels list, datasource and dates range.
                        </span>
                        :
                        <>
                            <div className={visualizationCss.wordCloudFilters}>
                                <FilteringBlock
                                    currentOption={filters.categoryFilter}
                                    options={[
                                        {
                                            label: "All",
                                            onClick: () => {
                                                setRebuilding(true);

                                                setFilters({
                                                    ...filters,
                                                    categoryFilter: "All",
                                                });
                                            }
                                        },
                                        ...report.postsCategories.map((el) => {
                                            return {
                                                label: el,
                                                onClick: () => {
                                                    setRebuilding(true);

                                                    setFilters({
                                                        ...filters,
                                                        categoryFilter: el,
                                                    });
                                                }
                                            };
                                        }),
                                    ]}
                                    style={{position: "relative"}}
                                />
                                <FilteringBlock
                                    currentOption={filters.channelFilter}
                                    options={[
                                        {
                                            label: "All Channels",
                                            onClick: () => {
                                                setRebuilding(true);
                                                setFilters({
                                                    ...filters,
                                                    channelFilter: "All Channels",
                                                });
                                            }
                                        },
                                        ...Object.keys(report.dataByChannel).map(
                                            (el) => {
                                                return {
                                                    label: el,
                                                    onClick: () => {
                                                        setRebuilding(true);

                                                        setFilters({
                                                            ...filters,
                                                            channelFilter: el,
                                                        });
                                                    }
                                                };
                                            }
                                        ),
                                    ]}
                                    style={{position: "relative"}}
                                />

                                <div
                                    className={visualizationCss.filterOutWordsButton}
                                    onClick={() =>
                                        showModal(<SelectFilteredWords />, 500, 800)
                                    }
                                >
                                    <div>
                                        <FiFilter style={{marginRight: "5px"}} />
                                        Filter out words
                                    </div>
                                </div>
                            </div>

                            <div className={visualizationCss.wordCloudContainer}>
                                {
                                    rebuilding ?
                                        <div style={{
                                            display: "flex",
                                            justifyContent: "center",
                                            alignItems: "center",
                                            width: "100%",
                                            height: "900px"
                                        }}>
                                            <LoadingSpinner width={100} height={100} marginTop={"-35%"} />;
                                        </div>
                                        :
                                        wcBuilder.build()
                                }
                            </div>
                        </>
                }

            </div>
        </>
    );
};

let mapStateToProps = (state) => {
    return { wordsList: state.wordsCloudReducer.wordsList };
};

let mapDispatchToProps = (dispatch) => {
    return {
        showModal: (content, width, height) => dispatch(showModalWindow(content, width, height)),
    };
};


export default connect(mapStateToProps, mapDispatchToProps)(WordCloudReport);
