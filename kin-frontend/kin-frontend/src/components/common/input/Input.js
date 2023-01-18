import inputCss from './Input.module.css'


function Input(props) {
    return (
        <>
            <div className={inputCss['input-container']}>
                <input
                    type={props.type ? props.type : "text"}
                    onChange={(e => props.onChange(e))}
                    value={props.value}
                    id={props.id}

                    required
                />
                <label>{props.placeholder}</label>
            </div>
        </>
    )
}

export default Input;