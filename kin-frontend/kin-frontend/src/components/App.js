import React from "react";
import Header from "./header/Header";
import ModalWindow from "./common/modal/ModalWindow";
import {Route, Switch, Redirect} from "react-router-dom";
import Login from "./auth/login";
import Register from "./auth/register";
import Statistics from "./body/Statistics/Statistics";
import Tape from "./body/Tape/Tape";
import {useEffect} from "react";
import store from "../redux/store";
import {loadUser} from "../redux/reducers/authReducer";
import {ReactNotifications} from "react-notifications-component";
import 'react-notifications-component/dist/theme.css'
import ComparisonWindow from "./body/Comparison/ComparisonWindow";
import ModelsList from "./body/Models/ModelsList";
import ModelCreateForm from "./body/Models/ModelForm/ModelCreateForm/ModelCreateForm";
import ModelUpdateForm from "./body/Models/ModelForm/ModelUpdateForm/ModelUpdateForm";


export function Main() {
    return (
        <>
            <Header/>

            <Switch>
                <Route exact path={"/statistics/compare"} render={() => <ComparisonWindow />} />
                <Route path={'/statistics'} render={() => <Statistics />} />
                <Route path={'/models/create'} render={() => <ModelCreateForm />} />
                <Route path={'/models/:id'} render={({match}) => <ModelUpdateForm modelId={match.params.id} />} />
                <Route path={'/models'} exact render={() => <ModelsList />} />
                <Route exact path={'/tape'} render={() => <Tape />} />
                <Route path={'/'} render={() => <Redirect to={'/statistics'}/>} />
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
