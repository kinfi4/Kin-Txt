import React, {useEffect, useState} from "react";
import TapeCss from "./Tape.module.css"
import mainPageCss from "../MainPage.module.css"
import {connect} from "react-redux";
import {showModalWindow} from "../../../redux/reducers/modalWindowReducer";
import Input from "../../common/input/Input";
import Button from "../../common/button/Button";
import {addChannel, fetchChannels} from "../../../redux/reducers/channelsReducer";
import ChannelBlock from "./channel/ChannelBlock";
import {fetchNextPosts} from "../../../redux/reducers/postsReducer";
import PostsTape from "./PostsTape";


const EnterLink = (props) => {
    const [link, setLink] = useState({link: ''})

    return (
        <div className={TapeCss.enterLinkContainer}>
            <h4>
                PROVIDE A LINK TO THE CHANNEL
            </h4>
            <Input
                value={link.link}
                onChange={(event) => setLink({link: event.target.value})}
                placeholder={"Channel link"}
            />

            <Button
                text={"Subscribe"}
                onClick={(event) => props.addChannel(link.link)}
            />
        </div>
    )
}


const Tape = (props) => {
    useEffect(() => {
        props.fetchChannels();
        props.fetchNewPosts();
    }, [])

    return (
        <div className={mainPageCss.container}>
            <div className={mainPageCss.sideBar}>
                <div className={mainPageCss.sideBarContent}>
                    <div
                        className={mainPageCss.controlButton}
                        onClick={() => props.showModal(<EnterLink addChannel={props.addChannel} />, 400, 300)}
                    >
                        SUBSCRIBE
                    </div>

                    <div className={TapeCss.channelsContainer}>
                        {
                            props.channels.map(
                                (channelEntity, i) => <ChannelBlock channel={channelEntity} key={i} />
                            )
                        }
                    </div>
                </div>
            </div>
            <div className={TapeCss.tape}>
                <PostsTape {...props} />
            </div>
        </div>
    )
}

let mapStateToProps = (state) => {
    return {
        channels: state.channels.channels,
        posts: state.postsReducer.posts,
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        showModal: (content, width, height) => dispatch(showModalWindow(content, width, height)),
        addChannel: (link) => dispatch(addChannel(link)),
        fetchChannels: () => dispatch(fetchChannels()),
        fetchNewPosts: () => dispatch(fetchNextPosts()),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Tape);
