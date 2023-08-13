import React from "react";

import {ChartDataFactory} from "./ChartDataFactory";
import FormPieChart from "./_ChartsVisualizations/FormPieChart";
import FormBarChart from "./_ChartsVisualizations/FormBarChart";
import FormTwoLevelPieChart from "./_ChartsVisualizations/FormTwoLevelPieChart";
import FormLineChart from "./_ChartsVisualizations/FormLineChart";
import FormStackedBarChart from "./_ChartsVisualizations/FormStackedBarChart";
import FormRadarChart from "./_ChartsVisualizations/FormRadarChart";
import FormMultiLineChart from "./_ChartsVisualizations/FormMultiLineChart";
import FormMultiAreaChart from "./_ChartsVisualizations/FormMultiAreaChart";


const FormChart = ({chartId, onClick, isSelected}) => {
    const chartDataFactory = new ChartDataFactory();
    const [visualizationCategory, chartType] = chartId.split("__");

    const data = chartDataFactory.createChartData(visualizationCategory);
    const params = {
        visualizationCategory,
        data,
        onClick,
        isSelected,
    }

    if (chartType === "Pie") {
        return <FormPieChart {...params} />;
    }

    if (chartType === "TwoLevelPie") {
        return <FormTwoLevelPieChart {...params} />;
    }

    if (chartType === "Bar") {
        return <FormBarChart {...params} />;
    }

    if (chartType === "Line") {
        return <FormLineChart {...params} />;
    }

    if (chartType === "MultiLine") {
        return <FormMultiLineChart {...params} />;
    }

    if (chartType === "StackedBar") {
        return <FormStackedBarChart {...params} />;
    }

    if (chartType === "Radar") {
        return <FormRadarChart {...params} />;
    }

    if(chartType === "MultiArea") {
        return <FormMultiAreaChart {...params} />;
    }

    return (
        <div>

        </div>
    );
};

export default FormChart;