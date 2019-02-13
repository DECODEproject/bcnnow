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
                        "component_id": 0,
                        "base_url": "https://www.decidim.barcelona/api",
                        "query" : [
                            "{ participatoryProcess(id: 1) { id title { translations { locale text } } components { id name { translations { text } } ... on Proposals { proposals(after: \"\") { pageInfo { endCursor startCursor } edges { node { id title reference voteCount totalCommentsCount publishedAt category { id name { translations { text } } } scope { id name { translations { text } } } } } } } } } }"
                            ]
                    },
                    "pam_meeting": {
                        "source_name": "pam_meeting",
                        "component_id": 1,
                        "base_url": "https://www.decidim.barcelona/api",
                        "query" : [
                            "{ participatoryProcess(id: 1) { id title { translations { locale text } } components { id name { translations { text } } ... on Meetings { meetings(after: \"\") { pageInfo { endCursor startCursor } edges { node { id startTime endTime attachments { url } reference attendeeCount totalCommentsCount contributionCount scope { id name { translations { text } } } title { translations { text } } coordinates { longitude latitude } address } } } } } } }"
                            ]
                    },
                    "dddc_proposal": {
                        "source_name": "dddc_proposal",
                        "component_id": 2,
                        "base_url": "https://dddc.decodeproject.eu/api",
                        "query" : [
                            "{ participatoryProcess(id: 1) { id title { translations { locale text } } components { id name { translations { text } } ... on Proposals { proposals(after: \"\") { pageInfo { endCursor startCursor } edges { node { id title reference voteCount totalCommentsCount publishedAt category { id name { translations { text } } } } } } } } } }"
                            ]
                    },
                    "dddc_meeting": {
                        "source_name": "dddc_meeting",
                        "component_id": 0,
                        "base_url": "https://dddc.decodeproject.eu/api",
                        "query" : [
                            "{ participatoryProcess(id: 1) { id title { translations { locale text } } components { id name { translations { text } } ... on Meetings { meetings(after: \"\") { pageInfo { endCursor startCursor } edges { node { id title { translations { text } } address coordinates { longitude latitude } reference startTime endTime attachments { url } attendeeCount totalCommentsCount contributionCount } } } } } } }"
                            ]
                    },
                    "dddc_survey": {
                        "source_name": "dddc_survey",
                        "component_id": 0,
                        "base_url": "answers/",
                        "paths" : ["demographics.json"]
                    }
                }
            }
        }

    def get(self):
        return self.config
