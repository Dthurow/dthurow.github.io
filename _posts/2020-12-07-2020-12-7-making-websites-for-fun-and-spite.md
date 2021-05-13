---
layout: post
title: Making Websites for Fun and Spite
slug: making-websites-for-fun-and-spite
categories:
- side project
- technical write up
tags:
- side project
- plants
- the flora and fauna walks
status: publish
type: post
published: true
meta:
  _thumbnail_id: '32'
---

One of my many side hobbies I enjoy is learning about plants. I like learning about wild native and invasive species wherever I am, and I like excitedly telling everyone within earshot about them whenever I spot an interesting plant. Thanks to the miracle of the modern internet, I can tell strangers I’ve never met about plants too. I set up an instagram for just such a purpose here: 
[https://www.instagram.com/thefloraandfaunawalks](https://www.instagram.com/thefloraandfaunawalks). However, my dad doesn’t have an instagram account, and he pointed out (rightly) that you had to have an account to see anything more than the first picture of each post, even for “public” instagram accounts! Well that frustrated me, because “public” should mean “public”! So in a fit of spite I decided to spin up my own static website. And instead of hand-crafting each page, build out a little bash script that generates my posts.

Now, I could have used something like jekyll to auto-generate my website, since it’s clearly a tool for doing something like what I want. The two reasons I didn’t use any pre-built tooling is a) learning the tooling would probably take about the same time as just doing it myself, and b) it’s way more fun to build it yourself.








  

    

![FloraAndFaunaWalksWebsite.png](/squarespace_images/FloraAndFaunaWalksWebsite.png)
  


  





You can see my final product at 
[http://plants.daniellethurow.com/](http://plants.daniellethurow.com/). The current build process is pretty clunky right now, but I hope to streamline it eventually. The workflow is this right now:

* Take a picture of a cool plant


* Research and write up a description of the plant


* Create a folder in Google Drive with the name of the plant, copy the pictures from my phone to the folder, and the description from my computer to the folder


* Publish on instagram via my phone


* Copy the Google Drive folder into my local copy of the 
[https://github.com/Dthurow/thefloraandfaunawalks](https://github.com/Dthurow/thefloraandfaunawalks) repo


* Run my createWebPages.sh script


* Open the websites folder and verify the files are all good, open in chrome, etc.


* Run my publishWebPage.sh script


* success!

Whew, that’s a lot of steps! I want to see if there’s a way to sync my phone with the github repo, and/or sync the google drive folder to my computer, to eliminate a step or two, but haven’t had the chance to look into it yet.

I decided to use github pages, since they provide free static-site hosting, both a user website that lives at <username>.github.io, and individual repository sites (which live at <username>.github.io/<repositoryname>). I hadn’t used my user-specific website yet (though I may end up migrating this blog over there at some point), so I decided to use that site for my plant page. I also own the daniellethurow.com domain (obviously, since I’m posting there), and my provider lets me create new CNAME records, so I can redirect a subdomain of daniellethurow.com to the github-hosted website. I chose plants.daniellethurow.com.

Originally, I hoped I could keep both my generated static site, and my bash scripts/templates/plant info all in one github repo. From what I could tell, that’s not how github wants you to do it, though, and I couldn’t find a way of setting it up. This means if I want to keep track of my bash scripts and templates I made, I have to have a separate repo, 
[https://github.com/Dthurow/thefloraandfaunawalks](https://github.com/Dthurow/thefloraandfaunawalks). That just adds more steps to get the site published, so I made a publishWebPage.sh script. It copies the generated website from thefloraandfaunawalks repo on my computer to the repo folder with just static pages, stages the changes and pushes them to github (
[https://github.com/Dthurow/dthurow.github.io](https://github.com/Dthurow/dthurow.github.io)). Once they’re there, github auto builds and releases the website using jekyll.

This is all setup though. The fun part was spinning up a bash script that would take individual folders with a plant’s images and description, and create a whole working website!

## Data walkthrough


First to make a plant site, I needed plants to put on it! I already had my photos on instagram and my phone, and the descriptions I had written earlier on my instragram. Frustratingly, they don’t allow you to download your own instagram posts (walled garden much?), so I decided to go manual on it. I had 46 posts when I did this, so I just copied all of them by hand into a description.txt file, each inside individual folders, one per plant post.

I then grabbed the pictures I had on the posts, either on my phone if I could find them, or from instagram. All photos for each plant also went into the same folder as the description file. And bam, I had a simple but consistent setup that would allow me to do some scripting.

## Script walkthrough


I need to make two pages: 1) the home page with a collection of links, and 2) a single post per plant that has the pictures in a slide show, with the description of the plant below the pictures.

First: the single post per plant. The pages were going to be basically identical, just with a few differences, so I certainly wasn’t going to make those by hand. Instead, I dealt with this by making template HTML pages. I made an individual postFormat.html that has all the HTML I want the plant post to have, but when I need to put in data that’s plant-specific, I put in a placeholder description, surrounded by curly braces, e.g. {description}. Then in my bash script, I loop through all the plant folders, and for each one, pull in the plant-specific data and replace the correct {placeholder} with the real data. Yes, this script is essentially a fancy find-and-replace tool.

As part of that, I had to have a way to include multiple images on the same page, so I created an image template HTML file. I loop through the images in a particular folder, put the image name in the appropriate place in the image template, and concatenate them all together, so I have a long string of HTML-formatted images, which I then put into the post template {images} placeholder. While I’m doing that, I also copy the images over into the website/images folder, so all images are in one place ready to be served on the static site. Once the plant post has had all curly braces replaced, I write it out to a file with the appropriate name in the website folder.

For the home page, I did something similar, though simpler. While I was looping through the plant folders, I added an extra step at the end, creating a link to the newly created plant post, and concatenating them all together. Then once I finished creating the plant posts, I had a list of links to the plants that I could put into my home page template.

Lastly, I have some simple CSS to make it look fancier in a separate file, site.css, that I also copy over, as well as some images that I put on the home page just for fun.

And voila, I have a finished static website in the website folder, ready to be copied and dropped wherever I can host static websites!

## Future Plans


Future plans for this include streamlining the building process, and potentially switching to something like jekyll for building the site out. I’m thinking I’ll move my personal website to something like jekyll soon anyway, so I’ll eventually learn the tooling, and I suspect it’ll be much more flexible than my current set up. This site is currently on squarespace, but there’s a lot of bells and whistles I’m paying for that I never use, so it may make sense financially to do that.

But in the meantime, I have a fun little hobby site to play with, and more importantly, yell at strangers about plants on, so I’m very happy with my (current) final result!
