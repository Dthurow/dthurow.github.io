---
layout: post
title: ".NET MVC Html.AntiForgeryToken and its side-effects"
categories:
- technical write up
tags:
- microsoft
- ".net mvc"
- antiforgery
- x-frame-options
status: publish
type: post
published: true
meta: {}
---

I’ve worked with .NET, and specifically .NET MVC for the last 5 years, and I’ve run across some interesting or aggravating issues with. Below is an example of an issue that was both. Interesting because the problem only manifested during the interaction of the code and production services, and aggravating because of how long it took to debug. Hopefully, this will help some other future dev avoid the aggravation!

## The Function


If you’ve worked with .NET MVC before and need to submit forms securely, you may have come across the Html.AntiForgeryToken() function. MSDN gives the below documentation for it (
[https://docs.microsoft.com/en-us/dotnet/api/system.web.mvc.htmlhelper.antiforgerytoken?view=aspnet-mvc-5.2](https://docs.microsoft.com/en-us/dotnet/api/system.web.mvc.htmlhelper.antiforgerytoken?view=aspnet-mvc-5.2)):

>Generates a hidden form field (anti-forgery token) that is validated when the form is submitted.


This is a useful security feature that prevents cross-site request forgery (CSRF). Every time a form with the antiforgery token in it is loaded, a new token is generated. On post back to the server, .NET auto-validates the token. This prevents third-party websites from submitting forms to your site from your user’s browser (the “cross site request” part of the forgery). Without that token, when the third-party website submits the form to your site from your user’s browser, your user’s cookie and session are passed as well, and your servers don’t realize your user didn’t mean to send all their money to a mysterious swiss bank account. Microsoft itself recommends using it to prevent CSRF attacks 
[https://docs.microsoft.com/en-us/aspnet/web-api/overview/security/preventing-cross-site-request-forgery-csrf-attacks# anti-forgery-tokens-in-aspnet-mvc](https://docs.microsoft.com/en-us/aspnet/web-api/overview/security/preventing-cross-site-request-forgery-csrf-attacks# anti-forgery-tokens-in-aspnet-mvc).

## The Setup


So why bring this up in the first place? Because this function has a side-effect that does not seem to be documented very well and has caused me a lot of pain. 

For every form in a view that you add the Html.AntiForgeryToken() call to, Microsoft also adds a X-Frame-Options: SAMEORIGIN header to your HTTP response. This header isn’t bad, necessarily. Adding it prevents clickjacking attacks, and if you don’t need to put your site in a frame, you really should add it to your site. More info: 
[https://owasp.org/www-community/attacks/Clickjacking](https://owasp.org/www-community/attacks/Clickjacking)

## The Issue


If you have a view that loads in partial views, and each partial view has a form with an AntiForgeryToken() call in it, the number of X-Frame-Options in your HTTP response can add up fast. If your QA or automated tests don’t check for header count, then your production website can start generating HTTP responses with literally 100s of HTTP headers. This becomes an issue because

* that’s wasted bandwidth


* production servers, load balancers, etc. can have a limit to the number of headers allowed in requests AND responses. 

In my case, a production load balancer defaulted to a max-header count of 64. This meant the page was generated on the server, and loaded fine, but the response was dropped by the production load balancer silently. Since the partial views being added were in a loop, the exact same page loading slightly different data would work, but only on ones that had less than 64 headers included. The only reason I ended up discovering this was the issue in the first place was because we had already spent over 10 hours working on this problem (including me, other devs, and ops guys), and with no luck on figuring out the issue, I decided to look at the X-Frame-Options issue, just to see if I could solve at least ONE problem. 

## The Solution


To prevent Microsoft from auto-adding the header for every AntiForgery token, you can update the application_start and set the AntiForgeryConfig.SuppressXFrameOptionsHeader to true in your global.asax or equivalent:

    protected void Application_Start() {

    AntiForgeryConfig.SuppressXFrameOptionsHeader = true;

    }


Do note though, this removes the X-Frame-Options header entirely. Like I mentioned above, it’s good to have it to prevent clickjacking. To make sure a single copy of that header is added to the response, you can update your web.config so IIS adds a single X-Frame-Options to all requests. Scroll down partway on this page to see what to add: 
[https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options)



So there you have it, the function, the issue, and solution. Good luck, and hopefully Microsoft will document this better in the future!
