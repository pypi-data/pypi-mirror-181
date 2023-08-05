#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 18:27:16 2020

@author: yefangon
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import mysql.connector
from mysql.connector import Error
from six import string_types
import datetime
import dateutil.parser
import sihtools.sihtools as tools

class sihmongodb:
    def __init__(self, host, port,username, password, authSource='admin',authMechanism='SCRAM-SHA-256'):
        url = 'mongodb://%s:%s@%s:%s/?authSource=%s&authMechanism=%s'
        try:
            self.client = MongoClient(url%(username, password,host, port,authSource,authMechanism))
            print("Connected to Mongo Server")
        except ConnectionFailure:
            print("Server not available")

    def setAll(self, databaseName, collectionName):
        self.setDatabase(databaseName)
        self.setCollection(collectionName)

    def setDatabase(self, databaseName):
        try:
            self.database = self.client[databaseName]
        except ConnectionFailure:
            print("Cannot connect to the databse: %s"%databaseName)

    def setCollection(self, collectionName):
        if not self.database:
            print("You must first set a database")
            return None
        else:
            self.collection = self.database[collectionName]
    
    def dropCollection(self, collectionName):
        if not self.database:
            print("You must first set a database")
            return None
        try:
            self.database[collectionName].drop()
        except:
            pass

    def findAll(self, criteria = {}, limit = None, skip = None):
        if not self.collection:
            print("No available connection found")
            return None
        else:
            if limit != None and skip != None:
                return self.collection.find(criteria).limit(limit).skip(skip)
            else:
                return self.collection.find(criteria)
    def findOne(self, criteria):
        if not self.collection:
            print("No available connection found")
            return None
        else:
            return self.collection.find_one(criteria)
    """
    Update one document in a collection
    criteria: dict
    doc: {'$set': {"col1": "value1", "col2": "value2" }}
    upsert: Bool
    """
    def update_one(self, criteria, doc,upsert=True):
        try:
            self.collection.update_one(filter=criteria, update=doc,upsert=upsert)
        except ConnectionFailure as e:
            print('Update failed: ',e)
            
            return None

        return True
    
    def update_many(self, documents, key, upsert = True):
        if not isinstance(documents, list) or len(documents) <= 0:
            return None
        done = 0
        for doc in documents:
            if not key in doc.keys():
                continue
            
            k_value = doc[key]
            self.update_one({key: k_value}, {'$set': doc}, upsert=upsert)
            done = done +1
        
        return done
    """
    insert one document in a collection
    
    insert_one({"colone": "value1", "coltwo": "value2"})
    """
    def insert_one(self, doc):
        try:
            self.collection.insert_one(document=doc)
        except ConnectionFailure as e:
            print('Insert one failed: ',e)
            
            return None
        
        return True
    def insert_many(self, docs):
        try:
            self.collection.insert_many(docs)
        except ConnectionFailure as e:
            print('Insert many failed: ',e)
            
            return None
        return True
    def createIndex(self, indexes = []):
        try:
            self.collection.create_index(indexes)
        except:
            raise('The indexes creation has failed')
  
    def dropIndexes(self):
        try:
            self.collection.drop_indexes()
        except:
            raise('The dropping of indexes has failed')
    def aggregate(self, pipeline):
        return self.collection.aggregate(pipeline)
    
    def map_reduce(self, mapper, reducer, target_collection):
        return self.collection.map_reduce(mapper, reducer, target_collection)
    
