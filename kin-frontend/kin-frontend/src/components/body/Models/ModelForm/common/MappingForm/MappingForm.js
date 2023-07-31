import React from "react";
import mappingStyles from "./MappingForm.module.css"
import {AiFillDelete} from "react-icons/ai";

const MappingForm = ({id, data, setData}) => {
    const addMapping = () => {
        let newMapping = data.categoryMapping;
        const newMappingIndex = newMapping.length;
        newMapping[newMappingIndex] = {value: newMappingIndex, categoryName: "New category"};
        setData({...data, categoryMapping: newMapping});
    }
    const removeMapping = (index) => {
        let newMapping = data.categoryMapping;
        newMapping.splice(index, 1);
        setData({...data, categoryMapping: newMapping});
    }
    const changeMapping = (index, newMapping) => {
        let newMappings = data.categoryMapping;
        newMappings[index] = newMapping;
        setData({...data, categoryMapping: newMappings});
    }

    return (
        <div>
            {
                data.categoryMapping.map((mapping, index) => (
                    <div key={index} className={mappingStyles.inputMappingContainer}>
                        <input
                            type="number"
                            value={mapping.value}
                            onChange={(event) =>
                                changeMapping(index, {value: event.target.value, categoryName: mapping.categoryName})
                            }
                        />
                        :
                        <input
                            type="text"
                            value={mapping.categoryName}
                            onChange={(event) =>
                                changeMapping(index, {value: mapping.value, categoryName: event.target.value})
                            }
                        />
                        <div
                            onClick={() => removeMapping(index)}
                            className={mappingStyles.deleteMappingButton}>
                            <AiFillDelete />
                        </div>
                    </div>
                ))
            }
            <div>
                {
                    Object.keys(data.categoryMapping).length < 10 &&
                    <div
                        onClick={() => addMapping()}
                        className={mappingStyles.addMappingButton}
                    >
                        Add mapping
                    </div>
                }
            </div>
        </div>
    );
};

export default MappingForm;