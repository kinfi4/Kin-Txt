import {
    Cell,
    Legend,
    Pie,
    PieChart,
    ResponsiveContainer,
    Tooltip,
} from "recharts";

import styles from "../styles.module.css";

import {BaseChartRenderer} from "../BaseChartRenderer";
import React from "react";

export class TwoLevelPieChartRenderer extends BaseChartRenderer {
    constructor(contentType, width, height, data) {
        super(contentType, width, height);

        const [firstContentType, secondContentType] =
            this.contentType.split("+");

        const firstChartData = data[firstContentType];
        this.firstChartData = Object.entries(firstChartData).map(
            ([key, value]) => ({name: key, value})
        );
        const secondChartData = data[secondContentType];
        this.secondChartData = Object.entries(secondChartData).map(
            ([key, value]) => ({name: key, value})
        );

        this._firstColors = [
            "#0088FE",
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
        this._secondColors = [
            "#8673A1",
            "#C1876B",
            "#B8B799",
            "#bbaaa6",
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
                    <PieChart width={this.width}>
                        <Pie
                            data={this.firstChartData}
                            dataKey="value"
                            outerRadius={70}
                            fill="#8884d8"
                        >
                            {this.firstChartData.map((entry, index) => (
                                <Cell
                                    key={`cell-${index}`}
                                    fill={
                                        this._firstColors[
                                            index % this._firstColors.length
                                        ]
                                    }
                                />
                            ))}
                        </Pie>
                        <Pie
                            data={this.secondChartData}
                            dataKey="value"
                            innerRadius={80}
                            outerRadius={100}
                            fill="#82ca9d"
                            label
                        >
                            {this.secondChartData.map((entry, index) => (
                                <Cell
                                    key={`cell-${index}`}
                                    fill={
                                        this._secondColors[
                                            index % this._secondColors.length
                                        ]
                                    }
                                />
                            ))}
                        </Pie>{" "}
                        <Legend
                            align={"right"}
                            verticalAlign={"middle"}
                            layout="vertical"
                        />
                        <Legend />
                        <Tooltip />
                    </PieChart>
                </ResponsiveContainer>
            </div>
        );
    }

    getChartDescription() {
        switch (this.contentType) {
            case "ByChannel+ByCategory":
                return "Double pie chart showing the distribution of posts by each category and each channel.";
        }
    }
}
