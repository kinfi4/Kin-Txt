class ModelBinariesUploadService {
    constructor(serviceUrl, chunkSize= 1024 * 1024 * 10, progressCallback) {
        this.serviceUrl = serviceUrl;
        this.chunkSize = chunkSize;
        this.progressCallback = progressCallback;
    }

    async uploadBlob(blob, uploadUrl, blobType) {
        const totalChunks = Math.ceil(blob.size / this.chunkSize);
        const chunkProgress = 100 / totalChunks;
        let chunkNumber = 0;
        let start = 0;
        let end = 0;


        const uploadNextChunk = async () => {
            if (end <= blob.size) {
                const chunk = blob.slice(start, end);

                const formData = new FormData();
                formData.append("chunk", chunk);
                formData.append("chunk_index", chunkNumber);
                formData.append("total_chunks", totalChunks);
                formData.append("blob_type", blobType);
                formData.append("model_code", blobType);

                fetch("http://localhost:8000/upload", {
                    method: "POST",
                    body: formData,
                })
                    .then((response) => response.json())
                    .then((data) => {
                        console.log({ data });

                        this.progressCallback(Number((chunkNumber + 1) * chunkProgress));

                        chunkNumber++;
                        start = end;
                        end = start + this.chunkSize;

                        uploadNextChunk();
                    })
                    .catch((error) => {
                        console.error("Error uploading chunk:", error);
                    });
            } else {
                this.progressCallback(100);
            }
        };

        await uploadNextChunk();
    };
}