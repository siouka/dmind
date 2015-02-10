#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2014 Techdealer
#
###############################################################
# Guideline para uma mais fácil manutenção/updates:
###############################################################
# 1-98: Menus
#--------------------------------------------------------------
# 99: Função Play
#--------------------------------------------------------------
# 100-199: Url Resolvers diversos
#     100 : Resolver sapovideos
#     101 : Resolver vk.com (Nota: actualmente não está em uso)
#--------------------------------------------------------------
# 200-299: Funções para listar conteúdos de serviços de video
#     200: Listar Youtube Playlist
#              Prototype: 
#              addDir('Programa (Fonte: User channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'id_da_playlist')
#     201: Search InChannel Youtube
#              Prototype:
#              addDir('Programa (Fonte: User channel)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Nome Programa"',channel_id = 'id_do_canal')
#     202-203: Listar 2 Youtube Playlists
#              Prototype:
#              addDir('Programa (Fonte: User channel)','1',202,addonfolder+artfolder+'foldericon.png',playlist1_id = 'id_da_playlist_1',playlist2_id = 'id_da_playlist_2')
#     204: Listar Dailymotion Playlist
#              Prototype:
#              addDir('Programa (Fonte: User Dailymotion)','1',204,addonfolder+artfolder+'foldericon.png',playlist_id = 'id_da_playlist')
#     205: Search InChannel Dailymotion
#              Prototype:
#              addDir('Programa (Fonte: User Dailymotion)','1',205,addonfolder+artfolder+'foldericon.png',search_query = 'Nome Programa',channel_id = 'id_do_canal')
#     206: Listar SapoVideos Playlist
#              Prototype:
#              addDir('Programa (Fonte: User sapo)','1',206,addonfolder+artfolder+'foldericon.png',playlist_id = 'id_da_playlist',channel_id = 'greensavers')
#     207: Search InChannel SapoVideos
#              Prototype:
#              addDir('Programa (Fonte: User sapo)','1',207,addonfolder+artfolder+'foldericon.png',search_query = 'Nome Programa',channel_id = 'id_do_canal')
#     208: Listar Podcast
#              Prototype:
#              addDir('Programa (Podcast)','1',208,addonfolder+artfolder+'foldericon.png',playlist_id = 'url_do_podcast')
#--------------------------------------------------------------
# 400 em diante: Funções para obter conteúdos de sites
###############################################################

##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,htmlentitydefs,HTMLParser
import json
import g1novelas
import maisnovelas
import novelasgravadas
import assistirnovelas
import vernovelas
import documentariosvarios
import todosdocumentarios
import filmesportugueses
import docverdade
import webdocumentarios
import curtadoc
import podflix

h = HTMLParser.HTMLParser()

addon_id = 'plugin.video.replaypt'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'

################################################## 

#MENUS############################################

def PAIS():
	if selfAddon.getSetting('startup') == "0":
		addDir('Portugal','',1,addonfolder+artfolder+'portugal.jpg')
		addDir('Brasil','',12,addonfolder+artfolder+'brasil.jpg')
	elif selfAddon.getSetting('startup') == "1":
		PORTUGAL()
	elif selfAddon.getSetting('startup') == "2":
		BRASIL()

def PORTUGAL():
	addDir('RTP','',2,addonfolder+artfolder+'rtp.jpg')
	addDir('Arquivo SIC','',3,addonfolder+artfolder+'sic.jpg')
	addDir('Novelas SIC','',4,addonfolder+artfolder+'sic.jpg')
	addDir('Séries SIC','',5,addonfolder+artfolder+'sic.jpg')
	addDir('Novelas TVI','',6,addonfolder+artfolder+'tvi.jpg')
	addDir('Séries TVI','',7,addonfolder+artfolder+'tvi.jpg')
	addDir('Rádio e Podcasts','',8,addonfolder+artfolder+'radio.jpg')
	addDir('Outros','',11,addonfolder+artfolder+'outros.jpg')
	
def RTP():
	addDir('A Mãe do Sr. Ministro (Fonte: FNunes94 channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLRrd7-_JAWxib0cK6OhU795bAPLfAbJWE')
	addDir('A Minha Sogra é uma Bruxa (Fonte: FNunes94 channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLRrd7-_JAWxil2LD6_XKczC3wtjGMkQHG')
	addDir('Hotel 5 Estrelas (Fonte: FNunes94 channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLRrd7-_JAWxhoC7kgwA5xFa_SNDPvg4yr')
	addDir('Os Compadres 2 (Fonte: FNunes94 channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLRrd7-_JAWxj9p1wHxGEfDEydnghb9NfY')
	addDir('Telerural (Fonte: dioved channel)','1',202,addonfolder+artfolder+'foldericon.png',playlist1_id = 'PL0CF2E74C735A0102',playlist2_id = 'PLE8A681D23E2D2219')
	
def ARQ_SIC():
	addDir('SIC','?arquivo_modo=1&canal=sic&playview=0&pagina=0',400,addonfolder+artfolder+'foldericon.png')
	addDir('SIC Notícias','?arquivo_modo=1&canal=sicnoticias&playview=0&pagina=0',400,addonfolder+artfolder+'foldericon.png')
	addDir('SIC Radical','?arquivo_modo=1&canal=sicradical&playview=0&pagina=0',400,addonfolder+artfolder+'foldericon.png')
	addDir('SIC Mulher','?arquivo_modo=1&canal=sicmulher&playview=0&pagina=0',400,addonfolder+artfolder+'foldericon.png')
	addDir('SIC K','?arquivo_modo=1&canal=sickapa&playview=0&pagina=0',400,addonfolder+artfolder+'foldericon.png')
	addDir('SIC Internacional','?arquivo_modo=1&canal=sicinternaciona&playview=0&pagina=0',400,addonfolder+artfolder+'foldericon.png')

def NOV_SIC():
	addDir('A Guerreira (Fonte: Daniel Portela DM)','1',204,addonfolder+artfolder+'foldericon.png',playlist_id = 'x33eca')
	addDir('Amor à Vida (Fonte: Daniel Portela DM)','1',204,addonfolder+artfolder+'foldericon.png',playlist_id = 'x33z3h')
	addDir('Dancin Days (Fonte: tugarec)','1',204,addonfolder+artfolder+'foldericon.png',playlist_id = 'x2j54h')
	addDir('Em Familia (Fonte: Daniel Portela DM)','1',204,addonfolder+artfolder+'foldericon.png',playlist_id = 'x34j50')
	addDir('Gabriela (Fonte: tugarec)','1',204,addonfolder+artfolder+'foldericon.png',playlist_id = 'x2ajvv')
	addDir('Gabriela (Fonte: Daniel Portela DM)','1',204,addonfolder+artfolder+'foldericon.png',playlist_id = 'x345tv')
	addDir('Lua Vermelha (Fonte: LuaVermelhaSIC channel)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Lua Vermelha"',channel_id = 'LuaVermelhaSIC')
	addDir('Os aliados (Fonte: Daniel Portela DM)','1',204,addonfolder+artfolder+'foldericon.png',playlist_id = 'x33ecj')
	addDir('Sangue Bom (Fonte: Daniel Portela DM)','1',204,addonfolder+artfolder+'foldericon.png',playlist_id = 'x33qzy')
	addDir('Senhora do Destinho (Fonte: Daniel Portela DM)','1',204,addonfolder+artfolder+'foldericon.png',playlist_id = 'x34j5b')
	addDir('Sol De Inverno (Fonte: Daniel Portela DM)','1',204,addonfolder+artfolder+'foldericon.png',playlist_id = 'x33z2z')
	
def SER_SIC():
	addDir('A familia mata (Fonte: Portugal TV channel)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"A Família Mata"',channel_id = 'maradochanfrado')
	addDir('A Minha Família é Uma Animação - Série 1 (Fonte: filmesgratisonline)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"A Minha Família é Uma Animação"',channel_id = 'filmesgratisonline')
	addDir('Aqui Não Há Quem Viva (Fonte: FNunes94 channel)','1',202,addonfolder+artfolder+'foldericon.png',playlist1_id = 'PLRrd7-_JAWxgVB4LRLUC008XG9X1V4W04',playlist2_id = 'PLRrd7-_JAWxixcprtZy8NGnYEY8FfBTNg')
	addDir('As aventuras de Camilo (Fonte: FNunes94 channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLRrd7-_JAWxhGbfZPSpViLm5iZ9ef2xoL')
	addDir('Gosto Disto T6 (Fonte: tugarec)','1',204,addonfolder+artfolder+'foldericon.png',playlist_id = 'x2afs7')
	addDir('Programas diversos (Fonte: Daniel Portela DM)','1',204,addonfolder+artfolder+'foldericon.png',playlist_id = 'x35071')
	addDir('Uma Aventura (Fonte: FNunes94 channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLRrd7-_JAWxgW0MaPY1NCvLSqtMW9PuuT')
	
