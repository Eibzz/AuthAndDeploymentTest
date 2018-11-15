# AuthAndDeploymentTest
A message board web application I made to study REST endpoints, postgreSQL, cloud deployment, and user authentication + authorization.

# Resources

### Users
 * Email
 * Password
 * First Name
 * Last Name

### Session
 * Session ID
  * User ID
  * User First Name

### Messages
 * Timestamp
 * Sender
 * Message Text
 
# Database Schema
 
### Messages

```
CREATE TABLE messages (
  id INTEGER PRIMARY KEY,
  timestamp VARCHAR(255) NOT NULL,
  sender VARCHAR(255) NOT NULL,
  message VARCHAR NOT NULL,
);
```
### Users

```
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  email VARCHAR NOT NULL,
  encpass VARCHAR NOT NULL,
  firstname VARCHAR(255) NOT NULL,
  lastname VARCHAR(255) NOT NULL
);
```

# Rest Endpoints

Name | Path | HTTP Method
--- | --- | ---
Register User | /users | POST
Login User | /session | POST
Retrieve Messages | /messages | GET
Post Message | /messages | POST

# Encryption Used

### Hashlib/bcrypt

```
encpass = bcrypt.encrypt(parsed_data['encpass'][0])
# encpass is the form data key for a password
# uses random salt
```




