import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import Box from '@material-ui/core/Box';
import Button from '@material-ui/core/Button';
import placeholderImage from './placeholder.png';
import TextField from '@material-ui/core/TextField';
import './ItemSelectionPage.css';

const axios = require('axios');

class ItemSelectionPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            items: null,
            redirect: false,
            quantity: {},
        }

        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    componentDidMount() {
        this.getItems();
    }

    getItems() {
        axios.get('http://127.0.0.1:5000/getProducts')
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

    onClick(name, price, product_id) {
        const quantity = this.state.quantity[name] ? this.state.quantity[name] : 1;
        const total = quantity * price;
        axios.get('http://127.0.0.1:5000/addToCart', {
            params: {
                product_id: product_id,
                cust_id: window.location.href.split("userid=")[1],
                quantity: quantity,
                total: total,
            }
        })
        .then(res => {
            console.log(res);
        })
        .catch(err => {
            console.log(err);
        })
    }

    handleSubmit() {
        this.setState({
            redirect: true,
        })
    }

    handleChange(event) {
        const quantity = this.state.quantity;
        quantity[event.target.id] = event.target.value
        this.setState({
            quantity,
        });
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
            <div>
                <Button variant="contained" color="primary" onClick={this.handleSubmit}>Go to Cart</Button>
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

export { ItemSelectionPage };