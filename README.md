# mbtpi
 a wrapper for the mbta api

<a id="contents"></a>
### Contents
- [How To Use](#htu)
- [Features](#feat)
- [API Information](#api)
- [Notes](#notes)

<a id="htu"></a>
# How To Use

GitHub:
- First, clone the repo.
- Locate the [.env.example](src/mbtpi/.env.example) file in the src/mbtpi root. 
Make a copy, name it `.env`, and replace the dummy value for 'MBTA_API_KEY' with your key.

[Back to contents](#contents)

<a id="feat"></a>
# Features
Supplies the ability to work with objects (ex. ALERT, LINE, STOP) as well as JSON.

Supports all endpoints of the MBTA API, including:
- alerts
- facilities
- lines
- live facilities
- predictions
- routes
- route patterns
- schedules
- services
- shapes
- stops
- trips
- vehicles

as well as all parameters those endpoints accept.

[Back to contents](#contents)

<a id="api"></a>
# API Information
This code is written for version 3 of the MBTA API, which follows JSON API standard.

API Link: https://api-v3.mbta.com/

Developer Page: https://www.mbta.com/developers/v3-api

Key Registration: https://api-v3.mbta.com

Developer Group: https://groups.google.com/g/massdotdevelopers

[Back to contents](#contents)

<a id="notes"></a>
# Notes

Repository link: https://github.com/Anzhuo-W/mbtpi

- Bug? Check if it's related to making requests to the API. If not, open an issue on GitHub and tag it `bug`.
- Feature request? Tag your issue `feature request`.

This wrapper is not officially affiliated with the MBTA.

[Back to contents](#contents)