def NOV_TVI():
	addDir('A Jóia de África (Fonte: mary1sofia channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLFfuPRYEifM2tWTIyT2a7zkD1zfOXoXpN')
	addDir('A Outra (Fonte: TVStory Portugal)','A%20OUTRA',401,addonfolder+artfolder+'foldericon.png')
	addDir('Anjo Selvagem (Fonte: tvificcao channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLLJ97C61sSs8Vouf2jI4WSRcrP3slQLfy')
	addDir('Anjo Meu (Fonte: espirit0indomavel channel)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Anjo Meu"',channel_id = 'espirit0indomavel')
	addDir('Belmonte (Fonte: TVStory Portugal)','1',402,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Belmonte"',channel_id = 'BELMONTE')
	addDir('Belmonte (Fonte: SerenaSM channel)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Belmonte"',channel_id = 'SerenaSM')
	addDir('Destinos Cruzados (Fonte: FNunes94 channel)','1',202,addonfolder+artfolder+'foldericon.png',playlist1_id = 'PLRrd7-_JAWxj02DZC6JaCzAHGgCThXvgF',playlist2_id = 'PLRrd7-_JAWxi5xn4mRMEWpFOts311U6vd')
	addDir('Destinos Cruzados (Fonte: TVStory Portugal)','',402,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Destinos Cruzados"',channel_id = 'DESTINOS%20CRUZADOS')
	addDir('Doce Fugitiva (Fonte: FNunes94 channel)','1',202,addonfolder+artfolder+'foldericon.png',playlist1_id = 'PLRrd7-_JAWxj_Kz1V5_otZkPswyQCkejR',playlist2_id = 'PLRrd7-_JAWxg59-0CsRfWmrBIT_sKkpo8')
	addDir('Doce Tentação (Fonte: SerenaSM channel)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Doce Tentação"',channel_id = 'SerenaSM')
	addDir('Doida por ti (Fonte: FNunes94 channel)','1',202,addonfolder+artfolder+'foldericon.png',playlist1_id = 'PLRrd7-_JAWxi8cBzEW10K6sAwax045IQF',playlist2_id = 'PLRrd7-_JAWxgoziN6K2WbKhwcEUN4oggQ')
	addDir('Doida por ti (Fonte: TVStory Portugal)','DOIDA%20POR%20TI',401,addonfolder+artfolder+'foldericon.png')
	addDir('Ele é Ela (Fonte: FNunes94 channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLRrd7-_JAWxiqDHFHG_kRcsHMxa4eLW0c')
	addDir('Equador (Fonte: FNunes94 channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLRrd7-_JAWxgb0z8S_VOl_6XGuPZcVzkI')
	addDir('Espírito Indomável (Fonte: espirit0indomavel channel)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Espírito Indomável"',channel_id = 'espirit0indomavel')
	addDir('Espírito Indomável (Fonte: SerenaSM channel)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Espírito Indomável"',channel_id = 'SerenaSM')
	addDir('Feitiço de Amor (Fonte: Novelas Portugal channel)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Feitiço de Amor"',channel_id = 'UCL3dTyP-6b5jR5fBxTT8IJw')
	addDir('I Love It (Fonte: il0veit.com)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"I Love It"',channel_id = 'iloveittvi')
	addDir('I Love It (Fonte: FNunes94 channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLRrd7-_JAWxjD56OXvWnzi1IeNj85llyl')
	addDir('I Love It (Fonte: TVStory Portugal)','',402,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"I Love It"',channel_id = 'I%20LOVE%20IT')
	addDir('I Love It (Fonte: slipanc dailymotion)','1',204,addonfolder+artfolder+'foldericon.png',playlist_id = 'x2y5au')
	addDir('Ilha dos Amores (Fonte: mary1sofia channel)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Ilha dos Amores"',channel_id = 'mary1sofia')
	addDir('Louco Amor (Fonte: canaltvportugal)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Louco Amor Episódio"',channel_id = 'canaltvportugal')
	addDir('Louco Amor (Fonte: tugarec)','1',204,addonfolder+artfolder+'foldericon.png',playlist_id = 'x2j54i')
	addDir('Mar de Paixão (Fonte: mardepaixaotvi channel)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Mar de Paixão"',channel_id = 'mardepaixaotvi')
	addDir('Mistura Fina (Fonte: Portugal TV channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLEPrnBzo5vK3z-Omf_SovaZgcFusoYBFJ')
	addDir('Morangos com Açucar 1 (Fonte: VerMorangosOnline)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Morangos com Açúcar 1"',channel_id = 'vermorangosonline')
	addDir('Morangos com Açucar 1 (Fonte: FNunes94 channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLRrd7-_JAWxgnx99ye8SzjpyAZf8TODUu')
	addDir('Morangos com Açucar 2 (Fonte: morangosonline Dailymotion)','1',204,addonfolder+artfolder+'foldericon.png',playlist_id = 'x36p74')
	addDir('Morangos com Açucar 3 (Fonte: il0veit.com)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Morangos Com Açúcar 3"',channel_id = 'iloveittvi')
	addDir('Morangos com Açucar 7 (Fonte: thedanielasofia12)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Morangos Com Açucar 7"',channel_id = 'thedanielasofia12')
	addDir('Morangos com Açucar 8 (Fonte: MissSaruska)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Morangos com Açúcar 8"',channel_id = 'MissSaruska')
	addDir('Morangos com Açucar 9 (Fonte: VerMorangosOnline)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Morangos com Açúcar 9"',channel_id = 'vermorangosonline')
	addDir('Mulheres (Fonte: TVStory Portugal)','MULHERES',401,addonfolder+artfolder+'foldericon.png')
	addDir('Mulheres (Fonte: Love channel)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Mulheres"',channel_id = 'UCZiiYd0nBgGjazT_TLwMmFw')
	addDir('Mundo ao Contrário (Fonte: tugarec)','1',204,addonfolder+artfolder+'foldericon.png',playlist_id = 'x2l6lj')
	addDir('O Beijo do Escorpião (Fonte: TVStory Portugal)','O%20BEIJO%20DO%20ESCORPI%C3%83O',401,addonfolder+artfolder+'foldericon.png')
	addDir('O Teu Olhar (Fonte: mary1sofia channel)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"O Teu Olhar"',channel_id = 'mary1sofia')
	addDir('Sedução (Fonte: minicash channel)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Telenovela SEDUÇÃO"',channel_id = 'minicashsantaclara')
	addDir('Sentimentos (Fonte: SerenaSM channel)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Sentimentos"',channel_id = 'SerenaSM')
	addDir('Super Pai (Fonte: FNunes94 channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLRrd7-_JAWxgdXgysXlb8EG51jpPrGBqV')
	addDir('Super Pai (Fonte: tvificcao channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLLJ97C61sSs-PZYCSmhBPYIkQMWDHGfkP')
	addDir('Tempo de Viver (Fonte: FNunes94 channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLRrd7-_JAWxhGnmtJSZBjz4SDIN26OtKO')
	addDir('Último Beijo (Fonte: formyworld dailymotion)','1',205,addonfolder+artfolder+'foldericon.png',search_query = 'O Último Beijo',channel_id = 'formyworld')
	
def SER_TVI():
	addDir('A Tua Cara Não Me É Estranha: Kids (tvivirtual channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLeoLzoRQPDKgw7UKcnEDIMAM58ZE2a2dI')
	addDir('Bando dos 4 (Fonte: FNunes94 channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLRrd7-_JAWxjN0xtc5ZqNFnFovLfyaJAP')
	addDir('Casos da Vida (Fonte: FNunes94 channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLRrd7-_JAWxhdI5WOhD-CgyNhLVoly_Y5')
	addDir('Giras e Falidas (Fonte: TVStory Portugal)','GIRAS%20E%20FALIDAS',401,addonfolder+artfolder+'foldericon.png')
	addDir('Inspector Max (Fonte: FNunes94 channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLRrd7-_JAWxhkpHq_1lC8X9J73m9izG-D')
	addDir('Inspector Max (Fonte: beto4384 channel)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Inspector Max"',channel_id = 'beto4384')
	addDir('Melhor do que falecer (Fonte: tvi.iol.pt)','1',436,addonfolder+artfolder+'foldericon.png')
	addDir('O Bairro (Fonte: FNunes94 channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLRrd7-_JAWxg_ShOulIV2UNhbhVGeU91z')
	addDir('O Bairro (Fonte: TVStory Portugal)','O%20BAIRRO',401,addonfolder+artfolder+'foldericon.png')
	addDir('Os batanetes (Fonte: cabe917357295 channel)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"batanetes"',channel_id = 'cabe917357295')
	addDir('Série 37 (Fonte: FNunes94 channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLRrd7-_JAWxjywWYnOIe31L7gGCNWhKHG')
	addDir('Série 37 (Fonte: mary1sofia channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLFfuPRYEifM36WCQcQRL48tlxbu4OXrlP')

def RADIO_PT():
	addDir('[B]M80 Podcasts[/B]','',10,addonfolder+artfolder+'m80.jpg')
	addDir('[B]Rádio Comercial Podcasts[/B]','',9,addonfolder+artfolder+'comercial.jpg')
	addDir('[B]Rádio Renascença Podcasts[/B]','',442,addonfolder+artfolder+'renascenca.jpg')
	addDir('[B]RTP Podcasts[/B]','',443,addonfolder+artfolder+'rtp.jpg')
	addDir('[B]TSF Podcasts[/B]','',441,addonfolder+artfolder+'tsf.jpg')
	addDir('A Hora do Manzarra - Cidade FM (Podcast)','1',208,addonfolder+artfolder+'foldericon.png',playlist_id = 'http://feeds.feedburner.com/ahoradomanzarra')
	addDir('Café da Manhã (Rfm channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLJgZw8Ck8x_yCc5fnWnq2kmRCq9u02CDt')
	addDir('Mixórdia de Temáticas: Série Miranda (Rádio Comercial channel)','1',201,addonfolder+artfolder+'foldericon.png',search_query = '"Série Miranda"',channel_id = 'Radiocomercial')
	addDir('Mixórdia de Temáticas: Série Ribeiro (Rádio Comercial channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLZfnSUmb9pEf9VXLDf4CSSkJMAyJWT-yx')
	addDir('Nilton no Café - Rfm (Podcast)','1',208,addonfolder+artfolder+'foldericon.png',playlist_id = 'http://rfm.sapo.pt/podcast_itunes.aspx')
	addDir('O Homem que Mordeu o Cão (Rádio Comercial channel)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"O Homem Que Mordeu o Cão"',channel_id = 'Radiocomercial')
	addDir('Pastilhas para a tosse - Rfm (Podcast)','1',208,addonfolder+artfolder+'foldericon.png',playlist_id = 'http://rfm.sapo.pt/podcast_itunes_cafe.aspx')
	addDir('Showcase PT - Zwame (Podcast)','1',208,addonfolder+artfolder+'foldericon.png',playlist_id = 'http://podcast.zwame.pt/category/podcast/showcasept/feed/')
	addDir('ZWAME Foto - Zwame (Podcast)','1',208,addonfolder+artfolder+'foldericon.png',playlist_id = 'http://podcast.zwame.pt/category/podcast/zwamefoto/feed/')
	addDir('ZWAMEcast - Zwame (Podcast)','1',208,addonfolder+artfolder+'foldericon.png',playlist_id = 'http://podcast.zwame.pt/category/podcast/zwamecast/feed/')

def COMERCIAL():
	addDir('Mixórdia de Temáticas (Podcast)','1',208,'http://i.imgur.com/DGz7Cw4.jpg',playlist_id = 'http://feeds.feedburner.com/mixordiadetematicas')
	addDir('Caderneta de Cromos (Podcast)','1',208,'http://i.imgur.com/YIqketX.jpg',playlist_id = 'http://feeds.feedburner.com/rc-cadernetadecromos')
	addDir('PRIMO - Programa Realmente Incrível Mas Obtuso (Podcast)','1',208,'http://i.imgur.com/QgZFcqb.jpg',playlist_id = 'http://feeds.feedburner.com/rc-primo-programarealmenteincrvelmasobtuso')
	addDir('Momento da Manhã (Podcast)','1',208,'http://i.imgur.com/zFp6WPK.jpg',playlist_id = 'http://feeds.feedburner.com/rc-momentodamanha')
	addDir('Manhãs da Comercial (Podcast)','1',208,'http://i.imgur.com/Z9hnuzC.jpg',playlist_id = 'http://feeds.feedburner.com/rc-programadamanha')
	addDir('Rais Parta o Amor (Podcast)','1',208,'http://i.imgur.com/CEztkrW.jpg',playlist_id = 'http://radiocomercial.clix.pt/rss/raispartaoamor.xml')
	addDir('Barulho das Luzes (Podcast)','1',208,'http://i.imgur.com/ybCPR0W.jpg',playlist_id = 'http://feeds.feedburner.com/rc-entrevistasbarulhodasluzes')

def M80():
	addDir('A Cor do Dinheiro - M80 (Podcast)','1',208,addonfolder+artfolder+'foldericon.png',playlist_id = 'http://feeds.feedburner.com/cordodinheiro')
	addDir('Cromos M80 - M80 (Podcast)','1',208,addonfolder+artfolder+'foldericon.png',playlist_id = 'http://feeds.feedburner.com/cromosM80')
	addDir('Linha de Passe - M80 (Podcast)','1',208,addonfolder+artfolder+'foldericon.png',playlist_id = 'http://feeds.feedburner.com/linha-de-passe')
	addDir('Máquina do Tempo - M80 (Podcast)','1',208,addonfolder+artfolder+'foldericon.png',playlist_id = 'http://feeds.feedburner.com/m80maquinadotempo')
	addDir('Não me Choca - M80 (Podcast)','1',208,addonfolder+artfolder+'foldericon.png',playlist_id = 'http://feeds.feedburner.com/naomechoca')
	
def OUTROS_PT():
	addDir('Como Fazem Isso - Discovery Channel (Fonte: tugarec)','1',204,addonfolder+artfolder+'foldericon.png',playlist_id = 'x2amyn')
	addDir('Economia Verde - Sic Notícias (Fonte: greensavers sapo)','1',207,addonfolder+artfolder+'foldericon.png',search_query = 'Economia Verde',channel_id = 'greensavers')
	addDir('Exame Informática TV - Sic Notícias (Fonte: EI sapo)','1',207,addonfolder+artfolder+'foldericon.png',search_query = 'EITV',channel_id = 'exameinformatica')
	addDir('Filmesportugueses.com - Curtas','',429,addonfolder+artfolder+'foldericon.png')
	addDir('Isto é Matemática - Sic Notícias (Fonte: sigma3web channel)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"Isto é Matemática"',channel_id = 'sigma3web')
	addDir('Mega Construções - Discovery Channel (Fonte: tugarec)','1',204,addonfolder+artfolder+'foldericon.png',playlist_id = 'x2bbtb')
	addDir('Um Minuto Por Sua Casa (Fonte: century21 channel)','1',200,addonfolder+artfolder+'foldericon.png',playlist_id = 'PLVHgBQ1oJPj1dFTaeMi70k6KWeNGk_7kp')
	addDir('ZWAME News (Fonte: ZWAME Channel)','1',201,addonfolder+artfolder+'foldericon.png',search_query = 'allintitle:"ZWAME News"',channel_id = 'ZWAME')
	
def BRASIL():
	addDir('g1novelas.org','',403,addonfolder+artfolder+'g1novelas.png')
	addDir('maisnovelas.net','',407,addonfolder+artfolder+'maisnovelas.png')
	addDir('novelasgravadas.com','',411,addonfolder+artfolder+'novelasgravadas.png')
	addDir('assistirnovelas.tv','',415,addonfolder+artfolder+'assistirnovelas.png')
	addDir('vernovelas.com.br','',418,addonfolder+artfolder+'vernovelas.png')
	addDir('documentariosvarios.wordpress.com','',421,addonfolder+artfolder+'documentariosvarios.png')
	addDir('todosdocumentarios.blogspot.com','',425,addonfolder+artfolder+'todosdocumentarios.png')
	addDir('docverdade.blogspot.com','',432,addonfolder+artfolder+'docverdade.png')
	addDir('webdocumentarios.com','',437,addonfolder+artfolder+'webdocumentarios.png')
	addDir('curtadoc.tv','',445,addonfolder+artfolder+'curtadoc.png')
	addDir('podflix.com.br','',448,addonfolder+artfolder+'podflix.png')

###################################################################################
#FUNÇÕES PARA LISTAR CONTEÚDOS DE SERVIÇOS DE VIDEO

def listar_youtube_playlist(url,mode,playlist_id):
	videos_per_page = 15
	index = 1 + ((int(url)-1)*videos_per_page)
	codigo_fonte = abrir_url('https://gdata.youtube.com/feeds/api/playlists/' + playlist_id + '?max-results=' + str(videos_per_page) + '&start-index=' + str(index) + '&v=2&alt=json')
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['feed']['entry'])):
		name = decoded_data['feed']['entry'][x]['title']['$t'].encode("utf8")
		youtube_id = decoded_data['feed']['entry'][x]['media$group']['yt$videoid']['$t'].encode("utf8")
		addDir(name + ' - (Server: YOUTUBE)','plugin://plugin.video.youtube/?action=play_video&videoid='+youtube_id,99,'http://i1.ytimg.com/vi/'+youtube_id+'/0.jpg',False)
	if index<=500-videos_per_page+1 and index-1+videos_per_page<int(decoded_data['feed']['openSearch$totalResults']['$t']):
			addDir('Próximo >>',str(int(url)+1),mode,'',playlist_id = playlist_id)
			
def listar_search_inchannel_youtube(url,mode,search_query,channel_id):
	videos_per_page = 15
	index = 1 + ((int(url)-1)*videos_per_page)
	codigo_fonte = abrir_url('http://gdata.youtube.com/feeds/api/videos?author=' + channel_id + '&q=' + urllib.quote(search_query) + '&orderby=published&max-results=' + str(videos_per_page) + '&start-index=' + str(index) + '&v=2&alt=json')
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['feed']['entry'])):
		name = decoded_data['feed']['entry'][x]['title']['$t'].encode("utf8")
		youtube_id = decoded_data['feed']['entry'][x]['media$group']['yt$videoid']['$t'].encode("utf8")
		addDir(name + ' - (Server: YOUTUBE)','plugin://plugin.video.youtube/?action=play_video&videoid='+youtube_id,99,'http://i1.ytimg.com/vi/'+youtube_id+'/0.jpg',False)
	if index<=500-videos_per_page+1 and index-1+videos_per_page<int(decoded_data['feed']['openSearch$totalResults']['$t']):
			addDir('Próximo >>',str(int(url)+1),mode,'',search_query = search_query,channel_id = channel_id)
		
