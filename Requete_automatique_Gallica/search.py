# -*- coding: utf-8 -*-
#from urllib.parse import quote_plus #plus utilisé, remplacé par package immédiatement en-dessous
import urllib.parse

import requests
import re
from bs4 import BeautifulSoup
from document import Document
from parallel_process import request_and_parse_urls
from utils import makelist, request_and_parse

NUM_RESULTS_PER_QUERY = 15
SRU_BASEURL = 'https://gallica.bnf.fr/SRU?version=1.2&operation=searchRetrieve&suggest=0&query='


class Search(object):
    """Gallica search object"""
    def __init__(self, prox_fields=False, all_fields=None, dc_type=None, dc_creator=None, dc_title=None, dc_date=None, dc_Lib=None, dc_format=None, dc_geo=None, dc_langue=None, and_query=True, expansion="o", **kwargs):
        """Accepts all the elements of a search query as arguments.
        The kwargs is an optional additional parameter that can be specified"""

        self.base_query = build_query(prox_fields, all_fields, dc_type, dc_creator, dc_title, dc_date, dc_Lib, dc_format, dc_geo, dc_langue, and_query, expansion, **kwargs)
        self.total_records = self.get_total_records()
        print("There are " + str(self.total_records) + " records !")

    def execute(self, max_records=-1, processes=16, progress=True, worden=''):
        """Execute the query of the search.
        max_records can be used to choose the closest multiple of NUM_RESULTS_PER_QUERY to retrieve.
        Its default value (-1) retrieves all records.
        Store the raw results in self.records
        Store the parsed document objects in self.documents
        Store the urls of failures in self.failures
        Returns True if all the records were retrieved, False if there is some failures"""

        total_records = self.total_records
        if max_records != -1 and max_records < self.total_records:
            total_records = max_records

        # Generate the list of all urls for all records up to total_records
        print("Commence parsing")
        urls = [self.base_query + "&maximumRecords=%d" % NUM_RESULTS_PER_QUERY +
                "&startRecord=%d" % offset
                for offset in range(1, total_records+1, NUM_RESULTS_PER_QUERY)]
        print("Complete URLs are : "+ str(urls))
        records, failures = request_and_parse_search_queries(urls, processes, progress)
        
        self.documents = list(map(generate_document_from_record, records))
        while 'oops' in self.documents :
        	self.documents.remove('oops')
        self.records = records
        print("RECORDS : ", records)
        self.failures = failures
        print("FAILURES : ", failures)
        
        #half-injected from first wrapper to have an xml with the results
        nb = 0
        for i in urls: #for every page (15 results) of a given pair of words
            print("Loop " + str(urls.index(i)) + "\n")
            s = requests.get(urls[urls.index(i)], stream=True)
            soup = BeautifulSoup(s.content,"html.parser")
            worde = re.sub("\\\\", "", worden)
            print(worde)
            with open('gallica{}.xml'.format(worde + '_' + str(urls.index(i))), 'wb') as f:
                f.write(soup.prettify().encode('UTF-8'))
                f.close()
            nb += 1
        if total_records == 0 :
            nb = -1
        return nb

    def retry(self, processes=1, progress=True):
        """Retry to execute the query only on the failed urls.
        Otherwise behaves like self.execute.
        """
        if len(self.failures) <= 0:
            return True
        records, failures = request_and_parse_search_queries(self.failures,
                                                             processes,
                                                             progress)
        self.records += records
        self.documents += list(map(generate_document_from_record, records))
        self.documents = self.documents.remove('')
        self.failures = failures
        return len(self.failures) == 0

    def get_total_records(self):
        """Fetch in the search result the total number of records"""
        result_parsed = request_and_parse(self.base_query + "&maximumRecords=0")
        try:
            return int(result_parsed['srw:searchRetrieveResponse']['srw:numberOfRecords'])
        except KeyError:
            return 0


