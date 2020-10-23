import React, { Component } from 'react';
import Box from '@material-ui/core/Box';
import Button from '@material-ui/core/Button';
import placeholderImage from './placeholder.png';
import './ItemSelectionPage.css';

const items = [
    {name: 'blue t-shirt', price: 14.99, rating: 2.3, numberOfReviews: 34}, 
    {name: 'black t-shirt', price: 12.99, rating: 3.5, numberOfReviews: 4},
    {name: 'yello t-shirt', price: 11.99, rating: 3.8, numberOfReviews: 324},
    {name: 'pink t-shirt', price: 4.99, rating: 4.9, numberOfReviews: 342},
    {name: 'purple t-shirt', price: 10.99, rating: 5, numberOfReviews: 2}];

class ItemSelectionPage extends Component {
    render() {
        const displayItems = items.map(item => (
            <Box css={{ width: 300, height: 200}}>
                <img id="item-image" src={placeholderImage} alt="Logo" />
                <div>name: {item.name}</div>
                <div>price: {item.price}</div>
                <div>rating: {item.rating}</div>
                <div>Number of Reviews: {item.numberOfReviews}</div>
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