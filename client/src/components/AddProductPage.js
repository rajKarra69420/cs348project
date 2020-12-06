import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import { Typography } from '@material-ui/core';

const axios = require('axios');

class AddProductPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            name: null,
            price: null,
            type: null,
        }
        
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(e) {
        const value = e.target.value;
        this.setState({
            ...this.state,
            [e.target.id]: value,
        });
    }

    handleSubmit(e) {
        console.log(this.state);
        axios.get('http://127.0.0.1:5000/addProduct', {
            params: {
                product_name: this.state.name,
                price: this.state.price,
                type: this.state.type,
            }
        })
        .then(res => {
            console.log(res);
        })
        .catch(err => {
            console.log(err);
        })
    }

    render() {
        return(
            <div>
                <Typography variant="h2">Add Product</Typography>
                <form>
                    <TextField id="name" label="Name" variant="outlined" onChange={this.handleChange}/>
                    <br></br>
                    <TextField id="price" label="Price" variant="outlined" onChange={this.handleChange}/>
                    <br></br>
                    <TextField id="type" label="Type" variant="outlined" onChange={this.handleChange}/>
                    <br></br>
                    <Button variant="contained" color="primary" onClick={this.handleSubmit}>Add Product</Button>
                </form>
            </div>
        );
    }

}

export { AddProductPage };