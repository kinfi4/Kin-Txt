import React from "react";

import styles from "./PaginationStyles.module.css";

const range = (start = 0, end) => {
    return [...Array(end - start + 1)].map((_, idx) => start + idx);
};

const Pagination = ({currentPage, setPage, totalPages}) => {
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
                            currentPage === number ? styles.active : null
                        }`}
                        onClick={() => setPage(number)}
                    >
                        {number + 1}
                    </div>
                ))}
            </div>
        );
    }

    if (currentPage <= 2) {
        return (
            <div className={styles.paginationContainer}>
                {range(0, 3).map((number, idx) => (
                    <div
                        key={idx}
                        className={`${styles.paginationButton} ${
                            currentPage === number ? styles.active : null
                        }`}
                        onClick={() => setPage(number)}
                    >
                        {number + 1}
                    </div>
                ))}
                <div>...</div>
                <div
                    className={styles.paginationButton}
                    onClick={() => setPage(totalPages - 1)}
                >
                    {totalPages}
                </div>
            </div>
        );
    }

    if (currentPage >= totalPages - 2) {
        return (
            <div className={styles.paginationContainer}>
                <div
                    className={styles.paginationButton}
                    onClick={() => setPage(0)}
                >
                    1
                </div>
                <div>...</div>

                {range(currentPage - 3, totalPages - 1).map((number, idx) => (
                    <div
                        key={idx}
                        className={`${styles.paginationButton} ${
                            currentPage === number ? styles.active : null
                        }`}
                        onClick={() => setPage(number)}
                    >
                        {number + 1}
                    </div>
                ))}
            </div>
        );
    }

    return (
        <div className={styles.paginationContainer}>
            <div className={styles.paginationButton} onClick={() => setPage(0)}>
                1
            </div>
            <div>...</div>

            <div
                className={styles.paginationButton}
                onClick={() => setPage(currentPage - 1)}
            >
                {currentPage}
            </div>
            <div
                className={`${styles.paginationButton} ${styles.active}`}
                onClick={() => setPage(currentPage)}
            >
                {currentPage + 1}
            </div>
            <div
                className={styles.paginationButton}
                onClick={() => setPage(currentPage + 1)}
            >
                {currentPage + 2}
            </div>

            <div>...</div>
            <div
                className={styles.paginationButton}
                onClick={() => setPage(totalPages - 1)}
            >
                {totalPages}
            </div>
        </div>
    );
};

export default Pagination;
