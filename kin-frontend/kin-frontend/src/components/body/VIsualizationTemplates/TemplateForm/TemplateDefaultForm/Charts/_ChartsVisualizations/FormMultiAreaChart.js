import React from "react";
import {
    Legend,
    LineChart,
    Line,
    YAxis,
    XAxis,
    CartesianGrid,
    Area,
    AreaChart,
} from "recharts";

import styles from "../chartStyles.module.css";
import {toPercent} from "../../../../../Reports/ReportVisualization/helpers/DataTransformers";

const visualizationCategoryToTitleMapping = {
    ByDateByCategory: "Distribution of categories popularity by date",
    ByDateByChannel: "Distribution of channels posts by date",
};

const FormMultiAreaChart = ({
    visualizationCategory,
    data,
    onClick,
    isSelected = false,
}) => {
    return (
        <div
            className={`${styles.chartContainer} ${
                isSelected ? styles.active : ""
            }`}
            onClick={onClick}
            style={{width: "750px", height: "310px"}}
        >
            <h4>
                {visualizationCategoryToTitleMapping[visualizationCategory]}
            </h4>

            <div>
                <AreaChart
                    width={700}
                    height={300}
                    data={data}
                    stackOffset="expand"
                    margin={{left: -15}}
                >
                    <XAxis dataKey="date" />
                    <YAxis tickFormatter={toPercent} />
                    <Area
                        type="monotone"
                        dataKey="value1"
                        stackId="1"
                        stroke="#8884d8"
                        fill="#8884d8"
                    />
                    <Area
                        type="monotone"
                        dataKey="value2"
                        stackId="1"
                        stroke="#82ca9d"
                        fill="#82ca9d"
                    />
                    <Area
                        type="monotone"
                        dataKey="value3"
                        stackId="1"
                        stroke="#ffc658"
                        fill="#ffc658"
                    />
                </AreaChart>
            </div>
        </div>
    );
};

export default FormMultiAreaChart;
