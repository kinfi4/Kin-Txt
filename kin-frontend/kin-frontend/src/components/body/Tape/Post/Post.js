import React, {useEffect} from 'react';

const Post = (props) => {
    const postClassName = props.postLink.replace('/', '-')

    useEffect(() => {
        const script = document.createElement('script');
        script.src = "https://telegram.org/js/telegram-widget.js?21";

        script.setAttribute('data-telegram-Post', props.postLink);

        script.setAttribute('data-dark-color', 'BF8EFF');
        script.setAttribute('data-userpic', 'true');
        script.setAttribute('data-color', '000');
        // script.setAttribute('data-dark', '1');
        script.setAttribute('data-background', 'FFF');
        script.setAttribute('data-color-scheme', 'light');
        script.async = true;

        document.querySelector(`.${postClassName}`).appendChild(script);
    }, [postClassName, props.postLink])

    return (
        <div className={postClassName} style={{width: "70%", marginBottom: "15px"}}></div>
    );
};

export default Post;