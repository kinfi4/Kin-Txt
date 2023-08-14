import {Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis} from "recharts";
import {BaseChartRenderer} from "../BaseChartRenderer";
import styles from "../styles.module.css";

export class LineChartRenderer extends BaseChartRenderer {
    constructor(contentType, width, height, data) {
        super(contentType, width, height);

        const chartData = data[this.contentType];
        this._data = Object.entries(chartData).map(([key, value]) => ({ name: key, value }));

        this._colors = [
            '#0088FE', '#00C49F', '#FFBB28', '#FF8042',
            '#41B883', '#E46651', '#00D8FF', '#D7263D',
            '#F46036', '#2E294E'
        ]; // You can choose your own colors
    }

    render(key=null) {
        return (
            <div
                key={key}
                className={styles.chartContainer}
                style={{width: this.width, height: this.height}}
            >
                <h4>
                    {this.getChartDescription()}
                </h4>
                <ResponsiveContainer width="100%">
                    <LineChart
                        data={this._data}
                    >
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey="value" stroke={this._colors[0]} name="Messages count" dot={false} />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        );
    }

    getChartDescription() {
        switch (this.contentType) {
            case "ByDate":
                return "Line chart showing the distribution of telegram posts number for each day. ";
        }
    }
}