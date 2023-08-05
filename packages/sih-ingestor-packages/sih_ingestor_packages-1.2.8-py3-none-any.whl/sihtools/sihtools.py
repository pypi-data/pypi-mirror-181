#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 09:40:14 2020

@author: yefangon
"""

import os
import sys
import time
import urllib.parse as urlparse
import yaml
import psutil
import urllib.request
import zipfile
from fuzzywuzzy import fuzz
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from six import string_types
import ntpath
import xml.etree.ElementTree as ET
import xmltodict
import csv,string,random
import re
from unidecode import unidecode
import stringcase
import shutil
import tarfile
from ftplib import FTP
from ftplib import FTP_TLS
from ftplib import all_errors
from ftplib import error_perm
import subprocess

class sihfiletools:
    """[summary]
    Set of helpers
    """
    def scandir(self, root_directory, pattern = '.*(.zip)$'):
        print('scan directory (absolute) = ' + os.path.abspath(root_directory))
        fnames = []
        for root, subdirs, files in os.walk(root_directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                if pattern:
                    if re.match(pattern, file_path):
                        fnames.append(file_path)
                    else: 
                        continue
                else:
                    fnames.append(file_path)

        return fnames

    def fileExists(self, filename):
        """[summary]

        Args:
            filename (str): [the file name or path]

        Returns:
            [bool]: [description]
        """
        return os.path.exists(filename)
    
    
    def mkdir(self, dirname):
        if not self.fileExists(dirname):
            os.mkdir(dirname)

        return self.fileExists(dirname)

    def move (self, source, destination):

        if not self.fileExists(source) or not os.path.isfile(source):
            print('The source is not valid: ', source)

            return None
        if os.path.isdir(destination):
            basename = os.path.basename(source)
            destination = os.path.join(destination, basename)

        os.rename(source, destination)

        return self.fileExists(destination)
    """
    Copy file
    """
    def copy (self, source, destination):

        if not self.fileExists(source) or not os.path.isfile(source):
            print('The source is not valid: ', source)

            return None
        
        shutil.copy2(source, destination)

        return self.fileExists(destination)
    
    def scp(self,source, destination, option="-r"):
        """[summary]

        Args:
            source (str): [description]
            destination (str): [description]
            option (str, optional): [description] .Defaults to -r

        Returns:
            [bool]: [description]
        """
        try:
            completed = subprocess.run(["scp",option,source,destination])
        except subprocess.CalledProcessError as exc:
            print(exc.message)
        
        if completed.returncode == 0:
            return True
        
        return False
    def remove(self, filename):
        if self.fileExists(filename):
            if os.path.isdir(filename):
                os.removedirs(filename)

            if os.path.isfile(filename):
                os.remove(filename)

        return self.fileExists(filename) == False
    
    """
    Remove a directory including the content
    """
    def rmdirectory(self, directopry):
        try:
            shutil.rmtree(directopry)
            return True
        except OSError as e:
            print("Error: %s : %s" % (directopry, e.strerror))
            
            return None
        
    def resetdir(self, directory):
        if self.fileExists(directory):
            self.rmdirectory(directory)
            
        return self.mkdir(directory)
    
    def extract_file_parts(self, filepath):
        return os.path.splitext(filepath)
    
    def extrat_ext_from_url (self, url):
        path = urlparse.urlparse(url).path
        ext = os.path.splitext(path)[1]

        return ext
    
    def extract_path_info_from_url(self, url):
        path_parts = urlparse.urlparse(url).path
        split_path = os.path.splitext(path_parts)
        
        pathname = str(split_path[0])
        ext = str(split_path[1])
        
        pathname_split = pathname.split('/')
        
        filename = pathname_split[len(pathname_split)-1]
        
        return filename, ext
        
    def extract_ext_from_path (self, path):
        filename, ext = self.extract_file_parts(path)
        
        return ext
    
    def extract_filename(self, filepath):
        filename, ext = self.extract_file_parts(filepath)
        
        return filename
    '''
        Put the content a file. If the file exists, deletes it before
    '''
    def put_content(self, filepath, content):
        if self.fileExists(filepath):
            self.remove(filepath)
            
        file_object = open(filepath, 'w')
        file_object.write(content)
        file_object.close()
        
        return self.fileExists(filepath)
    '''
        Get the content of a file
    '''
    def get_content(self, filepath):
        if not self.fileExists(filepath):
            return None
        
        file_object = open(filepath, 'r')
        
        content = file_object.read()
        file_object.close()
        
        return content
    
    def get_full_pathname(self, basedir, suffix):
        return os.path.join(basedir, suffix)
    
    def download(self, url, filename):

        if os.path.isdir(filename):
            fname,ext = self.extract_path_info_from_url(url)
            
            filename = os.path.join(filename, fname+ext)

        print("Download from ", url, "to ", filename,' ....')

        return urllib.request.urlretrieve(url, filename)
    """
    Agnostic: zip, tar, taz
    """
    def download_decompress(self, url, destination ='/tmp', delete = True):
        pathname, header = self.download(url, destination)
        
        ext = str(self.extrat_ext_from_url(url))
        ext = ext.replace('.', '')
        
        if not pathname or not header:
            return False
        
        method = 'un'+ext
        
        try:
            un = getattr(self, method)(pathname, destination, delete)
            
            return un
        except :
            return False
        
    """
    .zip
    """
    def unzip(self, zipname, destination = '/tmp/', delete = True):
        try:
            zip_ref = zipfile.ZipFile(zipname, 'r')
            zip_ref.extractall(destination)
            zip_ref.close()

            if delete == True:
                os.remove(zipname)

            return True
        except:
            print("The unzip of the file ",zipname, " has failed. STOP!")
            return False
    """
    .taz
    """
    def untaz(self, tarname, destination = '/tmp/', delete=True):
        return self.untar(tarname, destination, delete)
    
    """
    .tar
    """
    def untar(self, tarname, destination = '/tmp/', delete=True):
        try:
            tar_obj = tarfile.open(tarname)
            tar_obj.extractall(destination)
            tar_obj.close()
            
            if delete == True:
                os.remove(tarname)
            
            return True
        except tarfile.TarError as err:
            print("The tar/taz of the file has failed: {0}".format(err))
            return False
        
    def download_unzip(self, url, destination = '/tmp/', reset = False):

        self.mkdir(destination)

        files = self.scandir(destination)

        if reset == True:
            if len(files) > 0:
                for f in files:
                    self.remove(f)
                files = []
        else:
            if len(files) > 0:

                return files

        zipname, header = self.download(url, destination)

        if not self.fileExists(zipname):
            print('The file ', zipname,' was not found!')

            return None

        if zipname.endswith('zip'):
            self.unzip(zipname, destination)
        else:
            self.move(zipname, destination)

        return self.scandir(destination)

    '''
        Get the chunk size according to the amount of free memory
        dockSize in bytes
    '''
    def getChunksize(self, docSize=2000):

        ram = dict(psutil.virtual_memory()._asdict())

        freeRam = ram['available']
        chunkSize= round(float(freeRam)/docSize)

        return chunkSize
    
    def to_csv(self,filename, data, write_mode='a', writeHearder = True, delimiter=','):
        
        if not isinstance(data, list) or len(data) <= 0:
                return None
        hearder = data[0].keys()
        
        try:
            with open(filename, mode=write_mode, newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=hearder, delimiter=delimiter)
                if writeHearder == True:
                    writer.writeheader()
                
                for row in data:
                    r2 = {k: str(v) for k, v in row.items()}
                    writer.writerow(r2)
        except IOError:
            print('An error occured')
            return None

        return len(data)
    
    def read_csv(self, filename, start=0, limit=100, delimiter=";", quotechar='"'):
        """[summary]

        Args:
            filename ([type]): [description]
            start (int, optional): [description]. Defaults to 0.
            limit (int, optional): [description]. Defaults to 100.
            delimiter (str, optional): [description]. Defaults to ";".
            quotechar (str, optional): [description]. Defaults to '"'.
        """
        
        if not self.fileExists(filename):
            return None
        rows = []
        with open(filename, newline='') as csvfile:
            reader = list(csv.DictReader(csvfile, delimiter=delimiter, quotechar=quotechar))
            idx = start
            idx_end = start+limit
        
            while True:
                
                if idx >= idx_end:
                    break
                
                try:
                    row = reader[idx]
                except:
                    break
                new_row = dict(row)
                new_row = sihstring().format_keys(new_row)
                rows.append(new_row)
                idx = idx+1
    
        return rows
    
    """
    Read CSV and returns a list
    """
    def read_csv2(self, filename,start=0, limit=100, delimiter=';',quotechar='"'):
        """[summary]

        Args:
            filename ([type]): [description]
            start (int, optional): [description]. Defaults to 0.
            limit (int, optional): [description]. Defaults to 100.
            delimiter (str, optional): [description]. Defaults to ';'.
            quotechar (str, optional): [description]. Defaults to '"'.

        Returns:
            [type]: [description]
        """
        if not self.fileExists(filename):
            return None
        content = str(self.get_content(filename))
        
        if not content:
            return None
        
        lines = re.split("\n", content)
        total_lines = len(lines)
        
        if total_lines <= start:
            return None
        
        header = str(lines[0]).split(delimiter)
        
        header = [sihstring().string_to_snake(sihstring().clean(v)) for v in header]
        
        h_len = len(header)
        
        start = start + 1
        rows = []
        for i in range(start, limit+1):
            if i >= total_lines:
                break
            
            line = str(lines[i]).replace(quotechar, '')
            values = line.split(delimiter)
            row = {}
            
            for h in range(0, h_len):
                try:
                    v = values[h]
                except :
                    v = ''
                    
                column = header[h]
                v = str(v)
                
                if column in row.keys():
                    column = column+'_2'
                    
                row[column] = v
            rows.append(row)

        return rows
    def count_rows(self, file_path):
        """[Counts the number of rows in a file]

        Args:
            file_path ([str]): [The file path]

        Returns:
            [int]: [The number of rows]
        """
        if not self.fileExists(file_path):
            return None
        
        file_wc = os.path.join('/tmp', 'wc_'+sihutilities().random_lower_string(5)+'.txt')
        wc_cmd = "wc -l %s > %s"%(file_path, file_wc)
        
        os.system(wc_cmd)
        
        if not self.fileExists(file_wc):
            return None
        
        wc_conten = self.get_content(file_wc)
        wc_lines = re.split("\n", wc_conten)
        self.remove(file_wc)
        
        if len(wc_lines) <= 0:
            return None
        
        wc_first_line = wc_lines[0].split(' ')
        wc_val = wc_first_line[0]
        wc_val = int(re.sub(r"[^0-9]", '', wc_val))
        
        return wc_val
    
    def file_size(self, file_path):
        """[Returns the file size in Bytes]

        Args:
            file_path ([str]): [The file path]

        Returns:
            [int]: [The file size in bytes]
        """
        file_size = os.path.join('/tmp', 'size_'+sihutilities().random_lower_string(5)+'.txt')
        
        sz_cmd = 'stat --format="%s" '+file_path+' > '+file_size

        os.system(sz_cmd)
        
        if not self.fileExists(file_size):
            return None
        
        sz_content = self.get_content(file_size)
        sz_lines = re.split("\n", sz_content)
        sz_val = int(re.sub(r"[^0-9]",'',sz_lines[0]))
        
        self.remove(file_size)
        
        return sz_val
    
    def get_avg_row_size(self, file_path):
        """[Returns the average size of a file in Bytes]

        Args:
            file_path ([str]): [The file path]

        Returns:
            [int]: [The average size of a row]
        """
        
        wc_val = self.count_rows(file_path)
        sz_val = self.file_size(file_path)
        
        if not wc_val or wc_val==0 or sz_val == 0:
            return 0
        
        avg = sz_val/wc_val
        
        return round(avg)
        
    def get_memory_max_rows(self, file_path):
        """[Get the max chunck size for a given file path]

        Args:
            file_path ([str]): [the file path]

        Returns:
            [int]: [The chunk size]
        """
        avg_row = self.get_avg_row_size(file_path)
        
        if not avg_row:
            return None
        
        return self.getChunksize(avg_row)
    
class sihparameters:
    def __init__(self, parametersFile):

        if os.path.exists(parametersFile) == False:
            print('Please set the parameters.yaml file')
            raise

        self.parameters = None

        with open(parametersFile, 'r') as f:
            self.parameters = yaml.load(f, Loader=yaml.FullLoader)

    def get(self, id, default=None):

        if id in self.parameters:
            return self.parameters[id]

        return default

class sihnlptilities:

    def getTokens(self, inputString):
        #Remove accents
    # inputString = unidecode.unidecode(inputString)

        inputString = inputString.lower()

        #Tokenize
        tokens = word_tokenize(inputString)

        #Remove stop words
        stopWordsFr = set(stopwords.words('french'))
        words = [word for word in tokens if not word in stopWordsFr]

        return words

    def clean_text(self, text):
        text = text.lower()

        '''rg1 = '(\sau|du\s|\s(de la)|\s(de l\')|(d\')|de\s|des\s|\s(a la)|\s(a l\')|(\sle\s)|(\sles\s)|(l\')|\sl\s|sarl\s|sas\s|sa\s|societe\s|hotel\s|domaine\s|\shotel|chateau\s|\schateau|\sauberge|auberge\s|\scamping|camping\s|\s?residence(s)?\s?)'

        text = re.sub(rg1, '', text)
        text = re.sub('[^0-9a-z]', '', text)'''

        return text

    #Returns a number between 0 and 100
    def getSimpleRatios(self, string1, string2):
        if string1 == '' or string2 == '':
            return 0

        string1 = self.clean_text(string1)
        string2 = self.clean_text(string2)

        return fuzz.ratio(string1, string2)

    def getPartialRatio(self, string1, string2):
        string1 = self.clean_text(string1)
        string2 = self.clean_text(string2)

        return fuzz.partial_ratio(string1, string2)

    def getTokenSortRatio(self, string1, string2):
        string1 = self.clean_text(string1)
        string2 = self.clean_text(string2)

        return fuzz.token_sort_ratio(string1, string2)

    def getTokenSetRatio(self, string1, string2):
        string1 = self.clean_text(string1)
        string2 = self.clean_text(string2)

        return fuzz.token_set_ratio(string1, string2)

class sihstring:
    
    def clean(self, string):
        removeManySpaces = '\s{2,}|\''
        removeSpecialChar = '[^A-Za-z0-9éèàêâîïäôö\-;\.,\s]'

        string = str(string)
        string  = self.remove_accent(string)
        string = re.sub(removeManySpaces, ' ', string)
        string= re.sub('\n{1,}', ' ', string)
        string = re.sub(removeSpecialChar, '', string)
                
        return string.strip()
    
    def remove_accent(self, string):
        if not string:
            return None
        
        return unidecode(string)
    
    def format_keys(self, dict_obj):
        if not isinstance(dict_obj, dict):
            return dict_obj
        
        return {self.string_to_snake(self.clean(key)): val  for key, val in dict_obj.items()}
    '''
    burkina_faso => BurkinaFaso 
    '''
    def string_to_camel_case(self, str): 
        
        return stringcase.camelcase(str) 
    
    """
    raison sociale => raison_sociale
    """
    def string_to_snake(self, text):
        
        return stringcase.snakecase(text)
    
    
class sihutilities:
    #### Fonctions générics #####
    def random_lower_string(self, length=10):
        letters = string.ascii_lowercase
        
        return ''.join(random.choice(letters) for i in range(length))
    
    def random_lower_string(self, length=10):
        letters = string.ascii_uppercase
        
        return ''.join(random.choice(letters) for i in range(length))
    
    def random_letters_string(self, length=10):
        letters = string.ascii_letters
        
        return ''.join(random.choice(letters) for i in range(length))
    
    def castToStr(self, dic={}):
        if isinstance(dic, dict) == True:
            for key in dic:
                val = str(dic[key])

                if val == 'nan':
                    val = ''


                dic[key] = val

        return dic

    """
    Convert Effectif to interger
    """
    def processEffectif (self, tranche):
        switcher = {
                '01': [1,2],
                '02': [3,5],
                '03': [6,9],
                '11': [10,19],
                '12': [20,49],
                '21': [50,99],
                '22': [100,199],
                '31': [200,249],
                '32': [250,499],
                '41': [500,999],
                '42': [1000,1999],
                '51': [2000,4999],
                '52': [5000, 9999],
                '53': [10000,20000]
            }
        if tranche in switcher:
            return switcher[tranche]
        else:
            return [0,0]


    def processDenomination(self, row):
        denomination = list()
        rkeys = row.keys()
        if 'denominationUsuelleEtablissement' in rkeys:
            val = row['denominationUsuelleEtablissement']
            if val != None and val != '':
                denomination.append(str(val))

        if 'enseigne1Etablissement' in rkeys:
            val = row['enseigne1Etablissement']
            if val != None and val != '':
                denomination.append(str(val))

        if 'enseigne2Etablissement' in rkeys:
            val = row['enseigne2Etablissement']
            if val != None and val != '':
                denomination.append(str(val))
        if 'enseigne3Etablissement' in rkeys:
            val = row['enseigne3Etablissement']
            if val and val != '':
                denomination.append(str(val))

        if len(denomination) <= 0:
            return ''
        
        if len(denomination) > 1:
            return '|'.join(denomination)

        return denomination[0]
    
    def processDenominationUniteLegale(self, row):
        denomination = list()

        rkeys = row.keys()
        
        if 'denominationUniteLegale' in rkeys :
            val = row['denominationUniteLegale']
            if val and val != '':
                denomination.append(str(val))

        if 'denominationUsuelle1UniteLegale' in rkeys:
            val = row['denominationUsuelle1UniteLegale']
            if val != None and val != '':
                denomination.append(str(val))

        if 'denominationUsuelle2UniteLegale' in rkeys:
            val = row['denominationUsuelle2UniteLegale']
            if val != None and val != '':
                denomination.append(str(val))
        if 'denominationUsuelle3UniteLegale' in rkeys:
            val = row['denominationUsuelle3UniteLegale']
            if val and val != '':
                denomination.append(str(val))
                
        if 'nomUniteLegale' in rkeys:
            val = row['nomUniteLegale']
            if val and val != '':
                denomination.append(str(val))
                
        if 'nomUsageUniteLegale' in row:
            val = row['nomUsageUniteLegale']
            if val and val != '':
                denomination.append(str(val))
                
        if 'nomUsageUniteLegale' in rkeys:
            val = row['nomUsageUniteLegale']
            if val and val != '':
                denomination.append(str(val))
                
        if 'prenom1UniteLegale' in rkeys:
            val = row['prenom1UniteLegale']
            if val and val != '':
                denomination.append(str(val))
                
        if 'prenom1UniteLegale' in rkeys:
            val = row['prenom1UniteLegale']
            if val and val != '':
                denomination.append(str(val))
                
        if 'prenom2UniteLegale' in rkeys:
            val = row['prenom2UniteLegale']
            if val and val != '':
                denomination.append(str(val))
                
        if 'prenom3UniteLegale' in rkeys:
            val = row['prenom3UniteLegale']
            if val and val != '':
                denomination.append(str(val))
                
        if 'prenom4UniteLegale' in rkeys:
            val = row['prenom4UniteLegale']
            if val and val != '':
                denomination.append(str(val))
                
        if 'prenomUsuelUniteLegale' in rkeys:
            val = row['prenomUsuelUniteLegale']
            if val and val != '':
                denomination.append(str(val))
                
        if 'pseudonymeUniteLegale' in rkeys:
            val = row['pseudonymeUniteLegale']
            if val and val != '':
                denomination.append(str(val))
        
        if len(denomination) <= 0:
            return ''
        if len(denomination) > 1:
            return '|'.join(denomination)

        return denomination[0]
    
    def decodeTypeDeVoie(self, typeVoie):
         mapping = {
                "ALL" :"Allée",
                "AV" :"Avenue",
                "BD" :"Boulevard",
                "CAR" :"Carrefour",
                "CHE" :"Chemin",
                "CHS" :"Chaussée",
                "CITE" :"Cité",
                "COR" :"Corniche",
                "CRS" :"Cours",
                "DOM" :"Domaine",
                "DSC" :"Descente",
                "ECA" :"Ecart",
                "ESP" :"Esplanade",
                "FG" :"Faubourg",
                "GR" :"Grande Rue",
                "HAM" :"Hameau",
                "HLE" :"Halle",
                "IMP" :"Impasse",
                "LD" :"Lieu-dit",
                "LOT" :"Lotissement",
                "MAR" :"Marché",
                "MTE" :"Montée",
                "PAS" :"Passage",
                "PL" :"Place",
                "PLN" :"Plaine",
                "PLT" :"Plateau",
                "PRO" :"Promenade",
                "PRV" :"Parvis",
                "QUA" :"Quartier",
                "QUAI" :"Quai",
                "RES" :"Résidence",
                "RLE" :"Ruelle",
                "ROC" :"Rocade",
                "RPT" :"Rond-point",
                "RTE" :"Route",
                "RUE" :"Rue",
                "SEN" :"Sentier",
                "SQ" :"Square",
                "TPL" :"Terre-plein",
                "TRA" :"Traverse",
                "VLA" :"Villa",
                "VLGE" :"Village"
            }

         if typeVoie in mapping:
             return mapping[typeVoie]

         return None

    def processTypeDeVoie(self, typeVoie):
        decode = self.decodeTypeDeVoie(typeVoie)

        return decode

    """
    Formattage de l'adresse
    """
    def processAddress(self, row):
        address = list()
        finalParts = list()
        rkeys = row.keys()
        if 'numeroVoieEtablissement' in rkeys:
            val = row['numeroVoieEtablissement']

            if val != None and val != '':
                address.append(str(val))

        if 'typeVoieEtablissement' in rkeys:
            val = row['typeVoieEtablissement']
            if val != None and val != '':
                address.append(self.processTypeDeVoie(val))

        if 'libelleVoieEtablissement' in rkeys:
            val = row['libelleVoieEtablissement']
            if val != None and val != '':
                address.append(str(val))
        
        if 'codePostalEtablissement' in rkeys:
            val = row['codePostalEtablissement']
            if val != None and val != '':
                address.append(str(val))
        
        if 'libelleCommuneEtablissement' in rkeys:
            val = row['libelleCommuneEtablissement']
            if val != None and val != '':
                address.append(str(val))
        
        p1 = ''
        address = [str(i) for i in address if i]

        if len(address) > 0:
            p1 = ' '.join(address)
         
        if p1 != '':
            finalParts.append(p1.strip())
            
        if 'complementAdresseEtablissement' in rkeys:
            val = row['complementAdresseEtablissement']

            if val != None and val != '':
                part1 = p1+' '+str(val)
                finalParts.append(part1.strip())
                                
        address2 = list()

        if 'numeroVoie2Etablissement' in rkeys:
            val = row['numeroVoie2Etablissement']

            if val != None and val != '':
                address2.append(str(val))

        if 'typeVoie2Etablissement' in rkeys:
            val = row['typeVoie2Etablissement']
            if val != None and val != '':
                address2.append(self.processTypeDeVoie(val))
        
        if 'libelleVoie2Etablissement' in rkeys:
            val = row['libelleVoie2Etablissement']
            if val != None and val != '':
                address2.append(val)


        p2 = ''
        nbreAdr2 = len(address2)

        if nbreAdr2>0:
            address2 = [str(i) for i in address2 if i]
            p2 = ' '.join(address2)
            
        if p2 != '':
            finalParts.append(p2.strip())
                
       
        if 'complementAdresse2Etablissement' in rkeys:
            val = str(row['complementAdresse2Etablissement'])

            if nbreAdr2>0 and val != None and val != '':
                part2 = p2+' '+val
                finalParts.append(part2.strip())
        
        finalParts = [str(i) for i in finalParts if i]

        nbre = len(finalParts)

        if nbre<=0:
            return ''

        if nbre>1:
            return '|'.join(finalParts)

        return finalParts[0]

    def quoteStrings(self, row):
        for key in row:
            item = row[key]
            if type(item) == str:
                row[key] = self.quote_str_action(item)
        return row
    def quote_str_action(self, value):
        '''
        If `value` is a string type, escapes single quotes in the string
        and returns the string enclosed in single quotes.
        '''
        if isinstance(value, string_types):
            new_value = str(value)
            new_value = new_value.replace("'", "''")
            return "{}".format(new_value)
        return value

class sihxml:

    def __init__(self, xfile):
        if os.path.isfile(xfile)== False:
            print("The file ", xfile, "was not found on the disk")
            return None
        
        tree = ET.parse(xfile)
        xml_data = tree.getroot()
        
        xmlstr = ET.tostring(xml_data)#, encoding='utf8', method='xml'
                
        data_dict = dict(xmltodict.parse(xmlstr))
        
        self.data = data_dict
        
    def recursive_extract(self, data, reSub=None):
        if isinstance(data, dict):
            values = dict()
            for k, row in data.items():
                if reSub:
                    k = re.sub(reSub, '', k)
                k = k.lower()    
                key = sihstring().string_to_snake(k)
                if isinstance(row, dict) or isinstance(row, list):
                    values[key] = self.recursive_extract(row)
                else:
                    values[key] = str(row)
                
            return values
        elif isinstance(data, list):
            values = list()
            for val in data:
                values.append(self.recursive_extract(val))
                
            return values
        else:
            return str(data)
    '''Method for comptes annuels extraction '''
    def process_data_inpi(self,data, reSub = '(ns0\:)|(\@)|[^0-9A-Za-z\_]'):
        results = {}
        for k,row in data.items():
            key = re.sub(reSub, '', k)
            key= k.replace('ns0','')
            key = re.sub(r"[^0-9A-Za-z\_]",'', key)
            
            results[key] = self.recursive_extract(row, reSub)
        
        return results

class sihftp:
    def __init__(self):
        self.connection = None
        
    def connect(self, host='127.0.0.1',user='anonymous',password='', type='ftp_tls'):
        self.interval = 0.05
        self.connection = None
        
        try:
            if type=='ftp':
                self.connection = FTP(host=host)
                self.connection.login(user=user, passwd=password)
            if type=='ftp_tls':
                self.connection = FTP_TLS(host=host)
                self.connection.login(user=user, passwd=password)
                self.connection.prot_c()
           
        except all_errors as e:
            print(type, 'connection failed: ',str(e))
            
            return None
        
        self.connection.set_pasv(True)
        
        print(self.connection.getwelcome())
        
        return self.connection
    
    def listcontent(self, directory='/'):
        
        if directory:
            self.connection.cwd(directory)
        
        self.connection.cwd(directory)
        
        return self.connection.retrlines('LIST')
    def nlist(self, remote):
        if remote:
            self.connection.cwd(remote)
        
        return self.connection.nlst()
    
    def downloadFiles(self, path, destination):
        try:
            self.connection.cwd(path)       
            os.chdir(destination)
            self.mkLocaldir(destination[0:len(destination)-1] + path)
            print ("Created: " + destination[0:len(destination)-1] + path)
        except OSError:     
            pass
        except error_perm as e:       
            print ("Error: could not change to " + path)
            print(e)
            sys.exit("Ending Application")
        
        filelist=self.connection.nlist()
    
        for file in filelist:
            time.sleep(self.interval)
            try:            
                self.connection.cwd(path + file + "/")          
                self.downloadFiles(path + file + "/", destination)
            except error_perm:
                os.chdir(destination[0:len(destination)-1] + path)
                
                try:
                    self.connection.retrbinary("RETR " + file, open(os.path.join(destination + path, file),"wb").write)
                    print ("Downloaded: " + file)
                except:
                    print ("Error: File could not be downloaded " + file)
        return
    def mkLocaldir(self, path):
        try:
            os.makedirs(path)
        except OSError:
            if os.path.isdir(path):
                pass
            else:
                raise