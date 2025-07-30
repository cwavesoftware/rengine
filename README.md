<p align="center">
<a href="https://rengine.wiki"><img src=".github/screenshots/banner.gif" alt=""/></a>
</p>

<p align="center">
</a>&nbsp;<a href="https://www.gnu.org/licenses/gpl-3.0" target="_blank"><img src="https://img.shields.io/badge/License-GPLv3-red.svg?&logo=none" alt="License" /></a>&nbsp;<a href="https://github.com/cwavesoftware/rengine/issues" target="_blank"><img src="https://img.shields.io/github/issues/cwavesoftware/rengine?color=red&logo=none" alt="reNgine Issues" /></a>&nbsp;<a href="#" target="_blank"><img src="https://img.shields.io/badge/first--timers--only-friendly-blue.svg?&logo=none" alt="" /></a></p>

<p align="left">An automated reconnaissance framework for web applications with focus on highly configurable streamlined recon process via Engines, recon data correlation and organization, continuous monitoring, backed by database and simple yet intuitive User Interface.</p>

<p align="left">
reNgine makes is easy for penetration testers to gather reconnaissance with minimal configuration and with the help of reNgine's correlation, it just makes recon effortless.
</p>

Dashboard             |  Scan Results
:-------------------------:|:-------------------------:
![](.github/screenshots/1.gif)  |  ![](.github/screenshots/2.gif)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Table of Contents

