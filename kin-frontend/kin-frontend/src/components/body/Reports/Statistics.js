import mainPageCss from "../MainPage.module.css";
import statisticsCss from "./Statistics.module.css"
import React, {useEffect} from "react";

import 'react-date-range/dist/styles.css'; // main style file
import 'react-date-range/dist/theme/default.css'; // theme css file
import "./GenerateReportMenu/styles/DateRangePickerStyles.css"
import {Link, Route, Switch} from "react-router-dom";
import {useRouteMatch} from "react-router-dom/cjs/react-router-dom";
import GenerateReportMenu from "./GenerateReportMenu/GenerateReportMenu";
import SelectReportMenu from "./SelectReport/SelectReportMenu";
import ReportVisualization from "./ReportVisualization/ReportVisualization";
import {connect} from "react-redux";
import {loadFilteredWordsFromStorage} from "../../../redux/reducers/wordCloud";


const Statistics = (props) => {
    useEffect(() => {
        props.loadFilteredWordsFromStorage();
    }, []);

    let {path, url} = useRouteMatch();

    return (
        <>
            <div className={mainPageCss.container}>
                <div className={statisticsCss.statsContainer}>
                    <Switch>
                        <Route exact path={path} render={() => <SelectReportMenu />} />
                        <Route exact path={`${path}/view/:id`} render={({match}) => <ReportVisualization reportId={match.params.id} />} />
                        <Route exact path={`${path}/generate`} render={() => <GenerateReportMenu />} />
                    </Switch>
                </div>
            </div>
        </>
    )
}

let mapStateToProps = (state) => {
    return {}
}

let mapDispatchToProps = (dispatch) => {
    return {
        loadFilteredWordsFromStorage: () => dispatch(loadFilteredWordsFromStorage)
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Statistics);
