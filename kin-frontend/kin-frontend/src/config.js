export const STATISTICS_SERVICE_URL = process.env.REACT_APP_STATISTICS_SERVICE_URL || "http://localhost:8080/api/statistics/v1";
export const MODEL_TYPES_URL = process.env.REACT_APP_MODEL_TYPES_URL || "http://localhost:8080/api/model-types/v1";
export const GENERIC_REPORTS_BUILDER_URL = process.env.REACT_APP_GENERIC_REPORTS_BUILDER_URL || "http://localhost:8080/api/generic-builder/v1";


export const REPORT_STATUS_POSTPONED = "Postponed";
export const REPORT_STATUS_PROCESSING = "Processing";
export const REPORT_STATUS_CREATED = "New";

export const WORD_CLOUD_REPORT = "WordCloud";
export const STATISTICAL_REPORT = "Statistical";

export const NOT_FOUND_STATUS_CODE = 404;

export const ModelTypes = {
    SKLEARN_MODEL: "Sklearn Model",
    KERAS: "Keras Model",
};

export const VisualizationPossibleModelTypes = {
    BUILTIN: "Built-in Model",
    SKLEARN_MODEL: "Sklearn Model",
    KERAS: "Keras Model",
};

export const ModelStatuses = {
    VALIDATED: "Validated",
    VALIDATION_FAILED: "ValidationFailed",
    VALIDATING: "Validating",
    CREATED: "Created",
};

export const DatasourceTypes = {
    TELEGRAM: "telegram",
    TWITTER: "twitter",
    REDDIT: "reddit",
};

export const BinariesTypes = {
    MODEL: "model",
    TOKENIZER: "tokenizer",
    STOP_WORDS: "stop_words",
};

export const SupportedLanguages = {
    UKRAINIAN: {label: "Ukrainian", value: "uk"},
    RUSSIAN: {label: "Russian", value: "ru"},
    ENGLISH: {label: "English", value: "en"},
    OTHER: {label: "Other", value: "other"},

    getLanguageByValue: (languageValue) => {
        for (const language of Object.values(SupportedLanguages)) {
            if (language.value === languageValue) {
                return language;
            }
        }
    },

    isSupported(language) {
        return Object.values(SupportedLanguages).includes(language);
    }
};

export const PossibleTruncatePaddingTypes = {
    Pre: "pre",
    Post: "post",

    getOptionsForSelect: () => {
        return [{value: "pre", label: "Pre"}, {value: "post", label: "Post"}];
    },
    getPaddingTypeByValue: (value) => {
        if(value === "pre") {
            return PossibleTruncatePaddingTypes.Pre;
        } else if(value === "post") {
            return PossibleTruncatePaddingTypes.Post;
        } else {
            return null;
        }
    },
};
