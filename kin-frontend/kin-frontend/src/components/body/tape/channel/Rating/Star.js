import {AiTwotoneStar} from "react-icons/ai";
import React from "react";
import {connect} from "react-redux";
import s from './Rating.module.css'
import {changeCurrentRating, rateChannel} from "../../../../../redux/reducers/ratingReducer";

const Star = (props) => {
    let starActiveClass = ''

    if (props.currentRating) {
        starActiveClass = props.index <= props.currentRating ? s.active : ''
    } else {
        starActiveClass = props.index <= Math.round(props.averageRating) ? s.active : ''
    }

    return (
        <div
            onClick={() => {props.rateChannel(props.link, props.index)}}
            className={starActiveClass}
            onMouseEnter={() => {props.changeCurrentRating(props.index)}}
            onMouseLeave={() => {
                props.changeCurrentRating(Math.round(props.averageRating))
            }}
        >
            <AiTwotoneStar />
        </div>
    )
}

let mapStateToProps = (state) => {
    return {
        averageRating: state.ratingReducer.averageRating,
        currentRating: state.ratingReducer.currentRating,
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        rateChannel: (channelLink, rating) => dispatch(rateChannel(channelLink, rating)),
        changeCurrentRating: (rating) => dispatch(changeCurrentRating(rating)),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Star);
