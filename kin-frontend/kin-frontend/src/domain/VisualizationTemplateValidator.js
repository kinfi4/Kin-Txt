export class VisualizationTemplateValidator {
    constructor(data) {
        this.data = data;
    }

    validate() {
        let isValid = true;
        let errorMessages = [];

        if (!this.data.name) {
            isValid = false;
            errorMessages.push("You have to name your template");
        }

        if(this.data.visualizationDiagramTypes.length === 0) {
            isValid = false;
            errorMessages.push("You have to specify at least one diagram type");
        }

        return [isValid, errorMessages]
    }

}