def listar_2_youtube_playlists(url,mode,playlist1_id,playlist2_id):
	videos_per_page = 15
	checker = 1
	if numero_par(mode) == True:
		index = 1 + ((int(url)-1)*videos_per_page)
		codigo_fonte = abrir_url('https://gdata.youtube.com/feeds/api/playlists/' + playlist1_id + '?max-results=' + str(videos_per_page) + '&start-index=' + str(index) + '&v=2&alt=json')
		decoded_data = json.loads(codigo_fonte)
		count = int(len(decoded_data['feed']['entry']))
		for x in range(0, len(decoded_data['feed']['entry'])):
			name = decoded_data['feed']['entry'][x]['title']['$t'].encode("utf8")
			youtube_id = decoded_data['feed']['entry'][x]['media$group']['yt$videoid']['$t'].encode("utf8")
			addDir(name + ' - (Server: YOUTUBE)','plugin://plugin.video.youtube/?action=play_video&videoid='+youtube_id,99,'http://i1.ytimg.com/vi/'+youtube_id+'/0.jpg',False)
		if index<=500-videos_per_page+1 and index-1+videos_per_page<int(decoded_data['feed']['openSearch$totalResults']['$t']):
			addDir('Próximo >>',str(int(url)+1),mode,'',playlist1_id = playlist1_id,playlist2_id = playlist2_id)
		else:
			if count != videos_per_page:
				index = 1
				print '@debug_url_1 '+'https://gdata.youtube.com/feeds/api/playlists/' + playlist2_id + '?max-results=' + str(videos_per_page - count) + '&start-index=' + str(index) + '&v=2&alt=json'
				codigo_fonte = abrir_url('https://gdata.youtube.com/feeds/api/playlists/' + playlist2_id + '?max-results=' + str(videos_per_page - count) + '&start-index=' + str(index) + '&v=2&alt=json')
				decoded_data = json.loads(codigo_fonte)
				for x in range(0, len(decoded_data['feed']['entry'])):
					name = decoded_data['feed']['entry'][x]['title']['$t'].encode("utf8")
					youtube_id = decoded_data['feed']['entry'][x]['media$group']['yt$videoid']['$t'].encode("utf8")
					addDir(name + ' - (Server: YOUTUBE)','plugin://plugin.video.youtube/?action=play_video&videoid='+youtube_id,99,'http://i1.ytimg.com/vi/'+youtube_id+'/0.jpg',False)
				#verificar se a próxima página existe
				if index<=500-len(decoded_data['feed']['entry'])+1 and index-1+len(decoded_data['feed']['entry'])<int(decoded_data['feed']['openSearch$totalResults']['$t']):
					checker = 0
					url = '1|'+str(videos_per_page - count)
					addDir('Próximo >>',str(url),mode+1,'',playlist1_id = playlist1_id,playlist2_id = playlist2_id)
					mode = mode + 1
			else:
				checker = 0
				url = '1|1'
				addDir('Próximo >>',str(url),mode+1,'',playlist1_id = playlist1_id,playlist2_id = playlist2_id)
				mode = mode + 1
	elif numero_par(mode) == False and checker == 1:
		url_split = url.split("|", 1)
		url1 = url_split[0] #current url
		url2 = url_split[1] #start-index
		index = 1 + int(url2) + ((int(url1)-1)*videos_per_page)
		print '@debug_url_2 '+'https://gdata.youtube.com/feeds/api/playlists/' + playlist2_id + '?max-results=' + str(videos_per_page) + '&start-index=' + str(index) + '&v=2&alt=json'
		codigo_fonte = abrir_url('https://gdata.youtube.com/feeds/api/playlists/' + playlist2_id + '?max-results=' + str(videos_per_page) + '&start-index=' + str(index) + '&v=2&alt=json')
		decoded_data = json.loads(codigo_fonte)
		for x in range(0, len(decoded_data['feed']['entry'])):
			name = decoded_data['feed']['entry'][x]['title']['$t'].encode("utf8")
			youtube_id = decoded_data['feed']['entry'][x]['media$group']['yt$videoid']['$t'].encode("utf8")
			addDir(name + ' - (Server: YOUTUBE)','plugin://plugin.video.youtube/?action=play_video&videoid='+youtube_id,99,'http://i1.ytimg.com/vi/'+youtube_id+'/0.jpg',False)
		if index<=500-videos_per_page+1 and index-1+videos_per_page<int(decoded_data['feed']['openSearch$totalResults']['$t']):
			addDir('Próximo >>',str(int(url1)+1)+'|'+url2,mode,'',playlist1_id = playlist1_id,playlist2_id = playlist2_id)
			
