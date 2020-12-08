import React from 'react';
import { Switch, Route, BrowserRouter as Router } from 'react-router-dom';

import { LoginPage } from './LoginPage.js';
import { ItemSelectionPage } from './ItemSelectionPage.js';
import { AddProductPage } from './AddProductPage.js';
import { RegistrationPage } from './RegistrationPage.js';
import { ShoppingCartPage } from './ShoppingCartPage.js';
import { TransactionsPage } from './TransactionsPage.js';
import { HomePage } from './HomePage.js';


function WebRouter() {
  return (
    <div>
      <Router>
          <Switch>
            <Route exact path='/' component={() => <HomePage/>} />
            <Route path='/itemSelectionPage' component={() => <ItemSelectionPage/>} />
            <Route path='/login' component={() => <LoginPage />} />
            <Route path='/addProduct' component={() => <AddProductPage/>}/>
            <Route path='/registerCustomer' component={() => <RegistrationPage/>}/>
            <Route path='/shoppingCart' component={() => <ShoppingCartPage/>}/>
            <Route path='/transactions' component={() => <TransactionsPage/>}/>
          </Switch>
      </Router>
    </div>
  )
}

export  { WebRouter };