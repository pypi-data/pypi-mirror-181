<div align="center">
<a href="https://janda.mod.land"><img width="600" src="https://cdn.discordapp.com/attachments/1046495201176334467/1053334095737917600/jikanmia.png" alt="jandapress"></a>

<h4 align="center">Python client for Jikan.moe, with simplicity in mind.</h4>
<p align="center">
	<a href="https://github.com/sinkaroid/jandapress/actions/workflows/status.yml"><img src="https://github.com/sinkaroid/jandapress/actions/workflows/status.yml/badge.svg"></a>
	<a href="https://codeclimate.com/github/sinkaroid/jandapress/maintainability"><img src="https://api.codeclimate.com/v1/badges/829b8fe63ab78a425f0b/maintainability" /></a>
</p>

 
The motivation is simplified the api call, apply customizable, and user should have no worries with ratelimit.  
Jikan4snek simulating the requests with saved cache and apply coroutine delay if cache was expired.

<a href="https://github.com/sinkaroid/jandapress/blob/master/CONTRIBUTING.md">Contributing</a> •
<a href="https://github.com/sinkaroid/jandapress/wiki/Routing">Documentation</a> •
<a href="https://github.com/sinkaroid/jandapress/issues/new/choose">Report Issues</a>
</div>

---

<a href="https://janda.mod.land"><img align="right" src="https://cdn.discordapp.com/attachments/1046495201176334467/1053335219828174978/miaaa.png" width="450"></a>

- [Jandapress](#)
  - [The problem](#the-problem)
  - [The solution](#the-solution)
  - [Features](#features)
    - [Jandapress vs. the doujinboards](#jandapress-vs-the-whole-doujin-sites)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Running tests](#running-tests)
  - [Routing](#routing)
    - [nhentai-api](#routing)
    - [pururin-api](#routing)
    - [hentaifox-api](#routing)
  - [Limitations](#limitations)
  - [Pronunciation](#Pronunciation)
  - [Legal](#legal)
  - [FAQ](#Frequently-asked-questions)
  - [Client libraries / Wrappers](#client-libraries--wrappers)



## Features

- Has own ratelimit flow
- Set expiration time for cache
- Simplified, nested method call
- Covers 80% of the v4 Jikan endpoints
- Easy to use, check your intelisense
