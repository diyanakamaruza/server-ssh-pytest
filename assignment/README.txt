SSH COMMUNICATIONS SECURITY CORPORATION
Senior Quality Engineer Code Assignment


THE ASSIGNMENT:
===============
Your task is to write tests for the simple REST server implementation.
Include a report file describing your actions and missing tests if any.

This task should not take more than a few working hours. You can also provide
a partial solution if the task turns to be substantially larger, but please
inform us that you run out of time and you skipped some parts of the task.
Your code will be used in evaluation, so please follow software engineering
practices as you see the best fit. Please be prepared to defend your solution
in the possible interview later on. Code must be on the substantial parts your
own handwriting. You are encouraged to use open source components and public
IPR code, but please mark the copyrights clearly.

 * Write tests for the simple test server using the provided APIs.
 * Run the server and the tests on separate docker containers.
 * Send the test code and instructions how to run the server and tests for
   review.
 * Document your doings, include any notes worth mentioning.


REST SERVER:
============
No need to do changes to the server implementation. The server implementation
may contain bugs.

Run the REST server:
    python3 server/server.py

 * No authorization required for the server.
 * The server creates five items to the database on initialization.
 * Name is the only required parameter for an item.

[GET]    /items/(?param=value)
Description
    List all items when no param given.
    Filter by param=value, for example /items/?tag=test
Response
    200    [{'name': 'item_1', ...}, ...]

[GET]    /items/<name>/
Description
    Get an item by name.
Response
    200    {'name': 'item_1', 'serial': '12345', ...}
    404    {'error': 'message'}

[POST]   /items/
Description
    Add new item.
Input
    {'name': 'item_name', 'email': 'test@ssh.com', ...}
Response
    201    {'name': 'item_name', ...}
    400    {'error': 'message'}

[DELETE] /items/<name>/
Description
    Delete an item by name.
Response
    204
    404    {'error': 'message'}
