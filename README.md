forumAPI
========

##API Documentation##
The API is root is accessible via /api/v1/\<resourcetype\>/(id/)

Register User:
* URL: http://\<server\>:\<server\>/api/v1/register/
* JSON fields: 
 * **email**: string
 * **username**: string
 * **password**: string
 * is\_staff:boolean _(optional. defaults to false)_
* methods: POST
* to add an admin user, set is_staff field to true

User List:
* operations on non-admin users
* URL: http://\<server\>:\<server\>/api/v1/user/
* methods: GET

Non-admin user operations:
* URL: http://\<server\>:\<server\>/api/v1/user/\<id\>/
* fields: 
 * email: string
 * username: string
* methods: GET, PATCH, DELETE

Admin User List:
* gets a list of admin users (have is_staff=true)
* URL: http://\<server\>:\<server\>/api/v1/adminuser/
* fields: 
 * email:string
 * username: string
* methods: GET

Admin users operations:
* URL: http://\<server\>:\<server\>/api/v1/adminuser/\<id\>/
* fields:
 * email: string
 * username: string
* methods: GET, PATCH, DELETE


Topic:
* URL: http://\<server\>:\<port\>/api/v1/topic/(id/)
* fields: 
 * **name**:string
 * blurb:string
* methods: GET, POST, PUT, PATCH, DELETE


Topic's comment:
* retrieves all the comments associated with a topic
* URL: http://\<server\>:\<port\>/api/v1/topic/\<id\>/comments/
* methods: GET


Comment:
* URL: http://\<server\>:\<port\>/api/v1/comment/
* fields: 
 *  **comment_body**: string
 *  **topic**: string _(href to topic)_
 *  author: string
 *  in\_reply\_to:string _(id of comment to which this is a reply of)_
* methods: GET, POST, PUT, PATCH, DELETE


Fields marked as **bold** are mandatory
