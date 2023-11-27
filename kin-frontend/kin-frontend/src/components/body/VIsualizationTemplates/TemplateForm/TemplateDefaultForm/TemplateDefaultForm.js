import React from "react";

import statsStyles from "../../../Reports/Statistics.module.css";
import commonStyles from "../../../../../common/CommonStyles.module.css";
import styles from "./DefaultFormStyles.module.css";
import formStyles from "../../../Models/ModelForm/ModelFormStyles.module.css";
import statsCss from "../../../Reports/Statistics.module.css";

import FormInput from "../../../../../common/formInputName/FormInput";
import FormChart from "./Charts/FormChart";
import BackLink from "../../../../../common/backLink/BackLink";


const possibleCharts = {
    "Pie": {
        title: "Pie Chart",
        charts: ["ByCategory__Pie", "ByChannel__Pie", "ByChannel+ByCategory__TwoLevelPie"],
    },
    "Bar": {
        title: "Bar Chart",
        charts: ["ByCategory__Bar", "ByChannel__Bar", "ByHour__Bar", "ByChannelByCategory__StackedBar"],
    },
    "Line": {
        title: "Line Chart",
        charts: ["ByDate__Line", "ByDateByCategory__MultiLine", "ByDateByChannel__MultiLine"],
    },
    "Area": {
        title: "Area Chart",
        charts: ["ByDateByCategory__MultiArea"],
    },
    "Radar": {
        title: "Radar Chart",
        charts: ["ByCategory__Radar"],
    },
}


const TemplateDefaultForm = ({isUpdateForm=false, data, setData, onCreationCallback}) => {
    const onChartSelected = (chartId) => {
        if(data.charts.includes(chartId)) {
            setData({...data, charts: data.charts.filter((chart) => chart !== chartId)});
            return;
        }

        setData({...data, charts: [...data.charts, chartId]});
    }
    const onSelectAll = () => {
        setData({
            ...data,
            charts: Object.values(possibleCharts).reduce((acc, chartType) => {
                return acc.concat(chartType.charts);
            }, [])
        });
    }
    const onUnselectAll = () => {
        setData({...data, charts: []});
    }

    return (
        <div className={statsStyles.statsContainer}>
            <BackLink url={"/templates"} />

            <h1 className={commonStyles.pageTitle}>{isUpdateForm ? "Update Template" : "Create Template"}</h1>

            <div className={styles.upperFormBlock}>
                <div className={formStyles.formInputContainer}>
                    <label
                        id="templateName"
                        className={statsCss.generateReportFormLabel}
                    >
                        Give your template a name:
                    </label>

                    <FormInput
                        placeholder={"Template name"}
                        id={"templateName"}
                        value={data.name}
                        onChange={(event) => setData({...data, name: event.target.value})}
                    />

                    <div>
                        <div
                            className={`${styles.selectButton} ${styles.createTemplateButton}`}
                            onClick={onCreationCallback}
                        >
                            {isUpdateForm ? "UPDATE TEMPLATE" : "CREATE TEMPLATE"}
                        </div>
                    </div>
                </div>

                <div className={formStyles.formInputContainer}>
                    <div className={styles.selectButton} onClick={onSelectAll}>SELECT ALL</div>
                    <div className={styles.selectButton} onClick={onUnselectAll}>UNSELECT ALL</div>
                </div>
            </div>

            <div className={styles.selectChartsContainer}>
                <h2>
                    Create your own visualization template to suit your needs.
                    Select all the charts you want to see in your future statistical reports
                </h2>
                {
                    Object.keys(possibleCharts).map((chartType) => {
                        return (
                            <div key={chartType} className={styles.chartCategoryContainer}>
                                <h2>{possibleCharts[chartType].title}</h2>

                                <div className={styles.chartsListContainer}>
                                    {
                                        possibleCharts[chartType].charts.map((chartId) => {
                                            return (
                                                <FormChart
                                                    key={chartId}
                                                    chartId={chartId}
                                                    isSelected={data.charts.includes(chartId)}
                                                    onClick={() => onChartSelected(chartId)}
                                                />
                                            );
                                        })
                                    }
                                </div>
                            </div>
                        );
                    })
                }
            </div>
        </div>
    );
};

export default TemplateDefaultForm;