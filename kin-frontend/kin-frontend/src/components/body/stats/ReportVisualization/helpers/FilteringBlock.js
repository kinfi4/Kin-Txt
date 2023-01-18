import React, {useState} from 'react';
import filteringCss from './Filtering.module.css';
import {HiOutlineBarsArrowDown} from "react-icons/hi2";
import {capitalizeFirstLetter} from "../../../../../utils/utils";

const FilteringBlock = ({currentOption, options, style}) => {
    const [filteringOptions, setFilteringOptions] = useState({optionsActive: false});

    function renderOptions() {
        if(filteringOptions.optionsActive) {
            return (
                <div className={filteringCss.filterOptions}>
                    {
                        options.map((el, idx) => {
                            return (
                                <div
                                    key={idx}
                                    onClick={el.onClick}
                                >
                                    {el.label}
                                </div>
                            )
                        })
                    }
                </div>
            )
        }

        return <></>
    }

    return (
        <div
            className={filteringCss.filterContainer}
            onMouseEnter={() => setFilteringOptions({optionsActive: true})}
            onMouseLeave={() => setFilteringOptions({optionsActive: false})}
            style={style}
        >
            <div>
                <HiOutlineBarsArrowDown className={filteringCss.filterIcon} />
                {capitalizeFirstLetter(currentOption)}
            </div>
            {renderOptions()}
        </div>
    );
};

export default FilteringBlock;
