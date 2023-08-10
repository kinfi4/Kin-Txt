import {BaseChartRenderer} from "../BaseChartRenderer";
import {Bar, BarChart, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis} from "recharts";
import styles from "../styles.module.css";

export class BarChartRenderer extends BaseChartRenderer {
    constructor(contentType, width, height, data) {
        super(contentType, width, height);

        const chartData = data[this.contentType];
        this._data = Object.entries(chartData).map(([key, value]) => ({ name: key, value }));

        this._colors = [
            '#2E294E', '#0088FE', '#46747e', '#FF8042',
            '#41B883', '#00D8FF', '#397c49', '#D7263D',
            '#F46036', '#0088FE'
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
                    <BarChart
                        data={this._data}
                    >
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="value" fill={this._colors[3]} name={"Number of messages"} />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        );
    }

    getChartDescription() {
        switch (this.contentType) {
            case "ByCategory":
                return "Bar chart showing the distribution of posts number by each predicted category. ";
            case "ByChannel":
                return "Bar chart showing the distribution of posts number by channel";
            case "ByHour":
                return "Bar chart showing the distribution of posts number by day hour";
            default:
                return "";
        }
    }
}