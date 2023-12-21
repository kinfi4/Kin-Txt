import React from "react";
import inputCss from "./Input.module.css";

function Input({type = "text", onChange, value, id, placeholder}) {
    return (
        <>
            <div className={inputCss["input-container"]}>
                <input
                    type={type ? type : "text"}
                    onChange={(e) => onChange(e)}
                    value={value}
                    id={id}
                    required
                />
                <label>{placeholder}</label>
            </div>
        </>
    );
}

export default Input;
