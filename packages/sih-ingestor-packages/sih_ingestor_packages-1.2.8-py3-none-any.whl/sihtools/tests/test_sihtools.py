#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 16:27:20 2020

@author: yefangon
"""

from unittest import TestCase
from sihtools import sihtools
import os

class TestSihfiletools(TestCase):
    def test_scandir(self):
        obj = sihtools.sihfiletools()

        self.assertTrue(len(obj.scandir('/home/data')) > 0)
    def test_getchunksize(self):
        obj = sihtools.sihfiletools()

        self.assertIsNotNone(obj.getChunksize())
        
    def test_extrat_ext_from_url(self):
        obj = sihtools.sihfiletools()

        self.assertEqual(obj.extrat_ext_from_url('https://static.data.gouv.fr/resources/donnees-des-urgences-hospitalieres-et-de-sos-medecins-relatives-a-lepidemie-de-covid-19/20200427-190017/sursaud-covid19-quotidien-2020-04-27-19h00-departement.csv'), '.csv')
    def test_download_unzip(self):
        obj = sihtools.sihfiletools()

        self.assertTrue(len(obj.download_unzip('https://static.data.gouv.fr/resources/donnees-relatives-a-lepidemie-du-covid-19/20200320-181924/code-tranches-dage.csv', '/home/data/test/'))>0)
    def test_download_decompress(self):
        obj = sihtools.sihfiletools()
        url = 'https://echanges.dila.gouv.fr/OPENDATA/BODACC/FluxHistorique/2019/RCS-A_BXA20190006.taz'
        
        self.assertTrue(obj.download_decompress(url, '/tmp', True))
    def test_read_csv2(self):
        obj = sihtools.sihfiletools()
        filename = '/home/data/inpi/IMR/test_tc/rep/0101_S1_20170504_5_rep.csv'
        rows = obj.read_csv2(filename,0,5)
        
        self.assertTrue(isinstance(rows, list) and len(rows)==5)
        
    def test_get_avg_row_size(self):
        obj = sihtools.sihfiletools()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        result = obj.get_avg_row_size(os.path.join(dir_path,'wc_test.txt'))
        
        self.assertTrue(result != None and result==33)
    
    def test_get_memory_max_rows(self):
        obj = sihtools.sihfiletools()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        result = obj.get_memory_max_rows(os.path.join(dir_path,'wc_test.txt'))
        print(result)
        self.assertTrue(result != None and result > 0)
        
class TestSihXml(TestCase):
    def test_init(self):
        f = '/tmp/RCS-A_BXA20190006/RCS-A_BXA20190006.xml'
        xml = sihtools.sihxml(f)
        
        data = xml.recursive_extract(xml.data)
        
        self.assertIsNotNone(data)
        
class TestSihString(TestCase):
    def test_string_to_camel_case(self):
        string = 'BurkinaFaso'
        obj = sihtools.sihstring()
        
        self.assertEqual(obj.string_to_camel_case(string), 'burkina_faso')
        
    def test_string_to_snake(self):
        string = 'Raison sociale'
        obj = sihtools.sihstring()
        
        self.assertEqual(obj.string_to_snake(string), 'raison_sociale')
    def test_format_keys(self):
        dict1 = {'keyOne': 'val1', 'key two': 'val2'}
        obj = sihtools.sihstring()
        dict2 = obj.format_keys(dict1)
        
        self.assertTrue('key_one' in dict2.keys() and 'key_two' in dict2.keys())
        
class TestSihXml(TestCase):
    def test_process_data_inpi(self):
        obj = sihtools.sihxml('/home/data/inpi/testCa/PUB_CA_300527082_6901_1974B00176_2018_B2018046112/PUB_CA_300527082_6901_1974B00176_2018_B2018046112.donnees.xml')
        
        data = obj.process_data_inpi(obj.data['ns0:bilans'])
        
        print(data)
        
        self.assertTrue(isinstance(data, dict))
        
class TestSihFtp(TestCase):
    def test_connect(self):
        sihftp = sihtools.sihftp()
        #"ftp1.at.proftpd.org"
        conn = sihftp.connect('opendata-rncs.inpi.fr','sih','Ouaga0201', 'ftp_tls')
        #conn = sihftp.connect('ftp1.at.proftpd.org','anonymous','', 'ftp')
        
        self.assertIsNotNone(conn)