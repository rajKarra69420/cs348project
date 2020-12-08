import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import { Typography } from '@material-ui/core';
import Box from '@material-ui/core/Box';
import Button from '@material-ui/core/Button';
import placeholderImage from './placeholder.png';
import './ItemSelectionPage.css';

const axios = require('axios');

class HomePage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            items: null,
            redirect: false,
        }

        this.handleSubmit = this.handleSubmit.bind(this);
    }

    componentDidMount() {
        this.getItems();
    }

    getItems() {
        axios.get('http://127.0.0.1:5000/bestSellers')
        .then((res) => {
            const items = []
            items.push(res.data.firstBest)
            items.push(res.data.secondBest)
            items.push(res.data.thirdBest)
            console.log(items)
            this.setState({
                items,
            });
            //console.log(res.data)
        })
        .catch((err) => {
            console.log(err);
        })
    }

    handleSubmit() {
        this.setState({
            redirect: true,
        })
    }

    render() {
        const displayItems = (this.state.items == null) ? null : this.state.items.map(item => (
            <Box css={{ width: 300, height: 350}}>
                <img id="item-image" src={placeholderImage} alt="Logo" />
                <div>{item.product_name}</div>
                <div>Amount Sold: {item.quantity}</div>
                <br></br>
            </Box>
        ));

        const redirect = this.state.redirect;
        const redirectString = '/registerCustomer?';
        if (redirect) {
            return <Redirect to={redirectString}/>
        }
        return(
            <div style={{textAlign: 'center'}}>
                <Typography variant="h2">Home Page</Typography>
                <Button variant="contained" color="primary" onClick={this.handleSubmit}>Get Started</Button>
                <Typography variant="h4">Best Selling Items</Typography>
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

export { HomePage };