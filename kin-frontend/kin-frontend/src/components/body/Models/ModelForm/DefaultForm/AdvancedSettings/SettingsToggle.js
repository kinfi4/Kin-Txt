import React, {useEffect, useRef, useState} from "react";
import { GoTriangleDown } from "react-icons/go";

import styles from "./styles/ToggleStyles.module.css";


const SettingsToggle = ({settingsForm}) => {
    const [showSettings, setShowSettings] = useState(false);
    const [collapsing, setCollapsing] = useState(false);
    const isFirstRender = useRef(true);

    useEffect(() => {
        if (isFirstRender.current) {
            // If it's the first render, do nothing and flip the ref for future renders
            isFirstRender.current = false;
            return;
        }

        // When expanded state changes, check if it's a transition from true to false
        if (!showSettings) {
            setCollapsing(true);
        }
    }, [showSettings]);
    const onAnimationEnd = () => {
        // When the closing animation ends, set collapsing to false
        if (collapsing) {
            setCollapsing(false);
        }
    };

    let contentClassName = `${styles.toggleContent}`;
    if (showSettings) {
        contentClassName = `${styles.toggleContent} ${styles.toggleContentExpanded}`;
    }
    if (collapsing) {
        contentClassName = `${styles.toggleContent} ${styles.toggleContentCollapsing}`;
    }

    return (
        <div className={styles.toggleContainer}>
            <div className={styles.toggleHeader} onClick={() => setShowSettings(!showSettings)}>
                <div className={`${styles.toggleIcon} ${showSettings ? styles.expanded : ''}`}>
                    {showSettings ? <GoTriangleDown /> : <GoTriangleDown />}
                </div>
                <div className={styles.toggleTitle}>Advanced model settings</div>
            </div>
            {(showSettings || collapsing) && <div className={contentClassName} onAnimationEnd={onAnimationEnd}>{settingsForm}</div>}
        </div>);
};

export default SettingsToggle;