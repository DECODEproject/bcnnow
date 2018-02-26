'''
    BarcelonaNow (c) Copyright 2018 by the Eurecat - Technology Centre of Catalonia

    This source code is free software; you can redistribute it and/or
    modify it under the terms of the GNU Public License as published
    by the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.

    This source code is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    Please refer to the GNU Public License for more details.

    You should have received a copy of the GNU Public License along with
    this source code; if not, write to:
    Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
'''


# This class defines a set of configuration variables for ASIA collector.
class Config:

    def __init__(self):
        self.config = {
            "collectors": {
                  "odi": {
                              "source_name": "odi",
                              "asia": {
                                        "source_name": "asia",
                                        "source_type": "event",
                                        "equipment_base_url": "http://www.bcn.cat/tercerlloc/",
                                        "equipment_urls" : ['esports.rdf',
                                                           'restaurants.rdf',
                                                           'educacio.rdf',
                                                           'sanitat.rdf',
                                                           'cementiris.rdf',
                                                           'comercial.rdf',
                                                           'transports.rdf',
                                                           'mediambient.rdf',
                                                           'cultura.rdf',
                                                           'religio.rdf',
                                                           'associacions.rdf',
                                                           'administracio_publica.rdf',
                                                           'centres_informacio.rdf',
                                                           'animals_plantes.rdf',
                                                           'serveis_socials.rdf',
                                                           'comunicacio.rdf'],
                                        "petition_base_url": "http://w10.bcn.es/APPS/asiasiacache/peticioXmlAsia?id=",
                                        "petition_urls": ['103',
                                                          '104',
                                                          '105',
                                                          '106'],
                              }
                  }
            }
        }

    def get(self):
        return self.config