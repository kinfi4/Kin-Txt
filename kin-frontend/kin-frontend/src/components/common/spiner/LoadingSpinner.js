import React from 'react';
import s from './LoadingSpinner.module.css'


const LoadingSpinner = (props) => {
    return (
        <div
            className={s['lds-roller']}
            style={{
                width: props.width,
                height: props.height,
                marginTop: props.marginTop ? props.marginTop : "50px",
        }}
        >
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
        </div>
    );
};

export default LoadingSpinner;
