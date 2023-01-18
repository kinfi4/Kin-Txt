import {Store} from "react-notifications-component";

export let showMessage = (messages) => {
    messages.forEach(el => {
        let message = el.message;
        if(el.message === undefined || el.message === null) {
            message = "Something went wrong. Sorry."
        }

        Store.addNotification({
            title: '',
            message: message,
            type: el.type,                           // 'default', 'success', 'info', 'warning'
            container: 'top-right',                  // where to position the notifications
            animationIn: ["animated", "fadeIn"],
            animationOut: ["animated", "fadeOut"],
            dismiss: {
                duration: 10000
            }
        })
    })
}
