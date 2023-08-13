import React from "react";
import {Legend, LineChart, Line, YAxis, XAxis} from "recharts";

import styles from "../chartStyles.module.css";


const visualizationCategoryToTitleMapping = {
    "ByCategory": "",
    "ByChannel": "",
    "ByDateByCategory": "Distribution of categories popularity by date",
    "ByDateByChannel": "Distribution of channels posts by date",
}

const FromMultiLineChart = ({visualizationCategory, data, onClick, isSelected=false}) => {
    return (
        <div
            className={`${styles.chartContainer} ${isSelected ? styles.active : ""}`}
            onClick={onClick}
            style={{width: "750px", height: "300px"}}
        >
            <h4>{visualizationCategoryToTitleMapping[visualizationCategory]}</h4>

            <div>
                <LineChart
                    width={700}
                    height={250}
                    data={data}
                >
                    <YAxis />
                    <XAxis dataKey="date" interval={0} />
                    <Line type="monotone" dataKey="value1" stroke="#8884d8" activeDot={{ r: 8 }} />
                    <Line type="monotone" dataKey="value2" stroke="#fff" activeDot={{ r: 8 }} />
                </LineChart>

            </div>
        </div>
    );
};

export default FromMultiLineChart;