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

# This class defines a set of configuration variables for Smart Citizen collector.
class Config:

    def __init__(self):
        self.config = {
            "collectors": {
                "decidim": {
                    "pam_proposal": {
                        "source_name": "pam_proposal",
                        "base_url": "https://www.decidim.barcelona/api",
                        "query" : [
                            "{ participatoryProcess(id: 1) { id title { translations { locale text } } components { id name { translations { text } } ... on Proposals { proposals(after: \"\") { pageInfo { endCursor startCursor } edges { node { id title reference voteCount publishedAt scope { id name { translations { text } } } } } } } } } }"
                            ]
                    },
                    "pam_meeting": {
                        "source_name": "pam_meeting",
                        "base_url": "https://www.decidim.barcelona/api",
                        "query" : [
                            "{ participatoryProcess(id: 1) { id title { translations { locale text } } components { id name { translations { text } } ... on Meetings { meetings(after: \"\") { pageInfo { endCursor startCursor } edges { node { id startTime endTime attachments { url } reference                            reference attendeeCount scope { id name { translations { text } } } title { translations { text } } coordinates { longitude latitude } address } } } } } } }"
                            ]
                    }
                }
            }
        }

    def get(self):
        return self.config
