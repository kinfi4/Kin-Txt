import React from "react";

import {BaseChartRenderer} from "../BaseChartRenderer";
import styles from "../styles.module.css";
import {
    Legend,
    Line,
    LineChart,
    PolarAngleAxis,
    PolarGrid,
    PolarRadiusAxis,
    Radar,
    RadarChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from "recharts";

export class MultiLineChartRenderer extends BaseChartRenderer {
    constructor(contentType, width, height, data) {
        super(contentType, width, height);

        const chartData = data[this.contentType];
        this._data = Object.entries(chartData).map(([date, categories]) => {
            return {
                date,
                ...categories,
            };
        });

        this._categories = Object.keys(this._data[0]).filter(
            (key) => key !== "date"
        );

        this._colors = [
            "#23886a",
            "#00C49F",
            "#FFBB28",
            "#FF8042",
            "#41B883",
            "#E46651",
            "#00D8FF",
            "#D7263D",
            "#F46036",
            "#2E294E",
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
                    <LineChart width={600} height={400} data={this._data}>
                        <XAxis dataKey="date" />
                        <YAxis />
                        <Tooltip />
                        <Legend />

                        {this._categories.map((category, idx) => (
                            <Line
                                type="monotone"
                                dataKey={category}
                                key={idx}
                                dot={false}
                                stroke={this._colors[idx % this._colors.length]}
                            />
                        ))}
                    </LineChart>
                </ResponsiveContainer>
            </div>
        );
    }

    getChartDescription() {
        switch (this.contentType) {
            case "ByDateByCategory":
                return "Line chart showing the distribution of posts number of each category by date";
            case "ByDateByChannel":
                return "Line chart showing the distribution of posts number for each telegram channel by date";
        }
    }
}
