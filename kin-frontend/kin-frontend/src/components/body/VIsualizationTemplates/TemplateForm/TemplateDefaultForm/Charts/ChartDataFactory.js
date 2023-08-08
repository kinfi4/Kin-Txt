export class ChartDataFactory {
    createChartData(visualizationCategory) {
        if(visualizationCategory.includes("+")) {
            const [visualizationCategory1, visualizationCategory2] = visualizationCategory.split("+");
            return {
                [visualizationCategory1]: this.createChartData(visualizationCategory1),
                [visualizationCategory2]: this.createChartData(visualizationCategory2),
            }
        }

        switch (visualizationCategory) {
            case "ByCategory":
                return [
                    {name: "Category 1", value: 400, color: "#b77070"},
                    {name: "Category 2", value: 300, color: "#5da45d"},
                    {name: "Category 3", value: 300, color: "#6262cc"},
                    {name: "Category 4", value: 200, color: "#86863a"},
                ];
            case "ByDateByCategory":
                return [
                    {date: "2020-01-01", name: "Category 1", value: 400, color: "#FF0000"},
                    {date: "2020-01-02", name: "Category 1", value: 300, color: "#FF0000"},
                    {date: "2020-01-03", name: "Category 1", value: 300, color: "#FF0000"},
                    {date: "2020-01-04", name: "Category 1", value: 200, color: "#FF0000"},
                    {date: "2020-01-01", name: "Category 2", value: 400, color: "#00FF00"},
                    {date: "2020-01-02", name: "Category 2", value: 300, color: "#00FF00"},
                    {date: "2020-01-03", name: "Category 2", value: 300, color: "#00FF00"},
                    {date: "2020-01-04", name: "Category 2", value: 200, color: "#00FF00"},
                ];
            case "ByHour":
                return [
                    {name: "00:00", value: 400, color: "#318c72"},
                    {name: "01:00", value: 300, color: "#5da45d"},
                    {name: "02:00", value: 300, color: "#6262cc"},
                    {name: "03:00", value: 200, color: "#86863a"},
                    {name: "04:00", value: 400, color: "#b77070"},
                    {name: "05:00", value: 300, color: "#5da45d"},
                    {name: "06:00", value: 300, color: "#6262cc"},
                    {name: "07:00", value: 200, color: "#86863a"},
                    {name: "08:00", value: 400, color: "#b77070"},
                    {name: "09:00", value: 300, color: "#5da45d"},
                    {name: "10:00", value: 300, color: "#6262cc"},
                    {name: "11:00", value: 200, color: "#86863a"},
                    {name: "12:00", value: 400, color: "#b77070"},
                    {name: "13:00", value: 300, color: "#5da45d"},
                    {name: "14:00", value: 300, color: "#6262cc"},
                    {name: "15:00", value: 200, color: "#86863a"},
                    {name: "16:00", value: 400, color: "#b77070"},
                    {name: "17:00", value: 300, color: "#5da45d"},
                    {name: "18:00", value: 300, color: "#6262cc"},
                    {name: "19:00", value: 200, color: "#86863a"},
                    {name: "20:00", value: 400, color: "#b77070"},
                    {name: "21:00", value: 300, color: "#5da45d"},
                    {name: "22:00", value: 300, color: "#6262cc"},
                    {name: "23:00", value: 200, color: "#86863a"},
                ]
            case "ByDate":
                return [
                    {date: "2020-01-01", value: 400, color: "#318c72"},
                    {date: "2020-01-02", value: 300, color: "#5da45d"},
                    {date: "2020-01-03", value: 300, color: "#6262cc"},
                    {date: "2020-01-04", value: 200, color: "#86863a"},
                    {date: "2020-01-05", value: 400, color: "#b77070"},
                ]
            case "ByChannel":
                return [
                    {name: "Channel 1", value: 400, color: "#6262cc"},
                    {name: "Channel 2", value: 300, color: "#5da45d"},
                    {name: "Channel 3", value: 300, color: "#b77070"},
                ];
            default:
                return [];
        }
    }
}
