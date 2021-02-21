# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 21:32:06 2018

@author: Ronald Scheffler
"""

import xml.etree.ElementTree as ET
import csv
import timeit
import re


#xmlns="http://www.mediawiki.org/xml/export-0.10/" 
#xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
#xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd" 
#version="0.10" 
#xml:lang="en">

# Methode zum suchen des n-ten Vorkommens eines Characters c in einem String s
def findx(string, char, n):
    # Wenn Char in String enthalten
    if string.__contains__(char):
        # Splitte String an Character
        new = string.split(char, n)
        # Finde Position
        # new[-1] gibt letzten Teilstring (Rest) zurück
        posx = len(string) - len(new[-1]) - len(char)
        # Rückgabe
        return posx
    # Wenn Char nicht in String enthalten
    else:
        return 999

def create(data):    
    
    temp = data[findx(data,'-',1)+1:findx(data,'-',2)]
    outputstring = r"C:\Users\Ronald Scheffler\.spyder-py3\output"+temp+".csv"
    outputnormstring = r"C:\Users\Ronald Scheffler\.spyder-py3\outputnorm"+temp+".csv"
    outputdb = r"C:\Users\Ronald Scheffler\.spyder-py3\datenbank"+temp+".csv"
    
    # Starte CSV Writer
    # "w" - Das für csvfile übergebene Dateiobjekt muss für den Schreibzugriff im Textmodus geöffnet werden
    # Python 3, nutze 'w' an Stelle von 'wb'
    # encoding = "utf-8" notwendig für I/O Operationen
    writer2018 = csv.writer(open(outputstring, 'w', encoding = "utf-8"))
    #Schreibe erste Zeile: Tabellennamen
    writer2018.writerow(['botname','AS1','AS2','AS3','AS4','AS5','AS6','AS7','AS8'])
    
    # Schreibe normalisierte Daten
    writernorm = csv.writer(open(outputnormstring, 'w', encoding = "utf-8"))
    #Schreibe erste Zeile: Tabellennamen
    writernorm.writerow(['botname','AS1','AS2','AS3','AS4','AS5','AS6','AS7','AS8'])
    
    # Schreibe DB Daten
    writerdb = csv.writer(open(outputdb, 'w', encoding = "utf-8"))
    #Schreibe erste Zeile: Tabellennamen
    writerdb.writerow(['title','ns','page_id','redirect','restrictions','discussion',
                       'revision_id','parent_id','timestamp','username','user_id',
                       'minor','comment','action','model','wikiformat','sha1'])
    
    # Counter für Gesamtzahl von Edits
    editcounter = 0    
    # Counter für Anzahl von Botedits
    boteditcounter = 0    
    # Zuteilung der Action für Klassifizierung
    actionnumber = 0         
    # Liste aller gefunden Edits
    editarray = []      
    # Liste aller gefundenen Bots
    botarray = []    
    # Liste aller Edits zusammen mit dem Bot
    bot_edit_array = []     
    # Anzahl der Edits für einen Bot
    bot_edit_array = []
    # Counter für Vorkommen jeder einzelnen Action
    edit_count_array = []
    
    # Action Sets
    actionset1 = ['wbcreateredirect', 
                  'wbmergeitems-from', 
                  'wbmergeitems-to',                  
                  'wbeditentity-create-item']
    actionset2 = ['wbcreateclaim', 
                  'wbcreateclaim-create',
                  'wbremoveclaims', 
                  'wbremoveclaims-remove',
                  'wbsetclaim',
                  'wbsetclaim-update', 
                  'wbsetclaim-create', 
                  'wbsetclaimvalue',  
                  'wbremovereferences-remove',  
                  'wbsetreference-add', 
                  'wbremovequalifiers-remove', 
                  'wbsetqualifier-add',
                  'wbsetqualifier-update',
                  'wbeditentity-update',
                  'wbeditentity-override',
                  'wbeditentity-create']
    actionset3 = ['wbsetlabel-set',
                  'wbsetlabel-add', 
                  'wbsetdescription', 
                  'wbsetdescription-set',
                  'wbsetdescription-add',
                  'wbsetaliases-update',
                  'wbsetaliases-add',
                  'wbsetaliases-set']
    actionset4 = ['wbsetsitelink-set-badges', 
                  'wbsetsitelink-set',
                  'wbsetsitelink-add',
                  'clientsitelink-remove',
                  'clientsitelink-update']
    actionset5 = ['wbremovequalifiers-remove', 
                  'wbsetqualifier-add',
                  'wbsetqualifier-update',
                  'wbremoveclaims',
                  'wbremoveclaims-remove',
                  'wbsetclaimvalue']
    actionset6 = ['wbsetlabel-set120',
                  'wbsetlabel-add120',
                  'wbsetdescription-set120',
                  'wbsetdescription-add120',
                  'wbsetaliases-update120',
                  'wbsetaliases-add120',
                  'wbsetaliases-set120']
    actionset7 = ['Wikidata list updated']
    actionset8 = ['Reverted', 'undo', 'Protected']
    # actionset9 = ['Protected'] Zusammengefasst mit Actionset 8
    
    # Counter für Edits pro Actionset
    as1counter = 0
    as2counter = 0
    as3counter = 0
    as4counter = 0
    as5counter = 0
    as6counter = 0
    as7counter = 0
    as8counter = 0
    as9counter = 0
    
    # Namespace Counter
    nsmediacounter = 0
    nsspecialcounter = 0
    ns0counter = 0
    ns0unknowncounter = 0
    ns1counter = 0
    ns2counter = 0
    ns3counter = 0
    ns4counter = 0
    ns5counter = 0
    ns6counter = 0
    ns7counter = 0
    ns8counter = 0
    ns9counter = 0
    ns10counter = 0
    ns11counter = 0
    ns12counter = 0
    ns13counter = 0
    ns14counter = 0
    ns15counter = 0
    ns120counter = 0
    ns120unknowncounter = 0
    ns121counter = 0
    ns121unknowncounter = 0
    ns122counter = 0
    ns123counter = 0
    ns828counter = 0
    ns829counter = 0
    ns1198counter = 0
    ns1199counter = 0
    ns2300counter = 0
    ns2301counter = 0
    ns2302counter = 0
    ns2303counter = 0
    ns2600counter = 0    
    
    # Unique Edits in Namespaces
    nsmediaarray = []
    nsspecialarray = []
    ns0array = []
    ns0unknownarray = []
    ns1array = []
    ns2array = []
    ns3array = []
    ns4array = []
    ns5array = []
    ns6array = []
    ns7array = []
    ns8array = []
    ns9array = []
    ns10array = []
    ns11array = []
    ns12array = []
    ns13array = []
    ns14array = []
    ns15array = []
    ns120array = []
    ns120unknownarray = []
    ns121array = []
    ns121unknownarray = []
    ns122array = []
    ns123array = []
    ns828array = []
    ns829array = []
    ns1198array = []
    ns1199array = []
    ns2300array = []
    ns2301array = []
    ns2302array = []
    ns2303array = []
    ns2600array = []
    
    # ElementTree verwendet ein Wörterbuch zum speichern von Attribut-Werte, so ist es grundsätzlich ungeordnet    
    treeNameET = ET.ElementTree(file=r'C:\Users\Ronald Scheffler\.spyder-py3\bot_list_20180716_field.xml')
    rootNameET = treeNameET.getroot()

    tree = ET.parse(data)
    root = tree.getroot()
    
    # Wenn Elemente leer sind, setze sie auf Siteinfo, damit sie weiter verarbeitet werden können
    # Setze sie danach auf ''        
    empty_revision_id = root.find('{http://www.mediawiki.org/xml/export-0.10/}siteinfo')
    empty_revision_id.text = ''
    empty_parent_id = root.find('{http://www.mediawiki.org/xml/export-0.10/}siteinfo')
    empty_parent_id.text = ''
    empty_timestamp = root.find('{http://www.mediawiki.org/xml/export-0.10/}siteinfo')
    empty_timestamp.text = ''
    empty_username = root.find('{http://www.mediawiki.org/xml/export-0.10/}siteinfo')
    empty_username.text = ''
    empty_user_id = root.find('{http://www.mediawiki.org/xml/export-0.10/}siteinfo')
    empty_user_id.text = ''
    
    empty_user_redirect = root.find('{http://www.mediawiki.org/xml/export-0.10/}siteinfo')
    empty_user_redirect.text = ''
    empty_user_restrictions = root.find('{http://www.mediawiki.org/xml/export-0.10/}siteinfo')
    empty_user_restrictions.text = ''
    empty_user_discussion = root.find('{http://www.mediawiki.org/xml/export-0.10/}siteinfo')
    empty_user_discussion.text = ''
    empty_user_minor = root.find('{http://www.mediawiki.org/xml/export-0.10/}siteinfo')
    empty_user_minor.text = ''
    empty_user_model = root.find('{http://www.mediawiki.org/xml/export-0.10/}siteinfo')
    empty_user_model.text = ''
    empty_user_wikiformat = root.find('{http://www.mediawiki.org/xml/export-0.10/}siteinfo')
    empty_user_wikiformat.text = ''
    empty_user_sha1 = root.find('{http://www.mediawiki.org/xml/export-0.10/}siteinfo')
    empty_user_sha1.text = ''
    
    # Sammle Informationen dieser Sonderfälle
    emptyarray = []
    
    # Durchsuche alle Pages
    for page in root.getiterator('{http://www.mediawiki.org/xml/export-0.10/}page'):
        #print(page)
        # Title - was wurde geändert?
        title = page.find('{http://www.mediawiki.org/xml/export-0.10/}title').text
    
        # Namespace - Wo wurde etwas geändert?
        ns = int(page.find('{http://www.mediawiki.org/xml/export-0.10/}ns').text)
    
        # Page ID
        page_id = page.find('{http://www.mediawiki.org/xml/export-0.10/}id').text
        
        if page.find('{http://www.mediawiki.org/xml/export-0.10/}redirect') != None:
            redirect = page.find('{http://www.mediawiki.org/xml/export-0.10/}redirect')
        else:
            redirect = empty_user_redirect
        
        if page.find('{http://www.mediawiki.org/xml/export-0.10/}restrictions') != None:
            restrictions = page.find('{http://www.mediawiki.org/xml/export-0.10/}restrictions')
        else:
            restrictions = empty_user_restrictions
            
        if page.find('{http://www.mediawiki.org/xml/export-0.10/}discussionthreadinginfo') != None:
            discussion = page.find('{http://www.mediawiki.org/xml/export-0.10/}discussionthreadinginfo')
        else:
            discussion = empty_user_discussion
    
        #Durchsuche alle revisions
        #Halte Revision fest
        for revision in page.getiterator('{http://www.mediawiki.org/xml/export-0.10/}revision'):
            #print(revision)
            # Erhöhe Gesamtcounter
            editcounter += 1
            
            # Suche nach Contributor {http://www.mediawiki.org/xml/export-0.10/}
            contributor = revision.find('{http://www.mediawiki.org/xml/export-0.10/}contributor')
            # Untersuche Namen {http://www.mediawiki.org/xml/export-0.10/}
            user_name = contributor.find('{http://www.mediawiki.org/xml/export-0.10/}username')
                        
            #print(username.text)
            # Name darf nicht None sein
            # Bei unregistrierten, menschlichen Nutzen steht nur eine IP
            if (user_name != None):
                #print(username.text)
                #Vergleiche mit Botnamenliste
                for botRoot in rootNameET:
                    
                    # Für alle Botnamen in der Botliste
                    for botname in botRoot:
                        
                        # Wenn User = Bot                    
                        # Bot Namen wurden manuell wieder mit Leerzeichen versehen
                        # Prüfe auch ob Extension Bots ohne Leerzeichen in der Edit History auftauchen
                        if user_name.text == botname.text or user_name.text == botname.text.strip():
                            
                            # Liste alle gefundenen Bots
                            if user_name.text not in botarray:
                                botarray.append(user_name.text)
                            # Erhöhe Botedit Counter
                            boteditcounter += 1                            
                            # Weise Elemente zu
                            if revision.find('{http://www.mediawiki.org/xml/export-0.10/}id') != None:
                                revision_id = revision.find('{http://www.mediawiki.org/xml/export-0.10/}id')
                            else:
                                revision_id = empty_revision_id
                            if revision.find('{http://www.mediawiki.org/xml/export-0.10/}parentid') != None:
                                parent_id  = revision.find('{http://www.mediawiki.org/xml/export-0.10/}parentid')            
                            else:
                                parent_id = empty_parent_id
                            if revision.find('{http://www.mediawiki.org/xml/export-0.10/}timestamp') != None:
                                timestamp = revision.find('{http://www.mediawiki.org/xml/export-0.10/}timestamp')
                            else: 
                                timestamp = empty_timestamp
                            if contributor.find('{http://www.mediawiki.org/xml/export-0.10/}username') != None:
                                username = contributor.find('{http://www.mediawiki.org/xml/export-0.10/}username')
                            else: 
                                username = empty_username
                            if contributor.find('{http://www.mediawiki.org/xml/export-0.10/}id') != None:
                                user_id = contributor.find('{http://www.mediawiki.org/xml/export-0.10/}id')
                            else: 
                                user_id = empty_user_id
                            #Kompletten Comment zwischenspeichern
                            comment = revision.find('{http://www.mediawiki.org/xml/export-0.10/}comment')
                            if comment != None:
                                # Wandle Element in String um
                                # Schließt b'<ns0:comment xmlns:ns0="http://www.mediawiki.org/xml/export-0.10/"> in Comment mit ein
                                # Länge: Anfang: 67 Ende: 21
                                comment = ET.tostring(comment)
                                # Entferne <comment> </comment> aus comment
                                comment = comment[67:len(comment)-21]
                                #print('Comment: ' + comment.decode())                
                                # decode() weil Byte Object erwartet wird???
                                comment = comment.decode()
                                #print(comment)
                            else:
                                comment = ''
                                
                            # minor
                            if revision.find('{http://www.mediawiki.org/xml/export-0.10/}minor') != None:
                                minor = revision.find('{http://www.mediawiki.org/xml/export-0.10/}minor')                       
                            else:
                                minor = empty_user_minor
                            # Model
                            if revision.find('{http://www.mediawiki.org/xml/export-0.10/}model') != None:
                                model = revision.find('{http://www.mediawiki.org/xml/export-0.10/}model')
                            else:       
                                model = empty_user_model
                            # Format
                            if revision.find('{http://www.mediawiki.org/xml/export-0.10/}format') != None:
                                wikiformat = revision.find('{http://www.mediawiki.org/xml/export-0.10/}format')
                            else:
                                wikiformat = empty_user_wikiformat
                            # sha1
                            if revision.find('{http://www.mediawiki.org/xml/export-0.10/}sha1') != None:
                                sha1 = revision.find('{http://www.mediawiki.org/xml/export-0.10/}sha1')
                            else: 
                                sha1 = empty_user_sha1                                             
        
                            # Reorganisation:
                            # Gruppiere nach dem was verändert wurde
                            # Achte auf Namespaces
                                
                            # Entferne alle Ziffern aus dem Comment
                            fullcomment = comment
                            comment = re.sub('\d*', "", comment)
                            
                            # Media
                            if ns == -2:
                                nsmediacounter += 1
                                if comment not in nsmediaarray:
                                    nsmediaarray.append(comment)
                                
                            # Special
                            if ns == -1:
                                nsspecialcounter += 1
                                if comment not in nsspecialarray:
                                    nsspecialarray.append(comment)
                            
                            # Wikidata Articles / Items
                            if ns == 0:
                                ns0counter += 1                                          
                                # createredirect
                                # createredirect:0||Q42307522|Q38076224 */
                                # mergeitems
                                # mergeitems-from:0||Q28034308 */ [[MediaWiki:Gadget-Merge.js|merge.js]]
                                # mergeitems-to:0||Q20625022 */
                                # betrifft Q
                                if findx(comment, 'wbcreateredirect', 1) == 3:
                                    as1counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]
                                    if comment not in ns0array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                                # betrifft Q                                    
                                if findx(comment, 'wbmergeitems', 1) == 3:
                                    as1counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]
                                    if comment not in ns0array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break   
                                # betrifft Q oder P
                                if findx(comment, 'wbeditentity-create-item', 1) == 3:
                                    as1counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]
                                    if comment not in ns0array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                            
                                # editentity
                                # editentity-override:0| */ clearing item to prepare for redirect
                                # editentity-update:0| */ BOT - Adding descriptions (5 languages): bn, he, ro, ru, sq
                                # createclaim
                                # createclaim-create:1| */ [[Property:P18]]: Vostanski Stecci.JPG
                                # getclaim
                                # removeclaim
                                # removeclaims-remove:1| */ [[Property:P127]]: [[Q1593113]]
                                # setclaim
                                # setclaim-update:2||1|4 */ [[Property:P19]]: [[Q1053854]]
                                # setclaim-create:2||1 */ [[Property:P106]]: [[Q15296811]]
                                # setclaimvalue
                                # setclaimvalue:1| */ [[Property:P212]]: 978-4-10-459603-4, [[Template:Autofix|autofix]]
                                # removereferences
                                # removereferences-remove:2||1 */ [[Property:P106]]: [[Q10800557]]
                                # setreference
                                # setreference-add:2| */ [[Property:P1015]]: 8038217, #quickstatements; invoked by Mix'n'match:Large catalogs (VIAF)
                                # removequalifiers
                                # removequalifiers-remove:1| */ [[Property:P813]]: 23 October 2017
                                # setqualifier
                                # setqualifier-add:1| */ [[Property:P459]]: [[Q39825]], #quickstatements
                                # setqualifier-update:1| */ [[Property:P768]]: [[Q1008728]]
                                # change rank? add source?  
                                                            
                                 # betrifft Q oder P
                                if findx(comment, 'wbeditentity', 1) == 3:
                                    as1counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]
                                    if comment not in ns0array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                                # betrifft
                                # Betrachte Claims als eigene Klasse?
                                if findx(comment, 'wbcreateclaim', 1) == 3:
                                    as2counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]
                                    if comment not in ns0array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                                # betrifft                                    
                                if findx(comment, 'wbgetclaim', 1) == 3:
                                    as2counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]
                                    if comment not in ns0array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                                # betrifft Q
                                if findx(comment, 'wbremoveclaims', 1) == 3:
                                    as2counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]
                                    if comment not in ns0array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                                # betrifft                                    
                                if findx(comment, 'wbsetclaim', 1) == 3:
                                    as2counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]
                                    if comment not in ns0array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                                # betrifft P
                                if findx(comment, 'wbsetclaimvalue', 1) == 3:
                                    as2counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]
                                    if comment not in ns0array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break                                
                                ###########################################                            
                                # betrifft P
                                if findx(comment, 'wbremovereferences', 1) == 3:
                                    as2counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]
                                    if comment not in ns0array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                                # betrifft P                                  
                                if findx(comment, 'wbsetreference', 1) == 3:
                                    as2counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]
                                    if comment not in ns0array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                                # Qualifier sind auch in Claim Klasse enthalten
                                # betrifft P
                                if findx(comment, 'wbremovequalifiers', 1) == 3:
                                    as2counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]
                                    if comment not in ns0array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                                # betrifft P
                                if findx(comment, 'wbsetqualifier', 1) == 3:
                                    as2counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]
                                    if comment not in ns0array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break                                                           
                                                        
                                # setlabel
                                # setlabel-add:1|en */ Guangxi Province (Republic of China)
                                # setlabel-set:1|en */ E. Wesley Ely
                                # setlabeldescriptionaliases:3|en */ كلب, male adult human, جزمه
                                # setdescription
                                # setdescription-set:1|en */ road in Kyoto prefecture, Japan
                                # setdescription-add:1|en */ building in Madrid
                                # setaliases
                                # setaliases-add:1|en */ DLsite Maniax & Home, bot: import label/alias from [[zh:Refeia]]
                                # betrifft Q
                                if findx(comment, 'wbsetlabel', 1) == 3:
                                    as3counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]
                                    if comment not in ns0array:
                                        ns0array.append(comment),
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    #break
                                # betrifft Q                                    
                                if findx(comment, 'wbsetdescription', 1) == 3:
                                    as3counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]
                                    if comment not in ns0array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    #break
                                # betrifft Q
                                if findx(comment, 'wbsetaliases', 1) == 3:
                                    as3counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]
                                    if comment not in ns0array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    #break
                                                            
                                # setsitelink
                                # setsitelink-set-badges:1|enwiki */ [[Q17437798]]
                                # setsitelink-set:1|enwiki */ Archangel (Gibson comic), Updated: [[en:William Gibson Archangel]] -> [[en:Archangel (Gibson comic)]]
                                # setsitelink-add:1|commonswiki */ Category:Stone sculptures in the United Kingdom
                                # move ?
                                # betrifft
                                if findx(comment, 'wbsetsitelink', 1) == 3:
                                    as4counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]
                                    if comment not in ns0array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                                
                                if findx(comment, 'clientsitelink', 1) == 3:
                                    as4counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]
                                    #print(username.text)
                                    if comment not in ns0array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                                
                            # revert (item or property):
                            # revert 
                            
                                # revert ?
                                # betrifft
                                if findx(comment, 'Reverted edits', 1) == 0:
                                    as8counter += 1
                                    comment = comment[:findx(comment, ' ', 2)]
                                    if comment not in ns0array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                                # /* undo:0||747777873|84.120.158.222 */
                                # User Florentyna - Kein Bot? Ist in keiner der Listen
                                # Revision ID 748141840, 749818411
                                if findx(comment, 'undo', 1) == 3:
                                    as8counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]
                                    if comment not in ns0array:
                                        ns0array.append(comment)   
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                            
                            # protect (item or property):
                            # protect
                            
                                # protect ?
                                # betrifft
                                if findx(comment, 'Protected', 1) == 0: 
                                    as9counter += 1
                                    comment = comment[:findx(comment, ' ', 1)]
                                    if comment not in ns0array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                                
                                
                                # Fange unbekannte Fälle ab,
                                ns0unknowncounter += 1
                                actionnumber = 9999
                                if comment not in ns0unknownarray:
                                    ns0unknownarray.append(comment)   
                                                    
                            # Talk
                            if ns == 1:
                                ns1counter += 1
                                if comment not in ns1array:
                                    ns1array.append(comment) 
                                
                            
                            # User
                            if ns == 2:
                                ns2counter += 1
                                # Sonderfall                        
                                # Wenn Comment Leer ist
                                # Comment wurde initial auf "Leer" gesetzt weil comment = None
                                # Comment existiert nicht? Leere Revision?
                                if comment == '':
                                    # Annahme: Nur Comment ist leer
                                    emptyarray.append([revision_id.text,
                                                   parent_id.text,
                                                   timestamp.text,
                                                   username.text,
                                                   user_id.text,
                                                   comment])
                                else:
                                    if comment not in ns2array:
                                        ns2array.append(comment) 
                                
                            # User Talk
                            if ns == 3:
                                ns3counter += 1
                                if comment not in ns3array:
                                    ns3array.append(comment)                             
                            
                            # Wikidata
                            if ns == 4:
                                ns4counter += 1
                                if comment not in ns4array:
                                    ns4array.append(comment) 
                                
                            # Wikidata Talk
                            if ns == 5:
                                ns5counter += 1
                                if comment not in ns5array:
                                    ns5array.append(comment) 
                                
                            # File
                            if ns == 6:
                                ns6counter += 1
                                if comment not in ns6array:
                                    ns6array.append(comment) 
                            
                            # File Talk
                            if ns == 7:
                                ns7counter += 1
                                if comment not in ns7array:
                                    ns7array.append(comment) 
                                
                            # Mediawiki
                            if ns == 8:
                                ns8counter += 1
                                if comment not in ns8array:
                                    ns8array.append(comment) 
                                
                            # Mediawiki Talk
                            if ns == 9:
                                ns9counter += 1
                                if comment not in ns9array:
                                    ns9array.append(comment) 
                                
                            # Template
                            if ns == 10:
                                ns10counter += 1
                                if comment not in ns10array:
                                    ns10array.append(comment) 
                                
                            # Template Talk
                            if ns == 11:
                                ns11counter += 1
                                if comment not in ns11array:
                                    ns11array.append(comment) 
                                
                            # Help
                            if ns == 12:
                                ns12counter += 1
                                if comment not in ns12array:
                                    ns12array.append(comment) 
    
                            # Help Talk                            
                            if ns == 13:
                                ns13counter += 1
                                if comment not in ns13array:
                                    ns13array.append(comment) 
                                                            
                            # Category    
                            if ns == 14:
                                ns14counter += 1
                                if comment not in ns14array:
                                    ns14array.append(comment) 
                                
                            # Category Talk                            
                            if ns == 15:
                                ns15counter += 1
                                if comment not in ns15array:
                                    ns15array.append(comment)                                    
                                
                            # Property
                            if ns == 120:
                                ns120counter += 1
                                print('120 ', ns120counter)
                                print('120 ', revision_id.text)
                                print('120 ', comment)                            
                                 # betrifft P
                                if findx(comment, 'wbremovequalifiers', 1) == 3:
                                    as5counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]+'120'
                                    if comment not in ns120array:
                                        ns120array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                                # betrifft P
                                if findx(comment, 'wbsetqualifier', 1) == 3:
                                    as5counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]+'120'     
                                    if comment not in ns120array:
                                        ns120array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                                 # betrifft P
                                if findx(comment, 'wbremoveclaims', 1) == 3:
                                    as5counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]+'120'     
                                    if comment not in ns120array:
                                        ns120array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                                 # betrifft P
                                if findx(comment, 'wbsetclaimvalue', 1) == 3:
                                    as5counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]+'120'     
                                    if comment not in ns120array:
                                        ns120array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                                                            
                                #########
                                
                                # betrifft P
                                if findx(comment, 'wbsetlabel', 1) == 3:
                                    as6counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]+'120'  
                                    print(revision_id.text)
                                    print(comment)
                                    print(username.text)
                                    if comment not in ns120array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                                # betrifft P                                    
                                if findx(comment, 'wbsetdescription', 1) == 3:
                                    as6counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]+'120' 
                                    print(revision_id.text)
                                    print(comment)
                                    print(username.text)
                                    if comment not in ns120array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                                # betrifft P
                                if findx(comment, 'wbsetaliases', 1) == 3:
                                    as6counter += 1
                                    comment = comment[findx(comment, ' ' , 1)+1:findx(comment, ':', 1)]+'120'  
                                    print(revision_id.text)
                                    print(comment)
                                    print(username.text)
                                    if comment not in ns120array:
                                        ns0array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                                
                                # Fange unbekannte Fälle ab,
                                ns120unknowncounter += 1
                                actionnumber = 9999
                                if comment not in ns120unknownarray:
                                    ns120unknownarray.append(comment) 
                                          
                            # Property Talk
                            if ns == 121:
                                as7counter += 1
                                ns121counter += 1                                
                                # betrifft P
                                if findx(comment, 'Wikidata list updated', 1) == 0:
                                    if comment not in ns121array:
                                        # Übernimm kompletten Comment
                                        ns121array.append(comment)
                                    # Füge Edit zu Editarray hinzu, wenn noch nicht vorhanden
                                    if comment not in editarray:
                                        editarray.append(comment)
                                    # Füge Bot zusammen mit Edit zu Liste hinzu, wenn noch nicht vorhanden
                                    bot_edit_array.append([username.text,comment])
                                    break
                                
                                # Fange unbekannte Fälle ab,
                                ns121unknowncounter += 1
                                if comment not in ns121unknownarray:
                                    ns121unknownarray.append(comment)                                     
                                
                            # Query
                            if ns == 122:
                                ns122counter += 1
                                if comment not in ns122array:
                                    ns122array.append(comment)
                                
                            # Query Talk
                            if ns == 123:
                                ns123counter += 1
                                ns123array.append(comment)
                                
                            # Module
                            if ns == 828:
                                ns828counter += 1
                                if comment not in ns828array:
                                    ns828array.append(comment)
                                
                            # Module Talk
                            if ns == 829:
                                ns829counter += 1
                                if comment not in ns829array:
                                    ns829array.append(comment)
                                
                            # Translation
                            if ns == 1198:
                                ns1198counter += 1
                                if comment not in ns1198array:
                                    ns1198array.append(comment)
                                
                            # Translation Talk
                            if ns == 1199:
                                ns1199counter += 1
                                if comment not in ns1199array:
                                    ns1199array.append(comment)
                                
                            # Gadget
                            if ns == 2300:
                                ns2300counter += 1
                                if comment not in ns2300array:
                                    ns2300array.append(comment)
                                
                            # Gadget talk
                            if ns == 2301:
                                ns2301counter += 1
                                if comment not in ns2301array:
                                    ns2301array.append(comment)
                                
                            # Gadget definition
                            if ns == 2302:
                                ns2302counter += 1
                                if comment not in ns2302array:
                                    ns2302array.append(comment)
                                
                            # Gadget definition talk
                            if ns == 2303:
                                ns2303counter += 1
                                if comment not in ns2303array:
                                    ns2303array.append(comment)
                            
                            # Topic
                            if ns == 2600:
                                ns2600counter += 1
                                if comment not in ns2600array:
                                    ns2600array.append(comment)
                                    
                            revisiondaten = ([title.rstrip(),
                                              ns,
                                              page_id.rstrip(),
                                              redirect.text,
                                              restrictions.text,
                                              discussion.text,
                                              revision_id.text.rstrip(),                                                                  
                                              parent_id.text.rstrip(),
                                              timestamp.text.rstrip(),
                                              username.text.rstrip(),
                                              user_id.text.rstrip(),     
                                              minor.text,
                                              fullcomment,  # Kompletter Comment
                                              comment,      # Action
                                              model.text,
                                              wikiformat.text,
                                              sha1.text])
                            # Schreibe DB Daten für jede Revision
                            writerdb.writerow(revisiondaten)                                     
                                    
    # Wieviele Bots haben einen bestimmten Edit durchgeführt
    for edit in editarray:
        counter = 0
        for bot in bot_edit_array:
            if edit == bot[1]:
                counter += 1
        edit_count_array.append([edit,counter])
                                                                                                                
    # Berechne Features:    
    # 1 - created items                                            
    # 2 - item terms
    # 3 - item statements
    # 4 - set sitelinks
    # 5 - created properties
    # 6 - property terms
    # 7 - property talk
    # 8 - protected pages and reverts
    
    # Für jeden Bot
    for bot in botarray:
        # Zähle Edits in allen Actionsets für diesen einen Bot
        as1 = 0
        as2 = 0
        as3 = 0
        as4 = 0
        as5 = 0
        as6 = 0
        as7 = 0
        as8 = 0
        # Welche Edits hat er durchgeführt?
        for edit in bot_edit_array:
            # Wenn Bot gefunden
            if bot == edit[0]:
                # Prüfe alle Actionsets, setze Counter
                if edit[1] in actionset1:
                    as1 += 1
                if edit[1] in actionset2:
                    as2 += 1
                if edit[1] in actionset3:
                    as3 += 1                    
                if edit[1] in actionset4:
                    as4 += 1
                if edit[1] in actionset5:
                    as5 += 1
                if edit[1] in actionset6:
                    as6 += 1
                if edit[1] in actionset7:
                    as7 += 1
                if edit[1] in actionset8:
                    as8 += 1                                            
    
        #Create CSV here! 
                       
        # Nachdem Daten für 1 Bot berechnet wurden:        
        # Fülle CSV Daten für den aktuellen Edit
        daten = ([bot,
                  as1,
                  as2,
                  as3,
                  as4,
                  as5,
                  as6,
                  as7,                            
                  as8])
        
        # Normalisiere Daten
        # Teile Wert durch Anzahl aller Actions im Actionset
        if as1counter != 0:
            norm1 = as1/as1counter
        else:
            norm1 = 0
        if as2counter != 0:
            norm2 = as2/as2counter
        else:
            norm2 = 0
        if as3counter != 0:
            norm3 = as3/as3counter
        else: 
            norm3 = 0
        if as4counter != 0:
            norm4 = as4/as4counter
        else:
            norm4 = 0
        if as5counter != 0:
            norm5 = as5/as5counter
        else:
            norm5 = 0
        if as6counter != 0:
            norm6 = as6/as6counter
        else:
            norm6 = 0
        if as7counter != 0:
            norm7 = as7/as7counter
        else:
            norm7 = 0
        if as8counter != 0:
            norm8 = as8/as8counter
        else:
            norm8 = 0
        
        # Schreibe normalisierte Daten
        norm = ([bot,
                 norm1,
                 norm2,
                 norm3,
                 norm4,
                 norm5,
                 norm6,
                 norm7,
                 norm8])        
        
        # Schreibe Daten 
        # Wenn Summe aller Actionsets = 0: Action war in einem anderen Namespace
        # Wenn Summe != 0: Schreibe Daten
        if as1+as2+as3+as4+as5+as6+as7+as7 != 0:
            writer2018.writerow(daten) 
             
                                  
        
    print('Edits: ', editcounter)
    print('Botedits: ', boteditcounter)
    print('Distinct Edits: ', len(editarray))
    percent = round(((boteditcounter/editcounter)*100),2)
    print(percent, '%')
    

    
#    # Anzahl der Edits in jedem Actionset
#    print('AS1: ', as1counter)
#    print('AS2: ', as2counter)
#    print('AS3: ', as3counter)
#    print('AS4: ', as4counter)
#    print('AS5: ', as5counter)
#    print('AS6: ', as6counter)
#    print('AS7: ', as7counter)
#    print('AS8: ', as8counter)
#    #print('AS9: ', as9counter)
#    
#    #print('-2: ', nsmediacounter)
#    #print('-1: ', nsspecialcounter)
#    print('NS0: ', ns0counter)
#    print('1: ', ns1counter)
#    print('2: ', ns2counter)
#    print('3: ', ns3counter)
#    print('4: ', ns4counter)
#    print('5: ', ns5counter)
#    #print('6: ', ns6counter)
#    #print('7: ', ns7counter)
#    print('8: ', ns8counter)
#    print('9: ', ns9counter)
#    print('10: ', ns10counter)
#    print('11: ', ns11counter)
#    print('12: ', ns12counter)
#    print('13: ', ns13counter)
#    print('14: ', ns14counter)
#    print('15: ', ns15counter)
#    print('NS120: ', ns120counter)
#    print('NS121: ', ns121counter)
#    #print('122: ', ns122counter)
#    #print('123: ', ns123counter)
#    #print('828: ', ns828counter)
#    #print('829: ', ns829counter)
#    print('1198: ', ns1198counter)
#    #print('1199: ', ns1199counter)
#    #print('2300: ', ns2300counter)
#    #print('2301: ', ns2301counter)
#    #print('2302: ', ns2302counter)
#    #print('2303: ', ns2303counter)
#    print('2600: ', ns2600counter)
#    #print("Great Success!")  
    
#create('F:\Wikidata\Stubs\wikidatawiki-20180906-stubs-meta-hist-incr.xml') 
create('F:\Wikidata\Stubs\wikidatawiki-20180907-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20180908-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20180909-stubs-meta-hist-incr.xml') 
create('F:\Wikidata\Stubs\wikidatawiki-20180910-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20180911-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20180912-stubs-meta-hist-incr.xml') 
create('F:\Wikidata\Stubs\wikidatawiki-20180913-stubs-meta-hist-incr.xml') 
create('F:\Wikidata\Stubs\wikidatawiki-20180914-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20180915-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20180916-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20180917-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20180918-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20180919-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20180920-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20180921-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20180922-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20180923-stubs-meta-hist-incr.xml') 
create('F:\Wikidata\Stubs\wikidatawiki-20180924-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20180925-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20180926-stubs-meta-hist-incr.xml') 
create('F:\Wikidata\Stubs\wikidatawiki-20180927-stubs-meta-hist-incr.xml') 
create('F:\Wikidata\Stubs\wikidatawiki-20180928-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20180929-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20181002-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20181003-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20181004-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20181005-stubs-meta-hist-incr.xml') 
create('F:\Wikidata\Stubs\wikidatawiki-20181006-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20181007-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20181008-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20181009-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20181010-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20181011-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20181012-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20181013-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20181014-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20181015-stubs-meta-hist-incr.xml') 
#create('F:\Wikidata\Stubs\wikidatawiki-20181017-stubs-meta-hist-incr.xml') 


