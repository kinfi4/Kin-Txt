import {STATISTICAL_REPORT} from "../config";

export class GenerateReportRequestValidator {
    constructor(data) {
        this.data = data;
    }

    validate() {
        let isValid = true;
        let errorMessages = [];

        if (!this.data.channels.length) {
            isValid = false;
            errorMessages.push("You didn't specify any channel");
        }
        if (!this.data.name) {
            isValid = false;
            errorMessages.push("You have to name your report");
        }
        if (!this.data.modelCode) {
            isValid = false;
            errorMessages.push("You have to specify model code");
        }
        if (!this.data.templateId && this.data.reportType === STATISTICAL_REPORT) {
            isValid = false;
            errorMessages.push("You have to specify template");
        }

        return [isValid, errorMessages]
    }
}