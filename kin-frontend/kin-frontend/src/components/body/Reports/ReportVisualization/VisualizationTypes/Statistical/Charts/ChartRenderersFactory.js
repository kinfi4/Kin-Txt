import {PieChartRenderer} from "./ChartTypes/PieChartRenderer";
import {LineChartRenderer} from "./ChartTypes/LineChartRenderer";
import {BarChartRenderer} from "./ChartTypes/BarChartRenderer";
import {TwoLevelPieChartRenderer} from "./ChartTypes/TwoLevelPieChartRenderer";
import {StackedBarChartRenderer} from "./ChartTypes/StackedBarChartRenderer";
import {RadarChartRenderer} from "./ChartTypes/RadarChartRenderer";
import {MultiLineChartRenderer} from "./ChartTypes/MultiLineChartRenderer";
import {MultiAreaChartRenderer} from "./ChartTypes/MultiAreaChartRenderer";

export class ChartRenderersFactory {
    static chartConfigs = {
        smallChartWidth: 450,
        smallChartHeight: 440,
        largeChartWidth: 1000,
        largeChartHeight: 440,
    };

    static getRenderer(visualizationDiagram, reportData) {
        const [contentType, chartType] = visualizationDiagram.split("__");

        switch (chartType) {
            case "Pie":
                return new PieChartRenderer(
                    contentType,
                    ChartRenderersFactory.chartConfigs.smallChartWidth,
                    ChartRenderersFactory.chartConfigs.smallChartHeight,
                    reportData
                );
            case "TwoLevelPie":
                return new TwoLevelPieChartRenderer(
                    contentType,
                    ChartRenderersFactory.chartConfigs.smallChartWidth,
                    ChartRenderersFactory.chartConfigs.smallChartHeight,
                    reportData
                );
            case "Bar":
                return new BarChartRenderer(
                    contentType,
                    ChartRenderersFactory.chartConfigs.smallChartWidth,
                    ChartRenderersFactory.chartConfigs.smallChartHeight,
                    reportData
                );
            case "StackedBar":
                return new StackedBarChartRenderer(
                    contentType,
                    ChartRenderersFactory.chartConfigs.smallChartWidth,
                    ChartRenderersFactory.chartConfigs.smallChartHeight,
                    reportData
                );
            case "Line":
                return new LineChartRenderer(
                    contentType,
                    ChartRenderersFactory.chartConfigs.largeChartWidth,
                    ChartRenderersFactory.chartConfigs.largeChartHeight,
                    reportData
                );
            case "MultiLine":
                return new MultiLineChartRenderer(
                    contentType,
                    ChartRenderersFactory.chartConfigs.largeChartWidth,
                    ChartRenderersFactory.chartConfigs.largeChartHeight,
                    reportData
                );
            case "MultiArea":
                return new MultiAreaChartRenderer(
                    contentType,
                    ChartRenderersFactory.chartConfigs.largeChartWidth,
                    ChartRenderersFactory.chartConfigs.largeChartHeight,
                    reportData
                );
            case "Radar":
                return new RadarChartRenderer(
                    contentType,
                    ChartRenderersFactory.chartConfigs.smallChartWidth,
                    ChartRenderersFactory.chartConfigs.smallChartHeight,
                    reportData
                );
            default:
                throw new Error(`Chart type ${chartType} not supported`);
        }
    }
}
