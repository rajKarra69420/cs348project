import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import { Typography } from '@material-ui/core';
import Box from '@material-ui/core/Box';
import './ItemSelectionPage.css';

const axios = require('axios');

class TransactionsPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            items: null,
        }
    }

    componentDidMount() {
        this.getItems();
    }

    getItems() {
        axios.get('http://127.0.0.1:5000/getTransactions', {
            params: {
                cust_id: window.location.href.split("userid=")[1]
            }
        })
        .then((res) => {
            const items = Object.values(res.data);
            this.setState({
                items,
            });
            console.log(items)
        })
        .catch((err) => {
            console.log(err);
        })
    }

    render() {
        const displayItems = (this.state.items == null) ? null : this.state.items.map(item => (
            <Box css={{ width: 200, height: 200}}>
                <div>Name: {item[0]}</div>
                <div>Price: ${item[1]}</div>
                <div>Quantity: {item[2]}</div>
                <br></br>
            </Box>
        ));

        const redirect = this.state.redirect;
        const redirectString = '/shoppingCart?userid=' + window.location.href.split("userid=")[1];
        if (redirect) {
            return <Redirect to={redirectString}/>
        }
        return(
            <div style={{textAlign: 'center'}}>
                <Typography variant="h2">Transactions</Typography>
                <br></br>
                <Box
                    display="flex"
                    flexWrap="wrap"
                    alignContent="flex-start"
                    p={1}
                    m={1}
                >
                    {displayItems}
                </Box>
            </div>
        )
    }
}

export { TransactionsPage };