def listar_dailymotion_playlist(url,mode,playlist_id):
	videos_per_page = 15
	codigo_fonte = abrir_url('https://api.dailymotion.com/playlist/' + playlist_id + '/videos?page=' + url + '&limit=' +str(videos_per_page))
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['list'])):
		addDir(decoded_data['list'][int(x)]['title'].encode("utf8") + ' - (Server: Dailymotion)','plugin://plugin.video.dailymotion_com/?mode=playVideo&url=' + decoded_data['list'][int(x)]['id'].encode("utf8"),99,'http://www.dailymotion.com/thumbnail/video/' + decoded_data['list'][int(x)]['id'].encode("ascii","ignore"),False)
	if str(decoded_data['has_more'])=='True':
		addDir('Próximo >>',str(int(url)+1),mode,'',playlist_id = playlist_id)
		
def listar_search_inchannel_dailymotion(url,mode,search_query,channel_id):
	videos_per_page = 15
	codigo_fonte = abrir_url('https://api.dailymotion.com/videos?search=' + urllib.quote(search_query) + '&owner=' + channel_id + '&limit=' + str(videos_per_page) + '&page=' + str(url))
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['list'])):
		addDir(decoded_data['list'][int(x)]['title'].encode("utf8") + ' - (Server: Dailymotion)','plugin://plugin.video.dailymotion_com/?mode=playVideo&url=' + decoded_data['list'][int(x)]['id'].encode("utf8"),99,'http://www.dailymotion.com/thumbnail/video/' + decoded_data['list'][int(x)]['id'].encode("ascii","ignore"),False)
	if str(decoded_data['has_more'])=='True':
		addDir('Próximo >>',str(int(url)+1),mode,'',search_query = search_query,channel_id = channel_id)
		
