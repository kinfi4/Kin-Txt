import React from "react";
import styles from "../chartStyles.module.css";
import {Bar, BarChart, Legend, XAxis, YAxis} from "recharts";


const visualizationCategoryToTitleMapping = {
    "ByChannelByCategory": "Visualization of categories popularity by channel",
}

const FormStackedBarChart = ({visualizationCategory, data, onClick, isSelected=false}) => {
    const percentageData = data.map((dataItem) => {
        const totalValue = dataItem.value1 + dataItem.value2 + dataItem.value3;
        return {
            name: dataItem.name,
            value1: dataItem.value1 / totalValue * 100,
            value2: dataItem.value2 / totalValue * 100,
            value3: dataItem.value3 / totalValue * 100,
        };
    });

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
                data={percentageData}
                margin={{left: -20}}
            >
                <Bar dataKey="value1" fill={data[0].color} barGap={3} stackId="1" />
                <Bar dataKey="value2" fill={data[1].color} barGap={3} stackId="1" />
                <Bar dataKey="value3" fill={data[2].color} barGap={3} stackId="1" />
                <XAxis dataKey="name" interval={0} angle={data.length < 5 ? 0 : -90} color="#fff"  dy={25} height={60} />
                <YAxis tickFormatter={(tick) => `${tick}%`} domain={[0, 100]} />
            </BarChart>
        </div>
    );
};

export default FormStackedBarChart;