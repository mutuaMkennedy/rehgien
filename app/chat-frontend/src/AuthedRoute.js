import React from "react";
import { Redirect, Route } from "react-router-dom";

const AuthedRoute = ({ component: Component, loading, ...rest }) => {
  const isAuthed = Boolean(localStorage.getItem("auth_token"));
  return (
    <Route
      {...rest}
      render={props =>
        loading ? (
          <p>Loading...</p>
        ) : isAuthed ? (
          <div>
            <Component history={props.history} {...rest} />
          </div>
        ) : (
          <Redirect
            to={{
              pathname: "/pro/auth/login",
              state: { next: props.location }
            }}
          />
        )
      }
    />
  );
};

export default AuthedRoute;
