import React, {useEffect} from "react";
import TapeCss from "./Tape.module.css";
import mainPageCss from "../MainPage.module.css";
import {connect} from "react-redux";
import {showModalWindow} from "../../../redux/reducers/modalWindowReducer";
import {
    addChannel,
    fetchChannels,
} from "../../../redux/reducers/channelsReducer";
import ChannelBlock from "./Channel/ChannelBlock";
import {fetchNextPosts} from "../../../redux/reducers/postsReducer";
import PostsTape from "./PostsTape";
import InputModalWindow from "../../../common/inputModalWindow/InputModalWindow";

const Tape = (props) => {
    useEffect(() => {
        props.fetchChannels();
        props.fetchNewPosts();
    }, []);

    return (
        <div className={mainPageCss.container}>
            <div className={mainPageCss.sideBar}>
                <div className={mainPageCss.sideBarContent}>
                    <div
                        className={mainPageCss.controlButton}
                        onClick={() =>
                            props.showModal(
                                <InputModalWindow
                                    actionCallback={props.addChannel}
                                    title={"PROVIDE A LINK TO THE CHANNEL"}
                                    inputPlaceholder={"Channel link"}
                                    submitPlaceholder={"Subscribe"}
                                />,
                                400,
                                300
                            )
                        }
                    >
                        SUBSCRIBE
                    </div>

                    <div className={TapeCss.channelsContainer}>
                        {props.channels.map((channelEntity, i) => (
                            <ChannelBlock channel={channelEntity} key={i} />
                        ))}
                    </div>
                </div>
            </div>
            <div className={TapeCss.tape}>
                <PostsTape {...props} />
            </div>
        </div>
    );
};

let mapStateToProps = (state) => {
    return {
        channels: state.channels.channels,
        posts: state.postsReducer.posts,
    };
};

let mapDispatchToProps = (dispatch) => {
    return {
        showModal: (content, width, height) =>
            dispatch(showModalWindow(content, width, height)),
        addChannel: (link) => dispatch(addChannel(link)),
        fetchChannels: () => dispatch(fetchChannels()),
        fetchNewPosts: () => dispatch(fetchNextPosts()),
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(Tape);
