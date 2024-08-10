# FastAPI/Python: API Basic Role-Based Access Control (RBAC)

This Python code sample demonstrates **how to implement Role-Based Access Control (RBAC)** in FastAPI API servers using oauth2 for keycloak integration.

COnfiguration
-------------

Copy [sample.env](./sample.env) and create or update *.env* file to get started.

The application will be accessible via a specified port, default being 8002

This assumes you have a Keycloak intance running, then configure:
-  REALM
-  CLIENT_ID
- AUTH_BASE_URL

The current code test for `andmin` or `user`, so tests should use those... please

Docker start up 
-------------
Afterwards, simply run the following command:

```
docker compose up --build -d
```

References
----------

1. Securing FastAPI with Keycloak by [Benjamin Buffet on Medium](https://medium.com/@buffetbenjamin). There are two parts to his blog:
   1. [The Adventure Begins (Part 1)](https://medium.com/@buffetbenjamin/securing-fastapi-with-keycloak-the-adventure-begins-part-1-e7eae3b79946)
   2. [(Part 2): A Tale of Roles](https://medium.com/@buffetbenjamin/securing-fastapi-with-keycloak-part-2-a-tale-of-roles-660ab5963ee5).

2. Seveloper tutorial on Auth0 - [FastAPI/Python Code Sample:
API Role-Based Access Control](https://developer.auth0.com/resources/code-samples/api/fastapi/basic-role-based-access-control)

