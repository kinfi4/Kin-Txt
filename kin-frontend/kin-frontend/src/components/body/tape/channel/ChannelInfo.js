import React, {useEffect, useState} from 'react';
import channelCss from './Channel.module.css'
import {connect} from "react-redux";
import {NEWS_SERVICE_URL} from "../../../../config";
import {truncate} from "../../../../utils/utils";
import {unsubscribe} from "../../../../redux/reducers/channelsReducer";
import {fetchChannelRating, rateChannel} from "../../../../redux/reducers/ratingReducer";
import EstimateGame from "./Rating/EstimateGame";


const ChannelInfo = (props) => {
    useEffect(() => {
        props.fetchRating(props.channel.link)
    }, [])

    return (
        <div className={channelCss.channelInfoContainer}>
            <div className={channelCss.ratingNPhotoContainer}>
                <img src={NEWS_SERVICE_URL + props.channel.profilePhotoUrl} alt={truncate(props.channel.title, 14)}/>
                <EstimateGame channelLink={props.channel.link} />
            </div>
            <div className={channelCss.informationContainer}>
                <h1>
                    {props.channel.title}
                </h1>
                <span className={channelCss.subscribersCount}>{props.channel.subscribersNumber} subscribers</span>
                <p>{props.channel.description ? props.channel.description : "NO DESCRIPTION PROVIDED"}</p>

                <div
                    className={channelCss.unsubscribeButton}
                    onClick={(e) => props.unsubscribe(props.channel.link)}
                >
                    UNSUBSCRIBE
                </div>
            </div>
        </div>
    );
};


let mapStateToProps = (state) => {
    return {
        myRate: state.ratingReducer.myRate,
        totalRate: state.ratingReducer.totalRate,
        averageRating: state.ratingReducer.averageRating,
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        unsubscribe: (channelLink) => dispatch(unsubscribe(channelLink)),
        fetchRating: (channelLink) => dispatch(fetchChannelRating(channelLink)),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(ChannelInfo);