def listar_sapovideos_playlist(url,mode,playlist_id,channel_id):
	videos_per_page = 15
	codigo_fonte = abrir_url('https://services.sapo.pt/videos/JSON2/Channel/' + channel_id + '/' + playlist_id + '?page=' + url + '&limit=' + str(videos_per_page))
	decoded_data = json.loads(codigo_fonte)
	total_videos = decoded_data['rss']['channel']['opensearch:totalResults'].encode("utf8")
	if int(total_videos)>0:
		if int(total_videos)==1 or int(total_videos)-int(decoded_data['rss']['channel']['opensearch:startIndex'].encode("utf8"))==1:
			data = decoded_data['rss']['channel']['item']['pubDate'].encode("utf8")
			name = decoded_data['rss']['channel']['item']['title'].encode("utf8")
			link = decoded_data['rss']['channel']['item']['sapo:videoURL'].encode("utf8")
			descricao = decoded_data['rss']['channel']['item']['sapo:synopse'].encode("utf8")
			iconimage = decoded_data['rss']['channel']['item']['media:content']['url'].encode("utf8")
			addDir(name + ' - (Server: Sapo Videos)',link,100,iconimage,False)
		else:
			for x in range(0, len(decoded_data['rss']['channel']['item'])):
				name = decoded_data['rss']['channel']['item'][x]['title'].encode("utf8")
				link = decoded_data['rss']['channel']['item'][x]['sapo:videoURL'].encode("utf8")
				iconimage = decoded_data['rss']['channel']['item'][x]['media:content']['url'].encode("utf8")
				addDir(name + ' - (Server: Sapo Videos)',link,100,iconimage,False)
		if int(total_videos)-(int(url)*videos_per_page)>0:
			addDir('Próximo >>',str(int(url)+1),mode,'',playlist_id = playlist_id,channel_id = channel_id)
		
def listar_search_inchannel_sapovideos(url,mode,search_query,channel_id):
	videos_per_page = 15
	codigo_fonte = abrir_url('https://services.sapo.pt/videos/JSON2/Query?user=' + channel_id + '&search=' + urllib.quote(search_query) + '&page=' + str(url) + '&limit=' + str(videos_per_page))
	decoded_data = json.loads(codigo_fonte)
	total_videos = decoded_data['rss']['channel']['opensearch:totalResults'].encode("utf8")
	if int(total_videos)>0:
		if int(total_videos)==1 or int(total_videos)-int(decoded_data['rss']['channel']['opensearch:startIndex'].encode("utf8"))==1:
			name = decoded_data['rss']['channel']['item']['title'].encode("utf8")
			link = decoded_data['rss']['channel']['item']['sapo:videoURL'].encode("utf8")
			iconimage = decoded_data['rss']['channel']['item']['media:content']['url'].encode("utf8")
			addDir(name + ' - (Server: Sapo Videos)',link,100,iconimage,False)
		else:
			for x in range(0, len(decoded_data['rss']['channel']['item'])):
				name = decoded_data['rss']['channel']['item'][x]['title'].encode("utf8")
				link = decoded_data['rss']['channel']['item'][x]['sapo:videoURL'].encode("utf8")
				iconimage = decoded_data['rss']['channel']['item'][x]['media:content']['url'].encode("utf8")
				addDir(name + ' - (Server: Sapo Videos)',link,100,iconimage,False)
		if int(total_videos)-(int(url)*videos_per_page)>0:
			addDir('Próximo >>',str(int(url)+1),mode,'',search_query = search_query,channel_id = channel_id)

def listar_podcasts(url,mode,playlist_id):
	videos_per_page = 15
	codigo_fonte = abrir_url_custom('http://query.yahooapis.com/v1/public/yql?q=' + urllib.quote_plus('SELECT * FROM feed(' + str(int(url)*videos_per_page-videos_per_page+1) + ',' + str(videos_per_page) + ') WHERE url="' + playlist_id + '"') + '&format=json&diagnostics=true&callback=', timeout=30)
	decoded_data = json.loads(codigo_fonte)
	try:
		if len(decoded_data['query']['results']['item']) > 0:
			for x in range(0, len(decoded_data['query']['results']['item'])):
				data = decoded_data['query']['results']['item'][x]['pubDate'].encode("utf8")
				data_timezone = re.search('^(.+) (GMT|EDT|[-+][\d]+)$', data)
				if data_timezone:
					data = data[:-(len(data_timezone.group(2))+1)]
				name = decoded_data['query']['results']['item'][x]['title'].encode("utf8")
				link = decoded_data['query']['results']['item'][x]['enclosure']['url'].encode("utf8")
				if playlist_id.startswith('http://www.rtp.pt/play/'): #os rss da rtp ja têm a data no título
					addDir(name,link,99,'',False)
				else:
					addDir('[B]' + data+ '[/B] - ' + name,link,99,'',False)
	except:
		pass
	try:
		codigo_fonte_2 = abrir_url_custom('http://query.yahooapis.com/v1/public/yql?q=' + urllib.quote_plus('SELECT * FROM feed(' + str((int(url)+1)*videos_per_page-videos_per_page+1) + ',' + str(videos_per_page) + ') WHERE url="' + playlist_id + '"') + '&format=json&diagnostics=true&callback=', timeout=30)
		decoded_data_2 = json.loads(codigo_fonte_2)
		if len(decoded_data_2['query']['results']['item']) > 0:
			addDir('Próximo >>',str(int(url)+1),mode,'',playlist_id = playlist_id)
	except:
		pass
	
###################################################################################
#FUNÇÕES PARA OBTER CONTEÚDOS DE SITES
		
def listar_sic_arquivo(url,mode):
	videos_per_page = 15
	arquivo_modo = re.search('^\?arquivo_modo=([\d]+)&canal=(.+)&playview=([\d]+)&pagina=([\d]+)', url).group(1)
	channel_id = re.search('^\?arquivo_modo=([\d]+)&canal=(.+)&playview=([\d]+)&pagina=([\d]+)', url).group(2)
	playlist_id = re.search('^\?arquivo_modo=([\d]+)&canal=(.+)&playview=([\d]+)&pagina=([\d]+)', url).group(3)
	pagina = re.search('^\?arquivo_modo=([\d]+)&canal=(.+)&playview=([\d]+)&pagina=([\d]+)', url).group(4)
	#listar as categorias do arquivo
	if int(arquivo_modo) == 1:
		if channel_id=='sic':
			codigo_fonte = abrir_url('http://v2.videos.sapo.pt/sic/sic.html')
		else:
			codigo_fonte = abrir_url('http://v2.videos.sapo.pt/'+channel_id)
		addDir('[B]Ver últimas entradas...[/B]','?arquivo_modo=3&canal='+channel_id+'&playview=0&pagina=1',mode,'')
		html_source_trunk = re.search('<div class="module show-list">(.*?)</div>', codigo_fonte, re.DOTALL)
		if html_source_trunk != None:
			programasaz = re.findall('<li><a href="http://v2.videos.sapo.pt/'+channel_id+'/playview/(.+?)" title=".+?">(.+?)</a></li>', html_source_trunk.group(1))
			for playlist_id, name in programasaz:
				addDir(name,'?arquivo_modo=2&canal='+channel_id+'&playview='+playlist_id+'&pagina=1',mode,addonfolder+artfolder+'foldericon.png')
	#listar playlists de videos
	elif int(arquivo_modo) == 2:
		codigo_fonte = abrir_url('https://services.sapo.pt/videos/JSON2/Channel/' + channel_id + '/' + playlist_id + '?page=' + pagina + '&limit=' + str(videos_per_page))
		decoded_data = json.loads(codigo_fonte)
		total_videos = decoded_data['rss']['channel']['opensearch:totalResults'].encode("utf8")
		if int(total_videos)>0:
			if int(total_videos)==1 or int(total_videos)-int(decoded_data['rss']['channel']['opensearch:startIndex'].encode("utf8"))==1:
				data = decoded_data['rss']['channel']['item']['pubDate'].encode("utf8")
				name = decoded_data['rss']['channel']['item']['title'].encode("utf8")
				link = decoded_data['rss']['channel']['item']['sapo:videoURL'].encode("utf8")
				descricao = decoded_data['rss']['channel']['item']['sapo:synopse'].encode("utf8")
				iconimage = decoded_data['rss']['channel']['item']['media:content']['url'].encode("utf8")
				addDir(name + ' - (Server: Sapo Videos)',link,100,iconimage,False)
			else:
				for x in range(0, len(decoded_data['rss']['channel']['item'])):
					name = decoded_data['rss']['channel']['item'][x]['title'].encode("utf8")
					link = decoded_data['rss']['channel']['item'][x]['sapo:videoURL'].encode("utf8")
					iconimage = decoded_data['rss']['channel']['item'][x]['media:content']['url'].encode("utf8")
					addDir(name + ' - (Server: Sapo Videos)',link,100,iconimage,False)
			if int(total_videos)-(int(pagina)*videos_per_page)>0:
				addDir('Próximo >>','?arquivo_modo=2&canal='+channel_id+'&playview='+playlist_id+'&pagina='+str(int(pagina)+1),mode,'')
	#listar últimos vídeos
	elif int(arquivo_modo) == 3:
		codigo_fonte = abrir_url('https://services.sapo.pt/videos/JSON2/User/'+channel_id+'?page=' + pagina + '&limit=' + str(videos_per_page))
		decoded_data = json.loads(codigo_fonte)
		total_videos = decoded_data['rss']['channel']['opensearch:totalResults'].encode("utf8")
		if int(pagina)==1:
			addDir('[B]Ver programas...[/B]','?arquivo_modo=1&canal='+channel_id+'&playview=0&pagina=0',mode,'')
		if int(total_videos)>0:
			if int(total_videos)==1 or int(total_videos)-int(decoded_data['rss']['channel']['opensearch:startIndex'].encode("utf8"))==1:
				data = decoded_data['rss']['channel']['item']['pubDate'].encode("utf8")
				name = decoded_data['rss']['channel']['item']['title'].encode("utf8")
				link = decoded_data['rss']['channel']['item']['sapo:videoURL'].encode("utf8")
				descricao = decoded_data['rss']['channel']['item']['sapo:synopse'].encode("utf8")
				iconimage = decoded_data['rss']['channel']['item']['media:content']['url'].encode("utf8")
				addDir(name + ' - (Server: Sapo Videos)',link,100,iconimage,False)
			else:
				for x in range(0, len(decoded_data['rss']['channel']['item'])):
					name = decoded_data['rss']['channel']['item'][x]['title'].encode("utf8")
					link = decoded_data['rss']['channel']['item'][x]['sapo:videoURL'].encode("utf8")
					iconimage = decoded_data['rss']['channel']['item'][x]['media:content']['url'].encode("utf8")
					addDir(name + ' - (Server: Sapo Videos)',link,100,iconimage,False)
			if int(total_videos)-(int(pagina)*videos_per_page)>0:
				addDir('Próximo >>','?arquivo_modo=3&canal='+channel_id+'&playview=0&pagina='+str(int(pagina)+1),mode,'')

		
