import {showMessage} from "./messages";
import {
    ReportNotFoundError,
    SomethingWentWrongError
} from "../components/body/Reports/ReportVisualization/helpers/Errors";
import {NOT_FOUND_STATUS_CODE} from "../config";

export function truncate(str, n){
    return (str.length > n) ? str.slice(0, n-1) + "..." : str;
}


export function translateDateToString(date) {
    return `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}`;
}

export function shuffle(array) {
    return array.sort(() => 0.5 - Math.random());
}

export function downloadFile(url, contentType="csv") {
    const token = localStorage.getItem("token");
    showMessage([{message: "Download will start soon...", type: "success"}])

    fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": 'application/' + contentType,
            'Authorization': `Token ${token}`,
        },
    })
        .then((response) => {
            if(response.status === NOT_FOUND_STATUS_CODE) {
                throw new ReportNotFoundError();
            }

            if(response.status !== 200) {
                throw new SomethingWentWrongError();
            }

            response.blob().then(blob => {
                showMessage([{message: 'Downloading started', type: 'success'}])

                const url = window.URL.createObjectURL(
                    new Blob([blob]),
                );

                const link = document.createElement('a');

                link.href = url;
                link.download = "Report-Data." + contentType;

                document.body.appendChild(link);
                link.click();
                link.parentNode.removeChild(link);
            })
        })
        .catch(err => {
            if(err instanceof ReportNotFoundError) {
                showMessage([{message: "Report data not found :(((", type: 'danger'}])
            } else if (err instanceof SomethingWentWrongError) {
                showMessage([{message: "Something went wrong during report download :(", type: "danger"}])
            } else {
                showMessage([{message: "Report exporting failed(", type: 'danger'}])
            }
        });

}

export function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}


export function transformLargeNumberToReadable(number) {
    if (number < 10000) {
        return number;
    }

    if (number < 1000000) {
        return (number / 1000).toFixed(1) + "K";
    }

    return (number / 1000000).toFixed(1) + "M";
}
