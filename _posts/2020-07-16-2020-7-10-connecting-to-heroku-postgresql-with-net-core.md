---
layout: post
title: Connecting to Heroku Postgresql with .Net Core
categories:
- technical write up
- How-to
tags:
- heroku
- ".net core"
- postgresql
status: publish
type: post
published: true
meta: {}
---

In my adventures using Heroku for hosting a .Net Core app (previous writeup here: 
[Running Net Core in Heroku]({% post_url 2020-07-09-2020-7-9-running-net-core-in-heroku %})), I decided to use the built-in Heroku postgresql database. Once again, there wasn’t an official way to connect a .Net Core app to that, so I had to piece together my own version. Happily it’s pretty straightforward. 

I chose the Npgsql library (
[https://www.npgsql.org/](https://www.npgsql.org/)) mainly because it seemed easy enough to use, and so far I haven’t had any issues with it. I then read through the library’s documentation and read Heroku’s documentation about connecting with other languages. Using that, I pieced together what was required to take the environment variable that Heroku sets in the app and transform it into a connection string that Npgsql will accept. 

## Documentation


General Heroku postgresql documentation is here, with other language implementations: 
[https://devcenter.heroku.com/articles/heroku-postgresql](https://devcenter.heroku.com/articles/heroku-postgresql)

.net Core’s Npgsql library connection string documentation: 
[https://www.npgsql.org/doc/connection-string-parameters.html](https://www.npgsql.org/doc/connection-string-parameters.html)

## Code snippets


Below is the relevant code snippet to create a connection string from Heroku’s postgres instance’s environment variable DATABASE_URL, otherwise default pull from your app settings file. This way you can push to Heroku and have it auto-connect correctly, or you can easily set your own local postgres database if you need to test something locally.

This section goes in Startup.cs, replace “YourDataContext” with the datacontext you’re using:

    public void ConfigureServices(IServiceCollection services)

           {

               //other service configuration goes here...

               //pull in connection string

               string connectionString = null;

               string envVar = Environment.GetEnvironmentVariable("DATABASE_URL");



               if (string.IsNullOrEmpty(envVar)){

                   connectionString = Configuration["Connectionstrings:database"];

               }

               else{

                   //parse database URL. Format is postgres://<username>:<password>@<host>/<dbname>

                   var uri = new Uri(envVar);

                   var username = uri.UserInfo.Split(':')[0];

                   var password = uri.UserInfo.Split(':')[1];

                   connectionString =

                   "; Database=" + uri.AbsolutePath.Substring(1) +

                   "; Username=" + username +

                   "; Password=" + password + 

                   "; Port=" + uri.Port +

                   "; SSL Mode=Require; Trust Server Certificate=true;";

               }

               services.AddDbContext<YourDataContext>(opt =>

                 	opt.UseNpgsql(connectionString)

               );

    }



In your appsettings.json file:

    {

    //Other settings go here…



     "Connectionstrings":{

       "database" : "local database connection string here"

    }

    }

If you read through the code it’s pretty straightforward. If the Database_URL environment variable exists, pull that in. The URL is a proper URI, so I can use the built in URI class to pull some data from the string without having to rely solely on regex and string parsing. Then it’s a matter of placing the pieces in the correct order with the correct name in the name-value pairs of the connection string for Npgsql to parse out.
