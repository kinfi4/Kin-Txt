import {ModelTypes} from "../../../../../config";
import {showMessage} from "../../../../../utils/messages";

export const validateFormData = (data, isUpdate=false) => {
    if(!Object.values(ModelTypes).includes(data.modelType)) {
        showMessage([{message: `Unknown model type selected: '${data.modelType}'`, type: 'danger'}]);
        return false;
    }

    if(!data.name) {
        showMessage([{message: `No model name provided`, type: 'danger'}]);
        return false;
    }

    // check mappings
    if(!data.categoryMapping || !data.categoryMapping.length) {
        showMessage([{message: `No mappings provided`, type: 'danger'}]);
        return false;
    }

    return true;
}
