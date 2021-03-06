import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import { Alert } from '@material-ui/lab';
import { Typography } from '@material-ui/core';
import { Redirect } from 'react-router-dom';

const axios = require('axios');

class RegistrationPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: null,
            password: null,
            address: null,
            email_address: null,
            error: false,
            redirect: false,
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
        axios.get('http://127.0.0.1:5000/registerCustomer', {
            params: {
                username: this.state.username,
                password: this.state.password,
                address: this.state.address,
                email_address: this.state.email_address,
            }
        })
        .then(() => {
            this.setState({
                redirect: true,
            }) 
        })
        .catch(() => {
            this.setState({
                error: true,
            })
        })
    }

    render() {
        const redirect = this.state.redirect;
        const redirectString = '/login'
        if (redirect) {
            return <Redirect to={redirectString}/>
        }

        return(
            <div style={{textAlign: 'center', marginTop: '10%'}}>
                {this.state.error ? <Alert severity="error">There was an error creating your account. Please try again.</Alert> : null}
                <Typography variant="h2">Create New Account</Typography>
                <form>
                    <TextField id="username" label="Username" variant="outlined" onChange={this.handleChange}/>
                    <br></br>
                    <TextField id="password" label="Password" variant="outlined" type="password" onChange={this.handleChange}/>
                    <br></br>
                    <TextField id="address" label="Address" variant="outlined" onChange={this.handleChange}/>
                    <br></br>
                    <TextField id="email_address" label="Email Address" variant="outlined" onChange={this.handleChange}/>
                    <br></br>
                    <Button variant="contained" color="primary" onClick={this.handleSubmit}>Register</Button>
                </form>
            </div>
        );
    }

}

export { RegistrationPage };