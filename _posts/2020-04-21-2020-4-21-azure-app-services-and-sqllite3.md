---
layout: post
title: Azure App Services and SQLLite3
categories: []
tags: []
status: publish
type: post
published: true
meta:
  _thumbnail_id: '19'
---

I created a .NET Core API that talks with a sqllite3 database. The plan is to start with a sqllite3 database, and when I run into storage or other issues once the project is launched, I’ll switch to a bigger or fancier sql instance as needed. I’m to the point where I want to start building a test environment, so other people who help me with the project can test. Azure App Services allows you to do a local git push to an app service and auto-magically (using the Kudu build program) have your code running on the internet. It also allows 1gb of storage in the app service. Since I want to just have an initial website for testing purposes and not for production, having a sqllite3 database on the single server in the app service seems to make sense. I don’t have to pay for extra storage I won’t need, and I don’t have to worry about concurrency or scaling because it’s a single instance of the site, and I can deploy as I go using a git remote branch. KISS principle, right?

## The problem:


Running on my local dev box, the API works great (yes, standard dev complaint, “it works on my machine!”). But when I push it to the Azure app service and try to access a table (in this case, “Plants”), I get the following error:  Error message: SQLite Error 1: 'no such table: Plants'.     Looking into my logs, I find the initial seeding of the database fails with the below error:

Microsoft.Data.Sqlite.SqliteException (0x80004005): SQLite Error 5: 'database is locked'.

There’s only a single instance of the site, so only one website should be accessing it, how can it be locked? And why does it work locally? After some initial googling, I found this stack overflow response: 
[https://stackoverflow.com/questions/53226642/sqlite3-database-is-locked-in-azure](https://stackoverflow.com/questions/53226642/sqlite3-database-is-locked-in-azure).

The problem is that /home is mounted as CIFS filesystem which can not deal with SQLite3 lock.  Well that’s unfortunate. I did some more research and found out the following. Azure App service does indeed still mount the /home directory as a CIFS filesystem, which is a type of NFS (Network File system). I verified this by going to the azure portal, then opened the specific App Service. On the left toolbar you can see the “Advanced Tools” option. If you click “Go->” it will open a new window, and on the top menu bar there’s a “BASH” option. That will give you a bash instance on the App service server. To view filesystem types, I used the command df -Th which gives me a list of the filesystems with the type (-T flag), and human readable (-h flag). The screenshot below shows the /home directory is type cifs, and since the website is deployed to /home/site/wwwroot, this confirms the internet’s theory.









![azureAppServiceScreenshot.png](/squarespace_images/azureAppServiceScreenshot.png)
  


  















I also looked on the sqllite website and confirmed it’s a known issue with NFS filesystems. It currently states (
[https://sqlite.org/lockingv3.html](https://sqlite.org/lockingv3.html)):

>One should note that POSIX advisory locking is known to be buggy or even unimplemented on many NFS implementations (including recent versions of Mac OS X) and that there are reports of locking problems for network filesystems under Windows. Your best defense is to not use SQLite for files on a network filesystem.


## The result:


Unfortunately, there was no way I could find to update the mount type of the filesystem in the azure app service to a version that SQLLite3 supports. I suspect the official “correct” way to do it is to spin up a separate sql database instance in the azure offerings (or elsewhere), and then connect it to the app. The official documentation has a tutorial for just that: 
[https://docs.microsoft.com/en-us/azure/app-service/app-service-web-tutorial-dotnet-sqldatabase](https://docs.microsoft.com/en-us/azure/app-service/app-service-web-tutorial-dotnet-sqldatabase)  As far as I can tell, it uses a paid version of azure’s sql database offerings. Given the simplicity of my app and the complexity of the azure sql offerings (I’m pretty sure you get offered a microsoft job on the spot if you fully understand their pricing tiers 
[https://azure.microsoft.com/en-us/pricing/details/sql-database/single/](https://azure.microsoft.com/en-us/pricing/details/sql-database/single/).) I decided to try my hand at a different online hosting platform for my app.  It’s an end result I’d rather not have, but such is life. I wrote this in part to help others who come across this weird error (right now a single stack overflow had the correct info in it), and partly to show that programming does not always involve finding a good solution. For me, it seems finding the correct solution can mean simply brute forcing all solutions until one works.