def listar_videos_tvstory_new(url,mode):
	#lista as novelas da tvstory apenas no novo site deles
	codigo_fonte = abrir_url('http://tvstoryoficial.blogspot.pt/search/label/' + url)
	match=re.compile("<h3 class='post-title entry-title' itemprop='name'>\n<a href='(.+?)'>(.+?)</a>\n</h3>").findall(codigo_fonte)
	for page_link, name in match:
		codigo_fonte_2 = abrir_url(page_link)
		match_2=re.compile('<iframe.+?src=".+?www.youtube.com/embed/([^?"]+).+?>').findall(codigo_fonte_2)
		video_parte = 1
		for youtube_id in match_2:
			if len(match_2)>1:
				addDir(name + ' - parte ' + str(video_parte) + ' (Server: YOUTUBE)','plugin://plugin.video.youtube/?action=play_video&videoid='+youtube_id.decode('utf-8'),99,'http://i1.ytimg.com/vi/'+youtube_id.decode('utf-8')+'/0.jpg',False)
				video_parte += 1
			else:
				addDir(name + ' - (Server: YOUTUBE)','plugin://plugin.video.youtube/?action=play_video&videoid='+youtube_id.decode('utf-8'),99,'http://i1.ytimg.com/vi/'+youtube_id.decode('utf-8')+'/0.jpg',False)
	match=re.search("<span id='blog-pager-older-link'>\n<a class='blog-pager-older-link' href='(.+?)' id='Blog1_blog-pager-older-link' title='Mensagens antigas'>Mensagens antigas</a>\n</span>", codigo_fonte)
	if match != None:
		codigo_fonte_2 = abrir_url(match.group(1))
		match_2=re.search("<h3 class='post-title entry-title' itemprop='name'>\n<a href='(.+?)'>(.+?)</a>\n</h3>", codigo_fonte_2)
		if match_2 != None:
			addDir('Próximo >>',match.group(1),mode,'')
		
def listar_videos_tvstory_old(url,mode,search_query,channel_id):
	#lista as novelas da tvstory divididas entre o antigo canal e o novo site
	tv_story_suburl = channel_id
	ytchannel_id = 'UC3gXb0jTm9cgRb6vseICJNQ' #old tv story channel
	videos_per_page = 15 #configuração apenas se aplica ao youtube
	checker = 1
	if numero_par(mode) == True:
		if url == None:
			codigo_fonte = abrir_url('http://tvstoryoficial.blogspot.pt/search/label/' + tv_story_suburl)
		else:
			codigo_fonte = abrir_url('http://tvstoryoficial.blogspot.pt/search/label/' + tv_story_suburl + '?' + url)
		match=re.compile("<h3 class='post-title entry-title' itemprop='name'>\n<a href='(.+?)'>(.+?)</a>\n</h3>").findall(codigo_fonte)
		count = 0
		for page_link, name in match:
			codigo_fonte_2 = abrir_url(page_link)
			match_2=re.compile('<iframe.+?src=".+?www.youtube.com/embed/([^?"]+).+?>').findall(codigo_fonte_2)
			count += len(match_2)
			video_parte = 1
			for youtube_id in match_2:
				if len(match_2)>1:
					addDir(name + ' - parte ' + str(video_parte) + ' (Server: YOUTUBE)','plugin://plugin.video.youtube/?action=play_video&videoid='+youtube_id.decode('utf-8'),99,'http://i1.ytimg.com/vi/'+youtube_id.decode('utf-8')+'/0.jpg',False)
					video_parte += 1
				else:
					addDir(name + ' - (Server: YOUTUBE)','plugin://plugin.video.youtube/?action=play_video&videoid='+youtube_id.decode('utf-8'),99,'http://i1.ytimg.com/vi/'+youtube_id.decode('utf-8')+'/0.jpg',False)
		match=re.search("<span id='blog-pager-older-link'>\n<a class='blog-pager-older-link' href='http://(.+?)/.+?\?(.+?)' id='Blog1_blog-pager-older-link' title='Mensagens antigas'>Mensagens antigas</a>\n</span>", codigo_fonte)
		if match != None:
			codigo_fonte_2 = abrir_url('http://'+match.group(1)+'/search/label/' + tv_story_suburl + '?' + match.group(2))
			match_2=re.search("<h3 class='post-title entry-title' itemprop='name'>\n<a href='(.+?)'>(.+?)</a>\n</h3>", codigo_fonte_2)
			if match_2 != None:
				addDir('Próximo >>',match.group(2),mode,'',search_query = search_query,channel_id = channel_id)
			else:
				if count < videos_per_page:
					index = 1
					codigo_fonte = abrir_url('http://gdata.youtube.com/feeds/api/videos?author=' + ytchannel_id + '&q=' + urllib.quote(search_query) + '&orderby=published&max-results=' + str(videos_per_page - count) + '&start-index=' + str(index) + '&v=2&alt=json')
					decoded_data = json.loads(codigo_fonte)
					for x in range(0, len(decoded_data['feed']['entry'])):
						name = decoded_data['feed']['entry'][x]['title']['$t'].encode("utf8")
						youtube_id = decoded_data['feed']['entry'][x]['media$group']['yt$videoid']['$t'].encode("utf8")
						addDir(name + ' - (Server: YOUTUBE)','plugin://plugin.video.youtube/?action=play_video&videoid='+youtube_id,99,'http://i1.ytimg.com/vi/'+youtube_id+'/0.jpg',False)
					#verificar se a próxima página existe
					if index<=500-len(decoded_data['feed']['entry'])+1 and index-1+len(decoded_data['feed']['entry'])<int(decoded_data['feed']['openSearch$totalResults']['$t']):
						checker = 0
						url = '1|'+str(videos_per_page - count)
						addDir('Próximo >>',str(url),mode+1,'',search_query = search_query,channel_id = channel_id)
						mode = mode + 1
				else:
					checker = 0
					url = '1|1'
					addDir('Próximo >>',str(url),mode+1,'',search_query = search_query,channel_id = channel_id)
					mode = mode + 1
	elif numero_par(mode) == False and checker == 1:
		url_split = url.split("|", 1)
		url1 = url_split[0] #current url
		url2 = url_split[1] #start-index
		index = 1 + int(url2) + ((int(url1)-1)*videos_per_page)
		codigo_fonte = abrir_url('http://gdata.youtube.com/feeds/api/videos?author=' + ytchannel_id + '&q=' + urllib.quote(search_query) + '&orderby=published&max-results=' + str(videos_per_page) + '&start-index=' + str(index) + '&v=2&alt=json')
		decoded_data = json.loads(codigo_fonte)
		for x in range(0, len(decoded_data['feed']['entry'])):
			name = decoded_data['feed']['entry'][x]['title']['$t'].encode("utf8")
			youtube_id = decoded_data['feed']['entry'][x]['media$group']['yt$videoid']['$t'].encode("utf8")
			addDir(name + ' - (Server: YOUTUBE)','plugin://plugin.video.youtube/?action=play_video&videoid='+youtube_id,99,'http://i1.ytimg.com/vi/'+youtube_id+'/0.jpg',False)
		if index<=500-videos_per_page+1 and index-1+videos_per_page<int(decoded_data['feed']['openSearch$totalResults']['$t']):
			addDir('Próximo >>',str(int(url1)+1)+'|'+url2,mode,'',search_query = search_query,channel_id = channel_id)
			
