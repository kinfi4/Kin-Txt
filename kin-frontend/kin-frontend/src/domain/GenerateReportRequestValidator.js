import {STATISTICAL_REPORT} from "../config";

export class GenerateReportRequestValidator {
    constructor(data) {
        this.data = data;
    }

    validate() {
        if (!this.data.channels.length) {
            return [false, "You didn't specify any channel"]
        }
        if (!this.data.name) {
            return [false, "You have to name your report"]
        }
        if (!this.data.modelCode) {
            return [false, "You have to specify model code"];
        }
        if (!this.data.templateId && this.data.reportType === STATISTICAL_REPORT) {
            return [false, "You have to specify template"];
        }

        return [true, null]
    }
}