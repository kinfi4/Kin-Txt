import React, {useState} from "react";

import commonCss from "../../common/CommonStyles.module.css";

import Input from "../input/Input";
import Button from "../button/Button";

const InputModalWindow = ({
    title,
    actionCallback,
    inputPlaceholder,
    submitPlaceholder,
    ...props
}) => {
    const [input, setInput] = useState({value: ""});

    return (
        <div className={commonCss.enterLinkContainer}>
            <h4>{title}</h4>
            <Input
                value={input.value}
                onChange={(event) => setInput({value: event.target.value})}
                placeholder={inputPlaceholder}
            />

            <Button
                text={submitPlaceholder}
                onClick={(event) => actionCallback(input.value)}
            />
        </div>
    );
};

export default InputModalWindow;
