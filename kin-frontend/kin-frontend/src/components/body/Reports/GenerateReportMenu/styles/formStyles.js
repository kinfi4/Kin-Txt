export const selectStyles = {
    control: (styles) => ({
        ...styles,
        backgroundColor: "#1d2c3b",
        border: '1px solid #2CA884',
        '&:hover': {
            border: '1px solid #2CA884',
        },
        minWidth: "360px",
        maxWidth: "360px",
        cursor: "pointer"
    }),
    singleValue: (styles) => ({ ...styles, color: "#cecece" }),
    option: (styles) => ({ ...styles, cursor: "pointer" }),
}

export const multiSelectStyles = {
    control: (styles) => ({
        ...styles,
        cursor: "text",
        backgroundColor: "#1d2c3b",
        border: '1px solid #2CA884',
        '&:hover': {
            border: '1px solid #2CA884',
        },
        minHeight: '150px',
        maxHeight: "250px",
        minWidth: "360px",
        maxWidth: "360px",
    }),
    input: (styles) => ({ ...styles, color: "#cecece" }),
    placeholder: (styles) => ({ ...styles, color: "#bdbdbd" }),
    menu: (provided, state) => ({
        ...provided,
        width: 'fit-content',
        marginLeft: 0,
        marginTop: 0,
    }),
    multiValue: (base, state) => ({
        ...base,
        backgroundColor: '#64617E',
        color: 'white',
        borderRadius: '3px',
        padding: '5px',
    }),
    multiValueLabel: (base, state) => ({
        ...base,
        color: "#cecece",
        fontWeight: "bold",
    }),
    multiValueRemove: (base, state) => ({
        ...base,
        cursor: 'pointer',
    }),
}
