import React from "react";

import styles from "./styles/SettingsOptionsStyles.module.css";

const SettingsFormOptionNumber = ({data, setData, optionName, title, style=null}) => {
    return (
        <div
            style={style? style : {}}
        >
            <div className={styles.inputSelectContainer}>
                <label
                    id={optionName}
                    className={styles.label}
                >
                    {title}
                </label>
                <input
                    type="number"
                    id={optionName}
                    value={data.preprocessingConfig[optionName]}
                    onChange={(event) =>
                        setData({
                            ...data,
                            preprocessingConfig: {...data.preprocessingConfig, [optionName]: event.target.value}
                        })
                    }
                    className={styles.inputNumber}
                />
            </div>
        </div>
    );
};

export default SettingsFormOptionNumber;