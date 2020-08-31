import React from "react";
import { BrowserRouter as Router, Switch,Route, } from "react-router-dom";
import Login from "./Login.js";
import Home from "./ProHome.js";
import UnauthedRoute from "./UnauthedRoute.js";
import NotFound from "./PageNotFound.js";
import ProjectBase from "./ProjectBase.js";

const App = () => (
  <Router>
    <Switch>
      <UnauthedRoute exact path="/pro/auth/login" component={Login} />
      <ProjectBase/>
      <Route path="*">
        <NotFound/>
      </Route>
    </Switch>
  </Router>
);

export default App;
