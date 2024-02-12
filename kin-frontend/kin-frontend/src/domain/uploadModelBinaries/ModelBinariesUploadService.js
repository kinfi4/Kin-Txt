import axios from "axios";
import {showMessage} from "../../utils/messages";
import {BinariesTypes} from "../../config";

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export class ModelBinariesUploadService {
    constructor(serviceUrl, chunkSize = 1024 * 1024 * 5, modelCode) {
        this.serviceUrl = serviceUrl;
        this.chunkSize = chunkSize;
        this.modelCode = modelCode;
    }

    async uploadModelData(
        modelData,
        setModelFileUploadProgress,
        setTokenizerFileUploadProgress,
    ) {
        let promiseModelUploadSuccess = Promise.resolve(true);
        let promiseTokenizerUploadSuccess = Promise.resolve(true);
        let promiseStopWordsUploadSuccess = Promise.resolve(true);

        if (modelData.modelFile) {
            promiseModelUploadSuccess = this.uploadBlobByChunks(
                modelData.modelFile,
                "/blobs/upload",
                BinariesTypes.MODEL,
                setModelFileUploadProgress,
            );
        }

        if (modelData.tokenizerFile) {
            promiseTokenizerUploadSuccess = this.uploadBlobByChunks(
                modelData.tokenizerFile,
                "/blobs/upload",
                BinariesTypes.TOKENIZER,
                setTokenizerFileUploadProgress,
            );
        }

        if (modelData.preprocessingConfig.stopWordsFile) {
            promiseStopWordsUploadSuccess = this.uploadFile(
                modelData.preprocessingConfig.stopWordsFile,
                "/blobs/upload",
                BinariesTypes.STOP_WORDS,
            )
        }

        if (!(await promiseModelUploadSuccess)) {
            showMessage([
                {
                    message: `Error while uploading model file...`,
                    type: "danger",
                },
            ]);
            return;
        }
        if (!(await promiseTokenizerUploadSuccess)) {
            showMessage([
                {
                    message: `Error while uploading tokenizer file...`,
                    type: "danger",
                },
            ]);
            return;
        }
        if (!(await promiseStopWordsUploadSuccess)) {
            showMessage([
                {
                    message: `Error while uploading stop words file...`,
                    type: "danger",
                },
            ]);
        }
    }

    async uploadBlobByChunks(
        blob,
        uploadUrl,
        blobType,
        progressCallback,
    ) {
        const totalChunks = Math.ceil(blob.size / this.chunkSize);
        const chunkProgress = 100 / totalChunks;
        let chunkNumber = 0;
        let start = 0;
        let end = 0;

        const completeUploadUrl = `${this.serviceUrl}${uploadUrl}`;

        const uploadNextChunk = async () => {
            if (chunkNumber < totalChunks) {
                if (chunkNumber === totalChunks - 1) {
                    // that means we're uploading the last chunk
                    progressCallback({progress: 100, isValidating: true});
                }

                end = start + this.chunkSize;
                const chunk = blob.slice(start, end);

                const formData = new FormData();
                formData.append("chunk", chunk);
                formData.append("chunk_index", chunkNumber);
                formData.append("total_chunks", totalChunks);
                formData.append("blob_type", blobType);
                formData.append("model_code", this.modelCode);
                formData.append("chuck_hash", await this.calculateHash(chunk));

                try {
                    const success = await this._uploadSingleBlob(completeUploadUrl, formData);
                    if (!success) {
                        return false;
                    }

                    progressCallback({progress: Number((chunkNumber + 1) * chunkProgress), isValidating: false});

                    chunkNumber++;
                    start = end;

                    return await uploadNextChunk();
                } catch (e) {
                    showMessage([{message: `Error while uploading the file... \n${e}}`, type: "danger"}]);
                    return false;
                }
            } else {
                progressCallback({progress: 100, isValidating: false});
                return true;
            }
        };

        return await uploadNextChunk();
    }

    async uploadFile(file, uploadUrl, blobType) {
        const formData = new FormData();
        formData.append("chunk", file);
        formData.append("chunk_index", 0);
        formData.append("total_chunks", 1);
        formData.append("blob_type", blobType);
        formData.append("model_code", this.modelCode);
        formData.append("chuck_hash", await this.calculateHash(file));

        const completeUploadUrl = `${this.serviceUrl}${uploadUrl}`;

        return await this._uploadSingleBlob(completeUploadUrl, formData);
    }

    async calculateHash(file) {
        const buffer = await file.arrayBuffer();
        const hash = await crypto.subtle.digest("SHA-256", buffer);
        return Array.from(new Uint8Array(hash)).map((b) => b.toString(16).padStart(2, "0")).join("");
    }

    async _uploadSingleBlob(uploadUrl, formData) {
        const response = await axios({
            url: uploadUrl,
            method: "POST",
            data: formData,
            headers: {
                Authorization: `Token ${localStorage.getItem("token")}`,
                "Content-Type": "multipart/form-data",
            },
        });

        return response.status === 200;
    }
}
