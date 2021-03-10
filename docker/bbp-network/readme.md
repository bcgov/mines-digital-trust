# Debugging 
Running `docker-compose up` will run two copies of the business partners, each with an instance of ACA-py and a wallet. 

`bpa1` has slightly different parameters to enable remote debugging.

`bpa1` is configured to run a debug server for `jdb`, which can be attached to at `localhost:1044`, most java debugging tools are built on jdb, see your IDE's configuration for remote debugging to connect to it. 

cli command is as follows `jdb -sourcepath ./src/main/java -attach 1044`

VSCode's launch.json config looks like this to work with the 'Debugger for Java' extension. 

```
    "configurations": [
        ...
        {
            "type": "java",
            "name": "Attach to Remote Program",
            "request": "attach",
            "hostName": "localhost",
            "port": 1044
        }   
    ]
    ...
```    

This connection can also be used for hot changes allowing for most development and running take place in a containerized environment. 