def melhor_que_falecer(url,mode):
	try:
		codigo_fonte = abrir_url('http://www.tvi.iol.pt/melhor-do-que-falecer/ajax/videos/'+url)
	except:
		codigo_fonte = ''
	if codigo_fonte:
		match=re.findall('<li class="video-wrapper".*?data-video-id="(.+?)".*?>.*?<img src="(.+?)/".*?>.*?<h2 class="h1-shift">(.+?)</h2>.*?</li>', codigo_fonte, re.DOTALL)
		for video_id, iconimage, name in match:
			addDir(name + ' - (Server: tvi.iol.pt)','http://videos-cache.iol.pt/vod_http/mp4:'+video_id+'-L-500k.mp4/chunklist.m3u8',99,iconimage,False)
		try:
			codigo_fonte_2 = abrir_url('http://www.tvi.iol.pt/melhor-do-que-falecer/ajax/videos/'+str(int(url)+1))
		except:
			codigo_fonte_2 = ''
		if codigo_fonte_2:
			match_2=re.findall('<li class="video-wrapper".*?data-video-id="(.+?)".*?>.*?<img src="(.+?)/".*?>.*?<h2 class="h1-shift">(.+?)</h2>.*?</li>', codigo_fonte_2, re.DOTALL)
			if match_2:
				addDir('Próximo >>',str(int(url)+1),mode,'')

def listar_tsf_podcasts():
	try:
		codigo_fonte = abrir_url('http://www.tsf.pt/podcast/')
	except:
		codigo_fonte = ''
	if codigo_fonte:
		active_podcasts_html=re.search('<div class="podcasts_left">(.+?)</span>', codigo_fonte, re.DOTALL)
		if active_podcasts_html:
			addDir('[COLOR blue][B]Podcasts Activos[/B][/COLOR]','',441,addonfolder+artfolder+'foldericon.png',False)
			match=re.findall('<ul><li><a class="titlnk" href="(.+?)".*?>(.+?)</a></li></ul>', active_podcasts_html.group(1))
			if match:
				for link, name in match:
					addDir(name.decode('latin-1').encode("utf-8"),'1',208,addonfolder+artfolder+'foldericon.png',playlist_id=link)
		arquivo_podcasts_html=re.search('<div class="podcasts_arquivo">(.+?)</span>', codigo_fonte, re.DOTALL)
		if arquivo_podcasts_html:
			addDir('[COLOR blue][B]Podcasts Arquivados[/B][/COLOR]','',441,addonfolder+artfolder+'foldericon.png',False)
			match=re.findall('<ul><li><a class="titlnk" href="(.+?)".*?>(.+?)</a></li></ul>', arquivo_podcasts_html.group(1))
			if match:
				for link, name in match:
					addDir(name.decode('latin-1').encode("utf-8"),'1',208,addonfolder+artfolder+'foldericon.png',playlist_id=link)

def listar_rr_podcasts():
	try:
		codigo_fonte = abrir_url('http://rr.sapo.pt/podcast.aspx')
	except:
		codigo_fonte = ''
	if codigo_fonte:
		tab1inf_html=re.search("<div id='tab1Inf' class='tab-content-rss'>(.+?)<div id='tab2BB' class='tab-content-rss'>", codigo_fonte, re.DOTALL)
		if tab1inf_html:
			addDir('[COLOR blue][B]Informação[/B][/COLOR]','',442,addonfolder+artfolder+'foldericon.png',False)
			match=re.findall("<div class='infRss'.*?>.*?<a href='(.+?)'.*?>(.+?)</a></div>", tab1inf_html.group(1))
			if match:
				for link, name in match:
					addDir(name,'1',208,addonfolder+artfolder+'foldericon.png',playlist_id='http://rr.sapo.pt/'+link)
		tab2bb_html=re.search("<div id='tab2BB' class='tab-content-rss'>(.+?)<div id='tab3Prog' class='tab-content-rss'>", codigo_fonte, re.DOTALL)
		if tab2bb_html:
			addDir('[COLOR blue][B]Bola Branca[/B][/COLOR]','',442,addonfolder+artfolder+'foldericon.png',False)
			match=re.findall("<div class='infRss'.*?>.*?<a href='(.+?)'.*?>(.+?)</a></div>", tab2bb_html.group(1))
			if match:
				for link, name in match:
					addDir(name,'1',208,addonfolder+artfolder+'foldericon.png',playlist_id='http://rr.sapo.pt/'+link)
		tab3prog_html=re.search("<div id='tab3Prog' class='tab-content-rss'>(.+?)<div id='tab4EN' class='tab-content-rss'>", codigo_fonte, re.DOTALL)
		if tab3prog_html:
			addDir('[COLOR blue][B]Programação[/B][/COLOR]','',442,addonfolder+artfolder+'foldericon.png',False)
			match=re.findall("<div class='infRss'.*?>.*?<a href='(.+?)'.*?>(.+?)</a></div>", tab3prog_html.group(1))
			if match:
				for link, name in match:
					addDir(name,'1',208,addonfolder+artfolder+'foldericon.png',playlist_id='http://rr.sapo.pt/'+link)
		tab4en_html=re.search("<div id='tab4EN' class='tab-content-rss'>(.+?)<br class=\"clearfloat\"/>", codigo_fonte, re.DOTALL)
		if tab4en_html:
			addDir('[COLOR blue][B]Euranet[/B][/COLOR]','',442,addonfolder+artfolder+'foldericon.png',False)
			match=re.findall("<div class='infRss'.*?>.*?<a href='(.+?)'.*?>(.+?)</a></div>", tab4en_html.group(1))
			if match:
				for link, name in match:
					addDir(name,'1',208,addonfolder+artfolder+'foldericon.png',playlist_id='http://rr.sapo.pt/'+link)

def rtp_podcasts_canais():
	try:
		codigo_fonte = abrir_url('http://www.rtp.pt/play/podcasts')
	except:
		codigo_fonte = ''
	if codigo_fonte:
		match=re.findall('<a.*?href="(.+?)" title="Podcasts.*?".*?>(.+?)</a>', codigo_fonte)
		for link, name in match:
			addDir(h.unescape(name).encode('utf-8'),'http://www.rtp.pt'+link,444,addonfolder+artfolder+'foldericon.png')

def listar_rtp_podcasts(url):
	try:
		codigo_fonte = abrir_url(url)
	except:
		codigo_fonte = ''
	if codigo_fonte:
		match=re.findall('<li><b>(.+?)</b><a title=".*?" href="(.+?)".*?><span class="img_play_nr func_5">&nbsp;</span>Podcast</a>.*?</li>', codigo_fonte)
		for name, link in match:
			addDir(name.decode('latin-1').encode("utf-8"),'1',208,addonfolder+artfolder+'foldericon.png',playlist_id='http://www.rtp.pt'+link)

###################################################################################
#URL RESOLVERS E FUNÇÃO PLAY

def resolver_sapovideos(url,name,iconimage):
	progress = xbmcgui.DialogProgress()
	progress.create('Replay PT', 'Resolvendo Sapo Videos...')
	progress.update(0)
	if progress.iscanceled():
		sys.exit(0)
	source_code = abrir_url(url)
	progress.update(50)
	if progress.iscanceled():
		sys.exit(0)
	match = re.search('<meta property="og:video" content="http://imgs.sapo.pt/sapovideo/swf/flvplayer-sapo.swf\?file=(.+?)/mov.+?"/>', source_code)
	if match != None:
		tmp_url = match.group(1) + '/mov'
		req = urllib2.Request(tmp_url)
		res = urllib2.urlopen(req)
		url = res.geturl()
		progress.update(100)
		progress.close()
	else:
		url = ''
		progress.update(100)
		progress.close()
	play(url,name,iconimage)

