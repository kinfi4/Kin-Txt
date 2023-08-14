import {BaseChartRenderer} from "../BaseChartRenderer";
import {Bar, BarChart, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis} from "recharts";
import styles from "../styles.module.css";
import React from "react";
import {PercentageTooltip} from "./Helpers/ShowPercentageTooltip";

export class StackedBarChartRenderer extends BaseChartRenderer {
    constructor(contentType, width, height, data) {
        super(contentType, width, height);

        const chartData = data[this.contentType];
        this._data = Object.entries(chartData).map(([itemName, itemData]) => {
            const totalSum = Object.values(itemData).reduce((acc, value) => acc + value, 0);

            const percentageData = { name: itemName };
            for (const [category, value] of Object.entries(itemData)) {
                percentageData[category] = (value / totalSum) * 100;
            }

            return percentageData;
        });
        this._categories = Object.keys(this._data[0]).filter(key => key !== "name");

        this._colors = [
            '#DB7093', '#008B8B', '#483D8B', '#DEB887',
            '#5F9EA0', '#F5F5F5', '#7FFFD4', '#D7263D',
            '#F46036', '#0088FE'
        ];
    }

    render(key=null) {
        return (
            <div
                key={key}
                className={styles.chartContainer}
                style={{width: this.width, height: this.height}}
            >
                <h4>
                    {this.getChartDescription()}
                </h4>
                <ResponsiveContainer width="100%">
                    <BarChart
                        data={this._data}
                    >
                        <XAxis dataKey="name" interval={0} angle={this._data.length < 5 ? 0 : -90} color="#fff" dy={25} height={60} />
                        <YAxis tickFormatter={(tick) => `${tick}%`} domain={[0, 100]} />

                        {
                            this._categories.map((category, index) => (
                                <Bar
                                    key={category}
                                    dataKey={category}
                                    stackId="a"
                                    fill={this._colors[index % this._colors.length]}
                                />
                            ))
                        }

                        <Tooltip content={<PercentageTooltip />} />
                        <Legend />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        );
    }

    getChartDescription() {
        switch (this.contentType) {
            case "ByCategory":
                return "Bar chart showing the distribution of posts number by each predicted category. ";
            case "ByChannel":
                return "Bar chart showing the distribution of posts number by channel";
            case "ByHour":
                return "Bar chart showing the distribution of posts number by day hour";
            default:
                return "";
        }
    }
}





















//
// {
//     "reportId": 19,
//     "name": "Test template with all charts",
//     "reportType": "Statistical",
//     "processingStatus": "Ready",
//     "generationDate": "13/08/2023 17:43",
//     "reportFailedReason": null,
//     "totalMessagesCount": 538,
//     "postsCategories": [
//     "Economical",
//     "Political",
//     "Shelling",
//     "Humanitarian"
// ],
//     "visualizationDiagramsList": [
//     "ByCategory__Pie",
//     "ByChannel__Pie",
//     "ByChannel+ByCategory__TwoLevelPie",
//     "ByCategory__Bar",
//     "ByChannel__Bar",
//     "ByHour__Bar",
//     "ByChannelByCategory__StackedBar",
//     "ByDate__Line",
//     "ByDateByCategory__MultiLine",
//     "ByDateByChannel__MultiLine",
//     "ByDateByCategory__MultiArea",
//     "ByCategory__Radar"
// ],
//     "data": {
//     "ByDate": {
//         "01/08/2023": 87,
//             "02/08/2023": 77,
//             "03/08/2023": 58,
//             "04/08/2023": 72,
//             "05/08/2023": 58,
//             "06/08/2023": 59,
//             "07/08/2023": 66,
//             "08/08/2023": 61
//     },
//     "ByDateByCategory": {
//         "01/08/2023": {
//             "Economical": 4,
//                 "Political": 51,
//                 "Shelling": 31,
//                 "Humanitarian": 1
//         },
//         "02/08/2023": {
//             "Economical": 3,
//                 "Political": 32,
//                 "Shelling": 34,
//                 "Humanitarian": 8
//         },
//         "03/08/2023": {
//             "Economical": 6,
//                 "Political": 25,
//                 "Shelling": 23,
//                 "Humanitarian": 4
//         },
//         "04/08/2023": {
//             "Economical": 3,
//                 "Political": 36,
//                 "Shelling": 24,
//                 "Humanitarian": 9
//         },
//         "05/08/2023": {
//             "Economical": 2,
//                 "Political": 26,
//                 "Shelling": 26,
//                 "Humanitarian": 4
//         },
//         "06/08/2023": {
//             "Economical": 2,
//                 "Political": 26,
//                 "Shelling": 28,
//                 "Humanitarian": 3
//         },
//         "07/08/2023": {
//             "Economical": 5,
//                 "Political": 36,
//                 "Shelling": 23,
//                 "Humanitarian": 2
//         },
//         "08/08/2023": {
//             "Economical": 5,
//                 "Political": 32,
//                 "Shelling": 21,
//                 "Humanitarian": 3
//         }
//     },
//     "ByChannel": {
//         "uniannet": 538
//     },
//     "ByChannelByCategory": {
//         "uniannet": {
//             "Economical": 30,
//                 "Political": 264,
//                 "Shelling": 210,
//                 "Humanitarian": 34
//         }
//     },
//     "ByHour": {
//         "0": 13,
//             "1": 4,
//             "2": 0,
//             "3": 10,
//             "4": 23,
//             "5": 28,
//             "6": 34,
//             "7": 27,
//             "8": 30,
//             "9": 26,
//             "10": 22,
//             "11": 25,
//             "12": 26,
//             "13": 33,
//             "14": 29,
//             "15": 28,
//             "16": 28,
//             "17": 29,
//             "18": 25,
//             "19": 27,
//             "20": 27,
//             "21": 26,
//             "22": 9,
//             "23": 9
//     },
//     "ByCategory": {
//         "Economical": 30,
//             "Political": 264,
//             "Shelling": 210,
//             "Humanitarian": 34
//     },
//     "ByDateByChannel": {
//         "01/08/2023": {
//             "uniannet": 87
//         },
//         "02/08/2023": {
//             "uniannet": 77
//         },
//         "03/08/2023": {
//             "uniannet": 58
//         },
//         "04/08/2023": {
//             "uniannet": 72
//         },
//         "05/08/2023": {
//             "uniannet": 58
//         },
//         "06/08/2023": {
//             "uniannet": 59
//         },
//         "07/08/2023": {
//             "uniannet": 66
//         },
//         "08/08/2023": {
//             "uniannet": 61
//         }
//     }
// }
// }


