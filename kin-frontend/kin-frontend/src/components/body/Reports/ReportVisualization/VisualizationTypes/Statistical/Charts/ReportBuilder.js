import {ChartRenderersFactory} from "./ChartRenderersFactory";

export class ReportBuilder {
    constructor(reportData) {
        this.reportData = reportData;
        this.chartRenderers = [];
    }

    generateChartRenderers() {
        this.reportData.visualizationDiagramsList.forEach((diagramType) => {
            const chartRenderer = ChartRenderersFactory.getRenderer(
                diagramType,
                this.reportData.data
            );
            this.chartRenderers.push(chartRenderer);
        });

        return this;
    }

    build() {
        if (!this.chartRenderers.length) {
            throw new Error("No chart renderers were generated!");
        }

        return this.chartRenderers.map((chart, index) => chart.render(index));
    }

    organizeChartsOrder() {
        // split charts into small and big
        const smallCharts = this.chartRenderers.filter(
            (chart) =>
                chart.width ===
                ChartRenderersFactory.chartConfigs.smallChartWidth
        );
        const bigCharts = this.chartRenderers.filter(
            (chart) =>
                chart.width ===
                ChartRenderersFactory.chartConfigs.largeChartWidth
        );

        // sort small and big charts by content type
        bigCharts.sort((a, b) => a.contentType.localeCompare(b.contentType));
        smallCharts.sort((a, b) => a.contentType.localeCompare(b.contentType));

        // split small charts into pairs
        const smallChartPairs = [];
        for (let i = 0; i < smallCharts.length; i += 2) {
            smallChartPairs.push(smallCharts.slice(i, i + 2));
        }

        // merge small charts with big charts
        const sortedCharts = [];
        for (
            let i = 0;
            i < Math.max(smallChartPairs.length, bigCharts.length);
            i++
        ) {
            if (smallChartPairs[i]) {
                sortedCharts.push(...smallChartPairs[i]);
            }
            if (bigCharts[i]) {
                sortedCharts.push(bigCharts[i]);
            }
        }

        this.chartRenderers = sortedCharts;

        return this;
    }
}
