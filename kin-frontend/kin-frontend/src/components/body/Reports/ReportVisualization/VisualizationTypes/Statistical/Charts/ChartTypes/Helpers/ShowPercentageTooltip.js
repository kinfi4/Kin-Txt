import tooltipStyles from "./PercentageTooltipStyles.module.css";

export const PercentageTooltip = ({active, payload, normalize=false, total=0}) => {
    if (active && payload && payload.length) {
        function normalizeValue(value) {
            if (!normalize) {
                return value;
            }

            return (value / total)*100;
        }

        return (
            <div className={tooltipStyles.container}>
                {
                    payload.length > 1 && (
                        <div className={tooltipStyles.item}>
                            {payload[0].payload.name}
                        </div>
                    )
                }

                {
                    payload.map((item, index) => (
                        <div key={index} className={tooltipStyles.item}>
                            <span
                                className={tooltipStyles.label}
                                style={{color: item.color}}
                            >
                                {item.name}
                            </span>
                            <span
                                className={tooltipStyles.value}
                                style={{color: item.color}}
                            >
                                {
                                    `${normalizeValue(item.value).toFixed(2)}%`
                                }
                            </span>
                        </div>
                    ))
                }
            </div>
        );
    }

    return null;
};
