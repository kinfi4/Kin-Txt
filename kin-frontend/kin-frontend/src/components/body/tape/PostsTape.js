import React, {useCallback, useRef} from 'react';
import LoadingSpinner from "../../common/spiner/LoadingSpinner";
import {fetchNextPosts} from "../../../redux/reducers/postsReducer";
import {connect} from "react-redux";
import Post from "./post/Post";
import TapeCss from "./Tape.module.css"


const PostsTape = (props) => {
    function truncatePostLink(linkString) {
        let linkParts = linkString.split('/')
        let postId = linkParts[linkParts.length - 1]
        let channelId = linkParts[linkParts.length - 2]

        return `${channelId}/${postId}`
    }

    let observer = useRef();

    // eslint-disable-next-line react-hooks/exhaustive-deps
    let lastUserRef = useCallback(node => {
        if(observer.current) {
            observer.current.disconnect()
        }

        observer.current = new IntersectionObserver(entries => {
            if(entries[0].isIntersecting){
                props.fetchNewPosts()
                // console.log("FETCHING NEW POSTS")
            }
        })

        if (node) {
            observer.current.observe(node)
        }
    }, [props.posts]);

    if (props.userHasPosts === false) {
        return (
            <div
                style={{
                    color: "#fff",
                    fontWeight: "bold",
                    fontSize: "25px"
                }}
            >
                SORRY, BUT YOU HAVE NO SUBSCRIPTIONS :(
            </div>
        )
    }

    if(props.posts.length === 0) {
        props.fetchNewPosts();
        return (
            <LoadingSpinner width={100} height={100} marginTop={"10%"} />
        )
    }

    return (
        <>
            {
                props.posts.map((el, i) => {
                    if(i === props.posts.length - 1) {
                        return (
                            <div ref={lastUserRef} key={i} className={TapeCss.postWrapper}>
                                <Post postLink={truncatePostLink(el.link)} />
                            </div>
                        )
                    }
                    else {
                        return (
                            <div key={i} className={TapeCss.postWrapper}>
                                <Post postLink={truncatePostLink(el.link)} key={i} />
                            </div>
                        )
                    }
                })
            }
            {
                props.loading ? <LoadingSpinner width={100} height={100} marginTop={"10%"} /> : <></>
            }
        </>
    );
};

let mapStateToProps = (state) => {
    return {
        loading: state.postsReducer.loading,
        userHasPosts: state.postsReducer.userHasPosts,
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        fetchNewPosts: () => dispatch(fetchNextPosts()),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(PostsTape);