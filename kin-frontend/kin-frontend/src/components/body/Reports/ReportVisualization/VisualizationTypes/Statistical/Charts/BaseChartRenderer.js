export class BaseChartRenderer {
    constructor(contentType, width, height) {
        if(new.target === BaseChartRenderer) {
            throw new TypeError("Cannot construct BaseChartRenderer instances directly");
        }

        this.width = width;
        this.height = height;
        this.contentType = contentType;
    }

    render(key=null) {
        throw new Error("Method 'render()' must be implemented.");
    }
}