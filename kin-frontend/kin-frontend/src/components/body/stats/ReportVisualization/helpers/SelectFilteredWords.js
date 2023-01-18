import React, {useState} from 'react';
import {setFilterOutWords} from "../../../../../redux/reducers/wordCloud";
import {connect} from "react-redux";
import TapeCss from "../../../tape/Tape.module.css";
import Input from "../../../../common/input/Input";
import Button from "../../../../common/button/Button";
import generateReportCss from "../../GenerateReportMenu/GenerateReport.module.css";
import {AiFillDelete} from "react-icons/ai";
import {showMessage} from "../../../../../utils/messages";

const SelectFilteredWords = (props) => {
    const [filteredWord, setFilteredWord] = useState({filteredWord: ''});

    function addFilteredWord (word) {
        if(props.wordsList.includes(word)) {
            showMessage([{message: "Sorry but the specified word already in the list", type: "danger"}])
            return
        }

        let newWordsList = [...props.wordsList, word];
        props.setWordCloudFilterList(newWordsList);
        setFilteredWord({filteredWord: ''});
    }

    function removeWordFromList (word) {
        const newList = props.wordsList.filter(w => w !== word);
        props.setWordCloudFilterList(newList);
    }

    return (
        <div className={TapeCss.enterLinkContainer}>
            <h4 style={{marginBottom: "40px"}}>THE WORDS YOU CHOSE WILL BE FILTERED OUT OF YOUR WORD CLOUDS</h4>
            <Input
                value={filteredWord.filteredWord}
                onChange={(event) => setFilteredWord({filteredWord: event.target.value})}
                placeholder={"Word"}
            />

            <Button
                text={"Filter out word"}
                onClick={() => addFilteredWord(filteredWord.filteredWord)}
            />

            <>
                {
                    props.wordsList.map((w, idx) => {
                        return (
                            <div
                                key={idx}
                                className={`${generateReportCss.reportBlock}`}
                            >
                                {w}
                                <span onClick={() => removeWordFromList(w)}><AiFillDelete /></span>
                            </div>
                        )
                    })
                }
            </>
        </div>
    );
};

let mapStateToProps = (state) => {
    return {
        wordsList: state.wordsCloudReducer.wordsList,
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        setWordCloudFilterList: (wordList) => dispatch(setFilterOutWords(wordList)),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(SelectFilteredWords);