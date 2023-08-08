import React from "react";

import statsStyles from "../../../Reports/Statistics.module.css";
import commonStyles from "../../../../common/CommonStyles.module.css";
import styles from "./DefaultFormStyles.module.css";
import formStyles from "../../../Models/ModelForm/ModelFormStyles.module.css";
import statsCss from "../../../Reports/Statistics.module.css";

import FormInput from "../../../../common/formInputName/FormInput";
import {Cell, Pie, PieChart, ResponsiveContainer} from "recharts";
import FormChart from "./Charts/FormChart";


const TemplateDefaultForm = ({isUpdateForm=false, data, setData}) => {
    const onChartSelected = (chartId) => {
        if(data.charts.includes(chartId)) {
            setData({...data, charts: data.charts.filter((chart) => chart !== chartId)});
            return;
        }

        setData({...data, charts: [...data.charts, chartId]});
    }

    return (
        <div className={statsStyles.statsContainer}>
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
                        <div className={`${styles.selectButton} ${styles.createTemplateButton}`}>
                            CREATE TEMPLATE
                        </div>
                    </div>
                </div>

                <div className={formStyles.formInputContainer}>
                    <div className={styles.selectButton}>SELECT ALL</div>
                    <div className={styles.selectButton}>UNSELECT ALL</div>
                </div>
            </div>

            <div className={styles.selectChartsContainer}>
                <h2>
                    Create your own visualization template to suit your needs.
                    Select all the charts you want to see in your future statistical reports
                </h2>
                <div className={styles.chartCategoryContainer}>
                    <h2>Pie Charts</h2>
                    <div className={styles.chartsListContainer}>
                        <FormChart
                            chartId={"ByCategory__Pie"}
                            onClick={onChartSelected}
                            isSelected={data.charts.includes("ByCategory__Pie")}
                        />
                        <FormChart
                            chartId={"ByChannel__Pie"}
                            onClick={onChartSelected}
                            isSelected={data.charts.includes("ByChannel__Pie")}
                        />
                        <FormChart
                            chartId={"ByChannel+ByCategory__TwoLevelPie"}
                            onClick={onChartSelected}
                            isSelected={data.charts.includes("ByChannel+ByCategory__TwoLevelPie")}
                        />
                    </div>
                </div>
                <div className={styles.chartCategoryContainer}>
                    <h2>Bar Charts</h2>
                    <div className={styles.chartsListContainer}>
                        <FormChart
                            chartId={"ByCategory__Bar"}
                            onClick={onChartSelected}
                            isSelected={data.charts.includes("ByCategory__Bar")}
                        />
                        <FormChart
                            chartId={"ByChannel__Bar"}
                            onClick={onChartSelected}
                            isSelected={data.charts.includes("ByChannel__Bar")}
                        />
                        <FormChart
                            chartId={"ByHour__Bar"}
                            onClick={onChartSelected}
                            isSelected={data.charts.includes("ByHour__Bar")}
                        />
                    </div>
                </div>
                <div className={styles.chartCategoryContainer}>
                    <h2>Line Charts</h2>
                    <div className={styles.chartsListContainer}>
                        <FormChart
                            chartId={"ByDate__Line"}
                            onClick={onChartSelected}
                            isSelected={data.charts.includes("ByDate__Line")}
                        />
                    </div>
                </div>
                <div className={styles.chartCategoryContainer}>
                    <h2>Area Charts</h2>
                    <div className={styles.chartsListContainer}>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TemplateDefaultForm;