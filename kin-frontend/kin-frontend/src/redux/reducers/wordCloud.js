const SET_FILTER_WORDS = "SET_FILTER_WORDS"


const initialState = {
    wordsList: []
}

export const setFilterOutWords = (wordsList) => (dispatch) => {
    dispatch({type: SET_FILTER_WORDS, words: wordsList})
}

export const loadFilteredWordsFromStorage = (dispatch) => {
    let words = JSON.parse(localStorage.getItem("wordCloudFilterWords"));
    dispatch({type: SET_FILTER_WORDS, words: words});
}


export const wordsCloudReducer = (state=initialState, action) => {
    switch (action.type) {
        case SET_FILTER_WORDS:
            localStorage.setItem("wordCloudFilterWords", JSON.stringify(action.words));
            return {...state, wordsList: JSON.parse(localStorage.getItem("wordCloudFilterWords"))};
        default:
            return state;
    }
}