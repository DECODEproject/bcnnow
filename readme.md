## BarcelonaNow: Interactive Dashboards for Urban Data Exploration
[![Build Status](https://travis-ci.org/pages-themes/cayman.svg?branch=master)](https://travis-ci.org/pages-themes/cayman)
[![GitHub version](https://badge.fury.io/gh/boennemann%2Fbadges.svg)](http://badge.fury.io/gh/boennemann%2Fbadges)
[![Dependency Status](https://david-dm.org/boennemann/badges.svg)](https://david-dm.org/boennemann/badges)
[![Open Source Love](https://badges.frapsoft.com/os/gpl/gpl.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)

This is an environment which enables citizens to create and explore interactive visualizations of city-related data and arrange them into dashboards. The solution offers customization capabilities to different user-defined exploration scenarios and techniques according to specific needs and goals. The back-end data aggregator and manipulator built upon state-of-the-art technologies provides normalized access to heterogeneous data. On top of it, the front-end interface allows users to create and combine visualizations, get insights out of the data and share them with others, fostering data-driven public awareness. 

* [Online Demo](http://bcnnow.decodeproject.eu) 
* [Documentation](https://decodeproject.github.io/bcnnow/) 

## Installation 
Ready to install BarcelonaNow's environment? Here's how to get started on Linux.

Install Python (>=3.5):
```
$ sudo apt-get update
$ sudo apt-get install python3.5
```
Install and run MongoDB:
```
$ sudo apt-get update
$ sudo apt-get install -y mongodb-org
$ sudo service mongod restart
```
Install and run Apache:
```
$ sudo apt-get update
$ sudo apt-get install apache2
$ sudo ufw allow 'Apache Full'
$ sudo systemctl restart apache2
```
Clone this repository: 
```
$ git clone https://github.com/DECODEproject/bcnnow.git
```
Install all the required dependencies:
```
$ pip install -r bcnnow-master/requirements.txt
```
Copy the dashboard app folder into the Apache public folder:
```
$ cp 'bcnnow-master/apps/dashboard' '/var/www/html/'
```

## Usage
Once it is installed, let's run BarcelonaNow to see your dashboards online.

Open the crontab:
```
$ crontab -e
```
Copy and save the following commands:
```
* * */30 * * python3 bcnnow-master/backend/data/collectors/pull/AsiaEventCollector.py
*/10 * * * * python3 bcnnow-master/backend/data/collectors/pull/BicingCollector.py
* * */30 * * python3 bcnnow-master/backend/data/collectors/pull/EquipmentCollector.py
* * */90 * * python3 bcnnow-master/backend/data/collectors/pull/IrisCollector.py
* * */30 * * python3 bcnnow-master/backend/data/collectors/pull/PointsInterestCollector.py
*/30 * * * * python3 bcnnow-master/backend/data/collectors/pull/SentiloCollector.py
*/60 * * * * python3 bcnnow-master/backend/data/collectors/pull/SmartCitizenCollector.py
```
Run BarcelonaNow's API in background (see this [link](http://flask.pocoo.org/docs/0.12/deploying/) for Flask deployment in production):
```
nohup python3 bcnnow-master/backend/logic/api/v0/app.py &
```
Open your browser at the following link:
```
http://localhost/
```

## Contributing
We welcome contributions. Feel free to file issues and pull requests on the repo and we will address them as we can.

For questions or feedback about BarcelonaNow, contact us at [david.laniado@eurecat.org](http://) and [mirko.marras@ce.eurecat.org](http://).

## Citations
If you use BarcelonaNow in your research, please use the following entries.

```
Mirko Marras, Matteo Manca, Ludovico Boratto, Gianni Fenu, and David Laniado. 2018. 
BarcelonaNow: Empowering Citizens with Interactive Dashboards for Urban Data Exploration. 
In WWW ’18 Companion: The 2018 Web Conference Companion, April 23–27, 2018, Lyon, France. 
ACM, New York, NY, USA.
```

```
@inproceedings{marras2018barcelonanow,
  title={BarcelonaNow: Empowering Citizens with Interactive Dashboards for Urban Data Exploration},
  author={Marras, Mirko and Manca, Matteo and Boratto, Ludovico and Fenu, Gianni and Laniado, David},
  booktitle={Proceedings of the 2018 Web Conference Companion},
  year={2018},
  organization={International World Wide Web Conference Committee (IW3C2)}
}
```
## Credits and License
Copyright (C) 2018 by the [EURECAT - Technology Centre of Catalonia](https://www.decodeproject.eu/).

The European Union Horizon 2020 Programme under grant agreement N.732546 has been supporting this on-going pilot work during the [DECODE (DEcentralised Citizens Owned Data Ecosystem)](https://eurecat.org/en/) project.

This source code is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This software is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for details.

You should have received a copy of the GNU General Public License along with this source code. If not, go the following link: http://www.gnu.org/licenses/.

