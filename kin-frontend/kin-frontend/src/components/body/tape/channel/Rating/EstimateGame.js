import React, {useLayoutEffect} from 'react';
import {connect} from "react-redux";
import s from './Rating.module.css'
import Star from "./Star";
import {changeCurrentRating} from "../../../../../redux/reducers/ratingReducer";


const EstimateGame = (props) => {
    useLayoutEffect(() => {
        if(props.averageRating) {
            props.changeCurrentRating(Math.round(props.averageRating))
        }
    }, [props.averageRating]);

    return (
        <div className={s.estimateForm}>
            <div>{[1,2,3,4,5].map(number => <Star index={number} key={number} link={props.channelLink}/>)}</div>
            <div style={{fontWeight: 'bold', fontSize: '18px'}}>Average mark: {Number(props.averageRating).toFixed(2)}</div>
            <div style={{fontWeight: 'bold', fontSize: '18px'}}>Estimated times: {props.ratesCount}</div>
        </div>
    );
};


let mapStateToProps = (state) => {
    return {
        ratesCount: state.ratingReducer.ratesCount,
        averageRating: state.ratingReducer.averageRating,
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        changeCurrentRating: (rating) => dispatch(changeCurrentRating(rating))
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(EstimateGame);