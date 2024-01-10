import React from "react";

import styles from "./styles/SettingsOptionsStyles.module.css";

import SelectItem from "../../../../../../common/select/SelectItem";
import {capitalizeFirstLetter} from "../../../../../../utils/utils";

const SettingsFormOptionSelect = ({data, setData, optionName, title, options, defaultValue, style=null}) => {
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
                <SelectItem
                    defaultValue={defaultValue}
                    isSearchable={true}
                    name="language"
                    value={{
                        value: data.preprocessingConfig[optionName],
                        label: capitalizeFirstLetter(data.preprocessingConfig[optionName]),
                    }}
                    onChange={(newValue) =>
                        setData({
                            ...data,
                            preprocessingConfig: {
                                ...data.preprocessingConfig,
                                [optionName]: newValue.value,
                            }
                        })
                    }
                    options={options}
                    width={"100%"}
                />
            </div>
        </div>
    );
};

export default SettingsFormOptionSelect;