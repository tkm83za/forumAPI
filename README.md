forumAPI
========

API Documentation
----
The API is root is accessible via /api/v1/\<resourcetype\>/(id/)


User:
* URL: http://\<server\>:\<server\>/api/v1/user/
* fields: *email:string, first_name: string, last_name:string
* methods: GET, POST, PUT, PATCH, DELETE
* 


Topic:
* URL: http://\<server\>:\<port\>/api/v1/topic/
* fields: *name:string, blurb:string
* methods: GET, POST, PUT, PATCH, DELETE


Topic's comment:
* URL: http://\<server\>:\<port\>/api/v1/topic/\<id\>/comments/
* fields: *topic:string (ref to Topic URL ), comment_body:string, name: string, blurb:string
* methods: GET


Comment:
* URL: http://\<server\>:\<port\>/api/v1/comment/
* fields: email:string, name: string, blurb:string
* methods: GET, POST, PUT, PATCH, DELETE
