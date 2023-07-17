# API Endpoints


## User
```http
/user
```

### Get all users
**GET**
```http
/
```

| input | input json name | output | output json name |
| ----- | --------------- | ------ | ---------------- |
|       |                 | Name[] | 0
### Add user
**POST**
```http
/add_user
```

| input    | input json name | output  | output json name |
| -------- | --------------- | ------- | ---------------- |
| Name     | name            | User ID |     user_id             |
| E-Mail   | email           | ERROR        |    error              |
| password | password        |         |                  |

### Check if user is logged in
**POST**
```http
/check_login
```

| input      | input json name | output         | output json name |
| ---------- | --------------- | -------------- | ---------------- |
| E-Mail or  | email           | is Login Valid | valid_login      |
| User ID or | id              | User ID        | user_id          |
| Name       | name            |                |                  |
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
|       |                 | list of lists | -                 |
|       |                 | User Name     | 0                |
|       |                 | User Mail     | 1                |
|       |                 | Hardware UUID | 2                |
|       |                 | PC Name       | 3                |
|       |                 | Manufacturer  | 4                |
|       |                 | Model         | 5                 |

### Get all pcs of user wit id
**GET**
```http
/user/<user_id>
```

| input   | input json name | output        | output json name |
| ------- | --------------- | ------------- | ---------------- |
| User ID | -               | list of lists | pcs                |
|         |                 | Hardware UUID | 0                |
|         |                 | PC Name       | 1                |
|         |                 | Manufacturer  | 2                |
|         |                 | Model         | 3                |

### Add new PC
**POST**
```http
/add_user
```

| input                   | input json name | output | output json name |
| ----------------------- | --------------- | ------ | ---------------- |
| User ID                 | user_id         | ERROR  | error            |
| Hardware UUID           | hardware_uuid   | PC ID  | pc_id            | 
| Nick Name for Client PC | clientName      |        |                  |

