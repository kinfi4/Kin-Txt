import {SupportedLanguages} from "../config";

export class ModelValidator {
    constructor(data) {
        this.data = data;
    }

    validate(forUpdate=false) {
        let isValid = true;
        let errors = [];

        if (!this.data.name) {
            isValid = false;
            errors.push("You have to name your model");
        }
        if (!this.data.code) {
            isValid = false;
            errors.push("You have to specify model code");
        }
        // check if language is one of the supported languages
        if(!SupportedLanguages.isSupported(this.data.preprocessingConfig.language)) {
            isValid = false;
            errors.push("You have to specify language for preprocessing");
        }
        if(this.data.preprocessingConfig.lemmatize && this.data.preprocessingConfig.language === SupportedLanguages.OTHER) {
            isValid = false;
            errors.push("Currently lemmatization is not supported for the language you have chosen");
        }
        if(!forUpdate && !this.data.modelFile) {
            isValid = false;
            errors.push("You have to upload model file");
        }
        if(!forUpdate && !this.data.tokenizerFile) {
            isValid = false;
            errors.push("You have to upload tokenizer file");
        }
        if(
            this.data.preprocessingConfig.stopWordsFile &&
            !this.data.preprocessingConfig.stopWordsFile.name.split(".").pop().match(/^(txt|csv|json)$/)
        ) {
            isValid = false;
            errors.push("Stop words file must be in txt, csv or json format");
        }

        return [isValid, errors];
    }
}