export class ChartDataFactory {
    createChartData(visualizationCategory) {
        if (visualizationCategory.includes("+")) {
            const [visualizationCategory1, visualizationCategory2] =
                visualizationCategory.split("+");
            return {
                [visualizationCategory1]: this.createChartData(
                    visualizationCategory1
                ),
                [visualizationCategory2]: this.createChartData(
                    visualizationCategory2
                ),
            };
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
                    {
                        date: "2020-01-01",
                        value1: 300,
                        value2: 500,
                        value3: 234,
                        color: "#FF0000",
                    },
                    {
                        date: "2020-01-02",
                        value1: 400,
                        value2: 100,
                        value3: 430,
                        color: "#FF0000",
                    },
                    {
                        date: "2020-01-03",
                        value1: 100,
                        value2: 200,
                        value3: 300,
                        color: "#FF0000",
                    },
                    {
                        date: "2020-01-04",
                        value1: 600,
                        value2: 324,
                        value3: 234,
                        color: "#FF0000",
                    },
                    {
                        date: "2020-01-05",
                        value1: 400,
                        value2: 250,
                        value3: 243,
                        color: "#FF0000",
                    },
                    {
                        date: "2020-01-06",
                        value1: 400,
                        value2: 349,
                        value3: 300,
                        color: "#FF0000",
                    },
                    {
                        date: "2020-01-07",
                        value1: 100,
                        value2: 280,
                        value3: 200,
                        color: "#FF0000",
                    },
                    {
                        date: "2020-01-08",
                        value1: 230,
                        value2: 340,
                        value3: 120,
                        color: "#FF0000",
                    },
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
                ];
            case "ByDate":
                return [
                    {date: "2020-01-01", value: 400, color: "#318c72"},
                    {date: "2020-01-02", value: 300, color: "#5da45d"},
                    {date: "2020-01-03", value: 300, color: "#6262cc"},
                    {date: "2020-01-04", value: 200, color: "#86863a"},
                    {date: "2020-01-05", value: 400, color: "#b77070"},
                ];
            case "ByDateByChannel":
                return [
                    {
                        date: "2020-01-01",
                        value1: 40,
                        value2: 100,
                        color: "#FF0000",
                    },
                    {
                        date: "2020-01-02",
                        value1: 120,
                        value2: 100,
                        color: "#FF0000",
                    },
                    {
                        date: "2020-01-03",
                        value1: 65,
                        value2: 30,
                        color: "#FF0000",
                    },
                    {
                        date: "2020-01-04",
                        value1: 48,
                        value2: 123,
                        color: "#FF0000",
                    },
                    {
                        date: "2020-01-05",
                        value1: 94,
                        value2: 120,
                        color: "#FF0000",
                    },
                    {
                        date: "2020-01-06",
                        value1: 94,
                        value2: 20,
                        color: "#FF0000",
                    },
                    {
                        date: "2020-01-07",
                        value1: 100,
                        value2: 84,
                        color: "#FF0000",
                    },
                ];
            case "ByChannel":
                return [
                    {name: "Channel 1", value: 400, color: "#6262cc"},
                    {name: "Channel 2", value: 300, color: "#5da45d"},
                    {name: "Channel 3", value: 300, color: "#b77070"},
                ];
            case "ByChannelByCategory":
                return [
                    {
                        name: "Channel 1",
                        value1: 400,
                        value2: 200,
                        value3: 250,
                        color: "#6262cc",
                    },
                    {
                        name: "Channel 2",
                        value1: 300,
                        value2: 290,
                        value3: 120,
                        color: "#5da45d",
                    },
                    {
                        name: "Channel 3",
                        value1: 300,
                        value2: 100,
                        value3: 90,
                        color: "#b77070",
                    },
                ];
            default:
                return [];
        }
    }
}