def generate_document_from_record(record):
    """Given the xml of a record create a gallica document object"""
    try:
        ark = list(filter(lambda x: 'ark' in x, makelist(record['dc:identifier'])))[0].replace('https://gallica.bnf.fr/ark:/', '')
    except IndexError:
        return 'oops'
    return Document(ark)

def build_query(prox_fields=False, all_fields=None, dc_type=None, dc_creator=None, dc_title=None, dc_date=None, dc_Lib=None, dc_format=None, dc_geo=None, dc_langue=None, and_query=True, expansion="o",  **kwargs):
    """Given different search arguments build the url of the search query."""

    def build_param(field, query, all_fields=True, date_format=False, prox_format=False, exp=expansion):
        if date_format:
            sesect = ''
        elif all_fields:
            if exp=="o":
                sesect = 'all'
                
            else:    
                sesect = 'adj'
        else:
            sesect = 'any'
        if prox_format :
            query1 = query[0]
            query2 = query[1]
            return '%s%%20%s%%20%s%%20%s%%20%s' % (field, sesect, urllib.parse.quote(str(query1)), "prox/unit=word/distance="+str(prox_fields), urllib.parse.quote(str(query2)))
        return '%s%%20%s%%20%s' % (field, sesect, urllib.parse.quote(str(query)))

    if not all_fields and not dc_type and not dc_creator and not dc_title and not dc_date and not dc_Lib and not dc_format and not dc_geo and not dc_langue and not kwargs:
        raise ValueError("Search should contain at least on query")
    query = SRU_BASEURL
    params = []
    if all_fields:
        if prox_fields:
            n_fields = all_fields.strip("()")
            woo1 = n_fields.split(', ', 1)[0]
            woo2 = n_fields.split(', ', 1)[1]

            wo1 = '"' + woo1.strip("''") + '"'


            wo1 = re.sub('[\"\"]','', wo1)
            wo1 = '"' + wo1 + '"'
            
            wo2 = '"' + woo2.strip("''") + '"'


            wo2 = re.sub('[\"\"]','', wo2)
            wo2 = '"' + wo2 + '"'
            
            params.append(build_param('gallica', (wo1, wo2) , prox_format = True))
        else:
            params.append(build_param('gallica', all_fields, all_fields=True, prox_format = False))
    if dc_type:
        params.append(build_param('dc.type', dc_type, all_fields=False))
    if dc_creator:
        params.append(build_param('dc.creator', dc_creator))
    if dc_title:
        params.append(build_param('dc.title', dc_title))
    if dc_date :
        params.append(build_param('dc.date', dc_date, date_format=True))
    if dc_Lib :
        params.append(build_param('dc.source', dc_Lib))
    if dc_format :
        params.append(build_param('dc.format', dc_format))
    if dc_geo :
        params.append(build_param('dc.coverage', dc_geo))
    if dc_langue :
        params.append(build_param('dc.language', dc_langue))
        
    for field, search_term in kwargs.items():
        if search_term == '' or search_term == None:
            break
        field = field.replace('_', '.')
        params.append(build_param(field, search_term))
    join_field = "%20and%20" if and_query else "%20or%20"
    query += join_field.join(params)
    print("The query was : " + query)
    return query


def request_and_parse_search_queries(urls, processes, progress):
    """Given the url of the search query, get it and unwrap the records to get their dublin core."""
    records = []
    results, failures = request_and_parse_urls(urls, processes, progress)
    for result_parsed in results:
        try:
            records += unwrap_records(result_parsed)
        except TypeError:
            continue
    return records, failures


def unwrap_records(parsed_xml):
    """Given a parsed xml of search records, unwrap them to get parsed xml of their dublin core"""
    try:
        records = parsed_xml['srw:searchRetrieveResponse']['srw:records']['srw:record']
        if isinstance(records, dict) :
        	records = [records]
        return [record['srw:recordData']['oai_dc:dc'] for record in list(records)]
    except KeyError:
        return []
