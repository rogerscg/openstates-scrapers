'''Note, this needs to scrape both assembly and senate sites. Neither
house has the other's votes, so you have to scrape both and merge them.
'''
import re
import datetime
from collections import defaultdict

from billy.utils import term_for_session
from billy.scrape.bills import BillScraper, Bill
from billy.scrape.votes import Vote

import scrapelib
import lxml.html
import lxml.etree

from .models import AssemblyBillPage, SenateBillPage
from .actions import Categorizer


class NYBillScraper(BillScraper):

    jurisdiction = 'ny'
    categorizer = Categorizer()

    def scrape(self, chamber, session):

        term_id = term_for_session('ny', session)
        for term in self.metadata['terms']:
            if term['name'] == term_id:
                break

        index = 0
        bills = defaultdict(list)

        billdata = defaultdict(lambda: defaultdict(list))
        for year in (term['start_year'], term['end_year']):
            while True:

                index += 1
                url = (
                    'http://open.nysenate.gov/legislation/2.0/search.json'
                    '?term=otype:bill AND year:2013=&pageSize=20&pageIdx=%d'
                    )
                url = url % index
                resp = self.urlopen(url)

                data = resp.response.json()
                if not data['response']['results']:
                    break

                for bill in data['response']['results']:
                    details = self.bill_id_details(bill)
                    if details is None:
                        continue
                    (senate_url, assembly_url, bill_chamber, bill_type, bill_id,
                     title, (letter, number, is_amd)) = details
                    bills[(letter, number)].append((bill, details))

        for billset in bills.values():
            self.scrape_bill(session, chamber, bills)

    def scrape_bill(self, session, chamber, bills):

        billdata, details = bills[0][0]

        (senate_url, assembly_url, bill_chamber, bill_type, bill_id,
         title, (letter, number, is_amd)) = details

        data = billdata['data']['bill']
        source_url = billdata['url']
        bill = Bill(session, chamber, bill_id, data['title'])
        bill.add_source(senate_url)
        bill.add_source(assembly_url)

        # Add prime sponsor.
        bill.add_sponsor(name=data['sponsor']['fullname'], type='primary')

        # Add cosponsors.
        for sponsor in data['coSponsors'] + data['multiSponsors']:
            if sponsor['fullname']:
                bill.add_sponsor(name=sponsor['fullname'], type='cosponsor')

        for action in data['actions']:
            timestamp = int(action['date'])
            action_text = action['text']
            date = self.date_from_timestamp(timestamp)
            actor = 'upper' if action_text.isupper() else 'lower'
            attrs = dict(actor=actor, action=action_text, date=date)
            categories, kwargs = self.categorizer.categorize(action_text)
            attrs.update(kwargs, type=categories)
            bill.add_action(**attrs)

        # Add companion.
        if data['sameAs']:
            bill.add_companion(data['sameAs'])

        if data['summary']:
            bill['summary'] = data['summary']

        if data['votes']:
            for vote_data in data['votes']:
                vote = Vote(
                    chamber='upper',
                    date=self.date_from_timestamp(vote_data['voteDate']),
                    motion=vote_data['description'] or '[No motion available.]',
                    passed=False,
                    yes_votes=[],
                    no_votes=[],
                    other_votes=[],
                    yes_count=0,
                    no_count=0,
                    other_count=0)

                for name in vote_data['ayes']:
                    vote.yes(name)
                    vote['yes_count'] += 1
                for names in map(vote_data.get, ['absent', 'excused', 'abstains']):
                    for name in names:
                        vote.other(name)
                        vote['other_count'] += 1
                for name in vote_data['nays']:
                    vote.no(name)
                    vote['no_count'] += 1

                bill.add_vote(vote)

        # if data['previousVersions']:
        #   These are instances of the same bill from prior sessions.
        #     import pdb; pdb.set_trace()

        if not data['title']:
            bill['title'] = bill['summary']

        self.save_bill(bill)

    def date_from_timestamp(self, timestamp):
        return datetime.datetime.fromtimestamp(int(timestamp) / 1000)

    def bill_id_details(self, billdata):
        data = billdata['data']['bill']
        api_id = billdata['oid']
        source_url = billdata['url']

        title = data['title'].strip()
        if not title:
            return

        # Parse the bill_id into beginning letter, number
        # and any trailing letters indicating its an amendment.
        bill_id, year = api_id.split('-')
        bill_id_rgx = r'(^[A-Z])(\d{,6})([A-Z]{,3})'
        bill_id_base = re.search(bill_id_rgx, bill_id)
        letter, number, is_amd = bill_id_base.groups()

        bill_chamber, bill_type = {
            'S': ('upper', 'bill'),
            'R': ('upper', 'resolution'),
            'J': ('upper', 'legislative resolution'),
            'B': ('upper', 'concurrent resolution'),
            'A': ('lower', 'bill'),
            'E': ('lower', 'resolution'),
            'K': ('lower', 'legislative resolution'),
            'L': ('lower', 'joint resolution')}[letter]

        senate_url = billdata['url']

        assembly_url = (
            'http://assembly.state.ny.us/leg/?'
            'default_fld=&bn=%s&Summary=Y&Actions=Y') % bill_id

        return (senate_url, assembly_url, bill_chamber, bill_type, bill_id,
                title, (letter, number, is_amd))
