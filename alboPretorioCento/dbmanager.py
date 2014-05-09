#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

 
import tweepy, time, sys
import re

from twitterauth import *

ALBO_PRETORIO_URL="http://goo.gl/eojHcl"

KEEP_LAST_N=1000
 
 
def postTweet(statusline):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    api.update_status(statusline)
    time.sleep(2)
 
class dbInsertNuovi():
    def __init__(self,name='alboPretorio'):
        self.db = sqlite3.connect(name+'.sqlite3')
        self.cur = self.db.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS alboPretorio (
                      id_registro_anno NUMERIC NOT NULL,
                      id_registro_num NUMERIC NOT NULL,
                      oggetto TEXT NOT NULL,
                      data_inizio_pub TEXT NOT NULL,
                      data_fine_pub   TEXT NOT NULL,
                      tipo_documento  TEXT NOT NULL,
                      documenti       TEXT NOT NULL,
                      PRIMARY KEY (id_registro_anno, id_registro_num)
                      );''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS alboPretorio_daAggiungere (
                      id_registro_anno NUMERIC NOT NULL,
                      id_registro_num NUMERIC NOT NULL,
                      oggetto TEXT NOT NULL,
                      data_inizio_pub TEXT NOT NULL,
                      data_fine_pub   TEXT NOT NULL,
                      tipo_documento  TEXT NOT NULL,
                      documenti       TEXT NOT NULL,
                      PRIMARY KEY (id_registro_anno, id_registro_num)
                      );''')

        self.db.commit()

    def __del__(self):
        self.db.close()
            

    def add_item(self,item):
        res = self.cur.execute('SELECT count(*) FROM alboPretorio WHERE id_registro_anno = ? AND id_registro_num = ?', (item['id_registro_anno'],item['id_registro_num']))
        count = res.fetchone()[0]
        if count == 0:
                res = self.cur.execute('SELECT count(*) FROM alboPretorio_daAggiungere WHERE id_registro_anno = ? AND id_registro_num = ?', (item['id_registro_anno'],item['id_registro_num']))
                count = res.fetchone()[0]
                if count == 0:
                    self.cur.execute ('''INSERT INTO alboPretorio_daAggiungere(
                                         id_registro_anno,
                                         id_registro_num,
                                         oggetto,
                                         data_inizio_pub,
                                         data_fine_pub,
                                         tipo_documento,
                                         documenti)
                                         VALUES (?,
                                         ?,
                                         ?,
                                         ?,
                                         ?,
                                         ?,
                                         ?)
                                         ''', (
                                             item['id_registro_anno'],
                                             item['id_registro_num'],
                                             item['oggetto'],
                                             item['data_inizio_pub'],
                                             item['data_fine_pub'],
                                             item['tipo_documento'],
                                             item['documenti']))
                    self.db.commit()
                    

class dbElaboraNuovi():
    def __init__(self,name='alboPretorio'):
        self.db = sqlite3.connect(name+'.sqlite3')
        self.cur = self.db.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS alboPretorio (
                      id_registro_anno NUMERIC NOT NULL,
                      id_registro_num NUMERIC NOT NULL,
                      oggetto TEXT NOT NULL,
                      data_inizio_pub TEXT NOT NULL,
                      data_fine_pub   TEXT NOT NULL,
                      tipo_documento  TEXT NOT NULL,
                      documenti       TEXT NOT NULL,
                      PRIMARY KEY (id_registro_anno, id_registro_num)
                      );''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS alboPretorio_daAggiungere (
                      id_registro_anno NUMERIC NOT NULL,
                      id_registro_num NUMERIC NOT NULL,
                      oggetto TEXT NOT NULL,
                      data_inizio_pub TEXT NOT NULL,
                      data_fine_pub   TEXT NOT NULL,
                      tipo_documento  TEXT NOT NULL,
                      documenti       TEXT NOT NULL,
                      PRIMARY KEY (id_registro_anno, id_registro_num)
                      );''')

        self.db.commit()

    def abbrevia_oggetto(self, oggetto):
        oggetto = re.sub(r'\bprocedura\b','proced', oggetto)
        oggetto = re.sub(r'\bpubblicazion(e|i)\b','pubbl', oggetto)
        oggetto = re.sub(r'\bservizio?\b','serv', oggetto)
        oggetto = re.sub(r'\bprofessional(e|i)\b','prof', oggetto)
        oggetto = re.sub(r'\bdisposizion(e|i)\b','disp', oggetto)
        oggetto = re.sub(r'\bapprovazione\b','approv', oggetto)
        oggetto = re.sub(r'\bordinanz(a|e)\b','ordin', oggetto)
        oggetto = re.sub(r'\bnumer(o|i)\b','num', oggetto)
        oggetto = re.sub(r'\bpretorio\b','pret', oggetto)
        oggetto = re.sub(r'\bcivic(o|i)\b','civ', oggetto)
        oggetto = re.sub(r'\bcontribut(o|i)\b','contrib', oggetto)
        oggetto = re.sub(r'\bcollaborazion(e|i)\b','collab', oggetto)
        oggetto = re.sub(r'\bdiviet(o|i)\b','div', oggetto)
        oggetto = re.sub(r'\bregolament(o|i)\b','regolam', oggetto)
        oggetto = re.sub(r'\bprovincia\b','prov', oggetto)
        oggetto = re.sub(r'\bcomune\b','com', oggetto)
        oggetto = re.sub(r'\bautorizzazion(e|i)\b','aut', oggetto)
        oggetto = re.sub(r'\bpersonal(e|i)\b','pers', oggetto)
        oggetto = re.sub(r'\bdeposit(o|i)\b','depos', oggetto)
        return oggetto

    def elabora(self):
        curWrite = self.db.cursor()
        res = self.cur.execute('SELECT id_registro_num, id_registro_anno,oggetto,data_inizio_pub,data_fine_pub,tipo_documento,documenti FROM alboPretorio_daAggiungere ORDER BY id_registro_anno, id_registro_num')
        rows=self.cur.fetchall()
        for row in rows:
            (id_registro_num, id_registro_anno,oggetto,data_inizio_pub,data_fine_pub,tipo_documento,documenti) = row
            oggetto_abbr = oggetto.lower()
            oggetto_abbr = self.abbrevia_oggetto(oggetto_abbr)
            statusline = '[%d/%d]%s' % (id_registro_num, id_registro_anno,oggetto_abbr)
            statusline = statusline[:115]+'..' if len(statusline) > 115 else statusline
            statusline += " " + ALBO_PRETORIO_URL
            try:
                curWrite.execute ('''INSERT INTO alboPretorio(
                                     id_registro_anno,
                                     id_registro_num,
                                     oggetto,
                                     data_inizio_pub,
                                     data_fine_pub,
                                     tipo_documento,
                                     documenti)
                                     VALUES (?,
                                     ?,
                                     ?,
                                     ?,
                                     ?,
                                     ?,
                                     ?)
                                     ''', (
                                         id_registro_anno,
                                         id_registro_num,
                                         oggetto,
                                         data_inizio_pub,
                                         data_fine_pub,
                                         tipo_documento,
                                         documenti))
                curWrite.execute ('''DELETE FROM alboPretorio_daAggiungere
                                     WHERE id_registro_anno = ? AND id_registro_num = ?
                                 ''', (
                                     id_registro_anno,
                                     id_registro_num
                                     )
                                 )

                print "Tweeting %s" % (statusline,)
                postTweet(statusline)

                self.db.commit()
            except Exception,e: 
                print "ERROR TWEETING (%s)",e
                self.db.rollback()

        res = self.cur.execute('''WITH toKeep AS (
                                              SELECT id_registro_anno, id_registro_num
                                              FROM alboPretorio
                                              ORDER BY id_registro_anno DESC, id_registro_num DESC
                                              LIMIT ?)
                                              DELETE FROM alboPretorio 
                                              WHERE NOT EXISTS (SELECT * FROM toKeep tk 
                                                                WHERE tk.id_registro_anno = alboPretorio.id_registro_anno 
                                                                AND tk.id_registro_num = alboPretorio.id_registro_num)
                                ''', (KEEP_LAST_N,))

    def __del__(self):
        self.db.close()

