import React from "react";

import styles from "./PaginationStyles.module.css";

const range = (start = 0, end) => {
    return [...Array(end - start + 1)].map((_, idx) => start + idx);
};

const Pagination = ({currentPageIndex, setPageIndex, totalPages}) => {
    if (!totalPages || totalPages === 1) {
        return null;
    }

    if (totalPages <= 5) {
        return (
            <div className={styles.paginationContainer}>
                {range(0, totalPages - 1).map((number, idx) => (
                    <div
                        key={idx}
                        className={`${styles.paginationButton} ${
                            currentPageIndex === number ? styles.active : null
                        }`}
                        onClick={() => setPageIndex(number)}
                    >
                        {number + 1}
                    </div>
                ))}
            </div>
        );
    }

    if (currentPageIndex <= 2) {
        return (
            <div className={styles.paginationContainer}>
                {range(0, 3).map((number, idx) => (
                    <div
                        key={idx}
                        className={`${styles.paginationButton} ${
                            currentPageIndex === number ? styles.active : null
                        }`}
                        onClick={() => setPageIndex(number)}
                    >
                        {number + 1}
                    </div>
                ))}
                <div>...</div>
                <div
                    className={styles.paginationButton}
                    onClick={() => setPageIndex(totalPages - 1)}
                >
                    {totalPages}
                </div>
            </div>
        );
    }

    if (currentPageIndex >= totalPages - 2) {
        return (
            <div className={styles.paginationContainer}>
                <div
                    className={styles.paginationButton}
                    onClick={() => setPageIndex(0)}
                >
                    1
                </div>
                <div>...</div>

                {range(currentPageIndex - 3, totalPages - 1).map((number, idx) => (
                    <div
                        key={idx}
                        className={`${styles.paginationButton} ${
                            currentPageIndex === number ? styles.active : null
                        }`}
                        onClick={() => setPageIndex(number)}
                    >
                        {number + 1}
                    </div>
                ))}
            </div>
        );
    }

    return (
        <div className={styles.paginationContainer}>
            <div className={styles.paginationButton} onClick={() => setPageIndex(0)}>
                1
            </div>
            <div>...</div>

            <div
                className={styles.paginationButton}
                onClick={() => setPageIndex(currentPageIndex - 1)}
            >
                {currentPageIndex}
            </div>
            <div
                className={`${styles.paginationButton} ${styles.active}`}
                onClick={() => setPageIndex(currentPageIndex)}
            >
                {currentPageIndex + 1}
            </div>
            <div
                className={styles.paginationButton}
                onClick={() => setPageIndex(currentPageIndex + 1)}
            >
                {currentPageIndex + 2}
            </div>

            <div>...</div>
            <div
                className={styles.paginationButton}
                onClick={() => setPageIndex(totalPages - 1)}
            >
                {totalPages}
            </div>
        </div>
    );
};

export default Pagination;
