export class ModelValidator {
    constructor(data) {
        this.data = data;
    }

    validate() {
        if (!this.data.name) {
            return [false, "You have to name your model"]
        }
        if (!this.data.code) {
            return [false, "You have to specify model code"];
        }

        return [true, null]
    }
}