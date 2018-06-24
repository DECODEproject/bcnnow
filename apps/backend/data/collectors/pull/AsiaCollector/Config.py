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