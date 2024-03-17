import React, {useEffect} from "react";
import WordCloud from "react-d3-cloud";


export class WordCloudBuilder {
    MAX_WORD_SIZE = 140;
    MIN_WORD_SIZE = 12;
    WC_COLORS = [
        "#408f5e",
        "#2F6B9A",
        "#82a6c2",
        "#BA97B4",
        "#2CA884",
        "#E39E21",
        "#00C6B5",
        "#BF8520",
    ];

    constructor(words) {
        this.words = words;
        this.totalWords = words.length;

        this.theBiggestWordValue = Math.max(...words.map((el) => el.value));
        this.theSmallestWordValue = Math.min(...words.map((el) => el.value));
    }

    static fromWordsList = (words) => {
        return new WordCloudBuilder(words);
    };

    build() {
        return (
            <div style={{marginTop: this._calcMarginTop()}}>
                <WordCloud
                    data={this.words}
                    width={this._calcBoxSize()}
                    height={this._calcBoxSize()}
                    random={() => 0.5}
                    padding={this._calcPadding()}
                    fontSize={(word) => this._calcFontSize(word)}
                    fill={(w, i) => this._getColorFromIdx(i)}
                    rotate={() => 0}
                />
            </div>
        );
    }

    _calcMarginTop() {
        if(this.totalWords < 150) {
            return "15px";
        } else {
            return "50px";
        }
    }

    _calcBoxSize() {
        if (this.totalWords < 150) {
            return 500;
        } else if (this.totalWords < 300) {
            return 900;
        } else {
            return 1500;
        }
    }

    _calcFontSize(word) {
        return (
            ((word.value-this.theSmallestWordValue) / this.theBiggestWordValue)*this.MAX_WORD_SIZE + this.MIN_WORD_SIZE
        );
    }

    _calcPadding() {
        return 10;
    }

    _getColorFromIdx(idx) {
        return this.WC_COLORS[idx % this.WC_COLORS.length];
    }
}

