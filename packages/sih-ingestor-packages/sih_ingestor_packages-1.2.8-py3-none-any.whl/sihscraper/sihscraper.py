#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.parse import urljoin
import os
import re
import sihtools.sihtools as sihtool
from scraper_api import ScraperAPIClient
import scrapy
import json
from unidecode import unidecode

class sihscraperbase:
    def cleanValue(self, string):
        removeManySpaces = '\s{2,}'
        removeSpecialChar = '[^A-Za-z0-9éèàêâîïäôö\-;\.,\s]'

        string = str(string)
        string  = self.removeAccent(string)
        string = re.sub(removeManySpaces, ' ', string)
        string= re.sub('\n{1,}', ' ', string)
        string = re.sub(removeSpecialChar, '', string)
        
        
        return string.strip()
    
    def removeAccent(self, string):
        if not string:
            return None
        
        return unidecode(string)
    '''
    BurkinaFaso => burkina_faso
    '''
    def string_to_camel_case(self, str): 
        res = [str[0].lower()] 
        for c in str[1:]: 
            if c in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'): 
                res.append('_') 
                res.append(c.lower()) 
            else: 
                res.append(c) 
        
        return ''.join(res) 
    
    def get_links(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        links = []
        regexJs = '.*(javascript\:void).*'
        pJs = re.compile(regexJs, re.IGNORECASE)
        regexSharp = '^(\#).*'
        pSharp = re.compile(regexSharp, re.IGNORECASE)
        regexSm = '.*(twitter|facebook|easyshares|google|bfmtv|freebsd|mozilla|vimeo).*'
        pSm = re.compile(regexSm, re.IGNORECASE)
    
        for link in soup.findAll('a', attrs={'href': re.compile("[a-zA-Z\/\-\.]+")}):
            href = link.get('href')
            if not pJs.match(href) and not pSharp.match(href) and not pSm.match(href):
                links.append(href)

        return list(set(links))
    
'''
    Scraper utilities
'''
class sihscraper(sihscraperbase):
    def get_request(self, url, headers = {}):
        
        if not 'user-agent' in headers.keys():
            headers['user-agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
            
        self.request = requests.get(url, headers=headers)

        if self.request.status_code != 200:
            return None
        
        return self.request
    
    def post_request(self, url, data = {}, headers = {}):
        
        if not 'user-agent' in headers.keys():
            headers['user-agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
            
        self.request = requests.post(url=url, data=data, headers=headers)

        if self.request.status_code != 200:
            return None
        
        return self.request
    
    '''
        Make a request and write the output in a file
    '''
    def request_to_file(self, url, filepath):
        request = self.get_request(url)
        
        if not request:
            return False
        
        content = request.content
        
        return sihtool.sihfiletools().put_content(filepath, content)
    
    def scrape(self, url):
        try:
            requete = self.get_request(url)
            if not requete:
                return None
            
            page = requete.content

            if not page:
                return None

            self.soup = BeautifulSoup(page, 'html.parser')

            return self.soup
        except requests.exceptions.ConnectionError as e:
            print('Connection refused', e)
            return None
        
    def table_to_array(self, table_content):
        soup = BeautifulSoup(table_content, 'html.parser')
        tables = soup.findChildren('table')
        
        extracted_tables = []
        
        for table in tables:
            rows = table.findChildren(['th', 'tr'])
            extracted_rows = []
            
            for row in rows:
                cells = row.findChildren('td')
                
                extracted_cells = []
                for cell in cells:
                    if cell:
                        if cell and cell.text:
                            c_value = str(cell.text)
                            c_value = self.cleanValue(c_value)
                            extracted_cells.append(c_value)
                        
                extracted_rows.append(extracted_cells)
            
            extracted_tables.append(extracted_rows)
        
        return extracted_tables
    
    def dl_to_array (self, content):
        soup = BeautifulSoup(content, 'html.parser')
        
        dls = soup.findChildren('dl')
        results = []
        sih_string = sihtool.sihstring()
        
        for dl in dls:
            dt = dl.findChildren('dt')
            dd = dl.findChildren('dd')
            len_dt = len(dt)
            len_dd = len(dd)
            
            if len_dd != len_dt:
                min_len = min([len_dd, len_dt])
            else:
                min_len = len_dd
            
            i = 0
            while i < min_len:
                info = {}
                key = dt[i].text
                key = sih_string.clean(key)
                key = sih_string.string_to_snake(key)
                value = sih_string.clean(dd[i].text)
                info[key] = value
            
                results.append(info)
                i = i+1
        
        return results
        
    def list_to_array(self, ul_content):
        soup = BeautifulSoup(ul_content, 'html.parser')
        list_elements = soup.find_all('li')
        results = []
        
        if not list_elements:
            return None
        
        for li in list_elements:
            elt = {}
            elt['text'] = li.text
            links = li.findAll('a', attrs={'href': re.compile("[a-zA-Z\/\-\.]+")})
            l_href = []
            for link in links:
                l_href.append(link.get('href'))
                
            elt['links'] = list(set(l_href))
            
            results.append(elt)
        
        return results;
        
        
''' Form scraper '''          
class sihformscraper:
    def __init__(self):
        self.session    = HTMLSession()
    def get_all_form (self, url, renderJs = False):
        """Returns all form tags found on a web page's `url` """
        # GET request
        res = self.session.get(url)
        # for javascript driven website
        # res.html.render()
        if renderJs :
            soup = BeautifulSoup(res.html.render(), "html.parser")
        else:
            soup = BeautifulSoup(res.html.html, "html.parser")
        
        return soup.find_all("form")
    
    def get_form_by_name (self, url, formName, renderJs = False):
        forms   = self.get_all_form(url, renderJs)
        formName    = formName.lower()
        if not forms:
            return None
        
        for f in forms:
            fdetails = self.get_form_details(f)
            
            if fdetails['name'] == formName:
                return fdetails
        
        return None
    
    def get_form_by_action (self, url, formAction, renderJs = False):
        forms   = self.get_all_form(url, renderJs)
        formName    = formAction.lower()
        if not forms:
            return None
        
        for f in forms:
            fdetails = self.get_form_details(f)
            
            if fdetails['action'] == formAction:
                return fdetails
        
        return None
       
    def get_form_details(self, form):
        """Returns the HTML details of a form,
        including action, method and list of form controls (inputs, etc)"""
        details = {}
        attrs   = form.attrs
        # get the form action (requested URL)
        action = attrs.get("action").lower()
        # get the form method (POST, GET, DELETE, etc)
        # if not specified, GET is the default in HTML
        method = attrs.get("method", "get").lower()
        
        name = form.attrs.get("name", 'none').lower()
        
        # get all form inputs
        inputs = []
        for input_tag in form.find_all("input"):
            # get type of input form control
            input_type = input_tag.attrs.get("type", "text")
            # get name attribute
            input_name = input_tag.attrs.get("name")
            # get the default value of that input tag
            input_value =input_tag.attrs.get("value", "")
            # add everything to that list
            inputs.append({"type": input_type, "name": input_name, "value": input_value})
        # put everything to the resulting dictionary
        details["action"]   = action
        details["method"]   = method
        details['name']     = name
        details["inputs"]   = inputs
        
        return details
    
    def submit_form(self, base_url, form_details, data):
        # join the url with the action (form request URL)
        url = urljoin(base_url, form_details["action"])
        
        if form_details["method"] == "post":
            res = self.session.post(url, data=data)
        elif form_details["method"] == "get":
            res = self.session.get(url, params=data)
        else:
            res = None
        
        return res
                
'''
Scrape using the scraper api
'''
class sihscraperapi:
    def __init__(self, key):
       self.client  = ScraperAPIClient(key)
    
    def get (self, url):
        return self.client.get(url = url).text
    
    def post(self, url, data):
        return self.client.post(url = url, body=data).text
    
    def sihrequest(self, url):
        return self.get(url)
    
    def get_to_file (self, url, filepath):
        text = self.get(url)
        if text :
            return sihtool.sihfiletools().put_content(filepath, text)
        return None
    
    def post_to_file (self, url, filepath, data):
        text = self.post(url, data)
        if text :
            return sihtool.sihfiletools().put_content(filepath, text)
        
        return None

class sihscrapingbot:
    def __init__(self, username, key, apiurl= 'http://api.scraping-bot.io/scrape/raw-html'):
        self.api_url = apiurl
        self.username = username
        self.key    = key
    def sihrequest(self, url, useChrome = False, premiumProxy = False):
        options = {
            "useChrome": useChrome, #set to True if you want to use headless chrome for javascript rendering
            "premiumProxy": premiumProxy # set to True if you want to use premium proxies Unblock Amazon,Google,Rakuten
        }
        
        payload = json.dumps({"url":url, "options":options})
        
        headers = {
            'Content-Type': "application/json"
        }

        response = requests.request("POST", self.api_url, data=payload, auth=(self.username, self.key), headers=headers)
        
        return response
    
    def sihrequest_to_file(self, url, filepath, useChrome = False, premiumProxy = False):
        response = self.sihrequest(url)
        
        if not response:
            return False
        
        return sihtool.sihfiletools().put_content(filepath, response.text)

class sihscrapertask(sihscraper):
    def __init__(self, api_key, api_url = 'http://api.scrapestack.com/scrape'):
        self.api_key = api_key
        self.api_url = api_url
    
    def get_request(self, url, headers = {}):
        headers['access_key'] = self.api_key
        headers['url'] = url
    
        hkeys = headers.keys()
        if not 'render_js' in hkeys:
            headers['render_js'] = 1
        
        if not 'proxy_location' in hkeys:
            headers['proxy_location']   = 'fr'
        
        result = requests.get(self.api_url, params=headers)
        
        return result
    
    def scrape(self, url):
        self.soup = None
        
        try:
            requete = self.get_request(url)
            if not requete or requete.status_code != 200:
                raise ValueError('The request returns a '+str(requete.status_code)+" status code")
            
            page = requete.content
        
            if not page:
                return None
            
            soup = BeautifulSoup(page, 'html.parser')
            
            if re.match('\{\"error.+', str(soup)):
                json_obj = json.loads(str(soup))
                
                error = json_obj['error']
                status = int(error['status'])
                
                if status == 104:
                    raise ValueError('Scraperdesk api error: User has reached his limit')
                
                return None
            
            self.soup = soup

            return self.soup
        
        except requests.exceptions.ConnectionError as e:
            print('Connection refused', e)
            return None

class sihserpstack(sihscraper):
    def __init__(self, api_key,url='https://api.serpstack.com/search'):
        self.api_key = api_key
        self.url = url
    def scrape_tojson(self, query, params = {}):
        params['access_key'] = self.api_key
        params['query'] = query
        pkeys = params.keys()
        if not 'gl' in pkeys:
            params['gl'] = 'fr'
        
        if not 'hl' in pkeys:
            params['hl'] = 'fr'
        
        api_result = requests.get(self.url, params)

        api_response = api_result.json()
        
        if not isinstance(api_response, dict):
            raise Exception("The API return null")
        
        return api_response
        
'''
Base class
'''
class sihextractbase (sihscraperbase):
    def __init__ (self, filename):
        if os.path.exists(filename) == False:
           print('Please submit an existing file')
           raise
        self.filename = filename
    def getSoup(self):
        try:
            with open(self.filename, "r") as f:
                html = f.read()
        except:
            print("The file", self.filename, "was not found")
            return None

        soup = BeautifulSoup(html, 'html.parser')

        if soup == None:
            print("The file was found but no content inside")
            return None

        return soup
'''
Extract data from BK
'''
class sihextractbk(sihextractbase):

    def extractItems(self):
        soup = self.getSoup()
        
        hotelList = soup.find(id='search_results_table')
       
        if hotelList == None:
            
            return None

        hotelList = str(hotelList)
        hotelListSoup = BeautifulSoup(hotelList, 'html.parser')

        srItemDivs = soup.find_all('div', {'class': 'sr_item'})

        nbreHotels = len(srItemDivs)
        
        if nbreHotels == 0:
            print("There are no child divs found in the content")
            return None
        
        regexJs = '.*(javascript\:void).*'
        pJs = re.compile(regexJs, re.IGNORECASE)

        results = {}

        for item in srItemDivs:
           
            if item.has_attr('data-hotelid')==False:
                continue

            newHotel = {}

            attrs = item.attrs

            if attrs == None or 'data-hotelid' not in attrs or 'data-class' not in attrs or 'data-score' not in attrs:
                continue

            hotel_id = str(attrs['data-hotelid'])

            if hotel_id == None:
                continue

            hotel_class = int(attrs['data-class'])
            scoreStr = str(attrs['data-score'])

            if scoreStr=='':
                scoreFloat =0
            else:
                scoreStr = scoreStr.replace(',', '.')
                scoreFloat = float(scoreStr)

            hotel_score = scoreFloat

            newHotel['hotel_id'] = hotel_id
            newHotel['hotel_class'] = hotel_class
            newHotel['hotel_score'] = hotel_score     

            hotelLinks = item.find_all('a')
            links = {}
            
            # Links
            if hotelLinks != None and len(hotelLinks)>0:
                for l in hotelLinks:
                    l_attrs = l.attrs
                    l_attrs_keys = list(l_attrs)
                    
                    if not l_attrs_keys or 'class' not in l_attrs_keys or 'href' not in l_attrs_keys:
                        
                        continue
                    
                    l_class = l_attrs['class']
                    key = '_'.join(l_class)
                                  
                    if pJs.match(l_attrs['href']) == None:
                        links[key] = l_attrs['href']

                        if key == 'bui-link' and 'data-coords' in l_attrs and 'hotel_coords' not in newHotel:
                            coords = l_attrs['data-coords']
                            newHotel['hotel_coords'] = coords

                            if coords != '':
                                splitCoords = coords.split(',')
                                newHotel['coordinates'] = {'lat': float(splitCoords[1]), 'lng': float(splitCoords[0])}

            newHotel['links'] = links

            tables = item.find_all('table', {'class': 'sr_item_legacy'})

            if len(tables) > 0:

                table = tables[0]

                #Hotel description
                descs = table.find_all('div', {'class':'hotel_desc'})

                if len(descs) >0 and 'hotel_description' not in newHotel:
                    desc0 = descs[0]
                    sdesc= BeautifulSoup(str(desc0), 'html.parser').text

                    newHotel['hotel_description'] = self.cleanConent(sdesc)

                #Hotel name
                hnames = table.find_all('span', {'class': 'sr-hotel__name'})

                if len(hnames) >0:
                    hname = hnames[0]

                    name = BeautifulSoup(str(hname), 'html.parser').text

                    newHotel['hotel_name'] = self.cleanConent(name)

                # Hotel categorie

                htypes = [] #table.find_all('div')

                if len(htypes) >0:
                    htype = htypes[0]

                    typeh = BeautifulSoup(str(htype), 'html.parser').text

                    newHotel['hotel_type'] = self.cleanConent(typeh)

                scoreBadges = item.find_all('div', {'class': 'bui-review-score__badge'})

                if len(scoreBadges) >0:
                    divsbadge = scoreBadges[0]

                    sbadge = BeautifulSoup(str(divsbadge), 'html.parser').text
                    '''sbadge = str(sbadge)
                    sbadge = re.sub(removeManySpaces, '', sbadge)
                    sbadge = re.sub('\n', '', sbadge)
                    sbadge = re.sub(removeSpecialChar, '', sbadge)
                    sbadge = sbadge.replace(',','.')'''
                    sbadge = self.cleanConent(sbadge)
                    sbadge = sbadge.replace(',','.')
                    score = 0

                    if sbadge != '':
                        score = float(sbadge)
                    newHotel['hotel_score_badge'] = score

                # Review title
                scoreTitles = item.find_all('div', {'class': 'bui-review-score__title'})

                if len(scoreTitles) >0:
                    title = scoreTitles[0]

                    title = BeautifulSoup(str(title), 'html.parser').text

                    newHotel['hotel_score_title'] = self.cleanConent(title)


                scoreTexts = item.find_all('div', {'class': 'bui-review-score__text'})

                if len(scoreTexts) >0:
                    text = scoreTexts[0]

                    text = BeautifulSoup(str(text), 'html.parser').text
                    text = self.cleanConent(text)

                    newHotel['hotel_score_text'] = text

            results[hotel_id]   = newHotel
            

        return results

    def cleanConent (self, value):
        removeManySpaces = '\s{2,}'
        removeSpecialChar = '[^A-Za-z0-9éèàêâîïäôö\-;\.,\s]'

        value = str(value)
        value = re.sub(removeManySpaces, ' ', value)
        value = re.sub('\n', '', value)
        value = re.sub(removeSpecialChar, '', value)
        value = value.strip()

        return value

    def extractHeader(self):
        soup = self.getSoup()

        if soup == None:
            return None

        body = soup.find('body')

        if body == None:
            return None

        bodySoup = BeautifulSoup(str(body), 'html.parser')

        scripts = bodySoup.find_all('script')

        script0= scripts[0]

        script = str(BeautifulSoup(str(script0), 'html.parser').text)

        script = script.replace('window.utag_data =','')
        script = script.strip()
        parts = script.split('};')

        confPart = parts[0]+'}'
        confPart = re.sub('(\'\')', '', confPart)

        cityName = re.search('(city_name\:).+\,', confPart)

        header = {}

        if cityName:
            value = cityName.group(0)
            value = self.cleanHeaderValue('city_name',value)

            header['city_name'] = value

        hotelList = re.search('hotels_id_list\:.+\,', confPart)

        if hotelList:
            value = hotelList.group(0)
            values = self.cleanHeaderValueAndExplode('hotels_id_list:', value)

            header['hotels_id_list'] = values
        destName = re.search('dest_name\:.+\,', confPart)

        if destName:
            value = destName.group(0)
            values = self.cleanHeaderValueAndExplode('dest_name:', value)

            header['dest_name'] = values

        return header

    def cleanHeaderValue(self, tagname, value):
        value = value.replace(tagname+':','')
        value = value.replace('\'','')
        value = value.replace(',','')
        value = value.strip()

        return value
    def cleanHeaderValueAndExplode(self, tagname, value):
        value = value.replace(tagname,'')
        value = value.strip()
        value = value.replace('\'','')
        value = value.strip()
        values = value.split(',')

        return list(filter(None,values))

'''
Extract from exp
'''
class sihextractexp(sihextractbase) :

    def extractItems(self):
        soup = self.getSoup()

        listings = soup.find_all('div', {'class': 'imagelayout-left-fullbleed'})

        if len(listings) <= 0:
            return None

        for item in listings:
            item = str(item)
            newHotel= {}

            soupItem = BeautifulSoup(item, 'html.parser')

            titles = soupItem.find_all('h3')

            for title in titles:
                if title.has_attr('data-stid'):
                    attrs = title.attrs
                    stid = str(attrs['data-stid'])

                    if stid == 'content-hotel-title':
                        newHotel['hotel_name'] = self.cleanValue(title.text)
                        break

            return newHotel