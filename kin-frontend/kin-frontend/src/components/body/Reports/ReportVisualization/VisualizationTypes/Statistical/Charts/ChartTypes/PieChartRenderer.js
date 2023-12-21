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

export class PieChartRenderer extends BaseChartRenderer {
    constructor(contentType, width, height, data) {
        super(contentType, width, height);

        const chartData = data[this.contentType];
        this._data = Object.entries(chartData).map(([key, value]) => ({
            name: key,
            value,
        }));

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
        ]; // You can choose your own colors
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
                            data={this._data}
                            dataKey="value"
                            outerRadius={this.width / 3}
                            fill="#00C49F"
                        >
                            {this._data.map((entry, index) => (
                                <Cell
                                    key={`cell-${index}`}
                                    fill={
                                        this._colors[
                                            index % this._colors.length
                                        ]
                                    }
                                />
                            ))}
                        </Pie>
                        <Legend />
                        <Tooltip />
                    </PieChart>
                </ResponsiveContainer>
            </div>
        );
    }

    getChartDescription() {
        switch (this.contentType) {
            case "ByCategory":
                return "Pie chart showing the distribution of posts number by each predicted category. ";
            case "ByChannel":
                return "Pie chart showing the distribution of posts number by channel";
        }
    }
}
