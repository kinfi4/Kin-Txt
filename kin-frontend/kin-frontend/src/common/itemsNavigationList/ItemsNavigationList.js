import React from "react";
import Styles from "./ItemsListStyles.module.css";
import {NavLink} from "react-router-dom";
import {useRouteMatch} from "react-router-dom/cjs/react-router-dom";

const ItemsNavigationList = ({itemsList, ...props}) => {
    let {path, url} = useRouteMatch();

    return (
        <div>
            {itemsList.map((item, index) => {
                return (
                    <div
                        key={index}
                        className={Styles.itemContainer}
                        onClick={() => props.onClick(item)}
                    >
                        <NavLink
                            to={`${path}/${item.id}`}
                            className={Styles.itemLink}
                        >
                            {" "}
                            {item.name}{" "}
                        </NavLink>
                    </div>
                );
            })}
        </div>
    );
};

export default ItemsNavigationList;
