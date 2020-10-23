import React from 'react';
import { Switch, Route, BrowserRouter as Router } from 'react-router-dom';

import { LoginPage } from './LoginPage.js';
import { ItemSelectionPage } from './ItemSelectionPage.js';


function WebRouter() {
  return (
    <div>
      <Router>
          <Switch>
            <Route exact path='/' component={() => <ItemSelectionPage/>} />
            <Route path='/login' component={() => <LoginPage />} />
          </Switch>
      </Router>
    </div>
  )
}

export  { WebRouter };