export const toPercent = (decimal, fixed = 0) => {
    return `${(decimal * 100).toFixed(0)}%`;
};

export function transformReportToWordsList(
    report,
    channelFilter = null,
    categoryFilter = null,
    wordsFilters = []
) {
    const all = "All";
    const allChannels = "All Channels";
    let result = [];

    if (channelFilter !== allChannels && categoryFilter !== all) {
        result = report.dataByChannelByCategory[channelFilter][
            categoryFilter
        ].map((el) => {
            return {text: el[0], value: el[1]};
        });
    } else if (channelFilter !== allChannels && categoryFilter === all) {
        result = report.dataByChannel[channelFilter].map((el) => {
            return {text: el[0], value: el[1]};
        });
    } else if (channelFilter === allChannels && categoryFilter !== all) {
        result = report.dataByCategory[categoryFilter].map((el) => {
            return {text: el[0], value: el[1]};
        });
    } else {
        result = report.totalWordsFrequency.map((el) => {
            return {text: el[0], value: el[1]};
        });
    }

    if (wordsFilters !== []) {
        result = result.filter((el) => !wordsFilters.includes(el.text));
    }

    return result;
}
