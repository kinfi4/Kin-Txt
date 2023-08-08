import React from "react";

import {ChartDataFactory} from "./ChartDataFactory";
import FormPieChart from "./_ChartsVisualizations/FormPieChart";
import FormBarChart from "./_ChartsVisualizations/FormBarChart";
import FormTwoLevelPieChart from "./_ChartsVisualizations/FormTwoLevelPieChart";
import FormLineChart from "./_ChartsVisualizations/FormLineChart";


const FormChart = ({chartId, onClick, isSelected}) => {
    const chartDataFactory = new ChartDataFactory();
    const [visualizationCategory, chartType] = chartId.split("__");

    const data = chartDataFactory.createChartData(visualizationCategory);

    if (chartType === "Pie") {
        return <FormPieChart
            visualizationCategory={visualizationCategory}
            data={data}
            onClick={() => onClick(chartId)}
            isSelected={isSelected}
        />;
    }

    if (chartType === "TwoLevelPie") {
        return <FormTwoLevelPieChart
            visualizationCategory={visualizationCategory}
            data={data}
            onClick={() => onClick(chartId)}
            isSelected={isSelected}
        />;
    }

    if (chartType === "Bar") {
        return <FormBarChart
            visualizationCategory={visualizationCategory}
            data={data}
            onClick={() => onClick(chartId)}
            isSelected={isSelected}
        />;
    }

    if (chartType === "Line") {
        return <FormLineChart
            visualizationCategory={visualizationCategory}
            data={data}
            onClick={() => onClick(chartId)}
            isSelected={isSelected}
        />;
    }

    return (
        <div>

        </div>
    );
};

export default FormChart;