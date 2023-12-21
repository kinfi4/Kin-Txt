import React from "react";
import styles from "./Form.module.css";

const FormInput = ({id, value, placeholder, onChange, style, ...props}) => {
    return (
        <input
            type="text"
            value={value}
            onChange={onChange}
            id={id}
            placeholder={placeholder}
            className={styles.formInput}
            style={style}
            {...props}
        />
    );
};

export default FormInput;
