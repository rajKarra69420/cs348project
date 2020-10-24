import React, { Component } from 'react';
import Box from '@material-ui/core/Box';
import Button from '@material-ui/core/Button';
import placeholderImage from './placeholder.png';
import './ItemSelectionPage.css';

const axios = require('axios');

class ItemSelectionPage extends Component {
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
        axios.get('http://127.0.0.1:5000/getProducts')
        .then((res) => {
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
                <Button variant="contained" color="primary">Add to Cart</Button>
            </Box>
        ))
        
        return(
            <Box
                display="flex"
                flexWrap="wrap"
                alignContent="flex-start"
                p={1}
                m={1}
            >
                {displayItems}
            </Box>
        )
    }
}

export { ItemSelectionPage };