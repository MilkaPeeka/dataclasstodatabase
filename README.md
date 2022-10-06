**Dataclass To Database -> A very simple abstraction layer to make using SQL somewhat easier**


My goal with that project is to make life a little bit easier by creating an abstraction layer that simplifes the writing of basic SQL queries- and does that for you!
Basically, it takes a dataclass and automatically takes care of inserting, updating, deleting and fetching rows from the SQL database.


*How to use:*

1. First, we will start by creating a simple dataclass

![image](https://user-images.githubusercontent.com/75909725/194360649-4dcefe6d-8ee1-4bac-93d6-e782ae41fa70.png)


2. We will point a filename for the db, and generate a helper class which we can now utilize for our needs!

![image](https://user-images.githubusercontent.com/75909725/194361103-4ff6dae7-9211-4fe5-adbe-6609fe67fcbc.png)


![image](https://user-images.githubusercontent.com/75909725/194361241-2f689a4b-4da1-45a4-aea2-45b9e60459f7.png)




*So what does this support?*

1. Currently only the current types are supported: int, boolean, bytes, str
2. Automatically creating a table of a dataclass
3. Insert objects of said dataclass
4. Fetch and recreate all objects of said dataclass from database, while maintaining the original value types
5. Update objects by using a specific key from the user
6. Delete objects.



*The rational behind:*
The project should not be used for large projects, it was created for me to use as it just saves writing a lot of boilerplate SQL code. I am sure that it is not perfect, 
and probably has many issues. It is also not complete in a sense that it supports a really limited list of types, and has basically no checking for successful\failures when using the database.



*Features I want to add:*

1. Checking that the class we got is an actual dataclass
2. Maybe refactoring the code a little bit so it is more readable
3. Not a feature, but I hope I could learn PEP8 and implement its principals into the project.
