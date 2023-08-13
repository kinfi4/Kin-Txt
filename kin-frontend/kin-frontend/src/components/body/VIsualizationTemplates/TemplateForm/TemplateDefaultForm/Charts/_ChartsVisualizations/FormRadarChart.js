import React from "react";
import styles from "../chartStyles.module.css";
import {PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart} from "recharts";


const visualizationCategoryToTitleMapping = {
    "ByCategory": "Radar visualizing categories popularity",
}

const FormRadarChart = ({visualizationCategory, data, onClick, isSelected=false}) => {
    return (
        <div
            className={`${styles.chartContainer} ${isSelected ? styles.active : ""}`}
            onClick={onClick}
            style={{width: "460px", height: "380px"}}
        >
            <h4>{visualizationCategoryToTitleMapping[visualizationCategory]}</h4>

            <RadarChart
                data={data}
                width={450}
                height={350}
                outerRadius="80%"
            >
                <PolarGrid />
                <PolarAngleAxis dataKey="name" tick={{ fill: "white" }} />
                <PolarRadiusAxis angle={45} domain={[0, 150]} />
                <Radar dataKey="value" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
            </RadarChart>
        </div>
    );
};

export default FormRadarChart;