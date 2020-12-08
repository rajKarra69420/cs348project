import React, { Component } from 'react';
import { Typography } from '@material-ui/core';
import Button from '@material-ui/core/Button';
import Box from '@material-ui/core/Box';
import placeholderImage from './placeholder.png';
import './ItemSelectionPage.css';

const axios = require('axios');

class ShoppingCartPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            items: null,
            totalPrice: null,
            totalQuantity: null,
        }
    }

    componentDidMount() {
        this.getItems();
        this.getTotals();
    }

    getTotals() {
        axios.get('http://127.0.0.1:5000/getCustomerTotals', {
            params: {
                cust_id: window.location.href.split("userid=")[1],
            }
        })
        .then((res) => {
            console.log(res.data)
            this.setState({
                totalPrice: res.data.totalPrice,
                totalQuantity: res.data.totalQuantity,
            })
        })
        .catch((err) => {
            console.log(err);
        })
    }

    getItems() {
        axios.get('http://127.0.0.1:5000/getCustomerProducts', {
            params: {
                cust_id: window.location.href.split("userid=")[1],
            }
        })
        .then((res) => {
            console.log(res.data)
            const items = Object.values(res.data);
            this.setState({
                items,
            });
        })
        .catch((err) => {
            console.log(err);
        })
    }

    handleSubmit() {
        axios.get('http://127.0.0.1:5000/addTransaction', {
            params: {
                cust_id: window.location.href.split("userid=")[1],
            }
        })
        .then((res) => {
            window.location.reload(true);
        })
        .catch((err) => {
            console.log(err);
        })
    }

    render() {
        const displayItems = (this.state.items == null) ? null : this.state.items.map(item => (
            <Box css={{ width: 300, height: 300}}>
                <img id="item-image" src={placeholderImage} alt="Logo" />
                <div>Name: {item[0]}</div>
                <div>Price: ${item[1]}</div>
                <div>Quantity: {item[2]}</div>
            </Box>
        ))
        
        return(
            <div style={{textAlign: 'center'}}>
                <Typography variant="h2">Shopping Cart</Typography>
                <Box
                    display="flex"
                    flexWrap="wrap"
                    alignContent="flex-start"
                    p={1}
                    m={1}
                >
                    {displayItems}
                </Box>
                <Typography variant="h6">Total Number of Items: {this.state.totalQuantity}</Typography>
                <Typography variant="h6">Total Price: ${this.state.totalPrice}</Typography>
                <Button variant="contained" color="primary" onClick={this.handleSubmit}>Purchase Items</Button>
            </div>
        )
    }
}

export { ShoppingCartPage };