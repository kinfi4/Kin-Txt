export function calcFontSize(
    word,
    allWords,
    theBiggestWordValue,
    theSmallestWordValue
) {
    const maxSize = 140;
    const minSize = 12;

    return (
        ((word.value - theSmallestWordValue) / theBiggestWordValue) * maxSize +
        minSize
    );
}

export function calcPadding(allWords) {
    return 10;
}
