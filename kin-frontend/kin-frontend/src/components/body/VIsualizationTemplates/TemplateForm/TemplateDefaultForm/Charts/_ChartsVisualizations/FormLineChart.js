import React from "react";
import {Legend, LineChart, Line, YAxis, XAxis} from "recharts";

import styles from "../chartStyles.module.css";


const visualizationCategoryToTitleMapping = {
    "ByCategory": "",
    "ByChannel": "",
    "ByDate": "The dependency of the number of messages by date",
}

const FormLineChart = ({visualizationCategory, data, onClick, isSelected=false}) => {
    return (
        <div
            className={`${styles.chartContainer} ${isSelected ? styles.active : ""}`}
            onClick={onClick}
            style={{width: "550px", height: "300px"}}
        >
            <h4>{visualizationCategoryToTitleMapping[visualizationCategory]}</h4>

            <div>
                <LineChart
                    width={550}
                    height={250}
                    data={data}
                >
                    <YAxis />
                    <XAxis dataKey="date" interval={0} />
                    <Line type="monotone" dataKey="value" stroke="#8884d8" activeDot={{ r: 8 }} />
                </LineChart>

            </div>
        </div>
    );
};

export default FormLineChart;