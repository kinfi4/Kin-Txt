import tooltipStyles from "./PercentageTooltipStyles.module.css";

export const PercentageTooltip = ({active, payload, label}) => {
    if (active && payload && payload.length) {
        const total = payload.reduce((acc, item) => acc + item.value, 0);

        return (
            <div className={tooltipStyles.container}>
                {payload.map((item, index) => (
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
                            {`${item.value.toFixed(2)}%`}
                        </span>
                    </div>
                ))}
            </div>
        );
    }

    return null;
};
