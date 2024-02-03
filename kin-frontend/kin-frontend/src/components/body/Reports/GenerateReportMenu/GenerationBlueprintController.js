import {STATISTICS_SERVICE_URL} from "../../../../config";
import {showMessage} from "../../../../utils/messages";
import APIRequester from "../../../../domain/apiCalls/APIRequester";

export class GenerationBlueprintController {
    constructor(setReportData, setBlueprintsList, hideModalWindow) {
        this.setReportData = setReportData;
        this.setBlueprintsList = setBlueprintsList;
        this.hideModalWindow = hideModalWindow;
    }

    async loadBlueprint(blueprintId) {
        const apiRequester = new APIRequester(STATISTICS_SERVICE_URL);

        const response = await apiRequester.get(`/templates/${blueprintId}`);

        if (!response.data) {
            showMessage([
                {
                    message: "Something went wrong during template loading.",
                    type: "danger",
                },
            ]);
            return;
        }

        console.log(response.data.fromDate);
        console.log(response.data.toDate);

        this.setReportData({
            startDate: new Date(response.data.fromDate),
            endDate: new Date(response.data.toDate),
            reportType: response.data.reportType,
            channels: response.data.channelList,
            templateId: response.data.templateId,
            modelCode: response.data.modelCode,
            name: response.data.reportName,
            modelType: response.data.modelType,
            datasourceType: response.data.datasourceType,
        });

        this.hideModalWindow();
    }

    async loadUserBlueprintsList() {
        const apiRequester = new APIRequester(STATISTICS_SERVICE_URL);

        try {
            const response = await apiRequester.get("/templates");

            if (response.status === 200) {
                this.setBlueprintsList(
                    response.data.templates.map((template) => {
                        return {name: template.name, id: template.id};
                    })
                );
            } else {
                throw new Error(`HTTP status code ${response.status}`);
            }
        } catch(error) {
            showMessage([
                {
                    message: "Something went wrong during blueprint loading.",
                    type: "danger",
                },
            ]);
        }
    }

    async deleteBlueprint(blueprintId) {
        if (!window.confirm("Are you sure you want to delete this blueprint?")) {
            return;
        }

        const apiRequester = new APIRequester(STATISTICS_SERVICE_URL);

        try {
            const response = await apiRequester.delete(`/templates/${blueprintId}`);
            if (response.status === 204) {
                showMessage([{message: "Blueprint deleted.", type: "success"}]);

                await this.loadUserBlueprintsList();
            } else {
                throw new Error(`HTTP status code ${response.status}`);
            }
        } catch (error) {
            showMessage([
                {
                    message: "Something went wrong during blueprint deleting.",
                    type: "danger",
                },
            ]);
        }
    }

    async saveBlueprint(name, data) {
        if (!name) {
            showMessage([
                {
                    message: "You have to specify the blueprint name.",
                    type: "danger",
                },
            ]);
            return;
        }

        console.log(data.startDate.toLocaleString());
        console.log(data.endDate.toLocaleString());

        console.log(data.startDate);
        console.log(data.endDate);

        const postData = {
            name: name,
            reportType: data.reportType,
            channelList: data.channels,
            fromDate: data.startDate.toLocaleString().split(",")[0],
            toDate: data.endDate.toLocaleString().split(",")[0],
            modelCode: data.modelCode,
            templateId: data.templateId,
            reportName: data.name,
            modelType: data.modelType,
            datasourceType: data.datasourceType,
        };

        const apiRequester = new APIRequester(
            STATISTICS_SERVICE_URL,
            null,
            true
        );

        try {
            const response = await apiRequester.post("/templates", postData);
            if (response.status === 201) {
                showMessage([
                    {
                        message: "Blueprint has been saved successfully",
                        type: "success",
                    },
                ]);
                this.hideModalWindow();
            } else {
                throw new Error(`HTTP status code ${response.status}`);
            }
        } catch (error) {
            showMessage([
                {
                    message: "Something went wrong during blueprint saving.",
                    type: "danger",
                },
            ]);
        }
    }
}