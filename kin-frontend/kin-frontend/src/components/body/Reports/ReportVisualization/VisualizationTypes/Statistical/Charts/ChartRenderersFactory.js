import {PieChartRenderer} from "./ChartTypes/PieChartRenderer";
import {LineChartRenderer} from "./ChartTypes/LineChartRenderer";
import {BarChartRenderer} from "./ChartTypes/BarChartRenderer";

export class ChartRenderersFactory {
    static chartConfigs = {
        smallChartWidth: 450,
        smallChartHeight: 440,
        largeChartWidth: 1000,
        largeChartHeight: 440,
    }

    static getRenderer(visualizationDiagram, reportData) {
        const [contentType, chartType] = visualizationDiagram.split('__');

        switch (chartType) {
            case "Pie":
                return new PieChartRenderer(
                    contentType,
                    ChartRenderersFactory.chartConfigs.smallChartWidth,
                    ChartRenderersFactory.chartConfigs.smallChartHeight,
                    reportData,
                );
            case "Bar":
                return new BarChartRenderer(
                    contentType,
                    ChartRenderersFactory.chartConfigs.smallChartWidth,
                    ChartRenderersFactory.chartConfigs.smallChartHeight,
                    reportData,
                );
            case "Line":
                return new LineChartRenderer(
                    contentType,
                    ChartRenderersFactory.chartConfigs.largeChartWidth,
                    ChartRenderersFactory.chartConfigs.largeChartHeight,
                    reportData,
                );
            default:
                throw new Error(`Chart type ${chartType} not supported`);
        }
    }
}


// 0: "ByCategory__Pie"
// 1: "ByChannel__Pie"
// 2: "ByCategory__Bar"
// 3: "ByChannel__Bar"
// 4: "ByHour__Bar"
// 5: "ByDate__Line"