class sihmysql:
    def __init__(self, host , port, username, password, database):
        try:
            self.database = mysql.connector.connect(
                    host = host,
                    port=port,
                    user=username,
                    password=password,
                    db = database,
                    use_pure=True,
                    use_unicode=True,
                    charset="utf8"
                    )
            if self.database.is_connected:
                dbInfo = self.database.get_server_info()
                print("Connected to Mysql database", dbInfo)
        except Error as e:
            print("Connection failed", e)

    def select(self, query):
        self.cursor = self.database.cursor()

        self.cursor.execute(query)

        return self.cursor.fetchall()
    
    def select_one(self, query):
        self.cursor = self.database.cursor()

        self.cursor.execute(query)

        return self.cursor.fetchone()

    def update(self, sql, values={}):
        self.execute(sql, values)

        return self.cursor.rowcount
    
    def insert (self, sql, values = {}):
        return self.execute(sql, values)
        
    def lastrowid(self):
        if not self.cursor:
            return None
        
        return self.cursor.lastrowid
       
    def execute(self, sql, values = {}):
        self.cursor = self.database.cursor()

        self.cursor.execute(sql, values)
        self.database.commit()

        return True
    
    def quote_sql_string(self, value):
        '''
        If `value` is a string type, escapes single quotes in the string
        and returns the string enclosed in single quotes.
        '''
        if isinstance(value, string_types):
            new_value = str(value)
            new_value = new_value.replace("'", "''")
            return "{}".format(new_value)
        return value
    def get_upd_sihetablissement_query(self, ets = {}):
        utils = tools.sihutilities()
        query_upd = '''
                UPDATE `c1melanie`.`sih_etablissement`
                SET
                `activiteprincipaleetablissement` = '{activitePrincipaleEtablissement}',
                `activiteprincipaleregistremetiersetablissement` = '{activitePrincipaleRegistreMetiersEtablissement}',
                `anneeeffectifsetablissement` = '{anneeEffectifsEtablissement}',
                `caractereemployeuretablissement` = '{caractereEmployeurEtablissement}',
                `codecedex2etablissement` = '{codeCedex2Etablissement}',
                `codecedexetablissement` = '{codeCedexEtablissement}',
                `codecommune2etablissement` = '{codeCommune2Etablissement}',
                `codecommuneetablissement` = '{codeCommuneEtablissement}',
                `codepaysetranger2etablissement` = '{codePaysEtranger2Etablissement}',
                `codepaysetrangeretablissement` = '{codePaysEtrangerEtablissement}',
                `codepostal2etablissement` = '{codePostal2Etablissement}',
                `codepostaletablissement` = '{codePostalEtablissement}',
                `complementadresse2etablissement` = '{complementAdresse2Etablissement}',
                `complementadresseetablissement` = '{complementAdresseEtablissement}',
                `datecreationetablissement` = '{dateCreationEtablissement}',
                `datedebut` = '{dateDebut}',
                `datederniertraitementetablissement` = '{dateDernierTraitementEtablissement}',
                `denominationusuelleetablissement` = '{denominationUsuelleEtablissement}',
                `distributionspeciale2etablissement` = '{distributionSpeciale2Etablissement}',
                `distributionspecialeetablissement` = '{distributionSpecialeEtablissement}',
                `enseigne1etablissement` = '{enseigne1Etablissement}',
                `enseigne2etablissement` = '{enseigne2Etablissement}',
                `enseigne3etablissement` = '{enseigne3Etablissement}',
                `etablissementsiege` = '{etablissementSiege}',
                `etatadministratifetablissement` = '{etatAdministratifEtablissement}',
                `indicerepetition2etablissement` = '{indiceRepetition2Etablissement}',
                `indicerepetitionetablissement` = '{indiceRepetitionEtablissement}',
                `libellecedex2etablissement` = '{libelleCedex2Etablissement}',
                `libellecedexetablissement` = '{libelleCedexEtablissement}',
                `libellecommune2etablissement` = '{libelleCommune2Etablissement}',
                `libellecommuneetablissement` = '{libelleCommuneEtablissement}',
                `libellecommuneetranger2etablissement` = '{libelleCommuneEtranger2Etablissement}',
                `libellecommuneetrangeretablissement` = '{libelleCommuneEtrangerEtablissement}',
                `libelleeaysetranger2etablissement` = '{libellePaysEtranger2Etablissement}',
                `libelleeaysetrangeretablissement` = '{libellePaysEtrangerEtablissement}',
                `libellevoie2etablissement` = '{libelleVoie2Etablissement}',
                `libellevoieetablissement` = '{libelleVoieEtablissement}',
                `nic` = '{nic}',
                `nombreperiodesetablissement` = {nombrePeriodesEtablissement},
                `nomenclatureactiviteprincipaleetablissement` = '{nomenclatureActivitePrincipaleEtablissement}',
                `numerovoie2etablissement` = '{numeroVoie2Etablissement}',
                `numerovoieetablissement` = '{numeroVoieEtablissement}',
                `siren` = '{siren}',
                `siret` = '{siret}',
                `statutdiffusionetablissement` = '{statutDiffusionEtablissement}',
                `trancheeffectifsetablissement` = '{trancheEffectifsEtablissement}',
                `effectifetablissementmax` = {effectifetablissementmax},
                `effectifetablissementmin` = {effectifetablissementmin},
                `typevoie2etablissement` = '{typeVoie2Etablissement}',
                `typevoieetablissement` = '{typeVoieEtablissement}',
                `typevoieetablissement_normalise` = '{typevoieetablissement_normalise}',
                `adresse_normalisee` = '{adresse_normalisee}',
                `denomination_normalisee` = '{denomination_normalisee}',
                `updated_at` = '{updated_at}',
                `enabled` = {enabled}
                WHERE `id` = {item_id};

                '''

        if ets['dateDernierTraitementEtablissement']:
            dateTraitement = dateutil.parser.parse(ets['dateDernierTraitementEtablissement'])
            ets['dateDernierTraitementEtablissement'] = dateTraitement.strftime("%Y-%m-%d")
        else:
            ets['dateDernierTraitementEtablissement'] = ''

        eff = utils.processEffectif(ets['trancheEffectifsEtablissement'])
        ets['effectifetablissementmax'] = eff[0]
        ets['effectifetablissementmin'] = eff[1]

        ets['typevoieetablissement_normalise'] = utils.processTypeDeVoie(ets['typeVoieEtablissement'])

        ets['adresse_normalisee'] = utils.processAddress(ets)
        ets['denomination_normalisee'] = utils.processDenomination(ets)

        ets['enabled'] = 1

        ets['nombrePeriodesEtablissement'] = int(ets['nombrePeriodesEtablissement'])

        ets['updated_at'] = datetime.datetime.utcnow()

        ets = utils.quoteStrings(ets)

        sql = query_upd.format(**ets)

        return sql
    def get_ins_sihetablissement_query(self, ets = {}):
        utils = tools.sihutilities()
        query_upd = '''
                INSERT INTO `c1melanie`.`sih_etablissement`(
                `activiteprincipaleetablissement` ,
                `activiteprincipaleregistremetiersetablissement` ,
                `anneeeffectifsetablissement` ,
                `caractereemployeuretablissement` ,
                `codecedex2etablissement`,
                `codecedexetablissement`,
                `codecommune2etablissement`,
                `codecommuneetablissement`,
                `codepaysetranger2etablissement`,
                `codepaysetrangeretablissement` ,
                `codepostal2etablissement`,
                `codepostaletablissement`,
                `complementadresse2etablissement`,
                `complementadresseetablissement`,
                `datecreationetablissement`,
                `datedebut`,
                `datederniertraitementetablissement`,
                `denominationusuelleetablissement`,
                `distributionspeciale2etablissement`,
                `distributionspecialeetablissement`,
                `enseigne1etablissement`,
                `enseigne2etablissement`,
                `enseigne3etablissement`,
                `etablissementsiege`,
                `etatadministratifetablissement`,
                `indicerepetition2etablissement` ,
                `indicerepetitionetablissement`,
                `libellecedex2etablissement` ,
                `libellecedexetablissement`,
                `libellecommune2etablissement` ,
                `libellecommuneetablissement`,
                `libellecommuneetranger2etablissement`,
                `libellecommuneetrangeretablissement`,
                `libelleeaysetranger2etablissement`,
                `libelleeaysetrangeretablissement`,
                `libellevoie2etablissement`,
                `libellevoieetablissement`,
                `nic`,
                `nombreperiodesetablissement` ,
                `nomenclatureactiviteprincipaleetablissement`,
                `numerovoie2etablissement`,
                `numerovoieetablissement`,
                `siren`,
                `siret`,
                `statutdiffusionetablissement`,
                `trancheeffectifsetablissement`,
                `effectifetablissementmax`,
                `effectifetablissementmin`,
                `typevoie2etablissement`,
                `typevoieetablissement`,
                `typevoieetablissement_normalise`,
                `adresse_normalisee`,
                `denomination_normalisee`,
                `updated_at`,
                `enabled`
                )
                VALUES(
                 '{activitePrincipaleEtablissement}',
                '{activitePrincipaleRegistreMetiersEtablissement}',
                '{anneeEffectifsEtablissement}',
                '{caractereEmployeurEtablissement}',
                '{codeCedex2Etablissement}',
                '{codeCedexEtablissement}',
                '{codeCommune2Etablissement}',
                '{codeCommuneEtablissement}',
                '{codePaysEtranger2Etablissement}',
                '{codePaysEtrangerEtablissement}',
                '{codePostal2Etablissement}',
                '{codePostalEtablissement}',
                '{complementAdresse2Etablissement}',
                '{complementAdresseEtablissement}',
                '{dateCreationEtablissement}',
                '{dateDebut}',
                '{dateDernierTraitementEtablissement}',
                '{denominationUsuelleEtablissement}',
                '{distributionSpeciale2Etablissement}',
                '{distributionSpecialeEtablissement}',
                '{enseigne1Etablissement}',
                '{enseigne2Etablissement}',
                '{enseigne3Etablissement}',
                '{etablissementSiege}',
                '{etatAdministratifEtablissement}',
                '{indiceRepetition2Etablissement}',
                '{indiceRepetitionEtablissement}',
                '{libelleCedex2Etablissement}',
                '{libelleCedexEtablissement}',
                '{libelleCommune2Etablissement}',
                '{libelleCommuneEtablissement}',
                '{libelleCommuneEtranger2Etablissement}',
                '{libelleCommuneEtrangerEtablissement}',
                '{libellePaysEtranger2Etablissement}',
                '{libellePaysEtrangerEtablissement}',
                '{libelleVoie2Etablissement}',
                '{libelleVoieEtablissement}',
                '{nic}',
                {nombrePeriodesEtablissement},
                '{nomenclatureActivitePrincipaleEtablissement}',
                '{numeroVoie2Etablissement}',
                '{numeroVoieEtablissement}',
                '{siren}',
                '{siret}',
                '{statutDiffusionEtablissement}',
                '{trancheEffectifsEtablissement}',
                {effectifetablissementmax},
                {effectifetablissementmin},
                '{typeVoie2Etablissement}',
                '{typeVoieEtablissement}',
                '{typevoieetablissement_normalise}',
                '{adresse_normalisee}',
                '{denomination_normalisee}',
                '{created_at}',
                '{updated_at}',
                {enabled}
                );

                '''

        if ets['dateDernierTraitementEtablissement']:
            dateTraitement = dateutil.parser.parse(ets['dateDernierTraitementEtablissement'])
            ets['dateDernierTraitementEtablissement'] = dateTraitement.strftime("%Y-%m-%d")
        else:
            ets['dateDernierTraitementEtablissement'] = ''

        eff = utils.processEffectif(ets['trancheEffectifsEtablissement'])
        ets['effectifetablissementmax'] = eff[0]
        ets['effectifetablissementmin'] = eff[1]

        ets['typevoieetablissement_normalise'] = utils.processTypeDeVoie(ets['typeVoieEtablissement'])

        ets['adresse_normalisee'] = utils.processAddress(ets)
        ets['denomination_normalisee'] = utils.processDenomination(ets)

        ets['enabled'] = 1

        ets['nombrePeriodesEtablissement'] = int(ets['nombrePeriodesEtablissement'])

        ets['created_at'] = datetime.datetime.utcnow()
        ets['updated_at'] = datetime.datetime.utcnow()

        ets = utils.quoteStrings(ets)

        sql = query_upd.format(**ets)

        return sql
    
    def get_upd_unitelegale_query(self, uintelegale = {}):
        query = """
            UPDATE `sih_unite_legale`
                    SET
                    `activiteprincipaleunitelegale` = '{activitePrincipaleUniteLegale}',
                    `anneecategorieentreprise` = '{anneeCategorieEntreprise}',
                    `anneeeffectifseniteeegale` = '{anneeEffectifsUniteLegale}',
                    `caractereemployeurunitelegale` = '{caractereEmployeurUniteLegale}',
                    `categorieentreprise` = '{categorieEntreprise}',
                    `categoriejuridiqueunitelegale` = '{categorieJuridiqueUniteLegale}',
                    `datecreationunitelegale` = '{dateCreationUniteLegale}',
                    `datedebut` = '{dateDebut}',
                    `datederniertraitementunitelegale` = '{dateDernierTraitementUniteLegale}',
                    `denominationunitelegale` = '{denominationUniteLegale}',
                    `denominationusuelle1unitelegale` = '{denominationUsuelle1UniteLegale}',
                    `denominationusuelle2unitelegale` = '{denominationUsuelle2UniteLegale}',
                    `denominationusuelle3unitelegale` = '{denominationUsuelle3UniteLegale}',
                    `economiesocialesolidaireunitelegale` = '{economieSocialeSolidaireUniteLegale}',
                    `etatadministratifunitelegale` = '{etatAdministratifUniteLegale}',
                    `identifiantassociationunitelegale` = '{identifiantAssociationUniteLegale}',
                    `nicsiegeunitelegale` = '{nicSiegeUniteLegale}',
                    `nombreperiodesunitelegale` = '{nombrePeriodesUniteLegale}',
                    `nomenclatureactiviteprincipaleunitelegale` = '{nomenclatureActivitePrincipaleUniteLegale}',
                    `nomunitelegale` = '{nomUniteLegale}',
                    `nomusageunitelegale` = '{nomUsageUniteLegale}',
                    `prenom1unitelegale` = '{prenom1UniteLegale}',
                    `prenom2unitelegale` = '{prenom2UniteLegale}',
                    `prenom3unitelegale` = '{prenom3UniteLegale}',
                    `prenom4unitelegale` = '{prenom4UniteLegale}',
                    `prenomusuelunitelegale` = '{prenomUsuelUniteLegale}',
                    `pseudonymeunitelegale` = '{pseudonymeUniteLegale}',
                    `sexeunitelegale` = '{sexeUniteLegale}',
                    `sigleunitelegale` = '{sigleUniteLegale}',
                    `siren` = '{siren}',
                    `statutdiffusionunitelegale` = '{statutDiffusionUniteLegale}',
                    `trancheeffectifsunitelegale` = '{trancheEffectifsUniteLegale}',
                    `unitepurgeeunitelegale` = '{unitePurgeeUniteLegale}',
                    `siret` = '{siret}',
                    `effectif_max_unite_legale` = {effectif_max_unite_legale},
                    `effectif_min_unite_legale` = {effectif_min_unite_legale},
                    `denomination_normalisee` = '{denomination_normalisee}',
                    `updated_at` = '{updated_at}'
                    WHERE `id` = '{item_id}';
        """
        utils = tools.sihutilities()
        
        uintelegale['updated_at'] = datetime.datetime.utcnow()
        
        if 'dateDernierTraitementUniteLegale' in uintelegale and uintelegale['dateDernierTraitementUniteLegale']:
            dateTraitement = dateutil.parser.parse(uintelegale['dateDernierTraitementUniteLegale'])
            uintelegale['dateDernierTraitementUniteLegale'] = dateTraitement.strftime("%Y-%m-%d")
        else:
            uintelegale['dateDernierTraitementUniteLegale'] = ''
        
        if 'trancheEffectifsUniteLegale' in uintelegale:
            eff = utils.processEffectif(uintelegale['trancheEffectifsUniteLegale'])
            uintelegale['effectif_max_unite_legale'] = eff[0]
            uintelegale['effectif_min_unite_legale'] = eff[1]
        else:
            uintelegale['trancheEffectifsUniteLegale'] = 'NN'
            uintelegale['effectif_max_unite_legale'] = 0
            uintelegale['effectif_min_unite_legale'] = 0
        
        uintelegale['denomination_normalisee'] = utils.processDenominationUniteLegale(uintelegale)
        
        uintelegale = utils.quoteStrings(uintelegale)
        try :
            sql = query.format(**uintelegale)
        except:
            return None

        return sql