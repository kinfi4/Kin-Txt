import axios from "axios";

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export class ModelBinariesUploadService {
    constructor(serviceUrl, chunkSize= 1024 * 1024 * 5, modelCode) {
        this.serviceUrl = serviceUrl;
        this.chunkSize = chunkSize;
        this.modelCode = modelCode;
    }

    async uploadBlob(blob, uploadUrl, blobType, progressCallback) {
        const totalChunks = Math.ceil(blob.size / this.chunkSize);
        const chunkProgress = 100 / totalChunks;
        let chunkNumber = 0;
        let start = 0;
        let end = 0;

        const completeUploadUrl = `${this.serviceUrl}${uploadUrl}`;

        const uploadNextChunk = async () => {
            if (end <= blob.size) {
                const chunk = blob.slice(start, end);

                const formData = new FormData();
                formData.append("chunk", chunk);
                formData.append("chunk_index", chunkNumber);
                formData.append("total_chunks", totalChunks);
                formData.append("blob_type", blobType);
                formData.append("model_code", this.modelCode);

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
                    end = start + this.chunkSize;

                    return await uploadNextChunk();
                } catch (e) {
                    console.log(e);
                    return false;
                }
            } else {
                progressCallback(100);
                return true;
            }
        };

        return await uploadNextChunk();
    };
}