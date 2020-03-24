from openstates.utils import url_xpath, State
from .bills import MDBillScraper
from .people import MDPersonScraper
from .events import MDEventScraper
from .votes import MDVoteScraper

# from .committees import MDCommitteeScraper


class Maryland(State):
    scrapers = {
        "bills": MDBillScraper,
        "people": MDPersonScraper,
        "events": MDEventScraper,
        "votes": MDVoteScraper,
        # 'committees': MDCommitteeScraper,
    }
    legislative_sessions = [
        {
            "_scraped_name": "2007 Regular Session",
            "classification": "primary",
            "identifier": "2007",
            "name": "2007 Regular Session",
            "start_date": "2007-01-10",
            "end_date": "2007-04-10",
        },
        {
            "_scraped_name": "2007 Special Session 1",
            "classification": "special",
            "identifier": "2007s1",
            "name": "2007, 1st Special Session",
            "start_date": "2007-10-29",
            "end_date": "2007-11-19",
        },
        {
            "_scraped_name": "2008 Regular Session",
            "classification": "primary",
            "identifier": "2008",
            "name": "2008 Regular Session",
            "start_date": "2008-01-09",
            "end_date": "2008-04-07",
        },
        {
            "_scraped_name": "2009 Regular Session",
            "classification": "primary",
            "identifier": "2009",
            "name": "2009 Regular Session",
            "start_date": "2009-01-14",
            "end_date": "2009-04-13",
        },
        {
            "_scraped_name": "2010 Regular Session",
            "classification": "primary",
            "identifier": "2010",
            "name": "2010 Regular Session",
            "start_date": "2010-01-13",
            "end_date": "2010-04-12",
        },
        {
            "_scraped_name": "2011 Regular Session",
            "classification": "primary",
            "identifier": "2011",
            "name": "2011 Regular Session",
            "start_date": "2011-01-12",
            "end_date": "2011-04-12",
        },
        {
            "_scraped_name": "2011 Special Session 1",
            "classification": "special",
            "identifier": "2011s1",
            "name": "2011, 1st Special Session",
            "start_date": "2011-10-17",
            "end_date": "2012-10-20",
        },
        {
            "_scraped_name": "2012 Regular Session",
            "classification": "primary",
            "identifier": "2012",
            "name": "2012 Regular Session",
            "start_date": "2012-01-11",
            "end_date": "2012-04-09",
        },
        {
            "_scraped_name": "2012 Special Session 1",
            "classification": "special",
            "identifier": "2012s1",
            "name": "2012, 1st Special Session",
            "start_date": "2012-05-14",
            "end_date": "2012-05-16",
        },
        {
            "_scraped_name": "2012 Special Session 2",
            "classification": "special",
            "identifier": "2012s2",
            "name": "2012, 2nd Special Session",
            "start_date": "2012-08-09",
            "end_date": "2012-08-15",
        },
        {
            "_scraped_name": "2013 Regular Session",
            "classification": "primary",
            "identifier": "2013",
            "name": "2013 Regular Session",
            "start_date": "2013-01-09",
            "end_date": "2013-04-08",
        },
        {
            "_scraped_name": "2014 Regular Session",
            "classification": "primary",
            "identifier": "2014",
            "name": "2014 Regular Session",
            "start_date": "2014-01-08",
            "end_date": "2014-04-07",
        },
        {
            "_scraped_name": "2015 Regular Session",
            "classification": "primary",
            "identifier": "2015",
            "name": "2015 Regular Session",
            "start_date": "2015-01-14",
            "end_date": "2015-04-13",
        },
        {
            "_scraped_name": "2016 Regular Session",
            "classification": "primary",
            "identifier": "2016",
            "name": "2016 Regular Session",
            "start_date": "",
            "end_date": "",
        },
        {
            "_scraped_name": "2017 Regular Session",
            "classification": "primary",
            "identifier": "2017",
            "name": "2017 Regular Session",
            "start_date": "2017-01-11",
            "end_date": "2017-04-10",
        },
        {
            "_scraped_name": "2018 Regular Session",
            "classification": "primary",
            "identifier": "2018",
            "name": "2018 Regular Session",
            "start_date": "2018-01-10",
            "end_date": "2018-04-09",
        },
        {
            "_scraped_name": "2019 Regular Session",
            "classification": "primary",
            "identifier": "2019",
            "name": "2019 Regular Session",
            "start_date": "2019-01-09",
            "end_date": "2019-04-11",
        },
        {
            "_scraped_name": "2020 Regular Session",
            "classification": "primary",
            "identifier": "2020",
            "name": "2020 Regular Session",
            "start_date": "2020-01-08",
            "end_date": "",
        },
    ]
    ignored_scraped_sessions = [
        "1996 Regular Session",
        "1997 Regular Session",
        "1998 Regular Session",
        "1999 Regular Session",
        "2000 Regular Session",
        "2001 Regular Session",
        "2002 Regular Session",
        "2003 Regular Session",
        "2004 Regular Session",
        "2004 Special Session 1",
        "2005 Regular Session",
        "2006 Regular Session",
        "2006 Special Session 1",
    ]

    def get_session_list(self):
        return url_xpath(
            "http://mgaleg.maryland.gov/mgawebsite/Search/Legislation",
            '//select[@id="valueSessions"]/option/text()',
        )
