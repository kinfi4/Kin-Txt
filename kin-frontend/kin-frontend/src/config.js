export const NEWS_SERVICE_URL = "http://localhost:8080/api/news/v1"
export const STATISTICS_SERVICE_URL = "http://localhost:8080/api/statistics/v1"
export const FILE_STORAGE_URL = "http://localhost:8080/api/news/v1"
export const MODEL_TYPES_URL = "http://localhost:8080/api/model-types/v1"

// export const NEWS_SERVICE_URL = "http://kin-api-gateway:8080/api/news/v1"
// export const STATISTICS_SERVICE_URL = "http://kin-api-gateway:8080/api/statistics/v1"
// export const FILE_STORAGE_URL = "http://kin-api-gateway:8080"
// export const MODEL_TYPES_URL = "http://kin-api-gateway:8080/api/reports-builder/v1"

export const MS_IN_MINUTE = 60000

export const REPORT_STATUS_POSTPONED = "Postponed";
export const REPORT_STATUS_PROCESSING = "Processing";
export const REPORT_STATUS_CREATED = "New";

export const WORD_CLOUD_REPORT = "WordCloud"
export const STATISTICAL_REPORT = "Statistical"


export const NOT_FOUND_STATUS_CODE = 404
export const REQUEST_IS_TOO_EARLY_STATUS_CODE = 425

export const ModelTypes = {
    SKLEARN_MODEL: "Sklearn Model",
    KERAS: "Keras Model",
}

export const ModelStatuses = {
    VALIDATED: "Validated",
    VALIDATION_FAILED: "ValidationFailed",
    VALIDATING: "Validating",
    CREATED: "Created"
}
