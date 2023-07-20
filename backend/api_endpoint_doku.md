# API Endpoints


## User
```http
/user
```

### Get all users
Returns the Names of all users
**GET**
```http
/
```

| input | input json name | output | output json name |
| ----- | --------------- | ------ | ---------------- |
|       |                 | Name[] | name             | 

### Add user
when given name, valid email and password returns id of the user, if the email is valid or another error occurs an error is returned   
**POST**
```http
/add_user
```

| input    | input json name | output     | output json name |
| -------- | --------------- | ---------- | ---------------- |
| Name     | name            | User ID or | user_id          |
| E-Mail   | email           | ERROR      | error            | 
| password | password        |            |                  |

### Check if user is logged in
To confirm if a user is valid and can log in, you can pass either an email, ID, or name in combination with the password. The following conditions apply:

- If the user exists but the password is invalid, the ID will be returned and `valid_login` will be `False`.
- If the login is correct, `valid_login` will be `True`. 
- If the ID is `None`, it means the user doesn't exist.
- If an error is returned, it could indicate that no name, email, or ID was passed.

**POST**
```http
/check_login
```

| input      | input json name | output         | output json name |
| ---------- | --------------- | -------------- | ---------------- |
| E-Mail or  | email           | is Login Valid | valid_login      |
| User ID or | id              | User ID        | user_id          |
| Name       | name            | ERROR          | error            | 
| Password   | password        |                |                  |

## PC
```http
/pc
```

### Get all pcs
**GET**
```http
/
```

| input | input json name | output        | output json name |
| ----- | --------------- | ------------- | ---------------- |
|       |                 | list of lists | pcs              | 
|       |                 | User Name     | user_name        |
|       |                 | User Mail     | email            |
|       |                 | Hardware UUID | hardware_uuid    |
|       |                 | PC Name       | client_name      |
|       |                 | Manufacturer  | manufacturer     |
|       |                 | Model         | model            |

### Get all pcs of user wit id
**GET**
```http
/user/<user_id>
```

| input   | input json name | output        | output json name |
| ------- | --------------- | ------------- | ---------------- |
| User ID | -               | list of lists | pcs              |
|         |                 | Hardware UUID | hardware_uuid    |
|         |                 | PC Name       | client_name      |
|         |                 | Manufacturer  | manufacturer     |
|         |                 | Model         | model            | 

### Add new PC
**POST**
```http
/add_user
```

| input                   | input json name | output | output json name |
| ----------------------- | --------------- | ------ | ---------------- |
| User ID                 | user_id         | ERROR  | error            |
| Hardware UUID           | hardware_uuid   | PC ID  | pc_id            | 
| Nick Name for Client PC | client_name      |        |                  |
