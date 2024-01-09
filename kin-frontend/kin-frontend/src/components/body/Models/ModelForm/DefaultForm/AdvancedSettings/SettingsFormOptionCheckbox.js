import React from "react";
import styles from "./styles/SettingsOptionsStyles.module.css"


const SettingsFormOptionCheckbox = ({data, setData, optionName, title, style=null}) => {
    return (
        <div
            style={style? style : {}}
        >
            <div className={styles.checkboxOptionsContainer}>
                <label
                    id={optionName}
                    className={styles.label}
                >
                    {title}
                </label>
                <input
                    type="checkbox"
                    id={optionName}
                    checked={data.preprocessingConfig[optionName]}
                    onChange={(event) =>
                        setData({
                            ...data,
                            preprocessingConfig: {...data.preprocessingConfig, [optionName]: event.target.checked}
                        })
                    }
                />
            </div>
        </div>
    );
};

export default SettingsFormOptionCheckbox;