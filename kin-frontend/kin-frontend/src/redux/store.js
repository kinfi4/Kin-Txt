import {createStore, combineReducers, applyMiddleware} from "redux";
import {composeWithDevTools} from "redux-devtools-extension";
import thunk from "redux-thunk";

import {auth} from "./reducers/authReducer";
import {modalWindowReducer} from "./reducers/modalWindowReducer";
import {reportsReducer} from "./reducers/reportsReducer";
import {wordsCloudReducer} from "./reducers/wordCloud";
import {comparisonReducer} from "./reducers/comparisonReducer";
import modelsReducer from "./reducers/modelsReducer";
import visualizationTemplatesReducer from "./reducers/visualizationTemplates";

let store = createStore(
    combineReducers({
        auth: auth,
        modalWindow: modalWindowReducer,
        reportsReducer: reportsReducer,
        wordsCloudReducer: wordsCloudReducer,
        comparisonReducer: comparisonReducer,
        modelsReducer: modelsReducer,
        visualizationTemplatesReducer: visualizationTemplatesReducer,
    }),
    composeWithDevTools(applyMiddleware(thunk))
);

export default store;
