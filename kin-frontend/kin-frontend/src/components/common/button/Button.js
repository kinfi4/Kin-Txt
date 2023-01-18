import defaultButtonCss from './Button.module.css'


function Button(props) {
    return (
        <>
            <div
                className={defaultButtonCss.defaultButton}
                onClick={(event) => props.onClick(event)}
                style={props.styles}
            >
                { props.text }
            </div>
        </>
    )
}


export default Button;