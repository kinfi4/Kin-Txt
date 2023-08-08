import React from "react";
import {Cell, Pie, PieChart, Legend} from "recharts";

import styles from "../chartStyles.module.css";


const visualizationCategoryToTitleMapping = {
    "ByCategory": "Pie chart visualizing the number of records by category predicted",
    "ByChannel": "Pie chart showing number of messages per each channel that was analyzed",
}

const FormPieChart = ({visualizationCategory, data, onClick, isSelected=false}) => {
    return (
        <div
            className={`${styles.chartContainer} ${isSelected ? styles.active : ""}`}
            onClick={onClick}
            style={{
                width: "400px",
            }}
        >
            <h4>{visualizationCategoryToTitleMapping[visualizationCategory]}</h4>

            <div>
                <PieChart width={400} height={200} >
                    <Pie
                        data={data}
                        labelLine={false}
                        outerRadius={95}
                        dataKey="value"
                        cx={120}
                    >
                        {data.map((entry, index) => (
                            <Cell
                                key={`cell-${index}`}
                                fill={entry.color}
                                name={entry.name}
                            />
                        ))}
                    </Pie>
                    <Legend layout="vertical" verticalAlign="middle" align="right" />
                </PieChart>
            </div>
        </div>
    );
};

export default FormPieChart;