import React from "react";
import styles from "../chartStyles.module.css";
import {Bar, BarChart, XAxis} from "recharts";


const visualizationCategoryToTitleMapping = {
    "ByCategory": "Bar chart visualizing the number of records by category predicted",
    "ByChannel": "Bar chart visualizing the number of records by each channel was analyzed",
    "ByHour": "Visualization of number of messages by hours of the day",
}

const FormBarChart = ({visualizationCategory, data, onClick, isSelected=false}) => {
    return (
        <div
            className={`${styles.chartContainer} ${isSelected ? styles.active : ""}`}
            onClick={onClick}
            style={{width: "400px", height: "350px"}}
        >
            <h4>{visualizationCategoryToTitleMapping[visualizationCategory]}</h4>

            <BarChart
                width={400}
                height={220}
                data={data}
            >
                <Bar dataKey="value" fill={data[0].color} barSize={40} barGap={3} />
                <XAxis dataKey="name" interval={0} angle={data.length < 5 ? 0 : -90} color="#fff"  dy={25} height={60} />
            </BarChart>
        </div>
    );
};

export default FormBarChart;