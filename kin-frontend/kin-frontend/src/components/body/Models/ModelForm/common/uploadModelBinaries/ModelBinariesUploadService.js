import axios from "axios";

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export class ModelBinariesUploadService {
    constructor(serviceUrl, chunkSize= 1024 * 1024 * 5, modelCode) {
        this.serviceUrl = serviceUrl;
        this.chunkSize = chunkSize;
        this.modelCode = modelCode;
    }

    async uploadBlob(blob, uploadUrl, blobType, progressCallback, mergingStartedCallback) {
        const totalChunks = Math.ceil(blob.size / this.chunkSize);
        const chunkProgress = 100 / totalChunks;
        let chunkNumber = 0;
        let start = 0;
        let end = 0;

        const completeUploadUrl = `${this.serviceUrl}${uploadUrl}`;

        const uploadNextChunk = async () => {
            if (chunkNumber < totalChunks) {
                if(chunkNumber === totalChunks-1) {  // that means we're uploading the last chunk
                    mergingStartedCallback(true);
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
                    const response = await axios({
                        url: completeUploadUrl,
                        method: "POST",
                        data: formData,
                        headers: {
                            "Authorization": `Token ${localStorage.getItem("token")}`,
                            "Content-Type": "multipart/form-data",
                        }
                    });

                    if(response.status !== 200) {
                        return false;
                    }

                    progressCallback(Number((chunkNumber + 1) * chunkProgress));

                    chunkNumber++;
                    start = end;

                    return await uploadNextChunk();
                } catch (e) {
                    console.log(e);
                    return false;
                }
            } else {
                progressCallback(100);
                mergingStartedCallback(false);
                return true;
            }
        };

        return await uploadNextChunk();
    };

    async calculateHash(file) {
        const buffer = await file.arrayBuffer();
        const hash = await crypto.subtle.digest('SHA-256', buffer);
        return Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2, '0')).join('');
    }
}