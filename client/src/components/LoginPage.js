import React, { Component } from 'react';
import { Alert } from '@material-ui/lab';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import { Typography } from '@material-ui/core';
import { Redirect } from 'react-router-dom';

const axios = require('axios');

class LoginPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: null,
            password: null,
            redirect: false,
            error: false,
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
        axios.get('http://127.0.0.1:5000/login', {
            params: {
                username: this.state.username,
                password: this.state.password,
            }
        })
        .then(() => {
            this.setState({
                redirect: true,
            })
        })
        .catch(err => {
            this.setState({
                error: true,
            })
        })
    }

    render() {
        const redirect = this.state.redirect;
        const redirectString = '/?userid=' + this.state.username;
        if (redirect) {
            return <Redirect to={redirectString}/>
        }

        return(
            <div>
                {this.state.error ? <Alert severity="error">There was an error logging into your account. Please try again.</Alert> : null}
                <Typography variant="h2">Login</Typography>
                <form>
                    <TextField id="username" label="Username" variant="outlined" onChange={this.handleChange}/>
                    <br></br>
                    <TextField id="password" label="Password" variant="outlined" type="password" onChange={this.handleChange}/>
                    <br></br>
                    <Button variant="contained" color="primary" onClick={this.handleSubmit}>Register</Button>
                </form>
            </div>
        );
    }

}

export { LoginPage };