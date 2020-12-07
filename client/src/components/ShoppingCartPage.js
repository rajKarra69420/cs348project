import React, { Component } from 'react';
import { Typography } from '@material-ui/core';
import Box from '@material-ui/core/Box';
import placeholderImage from './placeholder.png';
import './ItemSelectionPage.css';

const axios = require('axios');

class ShoppingCartPage extends Component {
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

    render() {
        const displayItems = (this.state.items == null) ? null : this.state.items.map(item => (
            <Box css={{ width: 300, height: 300}}>
                <img id="item-image" src={placeholderImage} alt="Logo" />
                <div>name: {item[0]}</div>
                <div>price: {item[1]}</div>
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
            </div>
        )
    }
}

export { ShoppingCartPage };