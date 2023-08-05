#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase
from sihscraper import sihscraper as scraper

class test_sihformscraper(TestCase):
    def test_get_all_form(self):
        formscraper = scraper.sihformscraper()
        all_forms = formscraper.get_all_form('https://beta.sihfrance.com/sih/fr/login')
        
        self.assertTrue(len(all_forms) > 0)
        
    def test_get_form_by_name(self):
        formscraper = scraper.sihformscraper()
        form = formscraper.get_form_by_name('https://beta.sihfrance.com/sih/fr/login', 'rechAnnComm')
        
        self.assertFalse(form != None)
        
    def test_get_form_by_action(self):
        formscraper = scraper.sihformscraper()
        form = formscraper.get_form_by_action('https://beta.sihfrance.com/sih/fr/login', '/sih/fr/login')
        
        self.assertTrue(form != None)
    
    def test_submit_form(self):
        formscraper = scraper.sihformscraper()
        form = formscraper.get_form_by_action('https://beta.sihfrance.com/sih/fr/login', '/sih/fr/login')
        
        res = formscraper.submit_form('https://beta.sihfrance.com',form,  {'email': 'yefangon@sihfrance.com', 'password': 'zouzou'})
        
        self.assertTrue(res != None)

class test_sihscraper(TestCase):
    def test_table_to_array(self):
        html = """
          <table>
          <tr><td>col11</td><td>col12</td></tr>
          <tr><td>col21</td><td>col22</td></tr>
          </table>
        """
    
        sihscraper = scraper.sihscraper()
        
        array = sihscraper.table_to_array(html)
       
        self.assertTrue(array and len(array)>0)
        
    def test_li_to_array(self):
      html = """
      <div class="bloc">
      <ul>   
            <li><b>nom : </b>Foratier ; <b>pr&eacute;nom : </b>Julie, Cathy, Céline ; <b>RCS : </b>883 162 935 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>62<br/><a href="/annonce/detail-annonce/A/20200090/673">Voir l&acute;annonce n&deg;673 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>nom : </b>LECLERCQ ; <b>pr&eacute;nom : </b>Valentin, Hubert, Oscar ; <b>RCS : </b>883 089 716 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>62<br/><a href="/annonce/detail-annonce/A/20200090/675">Voir l&acute;annonce n&deg;675 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>nom : </b>LEFEBVRE ; <b>pr&eacute;nom : </b>Tony, Roger, Nicolas ; <b>RCS : </b>882 449 101 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>62<br/><a href="/annonce/detail-annonce/A/20200090/676">Voir l&acute;annonce n&deg;676 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>nom : </b>SEBERT ; <b>pr&eacute;nom : </b>Laëticia Paulette Suzanne ; <b>RCS : </b>751 801 002 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>62<br/><a href="/annonce/detail-annonce/A/20200090/678">Voir l&acute;annonce n&deg;678 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>nom : </b>LARTIGUE ; <b>pr&eacute;nom : </b>Paul, Bittor ; <b>RCS : </b>882 946 221 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>64<br/><a href="/annonce/detail-annonce/A/20200090/699">Voir l&acute;annonce n&deg;699 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>nom : </b>MAFFOLINI ; <b>pr&eacute;nom : </b>David ; <b>RCS : </b>883 098 774 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>64<br/><a href="/annonce/detail-annonce/A/20200090/703">Voir l&acute;annonce n&deg;703 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>d&eacute;nomination : </b>LARRUN LODGE ; <b>RCS : </b>882 745 334 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>64<br/><a href="/annonce/detail-annonce/A/20200090/730">Voir l&acute;annonce n&deg;730 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>d&eacute;nomination : </b>ZABAROTZEA ; <b>RCS : </b>883 021 735 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>64<br/><a href="/annonce/detail-annonce/A/20200090/744">Voir l&acute;annonce n&deg;744 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>nom : </b>DEMIR ; <b>pr&eacute;nom : </b>Nurican ; <b>RCS : </b>883 010 696 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>64<br/><a href="/annonce/detail-annonce/A/20200090/756">Voir l&acute;annonce n&deg;756 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>d&eacute;nomination : </b>SCI FIORBA ; <b>RCS : </b>883 136 129 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>64<br/><a href="/annonce/detail-annonce/A/20200090/770">Voir l&acute;annonce n&deg;770 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>d&eacute;nomination : </b>SCI LA PORSCHERIE ; <b>RCS : </b>883 063 810 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>64<br/><a href="/annonce/detail-annonce/A/20200090/771">Voir l&acute;annonce n&deg;771 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>d&eacute;nomination : </b>L'ATELIER DES DELICES ; <b>RCS : </b>881 885 990 ; <b>Cat&eacute;gorie : </b>Ventes et cessions ; <b>D&eacute;partement : </b>69<br/><a href="/annonce/detail-annonce/A/20200090/780">Voir l&acute;annonce n&deg;780 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>d&eacute;nomination : </b>STUDIO MARIE ROLLAND ; <b>RCS : </b>882 369 606 ; <b>Cat&eacute;gorie : </b>Ventes et cessions ; <b>D&eacute;partement : </b>75<br/><a href="/annonce/detail-annonce/A/20200090/790">Voir l&acute;annonce n&deg;790 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>nom : </b>Bah ; <b>pr&eacute;nom : </b>Aissata ; <b>RCS : </b>883 111 346 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>75<br/><a href="/annonce/detail-annonce/A/20200090/795">Voir l&acute;annonce n&deg;795 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>nom : </b>Dimitrova ; <b>pr&eacute;nom : </b>Simona ; <b>RCS : </b>883 115 461 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>75<br/><a href="/annonce/detail-annonce/A/20200090/797">Voir l&acute;annonce n&deg;797 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>d&eacute;nomination : </b>EVEN FLOW ; <b>RCS : </b>883 121 691 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>75<br/><a href="/annonce/detail-annonce/A/20200090/822">Voir l&acute;annonce n&deg;822 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>d&eacute;nomination : </b>Respawn Capital ; <b>RCS : </b>883 142 069 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>75<br/><a href="/annonce/detail-annonce/A/20200090/840">Voir l&acute;annonce n&deg;840 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>d&eacute;nomination : </b>SCI LES QUOKKAS ; <b>RCS : </b>883 116 410 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>75<br/><a href="/annonce/detail-annonce/A/20200090/846">Voir l&acute;annonce n&deg;846 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>nom : </b>Chabane ; <b>pr&eacute;nom : </b>Murielle Véronique ; <b>RCS : </b>883 113 771 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>77<br/><a href="/annonce/detail-annonce/A/20200090/868">Voir l&acute;annonce n&deg;868 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>nom : </b>HAMMA ; <b>pr&eacute;nom : </b>Mounir ; <b>RCS : </b>753 089 630 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>78<br/><a href="/annonce/detail-annonce/A/20200090/890">Voir l&acute;annonce n&deg;890 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>nom : </b>LOPEZ MARTIN ; <b>pr&eacute;nom : </b>Jean ; <b>RCS : </b>883 157 703 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>78<br/><a href="/annonce/detail-annonce/A/20200090/892">Voir l&acute;annonce n&deg;892 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>nom : </b>RODRIGUES ; <b>pr&eacute;nom : </b>Maxime ; <b>RCS : </b>883 201 725 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>78<br/><a href="/annonce/detail-annonce/A/20200090/895">Voir l&acute;annonce n&deg;895 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>d&eacute;nomination : </b>LA COMPRE ; <b>RCS : </b>883 206 245 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>78<br/><a href="/annonce/detail-annonce/A/20200090/901">Voir l&acute;annonce n&deg;901 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>d&eacute;nomination : </b>X-Elek ; <b>RCS : </b>502 136 898 ; <b>Cat&eacute;gorie : </b>Immatriculations ; <b>D&eacute;partement : </b>78<br/><a href="/annonce/detail-annonce/A/20200090/911">Voir l&acute;annonce n&deg;911 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>nom : </b>GALLARDO ; <b>pr&eacute;nom : </b>David Alexandre ; <b>RCS : </b>531 511 467 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>84<br/><a href="/annonce/detail-annonce/A/20200090/918">Voir l&acute;annonce n&deg;918 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>d&eacute;nomination : </b>"CABAC" ; <b>RCS : </b>883 122 822 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>85<br/><a href="/annonce/detail-annonce/A/20200090/928">Voir l&acute;annonce n&deg;928 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>d&eacute;nomination : </b>FABIEN MURAIL ; <b>RCS : </b>883 121 618 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>85<br/><a href="/annonce/detail-annonce/A/20200090/932">Voir l&acute;annonce n&deg;932 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>d&eacute;nomination : </b>CD PATRIMOINE ; <b>RCS : </b>883 112 443 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>86<br/><a href="/annonce/detail-annonce/A/20200090/944">Voir l&acute;annonce n&deg;944 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>nom : </b>RONDOT ; <b>pr&eacute;nom : </b>Vincent ; <b>RCS : </b>883 202 152 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>90<br/><a href="/annonce/detail-annonce/A/20200090/950">Voir l&acute;annonce n&deg;950 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
            <li><b>d&eacute;nomination : </b>SCI DES MAVIT ; <b>RCS : </b>883 196 370 ; <b>Cat&eacute;gorie : </b>Cr&eacute;ations ; <b>D&eacute;partement : </b>91<br/><a href="/annonce/detail-annonce/A/20200090/971">Voir l&acute;annonce n&deg;971 du Bodacc n&deg;20200090 du 10/05/2020</a></li>
          </ul>
    </div>
      """
      sihscraper = scraper.sihscraper()
        
      array = sihscraper.list_to_array(html)
     
      self.assertTrue(array and len(array)>0)
    
    def test_dl_to_array(self):
        html = """
        <div id="annonce">
            <h3>	Créations d'établissements</h3>
            <p class="standardMargin"><em>Bodacc A n°20200090 publié le 10/05/2020</em></p>
            <dl>
            <!-- numero annonce -->
            <dt>Annonce n° </dt><dd>11</dd>
            <!-- rectificatif, annulation -->
            <!-- RCS -->
            <dt>
            <abbr title="Registre du commerce et des sociétés">n°RCS</abbr> :
                                </dt>
            <dd>
                    883 119 448
                    RCS
                    Saint-Quentin
                    </dd>
            <!-- RM -->
            <!-- denomination --> <dt>Dénomination :</dt>
            <dd>SAS INSO</dd>
            <!-- Nom -->
            <!-- Prenom -->
            <!-- Nom d'usage -->
            <!-- Nationalite -->
            <!-- Sigle -->
            <!-- Forme Juridique -->
            <dt>Forme :</dt>
            <dd>Société par actions simplifiée</dd>
            <!-- capital -->
            <dt>Capital :</dt>
            <dd>1000 EUR</dd>
            <!-- pseudonyme -->
            <!-- nom commercial -->
            <dt>Nom commercial :</dt>
            <dd>L'Insolite</dd>
            <!-- administration -->
            <dt>Administration :</dt>
            <dd>Président : Paruch, Stéphane Henri, Directeur général : Tricqueneaux, Christophe Yvon Adrien</dd>
            <!-- adresse -->
            <dt>Adresse :</dt>
            <dd> 
                                28 
                                rue 
                                du Pont d'Elva 
                                02700 
                                Tergnier 
                            </dd>
            <dt>Etablissement(s) :</dt><dd>
            <dl>
            <!-- Qualité établissement -->
            <dt class="invisible">Qualité de l'établissement</dt>
            <dd>Etablissement principal</dd>
            <!-- origine du fond -->
            <dt>Origine du fond :</dt>
            <dd>Création</dd>
            <!-- Activite -->
            <dt>Activité :</dt>
            <dd>Restauration sur place avec vente d'alcool.</dd>
            <!-- Enseigne -->
            <dt>Enseigne :</dt>
            <dd>L'Insolite</dd>
            <!-- Adresse de l'établissement -->
            <dt>Adresse de l'établissement :</dt>
            <dd> 
                            15C 
                            rue 
                            Aristide Briand 
                            02300 
                            Chauny 
                        </dd>
            </dl>
            </dd>
            <!-- PRECEDENT PROPRIETAIRE -->
            <!-- PRECEDENT EXPLOITANT -->
            <!-- Date immatriculation -->
            <dt>A dater du :</dt>
            <dd>29 avril 2020</dd>
            <!-- date Effet -->
            <!-- date Commencement Activite -->
            <dt>Date de commencement d'activité :</dt>
            <dd>01 mai 2020</dd>
            <!-- Publication légale -->
            <!-- opposition -->
            <!-- déclarations de creances -->
            <!-- Descriptif -->
            </dl>
            <p class="pdf-unit">
            <a href="/annonce/telecharger/BODACC_A%5C2020%5C20200090%5C0%5CBODACC_A_PDF_Unitaire_20200090_00011.pdf" onclick="return xt_click(this,'C','2','temoin_publication_bodacc_A','T');" title="Téléchargez le témoin de publication de l'annonce n°11 du Bodacc A n°20200090 du 10/05/2020 - Format pdf - 137,40 kB">
            <img alt="" class="temoin" src="/extension/dilabodacc/design/dilabodacc/images/deco/temoin.png"/>
                                    Téléchargez le témoin de publication</a>
            </p>
            <p>
            <a class="lienExterne" href="http://www.infogreffe.fr/infogreffe/ficheIdentite.do?siren=883119448" title="Voir la fiche de renseignement sur l'entreprise 'SAS INSO' au Registre du commerce sur le site Infogreffe - Site externe">
                            Voir la fiche de renseignement sur l'entreprise 'SAS INSO'				au Registre du commerce sur le site Infogreffe
                            </a>
            <br/>
            </p>
            </div>
        """
        sihscraper = scraper.sihscraper()
        
        array = sihscraper.dl_to_array(html)
        print(array)
        self.assertTrue(isinstance(array, list) and len(array)>0)
      
class test_sihextractbk(TestCase):
    def test_extractItems(self):
        extractbk = scraper.sihextractbk('/home/data/crawler/booking/booking/20200206/search_5e3bdb1f125845.49581136.html')
        items = extractbk.extractItems()
        self.assertTrue(isinstance(items, dict))
        #self.assertTrue(len(list(items)) == 7)
        print(items)