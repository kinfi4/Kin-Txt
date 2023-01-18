export const getColor = (category) => {
    if(category.toLowerCase() === "negative") {
        return "#a62d2d"
    } else if (category.toLowerCase() === "positive") {
        return "#7ae17b"
    } else if (category.toLowerCase() === "neutral") {
        return "#7088ab"
    } else if (category.toLowerCase() === "economical") {
        return "#56b947"
    } else if (category.toLowerCase() === "political") {
        return "#4353c2"
    } else if (category.toLowerCase() === "shelling") {
        return "#d53737"
    } else if (category.toLowerCase() === "humanitarian") {
        return "#2da682"
    } else if (category.toLowerCase() === "count") {
        return "#a295bb";
    }

    let randomColors = [
        "#845fc7",
        "#bb95af",
        "#932d73",
    ];

    return randomColors[Math.floor(Math.random() * randomColors.length)];
}