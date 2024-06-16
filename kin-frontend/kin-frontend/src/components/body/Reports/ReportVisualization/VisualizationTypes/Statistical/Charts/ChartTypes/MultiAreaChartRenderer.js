import React from "react";

import {BaseChartRenderer} from "../BaseChartRenderer";
import styles from "../styles.module.css";
import {
    Area,
    AreaChart,
    Legend,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from "recharts";
import {toPercent} from "../../../../helpers/DataTransformers";
import {PercentageTooltip} from "./Helpers/ShowPercentageTooltip";

export class MultiAreaChartRenderer extends BaseChartRenderer {
    constructor(contentType, width, height, data) {
        super(contentType, width, height);

        const chartData = data[this.contentType];
        this._data = Object.entries(chartData).map(([xAxis, data]) => {
            const totalSum = Object.values(data).reduce(
                (acc, curr) => acc + curr,
                0
            );

            const percentageData = {name: xAxis};
            for (const [category, value] of Object.entries(data)) {
                percentageData[category] = (value / totalSum) * 100;
            }

            return percentageData;
        });
        this._categories = Object.keys(this._data[0]).filter(
            (key) => key !== "name"
        );

        this._colors = [
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
                    <AreaChart
                        width={this.width}
                        data={this._data}
                        stackOffset="expand"
                        margin={{left: -15}}
                    >
                        <XAxis dataKey="date" />
                        <YAxis tickFormatter={toPercent} />

                        {
                            this._categories.map((category, index) => (
                                <Area
                                    key={category}
                                    dataKey={category}
                                    stackId="1"
                                    stroke={
                                        this._colors[index % this._colors.length]
                                    }
                                    fill={this._colors[index % this._colors.length]}
                                />
                            ))
                        }

                        <Legend />
                        <Tooltip content={<PercentageTooltip />} />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        );
    }

    getChartDescription() {
        return "Area chart showing the distribution of posts percentage by each predicted category by date.";
    }
}
