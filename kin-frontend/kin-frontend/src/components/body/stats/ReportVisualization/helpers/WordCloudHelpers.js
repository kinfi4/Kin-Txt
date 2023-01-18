export function calcFontSize(word, allWords, theBiggestWordValue, theSmallestWordValue) {
    const maxSize = 200;
    const minSize = 7;

    let size = ((word.value - theSmallestWordValue) / theBiggestWordValue) * maxSize + minSize;
    let lastQuater = (theBiggestWordValue - theSmallestWordValue) * 0.75;
    let firstQuater = (theBiggestWordValue - theSmallestWordValue) * 0.25;

    if(word.value > lastQuater) {
        return size - minSize;
    }

    return size;
}

export function calcPadding (allWords) {
    return 10;
}