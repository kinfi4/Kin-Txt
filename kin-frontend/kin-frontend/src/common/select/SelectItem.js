import React from "react";
import Select from "react-select";


const SelectItem = ({defaultValue, name, value, onChange, options, width= "360px", styles= {}}) => {
    const selectStyles = {
        control: (styles) => ({
            ...styles,
            backgroundColor: "#1d2c3b",
            border: "1px solid #2CA884",
            "&:hover": {
                border: "1px solid #2CA884",
            },
            cursor: "pointer",
            width: width,
        }),
        singleValue: (styles) => ({...styles, color: "#cecece"}),
        option: (styles) => ({...styles, cursor: "pointer"}),
    };

    return (
        <Select
            defaultValue={defaultValue}
            isSearchable={true}
            name={name}
            value={value}
            onChange={onChange}
            options={options}
            styles={{
                ...selectStyles,
                ...styles,
            }}
        />
    );
};

export default SelectItem;