def resolver_vkcom(url,name,iconimage):
	codigo_fonte = abrir_url(url)
	vk_qualidade = []
	vk_url = []
	match = re.search('url1080=(.+?).1080.mp4', codigo_fonte)
	if match != None:
		vk_qualidade.append('1080p')
		vk_url.append(match.group(1)+'.1080.mp4')
	match = re.search('url720=(.+?).720.mp4', codigo_fonte)
	if match != None:
		vk_qualidade.append('720p')
		vk_url.append(match.group(1)+'.720.mp4')
	match = re.search('url480=(.+?).480.mp4', codigo_fonte)
	if match != None:
		vk_qualidade.append('480p')
		vk_url.append(match.group(1)+'.480.mp4')
	match = re.search('url360=(.+?).360.mp4', codigo_fonte)
	if match != None:
		vk_qualidade.append('360p')
		vk_url.append(match.group(1)+'.360.mp4')
	match = re.search('url240=(.+?).240.mp4', codigo_fonte)
	if match != None:
		vk_qualidade.append('240p')
		vk_url.append(match.group(1)+'.240.mp4')
	video_url = xbmcgui.Dialog().select('Escolha a qualidade do video...', vk_qualidade)
	play(vk_url[video_url],name,iconimage)
		
def play(url,name,iconimage):
	listitem = xbmcgui.ListItem(label=name, iconImage=str(iconimage), thumbnailImage=str(iconimage), path=url)
	listitem.setProperty('IsPlayable', 'true')
	try:
		xbmc.Player().play(item=url, listitem=listitem)
	except:
		pass
		self.message("Couldn't play item.")

###################################################################################
#FUNCOES DIVERSAS

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def abrir_url_custom(url,**kwargs):
	for key, value in kwargs.items():
		exec('%s = %s' % (key, repr(value)))
	req = urllib2.Request(url)
	if 'user_agent' in locals():
		req.add_header('User-Agent', user_agent)
	else:
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	if 'referer' in locals():
		req.add_header('Referer', referer)
	if 'timeout' in locals():
		response = urllib2.urlopen(req, timeout=timeout)
	else:
		response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + artfolder + 'fanart.png')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,pasta=True,**kwargs):
	extra_args = ''
	for key, value in kwargs.items():
		exec('%s = %s' % (key, repr(value)))
		extra_args = extra_args + '&' + str(key) + '=' + urllib.quote_plus(str(value))
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+extra_args
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta)
	return ok

def numero_par(i):
		return (i % 2) == 0

############################################################################################################
#                                               GET PARAMS                                                 #
############################################################################################################
              
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

      
params=get_params()
url=None
name=None
mode=None
iconimage=None
channel_id=None
search_query=None
playlist_id=None
playlist1_id=None
playlist2_id=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:        
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        channel_id=urllib.unquote_plus(params["channel_id"])
except:
        pass
try:        
        search_query=urllib.unquote_plus(params["search_query"])
except:
        pass
try:        
        playlist_id=urllib.unquote_plus(params["playlist_id"])
except:
        pass
try:        
        playlist1_id=urllib.unquote_plus(params["playlist1_id"])
except:
        pass
try:        
        playlist2_id=urllib.unquote_plus(params["playlist2_id"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)
if channel_id:
	print "Channel Id: "+str(channel_id)
if search_query:
	print "Search Query: "+str(search_query)
if playlist_id:
	print "Playlist Id: "+str(playlist_id)
if playlist1_id:
	print "Playlist1 Id: "+str(playlist1_id)
if playlist2_id:
	print "Playlist2 Id: "+str(playlist2_id)

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################

# 1-98: Menus
if mode==None: PAIS()
elif mode==1: PORTUGAL()
elif mode==2: RTP()
elif mode==3: ARQ_SIC()
elif mode==4: NOV_SIC()
elif mode==5: SER_SIC()
elif mode==6: NOV_TVI()
elif mode==7: SER_TVI()
elif mode==8: RADIO_PT()
elif mode==9: COMERCIAL()
elif mode==10: M80()
elif mode==11: OUTROS_PT()
elif mode==12: BRASIL()
# 99: Função Play
elif mode==99: play(url,name,iconimage)
# 100-199: Url Resolvers diversos
elif mode==100: resolver_sapovideos(url,name,iconimage)
elif mode==101: resolver_vkcom(url,name,iconimage)
# 200-299: Funções para listar conteúdos de serviços de video
elif mode==200: listar_youtube_playlist(url,mode,playlist_id)
elif mode==201: listar_search_inchannel_youtube(url,mode,search_query,channel_id)
elif mode==202 or mode==203: listar_2_youtube_playlists(url,mode,playlist1_id,playlist2_id)
elif mode==204: listar_dailymotion_playlist(url,mode,playlist_id)
elif mode==205: listar_search_inchannel_dailymotion(url,mode,search_query,channel_id)
elif mode==206: listar_sapovideos_playlist(url,mode,playlist_id,channel_id)
elif mode==207: listar_search_inchannel_sapovideos(url,mode,search_query,channel_id)
elif mode==208: listar_podcasts(url,mode,playlist_id)
# 400 em diante: Funções para obter conteúdos de sites
elif mode==400: listar_sic_arquivo(url,mode)
elif mode==401: listar_videos_tvstory_new(url,mode)
elif mode==402: listar_videos_tvstory_old(url,mode,search_query,channel_id)
elif mode==403: g1novelas.CATEGORIES_g1()
elif mode==404: g1novelas.listar_episodiosg1(url)
elif mode==405: g1novelas.procurar_fontesg1(url,name,iconimage)
elif mode==406: g1novelas.alterar_vistag1(g1novelas.g1novelas_url)
elif mode==407: maisnovelas.CATEGORIES_maisnovelas()
elif mode==408: maisnovelas.listar_episodios(url)
elif mode==409: maisnovelas.procurar_fontes(url,name,iconimage)
elif mode==410: maisnovelas.alterar_vista(maisnovelas.maisnovelas_url)
elif mode==411: novelasgravadas.listar_categorias()
elif mode==412: novelasgravadas.listar_episodios(url)
elif mode==413: novelasgravadas.procurar_fontes(url,name,iconimage)
elif mode==415: assistirnovelas.CATEGORIES_assistirnovelas()
elif mode==416: assistirnovelas.listar_episodios(url)
elif mode==417: assistirnovelas.procurar_fontes(url,name,iconimage)
elif mode==418: vernovelas.listar_categorias()
elif mode==419: vernovelas.listar_episodios(url)
elif mode==420: vernovelas.procurar_fontes(url,name,iconimage)
elif mode==421: documentariosvarios.CATEGORIES_documentariosvarios()
elif mode==422: documentariosvarios.listar_episodios(url)
elif mode==423: documentariosvarios.procurar_fontes(url,name,iconimage)
elif mode==424: documentariosvarios.alterar_vista(documentariosvarios.documentariosvarios_url)
elif mode==425: todosdocumentarios.CATEGORIES_todosdocumentarios()
elif mode==426: todosdocumentarios.listar_episodios(url)
elif mode==427: todosdocumentarios.procurar_fontes(url,name,iconimage)
elif mode==428: todosdocumentarios.alterar_vista(todosdocumentarios.todosdocumentarios_url)
elif mode==429: filmesportugueses.listar_categorias()
elif mode==430: filmesportugueses.listar_episodios(url)
elif mode==431: filmesportugueses.procurar_fontes(url,name,iconimage)
elif mode==432: docverdade.CATEGORIES_docverdade()
elif mode==433: docverdade.listar_episodios(url)
elif mode==434: docverdade.procurar_fontes(url,name,iconimage)
elif mode==435: docverdade.alterar_vista(docverdade.docverdade_url)
elif mode==436: melhor_que_falecer(url,mode)
elif mode==437: webdocumentarios.CATEGORIES_webdocumentarios()
elif mode==438: webdocumentarios.listar_episodios(url)
elif mode==439: webdocumentarios.procurar_fontes(url,name,iconimage)
elif mode==440: webdocumentarios.alterar_vista(webdocumentarios.webdocumentarios_url)
elif mode==441: listar_tsf_podcasts()
elif mode==442: listar_rr_podcasts()
elif mode==443: rtp_podcasts_canais()
elif mode==444: listar_rtp_podcasts(url)
elif mode==445: curtadoc.listar_categorias()
elif mode==446: curtadoc.listar_episodios(url)
elif mode==447: curtadoc.procurar_fontes(url,name,iconimage)
elif mode==448: podflix.listar_categorias()
elif mode==449: podflix.listar_episodios(url)
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))