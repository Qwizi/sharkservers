# SharkServers SDK

![SharkServers Logo](https://example.com/sharkservers-logo.png)

The SharkServers SDK is a powerful and easy-to-use toolkit for interacting with the SharkServers platform. It provides developers with a comprehensive set of functions and methods to manage and control various aspects of the SharkServers infrastructure programmatically.

## Features

- **API Authentication**: Simple and secure authentication mechanisms for using the SharkServers API. .
- **Users**: List users, online users.
- **Forum**: Simple forum, create threads, posts.
- **Servers**: Create servers, list servers, monitor servers for Team Fortress 2 game.

## Installation

To use the SharkServers SDK in your project, you can either download the source code and include it manually, or install it using a package manager.

```bash
npm install sharkservers-sdk --save
```
## Usage
```js
import {SharkServersClient as shark_api} from "sharkservers-sdk";

// Register user

const new_user = await shark_api.auth.register({
    username: "TestUser",
    password: "testpassword123",
    password2: "testpassword123",
    email: "test@website.pl"
})

// Get user access token and refresh token
const user = await shark_api.auth.loginUser({
    username: "TestUser",
    password: "testpassword123"
})

// Get user info
shark_api.request.TOKEN = user.access_token

const user_info = await shark_api.users.getLoggedUser()
console.log(user_info)
```
