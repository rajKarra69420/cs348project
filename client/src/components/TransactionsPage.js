import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import { Typography } from '@material-ui/core';
import Box from '@material-ui/core/Box';
import Button from '@material-ui/core/Button';
import placeholderImage from './placeholder.png';
import TextField from '@material-ui/core/TextField';
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
            console.log(res.data)
        })
        .catch((err) => {
            console.log(err);
        })
    }

    render() {
        const displayItems = (this.state.items == null) ? null : this.state.items.map(item => (
            <Box css={{ width: 300, height: 350}}>
                <img id="item-image" src={placeholderImage} alt="Logo" />
                <div>Name: {item[0]}</div>
                <div>Price: ${item[1]}</div>
                <div><TextField label="Quantity" id={item[0]} value={this.state.quantity[item[0]] ? this.state.quantity[item[0]] : 1} onChange={this.handleChange} type="number"/></div>
                <br></br>
                <div><Button variant="contained" color="primary" onClick={() => this.onClick(item[0], item[1], item[2])}>Add to Cart</Button></div>
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