* [About reNgine](#about-reNgine)
* [Features](#features)
* [Documentation](#documentation)
* [Screenshots](#screenshots)
* [Prerequisites](#presequisites)
* [Installation](#installation)
* [Related Projects](#related-projects)
* [Support and Sponsor](#support-and-sponsoring)
* [Acknowledgements & Credits](#acknowledgements-and-credits)
* [License](#license)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## About reNgine

<img src=".github/screenshots/rengine_1.jpeg">

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

reNgine is an automated reconnaissance framework with a focus on a highly configurable streamlined recon process. reNgine is backed by a database, with data correlation and organization, the custom query “like” language for recon data filtering, reNgine aims to address the shortcomings of traditional recon workflow. Developers behind the reNgine understand that recon data can be huge, manually looking up for entries to attack could be cumbersome, with features like Auto Interesting Subdomains discovery, reNgine automatically identifies interesting subdomains to attack based on certain keywords (both built-in and custom) and helps penetration testers focus on attack rather than recon.

reNgine is also focused on continuous monitoring. Penetration testers can choose to schedule the scan at periodic intervals, get notified on notification channels like Discord, Slack, and Telegram for any new subdomains or vulnerabilities identified, or any recon data changes.

Interoperability is something every recon tool needs, and reNgine is no different. Beginning reNgine 1.0, we additionally developed features such as import and export subdomains, endpoints, GF pattern matched endpoints, etc. This will allow you to use your favourite recon workflow in conjunction with reNgine.

reNgine features Highly configurable scan engines based on YAML, that allows penetration testers to create as many recon engines as they want of their choice, configure as they wish, and use it against any targets for the scan. These engines allow penetration testers to use tools of their choice, the configuration of their choice. Out of the box, reNgine comes with several scan engines like Full Scan, Passive Scan, Screenshot gathering, OSINT Engine, etc.

Our focus has always been on finding the right recon data with very minimal effort. While having a discussion with fellow hackers/pentesters, screenshots gallery was a must, reNgine 1.0 also comes with a screenshot gallery, and what's exciting than having a screenshot gallery with filters, filter screenshots with HTTP status, technology, ports, and services.

We also want our fellow hackers to stay ahead of the game, reNgine 1.0 introduces automatic vulnerability reporting (currently only Hackerone is supported, other platforms *may* come soon). This allows hackers to define their own vulnerability report template and reNgine will do the rest of the job to report vulnerability as soon as it is identified.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Features

- Perform Recon: Subdomain Discovery, Ports Discovery, Endpoints Discovery, Directory Bruteforce, Screenshot gathering
- IP Discovery, CNAME discovery, Vulnerability scan using Nuclei
- Ability to Automatically report Vulnerabilities to Hackerone
- Support for Parallel Scans
- Recon Data visualization
- Highly configurable scan engines
- OSINT Capabilities (Metainfo Gathering, Employees Gathering, Email Address with option to look password in leaked database, dorks etc)
- Customizable Alerts/Notification on Slack, Discord and Telegram
- Perform Advanced Query lookup using natural language alike and, or, not operations
- Support for Recon Notes and Todos
- Support for Clocked Scans (Run reconnaissance exactly at X Hours and Y minutes) and Periodic Scans (Runs reconnaissance every X minutes/hours/days/week)
- Proxy Support
- Screenshot Gallery with Filters
- Powerful recon data filtering with auto suggestions
- Recon Data changes, finds new/removed subdomains/endpoints
- Support for tagging targets into Organization
- Ability to identify Interesting Subdomains
- Support for custom GF patterns and custom Nuclei Templates
- Support for editing tool related configuration files (Nuclei, Subfinder, Naabu, amass)
- Ability to Mark Important Subdomains
- Interoperable with other tools, Import/Export Subdomains/Endpoints
- Option to send scan data directly to discord

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Documentation

The core features of reNgine are documented in the author's [original docs](https://rengine.wiki). This fork has additional features that <b>might</b> be documented at some point. Feel free to look into the code or check the commit history to get an idea about what has beed added.

## Screenshots

**General Usage**
<img src=".github/screenshots/3.gif">

**Dark Mode**
<img src=".github/screenshots/dark.gif">

**Recon Data filtering**
<img src=".github/screenshots/filtering.gif">

<details>
  <summary>Other Screenshots (Click to Expand!)</summary>

  **Auto Report Vulnerability to hackerone with customizable vulnerability report template**
  <img src=".github/screenshots/hackerone1.gif">

  **Report Vulnerability Manually**
  <img src=".github/screenshots/hackerone.gif">

  **Customizable Notification**
  <img src=".github/screenshots/notif.gif">

  **Tagging Organization**
  <img src=".github/screenshots/organization.gif">

  **Recon data Visualization**
  <img src=".github/screenshots/visualization.gif">

  **Upload custom GF and Nuclei patterns, with option to edit tool configuration**
  <img src=".github/screenshots/tool.gif">

  **Recon TODO**
  <img src=".github/screenshots/todo.gif">

</details>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)  

## Presequisites
* [docker](https://docs.docker.com/get-docker/)
* [docker-compose](https://github.com/docker/compose)

## Installation

1. Clone this repo

```
git clone https://github.com/cwavesoftware/rengine && cd rengine
```

2. Edit the dotenv file, **please make sure to change the password for postgresql POSTGRES_PASSWORD !**

```
vim .env
```

3. Start the services

```
docker-compose up -d
```

4. Create user
```
docker-compose exec web python3 manage.py createsuperuser
```

**reNgine can now be accessed from https://127.0.0.1 or if you're on the VPS https://your_vps_ip_address**

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Related Projects

There are many other great reconnaissance frameworks, you may use reNgine in conjunction with these tools. But, they themselves are great, and may sometimes even produce better results than reNgine.

- [ReconFTW](https://github.com/six2dez/reconftw#sample-video)
- [Osmedeus](https://github.com/j3ssie/Osmedeus)
- [EchoPwn](https://github.com/hackerspider1/EchoPwn)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Support and Sponsoring
If reNgine has helped you in any way, and you love this project and/or support active development of reNgine, please consider any of these options:

- Add a [GitHub Star](https://github.com/cwavesoftware/rengine) to the project.
- Tweet about this project, or maybe blogs?

Together, we can make reNgine **better** every day!


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Acknowledgements and Credits
***This is a fork of the original [reNgine](https://github.com/yogeshojha/rengine). Main credits go to [yogeshojha](https://github.com/yogeshojha).***

reNgine would not have been possible without the following individuals/organizations. Thanks to these amazing devs/hackers!

- Project Discovery
  - nuclei, httpx, naabu, subfinder
- Tom Hudson
  - gf, assetfinder, waybackurls, unfurl
- OWASP
  - amass
- Ahmed Aboul-Ela
  - Sublist3r
- Mauro Soria
  - dirsearch
- Corben Leo
  - gau
- Luke Stephens
  - hakrawler
- Jaeles Project
  - gospider
- Jing Ling
  - OneForAll
- FortyNorthSecurity
  - EyeWitness
- Davidtavarez
  - pwndb
- Deepseagirl
  - degoogle
- Josué Encinar
  - Metafinder, Emailfinder
- Bp0lr
  - gauplus
- Nicolas Crocfer
  - whatportis
- Helmut Wandl
  - Gridzy.js

<div>reNgine official Icon is made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## License
Distributed under the GNU GPL v3 License. See [LICENSE](LICENSE) for more information.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)
