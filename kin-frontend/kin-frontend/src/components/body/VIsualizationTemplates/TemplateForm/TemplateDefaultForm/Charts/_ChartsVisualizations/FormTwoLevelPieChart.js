import React from "react";
import {Bar, BarChart, Legend, Pie, PieChart} from "recharts";
import styles from "../chartStyles.module.css";

const visualizationCategoryToTitleMapping = {
    "ByChannel+ByCategory": "Pie chart visualizing both the number of records by category predicted and the number of messages per each channel that was analyzed",
}

const FormTwoLevelPieChart = ({visualizationCategory, isSelected, onClick, data}) => {
    const [firstLevel, secondLevel] = visualizationCategory.split("+");
    const firstLevelData = data[firstLevel];
    const secondLevelData = data[secondLevel];

    return (
        <div
            className={`${styles.chartContainer} ${isSelected ? styles.active : ""}`}
            onClick={onClick}
            style={{width: "400px"}}
        >
            <h4>{visualizationCategoryToTitleMapping[visualizationCategory]}</h4>

            <PieChart width={400} height={250}>
                <Pie data={firstLevelData} dataKey="value" outerRadius={60} fill="#8884d8" />
                <Pie data={secondLevelData} dataKey="value" innerRadius={70} outerRadius={90} fill="#82ca9d" label />
                <Legend align={"right"} verticalAlign={"middle"} layout="vertical" />
            </PieChart>
        </div>
    );
};

export default FormTwoLevelPieChart;