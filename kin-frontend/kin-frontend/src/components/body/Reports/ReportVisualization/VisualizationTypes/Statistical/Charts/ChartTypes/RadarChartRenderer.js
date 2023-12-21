import {
    Cell,
    Legend,
    Pie,
    PieChart,
    PolarAngleAxis,
    PolarGrid,
    PolarRadiusAxis,
    Radar,
    RadarChart,
    ResponsiveContainer,
    Tooltip,
} from "recharts";

import styles from "../styles.module.css";

import {BaseChartRenderer} from "../BaseChartRenderer";
import React from "react";

export class RadarChartRenderer extends BaseChartRenderer {
    constructor(contentType, width, height, data) {
        super(contentType, width, height);

        const chartData = data[this.contentType];
        this._data = Object.entries(chartData).map(([key, value]) => ({
            name: key,
            value,
        }));

        this._colors = [
            "#8673A1",
            "#C1876B",
            "#B8B799",
            "#8E402A",
            "#3B83BD",
            "#DE4C8A",
            "#F4F4F4",
            "#69373e",
            "#b68071",
            "#4739a6",
        ];
    }

    render(key = null) {
        return (
            <div
                key={key}
                className={styles.chartContainer}
                style={{width: this.width, height: this.height}}
            >
                <h4>{this.getChartDescription()}</h4>

                <ResponsiveContainer width="100%">
                    <RadarChart
                        data={this._data}
                        width={this.width}
                        outerRadius="80%"
                    >
                        <PolarGrid />
                        <PolarAngleAxis dataKey="name" tick={{fill: "white"}} />
                        <PolarRadiusAxis angle={45} domain={[0, 150]} />
                        <Radar
                            dataKey="value"
                            stroke="#8884d8"
                            fill="#8884d8"
                            fillOpacity={0.6}
                        />
                        <Tooltip />
                    </RadarChart>
                </ResponsiveContainer>
            </div>
        );
    }

    getChartDescription() {
        switch (this.contentType) {
            case "ByCategory":
                return "Radar chart showing the distribution of posts number by each predicted category. ";
            case "ByChannel":
                return "Pie chart showing the distribution of posts number by channel";
        }
    }
}
