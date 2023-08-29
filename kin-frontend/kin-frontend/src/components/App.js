import "react-notifications-component/dist/theme.css";
import React from "react";
import {Route, Switch} from "react-router-dom";
import {useEffect} from "react";
import {ReactNotifications} from "react-notifications-component";

import Header from "./header/Header";
import ModalWindow from "./common/modal/ModalWindow";
import Login from "./auth/login";
import Register from "./auth/register";
import Statistics from "./body/Reports/Reports";
import Tape from "./body/Tape/Tape";
import store from "../redux/store";
import ComparisonWindow from "./body/Comparison/ComparisonWindow";
import ModelsList from "./body/Models/ModelsList";
import ModelCreateForm from "./body/Models/ModelForm/ModelCreateForm/ModelCreateForm";
import ModelUpdateForm from "./body/Models/ModelForm/ModelUpdateForm/ModelUpdateForm";
import TemplatesList from "./body/VIsualizationTemplates/TemplatesList";
import TemplateCreateForm from "./body/VIsualizationTemplates/TemplateForm/TemplateCreateForm/TemplateCreateForm";
import TemplateUpdateForm from "./body/VIsualizationTemplates/TemplateForm/TemplateUpdateForm/TemplateUpdateForm";

import {loadUser} from "../redux/reducers/authReducer";


export function Main() {
    return (
        <>
            <Header/>

            <Switch>
                <Route exact path={"/reports/compare"} render={() => <ComparisonWindow />} />
                <Route path={'/reports'} render={() => <Statistics />} />
                <Route path={'/models/create'} render={() => <ModelCreateForm />} />
                <Route path={'/models/edit/:code'} render={({match}) => <ModelUpdateForm modelCode={match.params.code} />} />
                <Route path={'/models'} exact render={() => <ModelsList />} />
                <Route exact path={'/tape'} render={() => <Tape />} />
                <Route path={'/templates/create'} render={() => <TemplateCreateForm />} />
                <Route path={'/templates/edit/:id'} render={({match}) => <TemplateUpdateForm templateId={match.params.id} />} />
                <Route path={'/templates'} render={() => <TemplatesList />} />
                <Route path={'/'} render={() => <Statistics />} />
            </Switch>
        </>
    )
}

function App() {
    useEffect(() => {
        store.dispatch(loadUser())
    })

    return (
      <>
          <ReactNotifications />
          <ModalWindow />

          <Switch>
              <Route exact path={'/sign-in'} render={() => <Login />} />
              <Route exact path={'/sign-up'} render={() => <Register />} />
              <Route path={'/'} render={() => <Main />} />
          </Switch>
      </>
  );
}

export default App;
