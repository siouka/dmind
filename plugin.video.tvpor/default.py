# -*- coding: utf-8 -*-

""" TV Portuguesa
    2014 fightnight"""

import xbmc, xbmcgui, xbmcaddon, xbmcplugin,re,sys, urllib, urllib2,time,datetime,os
from resources.lib.net import Net
net = Net()

versao = '0.4.01'
RadiosNacionaisURL = 'http://www.radioonline.com.pt'
BeachcamURL = 'http://beachcam.sapo.pt/'
CanalHDURL = 'http://canalhd.tv/tv/'
SurflineURL= 'http://www.surfline.com'
SurftotalURL='http://www.surftotal.com'
RadiosURL = 'http://www.radios.pt/portalradio/'
MEOURL = 'http://www.meocanaltv.com'
RedwebURL = 'http://www.redweb.tv'
SptveuURL = 'http://www.gosporttv.com/'
TVGOURL = 'http://www.tvgo.be/'
TVDezURL = 'http://www.estadiofutebol.com'
TVGenteURL = 'http://www.tvgente.me'
TVTugaURL = 'http://www.tvtuga.com'
TugastreamURL = 'http://www.tugastream.com/'
TVPTHDURL = 'http://www.tvportugalhd.eu'
TVPTHDZuukURL = 'http://www.zuuk.pw'
TVCoresURL = 'http://tvfree.me'
LSHDURL= 'http://livesoccerhq.com'
TVZuneURL = 'http://www.tvzune.tv/'
TVZune2URL = 'http://soft.tvzune.co/'
RTPURL='http://www.rtp.pt'
VBURL= 'http://www.videosbacanas.com/'
ResharetvURL = 'http://resharetv.com/'
AltasEmocoesURL='http://sportslive.me/'
DesgrURL = 'http://www.desportogratis.com/'
PATH = "XBMC_TVPOR"
UATRACK="UA-39199007-1"
activado=False
user_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
addon_id = 'plugin.video.tvpor'
art = '/resources/art/'
selfAddon = xbmcaddon.Addon(id=addon_id)
tvporpath = selfAddon.getAddonInfo('path')
mensagemok = xbmcgui.Dialog().ok
menuescolha = xbmcgui.Dialog().select
mensagemprogresso = xbmcgui.DialogProgress()
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
cachepath = os.path.join(tvporpath,'resources','cache')
downloadPath = selfAddon.getSetting('pastagravador')
gravadorpath = os.path.join(selfAddon.getAddonInfo('path'),'resources','gravador')
activadoextra=[]
debug=[]

if not os.path.exists(tvporpath):
    tvporpath = tvporpath.decode('utf-8')
    cachepath = cachepath.decode('utf-8')
    pastaperfil = pastaperfil.decode('utf-8')
    downloadPath = downloadPath.decode('utf-8')
    gravadorpath = gravadorpath.decode('utf-8')

def menu_principal():
    if xbmc.getCondVisibility('system.platform.linux') or xbmc.getCondVisibility('system.platform.windows') or xbmc.getCondVisibility('system.platform.osx'):
        addDir('Ver Gravações','nada',12,tvporpath + art + 'gravador-ver1.png',1,'Aceda à lista das gravações já efectuadas',False)
    disponivel=versao_disponivel()
    if disponivel==versao: addLink('Última versao (' + versao+ ')','',tvporpath + art + 'versao-ver2.png')
    else: addDir('Instalada v' + versao + ' | Actualização v' + disponivel,'nada',15,tvporpath + art + 'versao-ver2.png',1,'',False)
    addDir("Definições do addon",'nada',22,tvporpath + art + 'defs-ver2.png',1,'',False)
    addDir("[COLOR red][B]LER AVISO[/B][/COLOR]",'nada',23,tvporpath + art + 'aviso-ver2.png',1,'',False)
    xbmc.executebuiltin("Container.SetViewMode(500)")

### LISTA CANAIS ###############

def canais():
    librtmpwindow()
    info_servidores()

    nrcanais=62
    canaison=[]
    empty='nada'
    GA("None","listacanais")
    if selfAddon.getSetting("prog-lista3") == "true":
        mensagemprogresso.create('TV Portuguesa', 'A carregar listas de programação.','Por favor aguarde.')
        mensagemprogresso.update(0)
        if mensagemprogresso.iscanceled(): sys.exit(0)
        programas=p_todos()
        mensagemprogresso.close()
    else: programas=[]
    
    sintomecomsorte()
    
    if activado==True: addCanal("[B]Lista Completa[/B]",empty,16,tvporpath + art + 'gravador-ver1.png',nrcanais,'')
    addDir("[B][COLOR white]Informações[/COLOR][/B]",'nada',1,tvporpath + art + 'defs-ver2.png',1,'Clique aqui para voltar ao menu principal.',True)
    if selfAddon.getSetting("listas-pessoais") == "true": addDir("[B][COLOR white]Listas Pessoais[/COLOR][/B]",'nada',6,tvporpath + art + 'listas-ver2.png',1,'Outras listas de canais criadas pela comunidade.',True)

    if selfAddon.getSetting("radios") == "true": addDir("[B][COLOR white]Radios[/COLOR][/B]",'nada',19,tvporpath + art + 'radios-v1.png',1,'Oiça comodamente radios nacionais.',True)
    if selfAddon.getSetting("eventos") == "true": canaison.append('[B][COLOR white]Eventos[/COLOR][/B]'); addCanal("[B][COLOR white]Eventos[/COLOR][/B] (Cesarix/Rominhos)",'http://dl.dropboxusercontent.com/u/266138381/Eventos.xml',11,tvporpath + art + 'eventos-v1.png',nrcanais,'')
    if selfAddon.getSetting("praias") == "true": addDir("[B][COLOR white]Praias[/COLOR][/B]",'nada',26,tvporpath + art + 'versao-ver2.png',1,'Webcams das melhores praias nacionais.',True)
    if selfAddon.getSetting("canais-rtp1") == "true": canaison.append('[B]RTP 1[/B]'); addCanal("[B]RTP 1[/B] " + p_umcanal(programas,'RTP1','nomeprog'),empty,16,tvporpath + art + 'rtp1-ver2.png',nrcanais,p_umcanal(programas,'RTP1','descprog'))
    if selfAddon.getSetting("canais-rtp2") == "true":  canaison.append('[B]RTP 2[/B]'); addCanal("[B]RTP 2[/B] " + p_umcanal(programas,'RTP2','nomeprog'),empty,16,tvporpath + art + 'rtp2-ver2.png',nrcanais,p_umcanal(programas,'RTP2','descprog'))
    if selfAddon.getSetting("canais-sic") == "true":  canaison.append('[B]SIC[/B]'); addCanal("[B]SIC[/B] " + p_umcanal(programas,'SIC','nomeprog'),empty,16,tvporpath + art + 'sic-ver3.png',nrcanais,p_umcanal(programas,'SIC','descprog'))
    if selfAddon.getSetting("canais-tvi") == "true":  canaison.append('[B]TVI[/B]'); addCanal("[B]TVI[/B] " + p_umcanal(programas,'TVI','nomeprog'),empty,16,tvporpath + art + 'tvi-ver2.png',nrcanais,p_umcanal(programas,'TVI','descprog'))
    if selfAddon.getSetting("canais-sporttv1") == "true":
        canaison.append('[B]SPORTTV 1[/B]'); addCanal("[B]SPORTTV 1[/B] " + p_umcanal(programas,'SPTV1','nomeprog'),empty,16,tvporpath + art + 'sptv1-ver2.png',nrcanais,p_umcanal(programas,'SPTV1','descprog'))
        #canaison.append('[B]SPORTTV 1 HD[/B]'); addCanal("[B]SPORTTV 1 HD[/B] " + p_umcanal(programas,'SPTV1','nomeprog'),empty,16,tvporpath + art + 'sptvhd-ver2.png',nrcanais,p_umcanal(programas,'SPTV1','descprog'))
    if selfAddon.getSetting("canais-sporttv2") == "true": canaison.append('[B]SPORTTV 2[/B]'); addCanal("[B]SPORTTV 2[/B] " + p_umcanal(programas,'SPTV2','nomeprog'),empty,16,tvporpath + art + 'sptv2-ver2.png',nrcanais,p_umcanal(programas,'SPTV2','descprog'))
    if selfAddon.getSetting("canais-sporttv3") == "true": canaison.append('[B]SPORTTV 3[/B]'); addCanal("[B]SPORTTV 3[/B] " + p_umcanal(programas,'SPTV3','nomeprog'),empty,16,tvporpath + art + 'sptv3-ver2.png',nrcanais,p_umcanal(programas,'SPTV3','descprog'))
    if selfAddon.getSetting("canais-sporttv4") == "true": canaison.append('[B]SPORTTV 4[/B]'); addCanal("[B]SPORTTV 4[/B] " + p_umcanal(programas,'SPTV4','nomeprog'),empty,16,tvporpath + art + 'sptv4-ver2.png',nrcanais,p_umcanal(programas,'SPTV4','descprog'))
    if selfAddon.getSetting("canais-sporttv5") == "true": canaison.append('[B]SPORTTV 5[/B]'); addCanal("[B]SPORTTV 5[/B] " + p_umcanal(programas,'SPTV5','nomeprog'),empty,16,tvporpath + art + 'sptv5-ver2.png',nrcanais,p_umcanal(programas,'SPTV5','descprog'))
    if selfAddon.getSetting("canais-btv1") == "true": canaison.append('[B]Benfica TV 1[/B]'); addCanal("[B]Benfica TV 1[/B] " + p_umcanal(programas,'SLB','nomeprog'),empty,16,tvporpath + art + 'btv1-ver1.png',nrcanais,p_umcanal(programas,'SLB','descprog'))
    if selfAddon.getSetting("canais-btv2") == "true": canaison.append('[B]Benfica TV 2[/B]'); addCanal("[B]Benfica TV 2[/B] " + p_umcanal(programas,'SLB2','nomeprog'),empty,16,tvporpath + art + 'btv2-ver1.png',nrcanais,p_umcanal(programas,'SLB2','descprog'))
    if selfAddon.getSetting("canais-sportingtv") == "true": canaison.append('[B]Sporting TV[/B]'); addCanal("[B]Sporting TV[/B] " + p_umcanal(programas,'SCP','nomeprog'),empty,16,tvporpath + art + 'scptv-ver1.png',nrcanais,p_umcanal(programas,'SCP','descprog'))
    if selfAddon.getSetting("canais-portocanal") == "true": canaison.append('[B]Porto Canal[/B]'); addCanal("[B]Porto Canal[/B] " + p_umcanal(programas,'PORTO','nomeprog'),empty,16,tvporpath + art + 'pcanal-ver2.png',nrcanais,p_umcanal(programas,'PORTO','descprog'))
    if selfAddon.getSetting("canais-abolatv") == "true": canaison.append('[B]A Bola TV[/B]'); addCanal("[B]A Bola TV[/B] " + p_umcanal(programas,'ABOLA','nomeprog'),empty,16,tvporpath + art + 'abola-ver1.png',nrcanais,p_umcanal(programas,'ABOLA','descprog'))
    if selfAddon.getSetting("canais-cmtv") == "true": canaison.append('[B]CM TV[/B]'); addCanal("[B]CM TV[/B] " + p_umcanal(programas,'CMTV','nomeprog'),empty,16,tvporpath + art + 'cmtv-ver1.png',nrcanais,p_umcanal(programas,'CMTV','descprog'))
    if selfAddon.getSetting("canais-ss5") == "true": canaison.append('[B]Casa dos Segredos 5[/B]'); addCanal("[B]Casa dos Segredos 5[/B] " + p_umcanal(programas,'SEM','nomeprog'),empty,16,tvporpath + art + 'casadseg-ver1.png',nrcanais,p_umcanal(programas,'SEM','descprog'))
    if selfAddon.getSetting("canais-rtpac") == "true": canaison.append('[B]RTP Açores[/B]'); addCanal("[B]RTP Açores[/B] " + p_umcanal(programas,'RTPAC','nomeprog'),empty,16,tvporpath + art + 'rtpac-ver1.png',nrcanais,p_umcanal(programas,'RTPAC','descprog'))
    if selfAddon.getSetting("canais-rtpaf") == "true": canaison.append('[B]RTP Africa[/B]'); addCanal("[B]RTP Africa[/B] " + p_umcanal(programas,'RTPA','nomeprog'),empty,16,tvporpath + art + 'rtpaf-ver1.png',nrcanais,p_umcanal(programas,'RTPA','descprog'))
    if selfAddon.getSetting("canais-rtpi") == "true": canaison.append('[B]RTP Informação[/B]'); addCanal("[B]RTP Informação[/B] " + p_umcanal(programas,'RTPIN','nomeprog'),empty,16,tvporpath + art + 'rtpi-ver1.png',nrcanais,p_umcanal(programas,'RTPIN','descprog'))
    if selfAddon.getSetting("canais-rtpint") == "true": canaison.append('[B]RTP Internacional[/B]'); addCanal("[B]RTP Internacional[/B] " + p_umcanal(programas,'RTPINT','nomeprog'),empty,16,tvporpath + art + 'rtpint-ver1.png',nrcanais,p_umcanal(programas,'RTPINT','descprog'))
    if selfAddon.getSetting("canais-rtpmad") == "true": canaison.append('[B]RTP Madeira[/B]'); addCanal("[B]RTP Madeira[/B] " + p_umcanal(programas,'RTPMD','nomeprog'),empty,16,tvporpath + art + 'rtpmad-ver1.png',nrcanais,p_umcanal(programas,'RTPMD','descprog'))
    if selfAddon.getSetting("canais-rtpmem") == "true": canaison.append('[B]RTP Memória[/B]'); addCanal("[B]RTP Memória[/B] " + p_umcanal(programas,'RTPM','nomeprog'),empty,16,tvporpath + art + 'rtpmem-ver1.png',nrcanais,p_umcanal(programas,'RTPM','descprog'))   
    if selfAddon.getSetting("canais-sick") == "true": canaison.append('[B]SIC K[/B]'); addCanal("[B]SIC K[/B] " + p_umcanal(programas,'SICK','nomeprog'),empty,16,tvporpath + art + 'sick-ver2.png',nrcanais,p_umcanal(programas,'SICK','descprog'))
    if selfAddon.getSetting("canais-sicmulher") == "true": canaison.append('[B]SIC Mulher[/B]'); addCanal("[B]SIC Mulher[/B] " + p_umcanal(programas,'SICM','nomeprog'),empty,16,tvporpath + art + 'sicm-ver3.png',nrcanais,p_umcanal(programas,'SICM','descprog'))
    if selfAddon.getSetting("canais-sicnoticias") == "true": canaison.append('[B]SIC Noticias[/B]'); addCanal("[B]SIC Noticias[/B] " + p_umcanal(programas,'SICN','nomeprog'),empty,16,tvporpath + art + 'sicn-ver2.png',nrcanais,p_umcanal(programas,'SICN','descprog'))
    if selfAddon.getSetting("canais-sicradical") == "true": canaison.append('[B]SIC Radical[/B]'); addCanal("[B]SIC Radical[/B] " + p_umcanal(programas,'SICR','nomeprog'),empty,16,tvporpath + art + 'sicrad-ver2.png',nrcanais,p_umcanal(programas,'SICR','descprog'))
    if selfAddon.getSetting("canais-tvi24") == "true": canaison.append('[B]TVI24[/B]'); addCanal("[B]TVI24[/B] " + p_umcanal(programas,'TVI24','nomeprog'),empty,16,tvporpath + art + 'tvi24-ver2.png',nrcanais,p_umcanal(programas,'TVI24','descprog'))
    if selfAddon.getSetting("canais-tvificcao") == "true": canaison.append('[B]TVI Ficção[/B]'); addCanal("[B]TVI Ficção[/B] " + p_umcanal(programas,'TVIFIC','nomeprog'),empty,16,tvporpath + art + 'tvif-ver2.png',nrcanais,p_umcanal(programas,'TVIFIC','descprog'))
    if selfAddon.getSetting("canais-maistvi") == "true": canaison.append('[B]Mais TVI[/B]'); addCanal("[B]Mais TVI[/B] " + p_umcanal(programas,'SEM','nomeprog'),empty,16,tvporpath + art + 'maistvi-ver2.png',nrcanais,p_umcanal(programas,'SEM','descprog'))
    if selfAddon.getSetting("canais-artv") == "true": canaison.append('[B]ARTV[/B]'); addCanal("[B]ARTV[/B] " + p_umcanal(programas,'ARTV','nomeprog'),empty,16,tvporpath + art + 'artv-ver1.png',nrcanais,p_umcanal(programas,'ARTV','descprog'))
    if selfAddon.getSetting("canais-economico") == "true": canaison.append('[B]Económico TV[/B]'); addCanal("[B]Económico TV[/B] " + p_umcanal(programas,'ETVHD','nomeprog'),empty,16,tvporpath + art + 'econ-v1.png',nrcanais,p_umcanal(programas,'ETVHD','descprog'))
    if selfAddon.getSetting("canais-euronews") == "true": canaison.append('[B]Euronews[/B]'); addCanal("[B]Euronews[/B] " + p_umcanal(programas,'EURN','nomeprog'),empty,16,tvporpath + art + 'euronews-ver1.png',nrcanais,p_umcanal(programas,'EURN','descprog'))
    if selfAddon.getSetting("canais-hollywood") == "true": canaison.append('[B]Hollywood[/B]'); addCanal("[B]Hollywood[/B] " + p_umcanal(programas,'HOLLW','nomeprog'),empty,16,tvporpath + art + 'hwd-ver2.png',nrcanais,p_umcanal(programas,'HOLLW','descprog'))
    if selfAddon.getSetting("canais-mov") == "true": canaison.append('[B]MOV[/B]'); addCanal("[B]MOV[/B] " + p_umcanal(programas,'SEM','nomeprog'),empty,16,tvporpath + art + 'mov-ver2.png',nrcanais,p_umcanal(programas,'SEM','descprog'))
    if selfAddon.getSetting("canais-axn") == "true": canaison.append('[B]AXN[/B]'); addCanal("[B]AXN[/B] " + p_umcanal(programas,'AXN','nomeprog'),empty,16,tvporpath + art + 'axn-ver2.png',nrcanais,p_umcanal(programas,'AXN','descprog'))
    if selfAddon.getSetting("canais-axnblack") == "true": canaison.append('[B]AXN Black[/B]'); addCanal("[B]AXN Black[/B] " + p_umcanal(programas,'AXNBL','nomeprog'),empty,16,tvporpath + art + 'axnb-ver2.png',nrcanais,p_umcanal(programas,'AXNBL','descprog'))
    if selfAddon.getSetting("canais-axnwhite") == "true": canaison.append('[B]AXN White[/B]'); addCanal("[B]AXN White[/B] " + p_umcanal(programas,'AXNWH','nomeprog'),empty,16,tvporpath + art + 'axnw-ver2.png',nrcanais,p_umcanal(programas,'AXNWH','descprog'))
    if selfAddon.getSetting("canais-fox") == "true": canaison.append('[B]FOX[/B]'); addCanal("[B]FOX[/B] " + p_umcanal(programas,'FOX','nomeprog'),empty,16,tvporpath + art + 'fox-ver2.png',nrcanais,p_umcanal(programas,'FOX','descprog'))
    if selfAddon.getSetting("canais-foxcrime") == "true": canaison.append('[B]FOX Crime[/B]'); addCanal("[B]FOX Crime[/B] " + p_umcanal(programas,'FOXCR','nomeprog'),empty,16,tvporpath + art + 'foxc-ver2.png',nrcanais,p_umcanal(programas,'FOXCR','descprog'))
    if selfAddon.getSetting("canais-foxlife") == "true": canaison.append('[B]FOX Life[/B]'); addCanal("[B]FOX Life[/B] " + p_umcanal(programas,'FLIFE','nomeprog'),empty,16,tvporpath + art + 'foxl-ver3.png',nrcanais,p_umcanal(programas,'FLIFE','descprog'))
    if selfAddon.getSetting("canais-foxmovies") == "true": canaison.append('[B]FOX Movies[/B]'); addCanal("[B]FOX Movies[/B] " + p_umcanal(programas,'FOXM','nomeprog'),empty,16,tvporpath + art + 'foxm-ver2.png',nrcanais,p_umcanal(programas,'FOXM','descprog'))
    if selfAddon.getSetting("canais-syfy") == "true": canaison.append('[B]Syfy[/B]'); addCanal("[B]Syfy[/B] " + p_umcanal(programas,'SYFY','nomeprog'),empty,16,tvporpath + art + 'syfy-ver1.png',nrcanais,p_umcanal(programas,'SYFY','descprog'))
    if selfAddon.getSetting("canais-disney") == "true": canaison.append('[B]Disney Channel[/B]'); addCanal("[B]Disney Channel[/B] " + p_umcanal(programas,'DISNY','nomeprog'),empty,16,tvporpath + art + 'disney-ver1.png',nrcanais,p_umcanal(programas,'DISNY','descprog'))
    if selfAddon.getSetting("canais-disneyj") == "true": canaison.append('[B]Disney Junior[/B]'); addCanal("[B]Disney Junior[/B] " + p_umcanal(programas,'DISNYJ','nomeprog'),empty,16,tvporpath + art + 'djun-ver1.png',nrcanais,p_umcanal(programas,'DISNYJ','descprog'))
    if selfAddon.getSetting("canais-cpanda") == "true": canaison.append('[B]Canal Panda[/B]'); addCanal("[B]Canal Panda[/B] " + p_umcanal(programas,'PANDA','nomeprog'),empty,16,tvporpath + art + 'panda-ver2.png',nrcanais,p_umcanal(programas,'PANDA','descprog'))
    if selfAddon.getSetting("canais-pbiggs") == "true": canaison.append('[B]Panda Biggs[/B]'); addCanal("[B]Panda Biggs[/B] " + p_umcanal(programas,'BIGGS','nomeprog'),empty,16,tvporpath + art + 'pbiggs-ver1.png',nrcanais,p_umcanal(programas,'BIGGS','descprog'))
    if selfAddon.getSetting("canais-motors") == "true": canaison.append('[B]Motors TV[/B]'); addCanal("[B]Motors TV[/B] " + p_umcanal(programas,'MOTOR','nomeprog'),empty,16,tvporpath + art + 'motors-ver1.png',nrcanais,p_umcanal(programas,'MOTOR','descprog'))
    if selfAddon.getSetting("canais-chelsea") == "true": canaison.append('[B]Chelsea TV[/B]'); addCanal("[B]Chelsea TV[/B] " + p_umcanal(programas,'CHELS','nomeprog'),empty,16,tvporpath + art + 'chel-v1.png',nrcanais,p_umcanal(programas,'CHELS','descprog'))
    if selfAddon.getSetting("canais-cacapesca") == "true": canaison.append('[B]Caça e Pesca[/B]'); addCanal("[B]Caça e Pesca[/B] " + p_umcanal(programas,'CAÇAP','nomeprog'),empty,16,tvporpath + art + 'cacapesca-v1.png',nrcanais,p_umcanal(programas,'CAÇAP','descprog'))
    if selfAddon.getSetting("canais-torostv") == "true": canaison.append('[B]Toros TV[/B]'); addCanal("[B]Toros TV[/B] " + p_umcanal(programas,'TOROTV','nomeprog'),empty,16,tvporpath + art + 'toros-v1.png',nrcanais,p_umcanal(programas,'TOROTV','descprog'))
    if selfAddon.getSetting("canais-discovery") == "true": canaison.append('[B]Discovery Channel[/B]'); addCanal("[B]Discovery Channel[/B] " + p_umcanal(programas,'DISCV','nomeprog'),empty,16,tvporpath + art + 'disc-ver2.png',nrcanais,p_umcanal(programas,'DISCV','descprog'))
    if selfAddon.getSetting("canais-discturbo") == "true": canaison.append('[B]Discovery Turbo[/B]'); addCanal("[B]Discovery Turbo[/B] " + p_umcanal(programas,'DISCT','nomeprog'),empty,16,tvporpath + art + 'discturbo-v1.png',nrcanais,p_umcanal(programas,'DISCT','descprog'))
    if selfAddon.getSetting("canais-odisseia") == "true": canaison.append('[B]Odisseia[/B]'); addCanal("[B]Odisseia[/B] " + p_umcanal(programas,'ODISS','nomeprog'),empty,16,tvporpath + art + 'odisseia-ver1.png',nrcanais,p_umcanal(programas,'ODISS','descprog'))
    if selfAddon.getSetting("canais-historia") == "true": canaison.append('[B]História[/B]'); addCanal("[B]História[/B] " + p_umcanal(programas,'HIST','nomeprog'),empty,16,tvporpath + art + 'historia-ver1.png',nrcanais,p_umcanal(programas,'HIST','descprog'))
    if selfAddon.getSetting("canais-ngc") == "true": canaison.append('[B]National Geographic Channel[/B]'); addCanal("[B]National Geographic Channel[/B] " + p_umcanal(programas,'NGC','nomeprog'),empty,16,tvporpath + art + 'natgeo-ver1.png',nrcanais,p_umcanal(programas,'NGC','descprog'))
    if selfAddon.getSetting("canais-eurosport") == "true": canaison.append('[B]Eurosport[/B]'); addCanal("[B]Eurosport[/B] " + p_umcanal(programas,'EURSP','nomeprog'),empty,16,tvporpath + art + 'eusp-ver2.png',nrcanais,p_umcanal(programas,'EURSP','descprog'))
    if selfAddon.getSetting("canais-eurosport2") == "true": canaison.append('[B]Eurosport 2[/B]'); addCanal("[B]Eurosport 2[/B] " + p_umcanal(programas,'EURS2','nomeprog'),empty,16,tvporpath + art + 'eusp2-ver1.png',nrcanais,p_umcanal(programas,'EURS2','descprog'))
    if selfAddon.getSetting("canais-espn") == "true": canaison.append('[B]ESPN[/B]'); addCanal("[B]ESPN[/B] " + p_umcanal(programas,'SEM','nomeprog'),empty,16,tvporpath + art + 'espn-ver1.png',nrcanais,p_umcanal(programas,'SEM','descprog'))
    if selfAddon.getSetting("canais-fashion") == "true": canaison.append('[B]Fashion TV[/B]'); addCanal("[B]Fashion TV[/B] " + p_umcanal(programas,'FASH','nomeprog'),empty,16,tvporpath + art + 'fash-ver1.png',nrcanais,p_umcanal(programas,'FASH','descprog'))
    if selfAddon.getSetting("canais-traceu") == "true": canaison.append('[B]TRACE Urban[/B]'); addCanal("[B]TRACE Urban[/B] " + p_umcanal(programas,'TRACE','nomeprog'),empty,16,tvporpath + art + 'traceu.png',nrcanais,p_umcanal(programas,'TRACE','descprog'))
    if selfAddon.getSetting("canais-virginrtv") == "true": canaison.append('[B]Virgin Radio TV[/B]'); addCanal("[B]Virgin Radio TV[/B] " + p_umcanal(programas,'SEM','nomeprog'),empty,16,tvporpath + art + 'virginr.png',nrcanais,p_umcanal(programas,'SEM','descprog'))
    if selfAddon.getSetting("canais-djingtv") == "true": canaison.append('[B]DJing TV[/B]'); addCanal("[B]DJing TV[/B] " + p_umcanal(programas,'SEM','nomeprog'),empty,16,tvporpath + art + 'djingtv.png',nrcanais,p_umcanal(programas,'SEM','descprog'))
    #canaison.append('[B]Clubbing TV[/B]'); addCanal("[B]Clubbing TV[/B] " + p_umcanal(programas,'SEM','nomeprog'),empty,16,tvporpath + art + 'djingtv.png',nrcanais,p_umcanal(programas,'SEM','descprog'))
    if selfAddon.getSetting("canais-vh1") == "true": canaison.append('[B]VH1[/B]'); addCanal("[B]VH1[/B] " + p_umcanal(programas,'VH1','nomeprog'),empty,16,tvporpath + art + 'vh1plus.png',nrcanais,p_umcanal(programas,'VH1','descprog'))
    if selfAddon.getSetting("canais-mtv") == "true": canaison.append('[B]MTV[/B]'); addCanal("[B]MTV[/B] " + p_umcanal(programas,'MTV','nomeprog'),empty,16,tvporpath + art + 'mtv-ver1.png',nrcanais,p_umcanal(programas,'MTV','descprog'))
    if selfAddon.getSetting("canais-tpai") == "true": canaison.append('[B]TPA Internacional[/B]'); addCanal("[B]TPA Internacional[/B] " + p_umcanal(programas,'TPA','nomeprog'),empty,16,tvporpath + art + 'tpa-ver1.png',nrcanais,p_umcanal(programas,'TPA','descprog'))
    if selfAddon.getSetting("canais-tvglobo") == "true": canaison.append('[B]TV Globo[/B]'); addCanal("[B]TV Globo[/B] " + p_umcanal(programas,'GLOBO','nomeprog'),empty,16,tvporpath + art + 'globo-v1.png',nrcanais,p_umcanal(programas,'GLOBO','descprog'))
    if selfAddon.getSetting("canais-tvrecord") == "true": canaison.append('[B]TV Record[/B]'); addCanal("[B]TV Record[/B] " + p_umcanal(programas,'TVREC','nomeprog'),empty,16,tvporpath + art + 'record-v1.png',nrcanais,p_umcanal(programas,'TVREC','descprog'))

    try:
        canaison=''.join(canaison)
        savefile('canaison', canaison)
    except: pass

    vista_canais()
    xbmcplugin.setContent(int(sys.argv[1]), 'livetv')

### SERVERS ###

def info_servidores():
    #tvgentelink= clean(abrir_url_cookie(CanalHDURL,erro=False))
    #print tvgentelink
    #tvgentefinal='\n'.join(re.compile('<h2(.+?)><img src="').findall(tvgentelink))
    #savefile('canalhd', tvgentefinal)
    if selfAddon.getSetting("fontes-tvgente") == "true":
        try:
            tvgentelink= clean(abrir_url_cookie(TVGenteURL + '/front.php',erro=False))
            tvgentefinal='\n'.join(re.compile('onclick="window.open(.+?)/></a>').findall(tvgentelink))
            savefile('tvgente', tvgentefinal)
        except: savefile('tvgente', '')

def request_servidores(url,name,tamanho=0,gravador=False):
    #if name=='[B]Eventos[/B] (Cesarix/Rominhos)':
    #    obter_lista(name,url)
    #    return

    nomelista=name
    name=name.replace('[','-')
    nome=re.compile('B](.+?)/B]').findall(name)[0]
    nomega=nome.replace('-','')
    GA("listacanais",nomega)
    titles=[]; ligacao=[]

    if url=='nada' and activado==True: todosact(nomelista)
    else:


        ### CASOS ESPECIAIS ###

        if re.search('Caça e Pesca',nomelista) or re.search('Toros TV',nomelista):
            titles.append('Pontucanal')
            ligacao.append('http://verlatelegratis.com')

        if re.search('Clubbing TV',nomelista):
            titles.append('Clubbing TV Oficial')
            ligacao.append('http://www.clubbingtv.com/jwsubscribe/clubbing.php')

        if re.search('\[B\]TVI\[/B\]',nomelista):
            titles.append('TVI Oficial')
            ligacao.append('http://www.tvi.iol.pt/direto')

        if re.search('TVI24',nomelista):
            titles.append('TVI Oficial')
            ligacao.append('http://www.tvi.iol.pt/direto/tvi24')

        if re.search('Casa dos Segredos',nomelista):
            titles.append('TVI Oficial')
            ligacao.append('http://www.tvi.iol.pt/secretstory/direto')

        if re.search('TV Globo',nomelista):
            titles.append('Look-TVs')
            ligacao.append('http://look-tvs.com/globo/')
            
        if re.search('TRACE Urban',nomelista):
            titles.append('Trace Oficial')
            ligacao.append('http://www.dailymotion.com/video/x1ahn4f_live-trace-urban_music')

        if re.search('Virgin Radio TV',nomelista):
            titles.append('Virgin Radio TV')
            ligacao.append('stream://http://wow01.105.net/live/virgin1/playlist.m3u8')

        if re.search('DJing TV',nomelista):
            titles.append('DJing TV')
            ligacao.append('stream://http://www.djing.com/tv/noaudio_PT.m3u8')

        if re.search('TPA Internacional',nomelista):
            titles.append('Muntumedia')
            ligacao.append('http://roku.muntumedia.s3.amazonaws.com/playlisttv/T_TPAI.xml')
            titles.append('TPAi Live')
            ligacao.append('http://www.tpai.tv/tpai_rtmp_dynamic_streaming.xml')
        
        #if re.search('Sporting TV',nomelista):
        #    titles.append('Altas Emoções')
        #    ligacao.append(AltasEmocoesURL)

        #if re.search('SPORTTV 1',nomelista) or re.search('SPORTTV 2',nomelista)or re.search('SPORTTV 3',nomelista) or re.search('SPORTTV 4',nomelista) or re.search('SPORTTV 5',nomelista):
            #titles.append('[B]Torrent-TV.RU (acestream)[/B]')
            #ligacao.append('http://api.torrent-tv.ru/t/BgF2xM3fd1KWxgEVO21eprkQPkZi55b0LosbJU8oeZVikr1wPAmjkV%2ByixKZYNGt')

        if re.search('ARTV',nomelista):
            titles.append('ARTV Oficial')
            ligacao.append('http://www.canal.parlamento.pt/h264.html')

        if selfAddon.getSetting("fontes-canalhd") == "true":
            try:
                canalhdref=int(0)
                canalhdlink=openfile('canalhd',pastafinal=cachepath).replace('+','Mais')
                nomecanalhd=nome.replace('RTP 1-','RTP 1').replace('RTP 2-','RTP 2').replace('TVI-','TVI').replace('FOX-','FOX').replace('AXN-','AXN').replace('SIC-','SIC').replace('AXN Black-','AXN Black').replace('AXN White-','AXN White').replace('FOX Life-','FOX Life').replace('FOX Crime-','FOX Crime').replace('FOX Movies-','FOX Movies').replace('SPORTTV 1-','Sportv 1').replace('SPORTTV 2-','Sportv 2').replace('SPORTTV 3-','Sportv 3').replace('SPORTTV 4-','Sportv 4').replace('SPORTTV 5-','Sportv 5').replace('Canal Panda-','Canal Panda').replace('Hollywood-','Canal Hollywood').replace('Eurosport-','Eurosport').replace('MOV-','MOV').replace('VH1-','VH1').replace('Porto Canal-','portocanal').replace('SIC Noticias-','Sic Noticias').replace('SIC Radical-','SIC Radical').replace('SIC Mulher-','SIC Mulher').replace('SIC K-','sick').replace('Big Brother VIP-','bigbrothervip').replace('TVI Ficção-','TVI Ficção').replace('Syfy-','Syfy').replace('Benfica TV 1-','Benfica TV').replace('Benfica TV 2-','Benfica TV').replace('CM TV-','cmtv').replace('RTP Africa-','rtpafrica').replace('RTP Informação-','RTP Informação').replace('Fashion TV-','fashiontv').replace('ESPN-','ESPN').replace('RTP Africa-','rtpafrica').replace('RTP Madeira-','rtpmadeira').replace('RTP Internacional-','rtpinternacional').replace('Casa dos Segredos 5-','casadossegredos').replace('Económico TV-','economicotv').replace('Sporting TV-','Sporting TV').replace('Chelsea TV-','Chelsea TV').replace('TVI24-','TVI 24').replace('Mais TVI-','TVI Mais').replace('MTV-','MTV').replace('História-','Canal História').replace('Odisseia-','Odisseia').replace('Discovery Channel-','Discovery Channel').replace('National Geographic Channel-','National Geographic').replace('Disney Channel-','Disney Channel')
                canalhd=re.compile('>'+nomecanalhd +'</h2><a href="([^"]+?)"').findall(canalhdlink)
                if canalhd:
                    for codigo in canalhd:
                        canalhdref=int(canalhdref + 1)
                        if len(canalhd)==1: canalhd2=str('')
                        else: canalhd2=' #' + str(canalhdref)
                        titles.append('CanalHD.tv' + canalhd2)
                        ligacao.append(CanalHDURL + codigo)
            except: pass


        ########################################DESPORTOGRATIS############################
        if selfAddon.getSetting("fontes-desportogratis") == "true":
            try:
                desgrref=int(0)
                desgrlink=openfile('desgratis',pastafinal=cachepath)
                nomedesgr=nome.replace('SPORTTV 1-','1.html').replace('SPORTTV 2-','2.html').replace('SPORTTV 3-','3.html').replace('SPORTTV 4-','4.html').replace('SPORTTV 5-','4.html').replace('SPORTTV LIVE-','4.html').replace('Benfica TV 1-','5.html').replace('Benfica TV 2-','5.html')
                desgr=re.compile('<a href="http://www.desportogratis.com/'+nomedesgr+'" target="iframe"><form>').findall(desgrlink)
                if desgr:
                    for resto in desgr:
                        desgrref=int(desgrref + 1)
                        if len(desgr)==1:
                            desgr2=str('')
                        else:
                            desgr2=' #' + str(desgrref)
                        titles.append('Desporto Grátis' + desgr2)
                        ligacao.append('http://www.desportogratis.com/' + nomedesgr)
                        
            except: pass

        if selfAddon.getSetting("fontes-meocanaltv") == "true":
            try:
                meocanaltv=False
                meocanaltvref=int(0)
                meocanaltvlink=openfile('meocanaltv',pastafinal=cachepath)
                nomemeocanaltv=nome.replace('RTP 1-','RTP 1').replace('RTP 2-','RTP 2').replace('RTP Informação-','RTP INFORMACAO').replace('RTP Africa-','RTP AFRICA').replace('RTP Madeira-','RTP MADEIRA').replace('RTP Internacional-','RTP INTERNACIONAL').replace('RTP Açores-','RTP ACORES').replace('RTP Memória-','RTP MEMORIA').replace('SIC-','SIC').replace('TVI-','TVI').replace('SPORTTV 1-','Sport TV em Direto').replace('Big Brother VIP-','BB VIP').replace('SIC K-','SIC KIDS').replace('SIC Radical-','SIC RADICAL').replace('SIC Mulher-','SIC MULHER').replace('SIC Noticias-','SIC NOTICIAS Online').replace('TVI24-','TVI 24').replace('Hollywood-','HOLLYWOOD').replace('MOV-','CANAL MOV').replace('AXN-','AXN').replace('AXN Black-','AXN BLACK').replace('AXN White-','AXN WHITE').replace('FOX-','FOX').replace('FOX Crime-','FOX CRIME').replace('FOX Life-','FOX LIFE').replace('FOX Movies-','FOX MOVIES').replace('Canal Panda-','CANAL PANDA').replace('Discovery Channel-','DISCOVERY CHANNEL').replace('Eurosport-','EUROSPORT 1').replace('Benfica TV 1-','Benfica TV online').replace('Benfica TV 2-','Benfica TV online').replace('Porto Canal-','PORTO CANAL').replace('Syfy-','SYFY').replace('Odisseia-','CANAL ODISSEIA').replace('História-','CANAL HISTÓRIA').replace('National Geographic Channel-','NATIONAL GEOGRAPHIC').replace('MTV-','MTV').replace('Disney Channel-','DISNEY CHANNEL').replace('Panda Biggs-','PANDA BIGGS').replace('Motors TV-','MOTORS TV').replace('ESPN-','ESPN Online BR').replace('ESPN America-','ESPN Online BR').replace('A Bola TV-','A BOLA TV').replace('Casa dos Segredos 5-','Secret Story 4 em Direto').replace('CM TV-','CM TV').replace('TVI Ficção-','TVI FICCAO').replace('Panda Biggs-','Panda Biggs').replace('Económico TV-','Económico TV - Emissão Online').replace('Disney Junior-','Canal Disney Junior').replace('TV Record-','Record Online ao Vivo').replace('Discovery Turbo-','Discovery Turbo Brasil').replace('Caça e Pesca-','Caza y Pesca').replace('Mais TVI-','+TVI').replace('Eurosport 2-','EUROSPORT 2')
                meocanaltv=re.compile('"(.+?)">%s<' % (nomemeocanaltv)).findall(meocanaltvlink)
                if meocanaltv:
                    for codigo in meocanaltv:
                        meocanaltvref=int(meocanaltvref + 1)
                        if len(meocanaltv)==1: meocanaltv2=str('')
                        else: meocanaltv2=' #' + str(meocanaltvref)
                        titles.append('MEOCanal TV' + meocanaltv2)
                        ligacao.append(MEOURL + codigo)
            except: pass

        ########################################RTPPLAY############################
        if selfAddon.getSetting("fontes-rtpplay") == "true":
            try:
                rtpplay=False
                rtpplayref=int(0)
                rtpplaylink=openfile('rtpplay',pastafinal=cachepath)
                nomertpplay=nome.replace('RTP 1-','rtp1').replace('RTP 2-','rtp2').replace('RTP Informação-','rtpinformacao').replace('RTP Africa-','rtpafrica').replace('RTP Madeira-','rtpmadeira').replace('RTP Internacional-','rtpinternacional').replace('RTP Açores-','rtpacores').replace('RTP Memória-','rtpmemoria')
                rtpplay=re.compile('id="' + nomertpplay + '" title=".+?" href="(.+?)">').findall(rtpplaylink)
                if rtpplay:
                    for codigo in rtpplay:
                        rtpplayref=int(rtpplayref + 1)
                        if len(rtpplay)==1: rtpplay2=str('')
                        else: rtpplay2=' #' + str(rtpplayref)
                        titles.append('RTP Play' + rtpplay2)
                        ligacao.append(RTPURL + codigo)
            except: pass

        ########################################TV A CORES############################
        if selfAddon.getSetting("fontes-tvacores") == "true":
            try:
                tvacoresref=int(0)
                tvacoreslink=openfile('tvacores',pastafinal=cachepath)
                nometvacores=nome.replace('RTP 1-','RTP 1 Online').replace('RTP 2-','RTP 2 Online').replace('SIC-','SIC Online').replace('TVI-','TVI Online').replace('SPORTTV 1-','Sport TV em Direto').replace('Big Brother VIP-','BB VIP').replace('SIC K-','SIC K Online').replace('SIC Radical-','SIC Radical Online').replace('SIC Mulher-','SIC Mulher Online').replace('SIC Noticias-','SIC Noticias Online').replace('TVI24-','TVI24 online').replace('Hollywood-','Canal Hollywood').replace('MOV-','Canal MOV').replace('AXN-','AXN Portugal').replace('AXN Black-','AXN Black Online').replace('AXN White-','AXN White online').replace('FOX-','Fox Online PT').replace('FOX Crime-','FOX Crime Online').replace('FOX Life-','FOX Life Online').replace('FOX Movies-','FOX Movies Portugal').replace('Canal Panda-','Canal Panda').replace('Discovery Channel-','Discovery Channel PT').replace('Eurosport-','Eurosport Portugal').replace('Benfica TV 1-','Benfica TV online').replace('Benfica TV 2-','Benfica TV online').replace('Porto Canal-','Porto Canal - Emissão Online').replace('Syfy-','SYFY Channel Portugal').replace('Odisseia-','Canal Odisseia').replace('História-','Canal Historia Portugal').replace('National Geographic Channel-','National Geographic PT').replace('MTV-','MTV Portugal').replace('RTP Açores-','RTP Açores Online').replace('RTP Africa-','RTP África Online').replace('RTP Informação-','RTP Informação - Emissão Online').replace('RTP Madeira-','RTP Madeira Online').replace('RTP Memória-','RTP Memória').replace('Disney Channel-','Disney Portugal').replace('Panda Biggs-','Panda Biggs').replace('Motors TV-','Motors TV Online').replace('ESPN-','ESPN Online BR').replace('ESPN America-','ESPN Online BR').replace('A Bola TV-','A Bola TV').replace('RTP Africa-','RTP Africa').replace('RTP Madeira-','RTP Madeira').replace('RTP Internacional-','RTP Internacional').replace('RTP Açores-','RTP Açores').replace('A Bola TV-','A Bola TV').replace('Casa dos Segredos 5-','A Casa dos Segredos').replace('CM TV-','CMTV em direto').replace('TVI Ficção-','TVI Ficção online').replace('Panda Biggs-','Panda Biggs').replace('Económico TV-','Económico TV - Emissão Online').replace('Disney Junior-','Canal Disney Junior').replace('TV Record-','Record Online ao Vivo').replace('Discovery Turbo-','Discovery Turbo Brasil').replace('Caça e Pesca-','Caza y Pesca').replace('Sporting TV-','Sporting TV online')
                tvacores=re.compile('<a href="(.*?)">'+nometvacores+'</a>').findall(tvacoreslink)
                if tvacores:
                    for codigo in tvacores:
                        tvacoresref=int(tvacoresref + 1)
                        if len(tvacores)==1: tvacores2=str('')
                        else: tvacores2=' #' + str(tvacoresref)
                        titles.append('TV a Cores' + tvacores2)
                        ligacao.append(TVCoresURL + codigo)
            except: pass
                  
        ########################################TUGASTREAM############################
        if selfAddon.getSetting("fontes-tugastream") == "true":
            try:
                tugastreamref=int(0)
                tugastreamlink=openfile('tugastream',pastafinal=cachepath)
                nometugastream=nome.replace('RTP 1-','rtp1').replace('RTP 2-','rtp2').replace('TVI-','tvi').replace('FOX-','fox').replace('AXN-','axn').replace('SIC-','sic').replace('AXN Black-','axnblack').replace('AXN White-','axnwhite').replace('FOX Life-','foxlife').replace('FOX Crime-','foxcrime').replace('FOX Movies-','foxmovies').replace('SPORTTV 1-','sporttv1').replace('SPORTTV 2-','sporttv2').replace('SPORTTV 3-','sporttv3').replace('SPORTTV 4-','sporttv4').replace('SPORTTV 5-','sporttv5').replace('Canal Panda-','panda').replace('Hollywood-','hollywood').replace('Eurosport-','eurosport').replace('MOV-','mov').replace('VH1-','vh1').replace('Porto Canal-','portocanal').replace('SIC Noticias-','sicnoticias').replace('SIC Radical-','sicradical').replace('SIC Mulher-','sicmulher').replace('SIC K-','sick').replace('Big Brother VIP-','bigbrothervip').replace('TVI Ficção-','tvificcao').replace('Syfy-','syfy').replace('Benfica TV 1-','benficatv').replace('Benfica TV 2-','benficatv').replace('CM TV-','cmtv').replace('RTP Africa-','rtpafrica').replace('RTP Informação-','rtpinformacao').replace('Fashion TV-','fashiontv').replace('ESPN-','espn').replace('RTP Africa-','rtpafrica').replace('RTP Madeira-','rtpmadeira').replace('RTP Internacional-','rtpinternacional').replace('Casa dos Segredos 5-','casadossegredos').replace('Económico TV-','economicotv')
                tugastream=re.compile('<a href="'+nometugastream + '(.+?)php">').findall(tugastreamlink)
                if tugastream:
                    for codigo in tugastream:
                        tugastreamref=int(tugastreamref + 1)
                        if len(tugastream)==1: tugastream2=str('')
                        else: tugastream2=' #' + str(tugastreamref)
                        titles.append('Tugastream' + tugastream2)
                        ligacao.append(TugastreamURL + nometugastream + codigo + 'php?altura=432&largura=768')
            except: pass

        ########################################TVGENTE############################
        if selfAddon.getSetting("fontes-tvgente") == "true":
            try:
                tvgenteref=int(0)
                tvgentelink=openfile('tvgente')
                nometvgente=nome.replace('SPORTTV 1-','sptv1novo.png').replace('SPORTTV 2-','sptv2novo.png').replace('SPORTTV 3-','sptv3novo.png').replace('SPORTTV 4-','jogooo.png').replace('SPORTTV 5-','sptv511.png').replace('Eurosport-','eurosportnovo.png').replace('Eurosport 2-','eurosport2novo.png').replace('ESPN-','espnnovo.png').replace('RTP 1-','1rtp.png').replace('RTP 2-','rtp2novo.png').replace('RTP Informação-','rtpinfonovo.png').replace('RTP Internacional-','rtp intnovo.png').replace('RTP Memória-','memoriartpnovo.png').replace('RTP Açores-','acoresnovortp.png').replace('RTP Madeira-','madeirartpnovo.png').replace('SIC-','sicnovo.png').replace('SIC Noticias-','sicnnovo.png').replace('TVI-','tvinovo.png').replace('TVI24-','tvi24novo.png').replace('Porto Canal-','portonovo.png').replace('Benfica TV 1-','btvnovo.png').replace('Benfica TV 2-','btvnovo.png').replace('Sporting TV-','sportingtv.png').replace('A Bola TV-','biolatv.png').replace('CM TV-','cmtv.png').replace('Económico TV-','ecnovo.png').replace('FOX-','foxnovo.png').replace('Discovery Channel-','discnovo.png').replace('História-','historia').replace('Casa dos Segredos 5-','casa do putedo1.jpg')
                tvgente=re.compile("\('(.+?)'.+?<img.+?" +nometvgente + '"').findall(tvgentelink)
                nometvgente=nome.replace('SPORTTV 1-','miga1.png').replace('SPORTTV 2-','miga2.png').replace('SPORTTV 3-','miga3.png').replace('SPORTTV 4-','miga 4.png').replace('SPORTTV 5-','miga5.png').replace('Benfica TV 1-','btv11.png').replace('Benfica TV 2-','btv11.png').replace('SIC Noticias-','hd1sic.png').replace('Sporting TV-','testesporting.png')
                tvgente+=re.compile("\('(.+?)'.+?<img.+?" +nometvgente + '"').findall(tvgentelink)
                if tvgente:
                    for codigo in tvgente:
                        tvgenteref=int(tvgenteref + 1)
                        if len(tvgente)==1: tvgente2=str('')
                        else: tvgente2=' #' + str(tvgenteref)
                        titles.append('TV Gente' + tvgente2)
                        ligacao.append(codigo)
            except: pass

        #if re.search('SPORTTV 1 HD',nomelista) or re.search('SPORTTV 1',nomelista):
        #    titles.append('TVGO.be')
        #    ligacao.append(TVGOURL)

        #if re.search('SPORTTV 2',nomelista):
        #    titles.append('TVGO.be')
        #    ligacao.append(TVGOURL + 'sport2.html')


        ########################################TVTUGA############################
        if selfAddon.getSetting("fontes-tvtuga") == "true":
            try:
                tvtugaref=int(0)
                tvtugalink=openfile('tvtuga',pastafinal=cachepath)
                
                nometvtuga=nome.replace('RTP 1-','rtp-1').replace('RTP 2-','rtp-2').replace('TVI-','tvi').replace('FOX-','fox').replace('AXN-','axn').replace('SIC-','sic').replace('AXN Black-','axnblack').replace('AXN White-','axn-white').replace('FOX Life-','fox-life').replace('FOX Crime-','fox-crime').replace('FOX Movies-','fox-movies').replace('SPORTTV 1-','sporttv1').replace('SPORTTV 2-','sporttv2').replace('SPORTTV 3-','sporttv3').replace('SPORTTV 4-','sporttvlive').replace('SPORTTV LIVE-','sporttvlive').replace('Canal Panda-','canal-panda').replace('Hollywood-','canal-hollywood').replace('Eurosport-','eurosport').replace('MOV-','mov').replace('VH1-','vh1').replace('Porto Canal-','portocanal').replace('SIC Noticias-','sic-noticias').replace('SIC Radical-','sicradical').replace('SIC Mulher-','sicmulher').replace('SIC K-','sick').replace('Big Brother VIP-','bigbrothervip').replace('TVI Ficção-','tvi-ficcao').replace('Syfy-','syfy').replace('Benfica TV 1-','benfica-tv').replace('Benfica TV 2-','benfica-tv').replace('CM TV-','cm-tv').replace('RTP Africa-','rtp-africa').replace('RTP Informação-','rtp-informacao').replace('Fashion TV-','fashiontv').replace('ESPN-','espn').replace('A Bola TV-','abola-tv').replace('Casa dos Segredos 4-','secret-story-4-casa-dos-segredos').replace('RTP Açores-','rtp-acores').replace('RTP Internacional-','rtp-internacional').replace('RTP Madeira-','rtp-madeira').replace('RTP Memória-','rtp-memoria').replace('TVI24-','tvi-24').replace('Panda Biggs-','panda-biggs').replace('Económico TV-','economico-tv').replace('Eurosport 2-','eurosport-2').replace('Casa dos Segredos 5-','secret-story-5').replace('Euronews-','euronews')

                tvtuga=re.compile('value="http://www.tvtuga.com/'+nometvtuga+'(.+?)">').findall(tvtugalink)
                if tvtuga:
                    for codigo in tvtuga:
                        tvtugaref=int(tvtugaref + 1)
                        if len(tvtuga)==1: tvtuga2=str('')
                        else: tvtuga2=' #' + str(tvtugaref)
                        titles.append('TVTuga' + tvtuga2)
                        ligacao.append(TVTugaURL + '/' + nometvtuga + codigo)
            except: pass

                
        ########################################TVDEZ############################
        if selfAddon.getSetting("fontes-tvdez") == "true":
            try:
                tvdezref=int(0)
                tvdezlink=openfile('tvdez',pastafinal=cachepath)
                tvdezlink=tvdezlink.replace('+ TVI','Mais TVI')
                nometvdez=nome.replace('RTP 1-','RTP').replace('RTP 2-','RTP 2').replace('FOX-','FOX').replace('AXN-','AXN').replace('AXN Black-','AXN Black').replace('AXN White-','AXN White').replace('FOX Life-','FOX Life').replace('FOX Crime-','FOX Crime').replace('FOX Movies-','FOX Movies').replace('SPORTTV 3-','Sport TV 3').replace('SPORTTV 4-','Sport TV 4').replace('SPORTTV 5-','Sport TV 5').replace('SPORTTV LIVE-','Sporttv Live').replace('Canal Panda-','Canal Panda').replace('Hollywood-','Hollywood').replace('Eurosport-','Eurosport').replace('MOV-','Canal MOV').replace('VH1-','VH1 Hits').replace('Porto Canal-','Porto Canal').replace('SIC Radical-','SIC Radical').replace('SIC Mulher-','SIC Mulher').replace('SIC K-','SIC K').replace('TVI Ficção-','TVI Fic&ccedil;&atilde;o').replace('Discovery Channel-','Discovery Channel').replace('TVI24-','TVI 24').replace('Mais TVI-','Mais TVI').replace('Syfy-','Syfy').replace('Odisseia-','Odisseia').replace('História-','Hist&oacute;ria').replace('National Geographic Channel-','National Geographic').replace('MTV-','MTV').replace('CM TV-','Correio da Manh&atilde; TV').replace('RTP Açores-','RTP A&ccedil;ores').replace('RTP Informação-','RTP Informa&ccedil;&atilde;o').replace('RTP Madeira-','RTP Madeira').replace('RTP Memória-','RTP Mem&oacute;ria').replace('Disney Channel-','Disney Channel').replace('Fashion TV-','Fashion TV').replace('Disney Junior-','Disney Junior').replace('Panda Biggs-','Panda Biggs').replace('Motors TV-','Motors TV').replace('ESPN-','ESPN Brasil').replace('ESPN America-','ESPN').replace('A Bola TV-','A Bola TV').replace('RTP Africa-','RTP Africa').replace('RTP Madeira-','RTP Madeira').replace('RTP Internacional-','RTP Internacional').replace('RTP Memória-','RTP Mem&oacute;ria').replace('RTP Açores-','RTP A&ccedil;ores').replace('Panda Biggs-','Panda Biggs').replace('Económico TV-','Econ&oacute;mico TV').replace('Chelsea TV-','Chelsea TV').replace('Disney Junior-','Disney Junior').replace('TV Globo-','TV Globo').replace('TV Record-','Rede Record').replace('Eurosport 2-','Eurosport 2').replace('Euronews-','EuroNews')
                tvdez=re.compile('<a href="(.+?)" title="'+nometvdez+'">').findall(tvdezlink)
                if not tvdez:
                    nometvdez=nome.replace('SPORTTV 1-','Sport TV 1').replace('SPORTTV 2-','Sport TV 2').replace('SIC-','SIC').replace('TVI-','TVI').replace('SIC Noticias-','SIC Not&iacute;cias').replace('Big Brother VIP-','Big Brother VIP 2013').replace('Benfica TV 1-','Benfica TV').replace('Benfica TV 2-','Benfica TV').replace('Casa dos Segredos 5-','Casa dos segredos 5 - TVI Direct')
                    tvdez=re.compile('<a href="(.+?)" title="'+nometvdez+'">').findall(tvdezlink)
                    nometvdez=nome.replace('SPORTTV 1-','Sporttv em Directo').replace('SPORTTV 2-','Sporttv 2').replace('SIC-','SIC Online - Stream 2').replace('TVI-','TVI Online - Stream 2').replace('SIC Noticias-','SIC Not&iacute;cias Online').replace('Big Brother VIP-','Big Brother Portugal').replace('Benfica TV 1-','Benfica-TV').replace('Benfica TV 2-','Benfica-TV').replace('Casa dos Segredos 5-','Secret Story 5')
                    tvdez+=re.compile('<a href="(.+?)" title="'+nometvdez+'">').findall(tvdezlink)
                    nometvdez=nome.replace('SPORTTV 1-','Sporttv HD')
                    tvdez+=re.compile('<a href="(.+?)" title="'+nometvdez+'">').findall(tvdezlink)
                if tvdez:
                    for codigo in tvdez:
                        tvdezref=int(tvdezref + 1)
                        if len(tvdez)==1: tvdez2=str('')
                        else: tvdez2=' #' + str(tvdezref)
                        titles.append('TVDez' + tvdez2)
                        ligacao.append(TVDezURL + codigo)
            except: pass


        ########################################TVZUNE############################
        if selfAddon.getSetting("fontes-tvzune2") == "true" and activado==False:
            try:
                tvzuneref=int(0)
                #tvzunelink=openfile('tvzune',pastafinal=cachepath)
                tvzunelink=openfile('tvzune2',pastafinal=cachepath)

                nometvzune=nome.replace('RTP 1-','RTP 1').replace('RTP 2-','RTP 2').replace('SIC-','SIC').replace('SPORTTV 1-','SPORT TV 1').replace('SPORTTV 2-','SPORT TV 2').replace('SPORTTV 3-','SPORT TV 3').replace('TVI-','TVI').replace('FOX-','FOX').replace('AXN-','AXN').replace('Discovery Channel-','discovery').replace('AXN Black','axnblack').replace('AXN White-','axnwhite').replace('FOX Life-','foxlife').replace('FOX Crime-','foxcrime').replace('FOX Movies-','foxmovies').replace('Canal Panda-','panda').replace('Hollywood-','hollywood').replace('Eurosport-','eurosport').replace('MOV-','mov').replace('VH1-','vh1').replace('TVI24-','tvi24').replace('SIC Noticias-','sicnoticias').replace('SIC Radical-','sicradical').replace('SIC Mulher-','sicmulher').replace('SIC K-','sick').replace('Big Brother VIP-','bigbrothervip').replace('TVI Ficção-','tvificcao').replace('Sporting TV-','sportingtv')
                tvzune=re.compile("channel.php\?ch=(.+?)'.+?<span>" + nometvzune + "</span>").findall(tvzunelink)

                nometvzune=nome.replace('RTP 1-','checkrtp1').replace('RTP 2-','checkrtp2').replace('FOX-','checkfox').replace('AXN-','checkaxn').replace('AXN Black-','checkaxnblack').replace('AXN White-','checkaxnwhite').replace('FOX Life-','checkfoxlife').replace('FOX Crime-','checkfoxcrime').replace('FOX Movies-','checkfoxmovies').replace('SPORTTV 1 HD-','checkpremiumsporttv1').replace('SPORTTV 3-','checkpremiumsporttv3').replace('SPORTTV 4-','checkpremiumsporttv4').replace('SPORTTV 5-','checkpremiumsporttv5').replace('SPORTTV LIVE-','checksporttv4').replace('Canal Panda-','checkpanda').replace('Hollywood-','checkhollywood').replace('MOV-','checkmov').replace('Porto Canal-','checkporto').replace('SIC Radical-','checksicradical').replace('SIC Mulher-','checksicmulher').replace('TVI Ficção-','checktvific').replace('Benfica TV 1-','checkbenficatv').replace('Benfica TV 2-','checkbenficatv2').replace('Discovery Channel-','checkdiscovery').replace('TVI24-','checktvi24').replace('Mais TVI-','checktvimais').replace('Syfy-','checksyfy').replace('Odisseia-','checkodisseia').replace('História-','checkhistoria').replace('National Geographic Channel-','checknational').replace('MTV-','checkmtv').replace('RTP Açores-','checkrtpa').replace('RTP Informação-','checkrtpi').replace('Disney Channel-','checkdisney').replace('Motors TV-','checkmotors').replace('A Bola TV-','checkbolatv').replace('SPORTTV 1-','checkpremiumsporttv1').replace('SPORTTV 2-','checkpremiumsporttv2').replace('SIC-','checksic').replace('TVI-','checktvi').replace('SIC Noticias-','checksicnoticias').replace('Económico TV-','checkeconomico').replace('Sporting TV-','checksportingtv').replace('TV Globo-','checkglobo')
                tvzuneextra=openfile('tvzune2',pastafinal=cachepath)
                if tvzuneextra and re.search('check',nometvzune):
                    tvzuneref=int(tvzuneref + 1)
                    if len(tvzune)==0: tvzune2=str('')
                    else: tvzune2=' #' + str(tvzuneref)
                    nometvzune=nometvzune.replace('check','')
                    titles.append('TVZune' + tvzune2)
                    ligacao.append(TVZune2URL + 'new/canais/' + nometvzune + '.txt')
                
                if tvzune:
                    for resto in tvzune:
                        tvzuneref=int(tvzuneref + 1)
                        if len(tvzune)==1 and len(titles)==0: tvzune2=str('')
                        else: tvzune2=' #' + str(tvzuneref)
                        titles.append('TVZune' + tvzune2)
                        ligacao.append(TVZuneURL + 'iframe/channel.php?ch=' + resto)
                
            except: pass  
        
        if len(ligacao)==1: index=0
        elif activado==True: index=0
        elif len(ligacao)==0: ok=mensagemok('TV Portuguesa', 'Nenhum stream disponivel.'); return
        else: index = xbmcgui.Dialog().select('Escolha o servidor', titles)
        if index > -1:
            if activado==False:
                mensagemprogresso.create('TV Portuguesa', 'A carregar stream. (' + titles[index] + ')','Por favor aguarde...')
                mensagemprogresso.update(0)
                if mensagemprogresso.iscanceled(): mensagemprogresso.close()
                pre_resolvers(titles,ligacao,index,nome,zapping=gravador)
            else:
                index=-1
                
                for linkescolha in ligacao:
                    index=index+1
                    pre_resolvers(titles,ligacao,index,nome,tamanho=tamanho,zapping=gravador)
                    
                activadoextra2=set(activadoextra)
                thumb=nome.replace('Mais TVI-','maistvi-ver2.png').replace('AXN-','axn-ver2.png').replace('FOX-','fox-ver2.png').replace('RTP 1-','rtp1-ver2.png').replace('RTP 2-','rtp2-ver2.png').replace('SIC-','sic-ver3.png').replace('SPORTTV 1-','sptv1-ver2.png').replace('SPORTTV 1 HD-','sptvhd-ver2.png').replace('SPORTTV 2-','sptv2-ver2.png').replace('SPORTTV 3-','sptv3-ver2.png').replace('SPORTTV 4-','sptv4-ver2.png').replace('SPORTTV LIVE-','sptvlive-ver1.png').replace('TVI-','tvi-ver2.png').replace('Discovery Channel-','disc-ver2.png').replace('AXN Black-','axnb-ver2.png').replace('AXN White-','axnw-ver2.png').replace('FOX Crime-','foxc-ver2.png').replace('FOX Life-','foxl-ver3.png').replace('FOX Movies-','foxm-ver2.png').replace('Eurosport-','eusp-ver2.png').replace('Hollywood-','hwd-ver2.png').replace('MOV-','mov-ver2.png').replace('Canal Panda-','panda-ver2.png').replace('VH1-','vh1-ver2.png').replace('Benfica TV 1-','btv1-ver1.png').replace('Benfica TV 2-','btv2-ver1.png').replace('Porto Canal-','pcanal-ver2.png').replace('Big Brother VIP-','bbvip-ver2.png').replace('SIC K-','sick-ver2.png').replace('SIC Mulher-','sicm-ver3.png').replace('SIC Noticias-','sicn-ver2.png').replace('SIC Radical-','sicrad-ver2.png').replace('TVI24-','tvi24-ver2.png').replace('TVI Ficção-','tvif-ver2.png').replace('Syfy-','syfy-ver1.png').replace('Odisseia-','odisseia-ver1.png').replace('História-','historia-ver1.png').replace('National Geographic Channel-','natgeo-ver1.png').replace('MTV-','mtv-ver1.png').replace('CM TV-','cmtv-ver1.png').replace('RTP Informação-','rtpi-ver1.png').replace('Disney Channel-','disney-ver1.png').replace('Motors TV-','motors-ver1.png').replace('ESPN America-','espna-ver1.png').replace('Fashion TV-','fash-ver1.png').replace('A Bola TV-','abola-ver1.png').replace('Casa dos Segredos 5-','casadseg-ver1.png').replace('RTP Açores-','rtpac-ver1.png').replace('RTP Internacional-','rtpint-ver1.png').replace('RTP Madeira-','rtpmad-ver1.png').replace('RTP Memória-','rtpmem-ver1.png').replace('RTP Africa-','rtpaf-ver1.png').replace('Panda Biggs-','pbiggs-ver1.png').replace('TV Record-','record-v1.png').replace('TV Globo-','globo-v1.png').replace('Eurosport 2-','eusp2-ver1.png').replace('Discovery Turbo-','discturbo-v1.png').replace('Toros TV-','toros-v1.png').replace('Chelsea TV-','chel-v1.png').replace('Disney Junior-','djun-ver1.png').replace('Económico TV-','econ-v1.png').replace('Caça e Pesca-','cacapesca-v1.png').replace('TPA Internacional-','tpa-ver1.png').replace('TRACE Urban-','traceu.png').replace('Virgin Radio TV-','virginr.png').replace('DJing TV-','djingtv.png')
                
                nome=nome.replace('-','')
                SIM='</link>\n<link>'.join(activadoextra2)
                if SIM=='':
                    return ''
                else:
                    SIM='<link>%s</link>' % (SIM)
                    if thumb=='tvif-ver2.png':nome='TVI Ficcao'
                    elif thumb=='historia-ver1.png': nome='Historia'
                    elif thumb=='rtpac-ver1.png': nome='RTP Acores'
                    elif thumb=='rtpi-ver1.png': nome='RTP Informacao'
                    elif thumb=='rtpmem-ver1.png': nome='RTP Memoria'
                    elif thumb=='econ-v1.png': nome='Economico TV'
                    elif thumb=='cacapesca-v1.png': nome='Caca e Pesca'
                    CONTEUDO='<item>\n<title>%s</title>\n%s\n<thumbnail>%s</thumbnail>\n</item>' % (nome,SIM,thumb)
                return CONTEUDO
                    

                
def todosact(parametro):
    LOLI=['<item>\n<title>Actualizado: ' + horaportuguesa(True).replace('%20',' ') + '</title>\n<link>nada</link>\n<thumbnail>nada</thumbnail>\n</item>']
    dialog = xbmcgui.Dialog()
    mensagemprogresso.create('TV Portuguesa', 'A criar lista.','Por favor aguarde...')
    if re.search('Lista Completa',parametro):
        canaison=openfile(('canaison'))
        canaison=canaison.replace('[','')
        lista=re.compile('B](.+?)/B]').findall(canaison)
        tamanhototal=int(len(lista))
        tamanho=int(-1)
        for nomes in lista:
            tamanho=tamanho+1
            tamanhoenviado=(tamanho*100)/tamanhototal
            print "Lista completa: Canal " + nomes
            global activadoextra
            activadoextra=[]
            SIM=request_servidores('ignore','[B]' + nomes + '[/B]',tamanho=tamanhoenviado)
            LOLI.append(SIM)
            AGORA='\n\n'.join(LOLI)
    else:
        SIM=request_servidores('ignore',parametro)
        LOLI.append(SIM)
        AGORA='\n\n'.join(LOLI)
    
    mensagemprogresso.close()

    debugfinal='\n'.join(debug)
    savefile('problema',debugfinal)
    
    keyb = xbmc.Keyboard('', 'Nome do ficheiro da lista')
    keyb.doModal()
    if (keyb.isConfirmed()):
        nomelista = keyb.getText()
        if nomelista=='': nomelista='lista'
    else: nomelista='lista'
    pastafinal = dialog.browse(int(0), "Local para guardar xml/m3u", 'myprograms')
    if not pastafinal: sys.exit(0)
    savefile(nomelista + '.xml',AGORA,pastafinal=pastafinal)
    m3uprep=['#EXTM3U#EXTM3U']
    openedfile=clean(AGORA)
    ya=re.compile('<item>(.+?)</item>').findall(openedfile)
    for lol in ya:
        chname=re.compile('<title>(.+?)</title>').findall(lol)[0]
        allstreams=False
        if allstreams==True:
            streams=re.compile('<link>(.+?)</link>').findall(lol)
            for umporum in streams:
                m3uprep.append('\n#EXTINF:-1,%s\n%s' % (chname,umporum))
        else:
            streams=re.compile('<link>(.+?)</link>').findall(lol)[0]
            m3uprep.append('\n#EXTINF:-1,%s\n%s' % (chname,streams))
    m3uprep='\n'.join(m3uprep)
    savefile(nomelista + '.m3u',m3uprep,pastafinal=pastafinal)
    xbmc.executebuiltin("XBMC.Notification(TV Portuguesa, Lista xml/m3u gravada,'100000'," + tvporpath + art + "icon32-ver1.png)")

def pre_resolvers(titles,ligacao,index,nome,tamanho=0,zapping=False):
    #import buggalo
    #buggalo.SUBMIT_URL = 'http://fightnight.pusku.com/exceptions/submit.php'
    marcador='A iniciar pre resolvers'
    try:
        sys.argv[2]=sys.argv[2]+ titles[index]
        if activado==True: mensagemprogresso.update(tamanho,'A criar lista. ' + nome+ ' ' + titles[index],'Por favor aguarde...')
        
        nomeserver=nome.replace('ç','c').replace('ã','a').replace('ó','o') + ' ' + titles[index]
        linkescolha=ligacao[index]
        if linkescolha:
            if re.search('api.torrent-tv.ru',linkescolha):
                marcador="Pre-catcher: torrent-tv"; print marcador
                if xbmc.getCondVisibility("System.HasAddon(plugin.video.p2p-streams)"):
                    link=clean(abrir_url_cookie(linkescolha))
                    if re.search('SPORTTV 1',nome): hname='Sport TV 1'
                    elif re.search('SPORTTV 2',nome): hname='Sport TV 2'
                    elif re.search('SPORTTV 3',nome): hname='Sport TV 3'
                    elif re.search('SPORTTV 4',nome): hname='Sport TV 4'
                    elif re.search('SPORTTV 5',nome): hname='Sport TV 5'
                    else: hname='non'
                    streamurl='plugin://plugin.video.p2p-streams/?url='+re.compile(hname+'.+?acestream://(.+?)#').findall(link)[0]+'&mode=1&name='+name
                    comecarvideo(streamurl,name,True,zapping)
                else:
                    if activado==False: mensagemok('TV Portuguesa','Precisa de instalar o addon p2p-streams!','Veja aqui como fazer:','http://bit.ly/p2p-instalar')
                
            elif re.search('estadiofutebol',linkescolha):
                marcador="Pre-catcher: tvdez"; print marcador
                link=abrir_url_cookie(linkescolha,forcedns=True)
                if re.search('televisaofutebol',link):
                    codigo=re.compile('<iframe src="http://www.televisaofutebol.com/([^"]+?)"').findall(link)[0]
                    embed='http://www.televisaofutebol.com/' + codigo
                    ref_data = {'Referer': 'http://www.estadiofutebol.com','User-Agent':user_agent}
                    html= abrir_url_tommy(embed,ref_data)
                    descobrirresolver(embed,nome,html,zapping,nomeserver)
                else:descobrirresolver(linkescolha, nome,False,zapping,nomeserver)

            elif re.search('tugastream',linkescolha):
                marcador="Pre-catcher: tugastream"; print marcador
                link=abrir_url_cookie(linkescolha,forcedns=True)
                descobrirresolver(linkescolha, nome,False,zapping,nomeserver)

            elif re.search('altas-emocoes',linkescolha):
                marcador="Pre-catcher: altas emocoes /sporting"; print marcador
                link=abrir_url(linkescolha)
                frame=re.compile('<a href="/([^"]+?)" target="_blank">SPORTING TV.+?</td>').findall(link)[0]
                ref_data = {'Referer': linkescolha,'User-Agent':user_agent}
                frame1=AltasEmocoesURL + frame
                link= abrir_url_tommy(frame1,ref_data)
                frame2='http://www.livesportshd.eu/' + re.compile('src="http://www.livesportshd.eu/([^"]+?)"').findall(link)[0]
                ref_data = {'Referer': frame1,'User-Agent':user_agent}
                
                link= abrir_url_tommy(frame2,ref_data)
                #frame=re.compile("src='(.+?)'").findall(link)[0]
                #ref_data = {'Referer': frame2,'User-Agent':user_agent}
                #link= abrir_url_tommy(frame,ref_data)
                descobrirresolver(frame2, nome,link,zapping,nomeserver)

            elif re.search('verlatelegratis',linkescolha):
                marcador="Pre-catcher: verlatelegratis"; print marcador
                temporary=''
                link=abrir_url(linkescolha)
                listacanais=re.compile('<center><iframe.+?src="(.+?)"').findall(link)[0]
                link=abrir_url(listacanais)
                canais=re.compile("javascript:popUp\('(.+?)'").findall(link)
                for temp in canais:
                    if re.search('toro',temp) and re.search('Toros TV',nome):temporary=temp
                    if re.search('pesca',temp) and re.search('Caça e Pesca',nome) :temporary=temp
                if temporary!='':
                    if re.search('http://',temporary): baseurl=temporary
                    else:baseurl='/'.join(listacanais.split('/')[:-1]) + temporary
                    ref_data = {'Referer': listacanais,'User-Agent':user_agent}
                    link= abrir_url_tommy(baseurl,ref_data)
                    urlfinal=re.compile('<iframe.+?src="(.+?)"').findall(link)[0]
                    ref_data = {'Referer': baseurl,'User-Agent':user_agent}
                    link= abrir_url_tommy(urlfinal,ref_data)
                    descobrirresolver(urlfinal, nome,link,zapping,nomeserver)

            elif re.search('meocanaltv',linkescolha):
                marcador="Pre-catcher: meocanaltv"; print marcador
                embed=linkescolha.replace('canais.php?stream=','embed/') + '.php?width=600&height=450'
                ref_data = {'Referer': linkescolha,'User-Agent':user_agent}
                #html= abrir_url_tommy(embed,ref_data)
                from resources.lib import cloudflare
                html=cloudflare.webpage_request(embed)
                if re.search('embedsecure.js',html):
                    html+=abrir_url_tommy(re.compile('src="([^"]+?)embedsecure.js"').findall(html)[0] + 'embedsecure.js',ref_data).decode('string-escape')
                descobrirresolver(embed,nome,html,zapping,nomeserver)
                
            elif re.search('tvfree',linkescolha):
                marcador="Pre-catcher: tv a cores"; print marcador
                ref_data = {'Referer': TVCoresURL,'User-Agent':user_agent}
                from resources.lib import cloudflare
                link=cloudflare.webpage_request(linkescolha)
                if re.search('antena.tvfree',link) or re.search('iframe id="player"',link):
                    marcador="Pre-catcher: tv a cores - antena"; print marcador
                    try:frame=re.compile('<iframe id="player"[^>]+?src="([^"]+?)"').findall(link)[0]
                    except:frame=re.compile('<iframe src="([^"]+?)" id="innerIframe"').findall(link)[0]
                    if not re.search('antena.tvfree',frame): frame= TVCoresURL + frame
                    ref_data = {'Referer': linkescolha,'User-Agent':user_agent}
                    link= abrir_url_tommy(frame,ref_data)
                    descobrirresolver(frame, nome,link,zapping,nomeserver)

                elif re.search('src="/meocanal.php',link):
                    marcador="Pre-catcher: tv a cores - meocanal"; print marcador
                    tempId=re.compile('<iframe src="/meocanal.php\?id=([^"]+?)"').findall(link)[0]
                    frame = "http://www.meocanaltv.com/embed/"+tempId+".php";
                    ref_data = {'Referer': linkescolha,'User-Agent':user_agent}
                    link= abrir_url_tommy(frame,ref_data)
                    if re.search('embedsecure.js',link):
                        link+=abrir_url_tommy(re.compile('src="([^"]+?)embedsecure.js"').findall(link)[0] + 'embedsecure.js',ref_data).decode('string-escape')
                    descobrirresolver(frame, nome,link,zapping,nomeserver)

                else: descobrirresolver(linkescolha, nome,False,zapping,nomeserver)
                

            elif re.search('gosporttv',linkescolha):
                marcador="Pre-catcher: thesporttv.eu"; print marcador
                link=clean(abrir_url(linkescolha))
                try:
                    linkcod=re.compile("id='(.+?)'.+?</script><script type='text/javascript' src='"+SptveuURL +"/teste/").findall(link)[0]
                    descobrirresolver(SptveuURL+ '/teste/c0d3r.php?id=' + linkcod,nome,'hdm1.tv',zapping,nomeserver)
                except:
                    frame=re.compile('</p>[^<]*<iframe allowtransparency="true" frameborder="0" scrolling="[^"]+?" src="([^"]+?)"').findall(link)[0]
                    frame=frame.replace('sporttvhdmi.com','gosporttv.com')
                    link=clean(abrir_url(frame))
                    if re.search('var urls = new Array',link):
                        framedupla=re.compile('new Array.+?"(.+?)".+?"(.+?)"').findall(link)[0]
                        if framedupla[0]==framedupla[1]: frame=framedupla[0]
                        else:
                            if activado==True: opcao=True
                            else:opcao= xbmcgui.Dialog().yesno("TV Portuguesa", "Escolha um stream da lista dos disponiveis.", "", "","Stream Extra", 'Stream Principal')
                            if opcao: frame=framedupla[0]
                            else: frame=framedupla[1]
              
                    descobrirresolver(frame, nome,False,zapping,nomeserver)
            elif re.search('lvshd',linkescolha):
                marcador="Pre-catcher: livesoccerhd"; print marcador
                link=abrir_url(linkescolha)
                linkfinal=limparcomentarioshtml(link,linkescolha)
                endereco=re.compile('<iframe.+?src="(.+?)".+?</iframe></div>').findall(link)[0]
                descobrirresolver(endereco, nome,False,zapping,nomeserver)

            elif re.search('redweb',linkescolha):
                marcador="Pre-catcher: redweb"; print marcador
                c=re.compile('c=(.+?)&').findall(linkescolha)[0]
                s=re.compile('s=(.+?)&').findall(linkescolha)[0]
                i=re.compile('i=(.+?)&').findall(linkescolha)[0]
                form_data = {'c':c,'s':s,'i':i}
                ref_data = {'User-Agent':user_agent}
                html= abrir_url_tommy(RedwebURL + '/monitor.php',ref_data,form_data=form_data)
                descobrirresolver(linkescolha, nome,html,zapping,nomeserver)

            elif re.search('tvtuga',linkescolha):
                marcador="Pre-catcher: tvtuga"; print marcador
                ref_data = {'Referer': TVTugaURL,'User-Agent':user_agent}
                link= abrir_url_tommy(linkescolha,ref_data)
                p = re.compile('<meta.*?>')
                link=p.sub('', link)
                descobrirresolver(linkescolha, nome,link,zapping,nomeserver)

            elif re.search('tvzune',linkescolha):
                print "Pre-catcher: tvzune"; print marcador
                if re.search('soft',linkescolha):
                    ref_data = {'User-Agent':''}
                    html= abrir_url_tommy(linkescolha,ref_data).replace('jw-play','')
                    descobrirresolver(linkescolha, nome,html,zapping,nomeserver)
                else:                    
                    ref_data = {'Referer': 'http://www.tvzune.tv','User-Agent':user_agent}
                    html= abrir_url_tommy(linkescolha,ref_data)
                    descobrirresolver(linkescolha, nome,html,zapping,nomeserver)
            else: descobrirresolver(linkescolha, nome,False,zapping,nomeserver)
    except Exception:
        if activado==False:
            mensagemprogresso.close()
            mensagemok('TV Portuguesa','Servidor não suportado.')
            (etype, value, traceback) = sys.exc_info()
            print etype
            print value
            print traceback
            #buggalo.onExceptionRaised()
        else:
            try:debug.append(nomeserver + ' - ' + marcador)
            except: pass
        

    

def _descobrirresolver(url_frame,nomecanal,linkrecebido,zapping,nomeserver):
    mensagemprogresso.create('TV Portuguesa', 'A carregar stream. (' + nomeserver + ')','Por favor aguarde...')
    descobrirresolver(url_frame,nomecanal,linkrecebido,zapping,nomeserver)

def descobrirresolver(url_frame,nomecanal,linkrecebido,zapping,nomeserver):
    marcador='A iniciar Resolvers'
    if zapping==False and activado==False: mensagemprogresso.update(50)
    try:
        #import buggalo
        #buggalo.SUBMIT_URL = 'http://fightnight.pusku.com/exceptions/submit.php'
        yoyo265='type:"flash".+?"'
        yoyo115='file:'

        if linkrecebido==False and not url_frame[0:9]=='stream://':
            marcador="Resolver: O url da frame e " + url_frame; print marcador
            
            url_frame=url_frame.replace(' ','%20')
            link=abrir_url_cookie(url_frame)
            try:link=limparcomentarioshtml(link,url_frame)
            except: pass
            link=clean(link)
        
            link=link.replace('cdn.zuuk.net\/boi.php','').replace('cdn.zuuk.net\/stats.php','').replace('cdn.zuuk.net/boi.php','').replace('cdn.zuuk.net/stats.php','').replace('<p><script language="JavaScript"> setTimeout','<p><script language="JavaScript">setTimeout').replace('micast_ads','')

        elif url_frame[0:9]=='stream://':
            marcador="Resolver: Stream Directo"; print marcador
            link=''
        else:
            marcador="Resolver: O produto final no descobrirresolver"; print marcador
            link=limparcomentarioshtml(linkrecebido,url_frame)
            link=link.replace('<title>Zuuk.net</title>','').replace('http://s.zuuk.net/300x250.html','').replace('www.zuuk.net\/test.php?ch=','').replace('cdn.zuuk.net\/boi.php','').replace('cdn.zuuk.net\/stats.php','').replace('cdn.zuuk.net/boi.php','').replace('cdn.zuuk.net/stats.php','').replace('<p><script language="JavaScript"> setTimeout','<p><script language="JavaScript">setTimeout').replace('micast_ads','')

        link=urllib.unquote(link)
        if url_frame[0:9]=='stream://':
            marcador="Catcher: direct stream url"; print marcador
            streamurl=url_frame.replace("stream://",'')
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search("<iframe src='http://www.zuuk.pw",link):
            marcador="Catcher: zuuk.pw"; print marcador
            name=re.compile("<iframe src='http://www.zuuk.pw(.+?)'").findall(link)[0]
            descobrirresolver('http://www.zuuk.pw' + name,nomecanal,False,zapping,nomeserver)
        
        elif re.search("zuuk.net",link):
            try:
                marcador="Catcher: zuuk"; print marcador
                l
#                try:chname=re.compile("file='(.+?)'.+?</script>").findall(link)[0]
#                except:chname=False
#                if not chname:
#                    chname=re.compile('src=.+?http://www.zuuk.net/el.php.+?ch=(.+?)&').findall(link)[0]
#                    link=abrir_url_cookie('http://www.zuuk.net/el.php?ch='+chname)
#                streamurl='rtmp://198.7.58.79/edge playPath='+ chname +' swfUrl=http://cdn.zuuk.net/ply.swf live=true timeout=15 swfVfy=1 pageUrl=http://www.zuuk.net/'
#                comecarvideo(streamurl,nomecanal,True,zapping)
            except:
                marcador="Catcher: zuuk outro"; print marcador
                
                if re.search('<script type="text/javascript">//var urls = new Array',link): url_final=re.compile('new Array.+?"(.+?)",').findall(link)[0]
                
                ##derbie##
                else:
                    #try:name=re.compile('<iframe.+?src="http://.+?zuuk.net/(.+?)"').findall(link)[0]
                    try:name=re.compile('<iframe.+?src="http://.+?zuuk.net/([^"]*\.php[^"]*)"').findall(link)[0]
                    except:
                        try:name=re.compile("<iframe.+?src='http://.+?zuuk.net/(.+?)'").findall(link)[0]
                        except:name=re.compile("""setTimeout\("window.open\('http://.+?zuuk.net/(.+?)'""").findall(link)[0]
                    url_final="http://cdn.zuuk.net/" + name
                
                link=abrir_url_cookie(url_final)
                link=limparcomentarioshtml(link,url_frame)
                try:
                    info=re.compile("<div id='mediaspace'>"+'<script language="javascript".+?' + "document.write.+?unescape.+?'(.+?)'").findall(link)[0]
                    if info=="' ) );</script> <script type=": info=False
                except:info=False
                if info: infotratada=urllib.unquote(info)
                else: infotratada=link
                descobrirresolver(url_final,nomecanal,infotratada,zapping,nomeserver)

        elif re.search('<p><script language="JavaScript">setTimeout', link):
            marcador="Catcher: tvtuga zuuk"; print marcador
            ptcanal=redirect(re.compile('setTimeout.+?"window.open.+?' + "'(.+?)',").findall(link)[0])
            if re.search('.f4m',ptcanal):
                ptcanal=ptcanal + '&'
                descobrirresolver(ptcanal,nomecanal,ptcanal,zapping,nomeserver)
            elif re.search('rtmp://live.2caster.com',ptcanal):
                descobrirresolver(ptcanal,nomecanal,ptcanal,zapping,nomeserver)           
            else:
                html=urllib.unquote(abrir_url(ptcanal))
                descobrirresolver(ptcanal,nomecanal,html,zapping,nomeserver)

        elif re.search('id="innerIframe"',link):
            marcador="Catcher: id=innerIframe"; print marcador
            link=clean(link)
            #embed=re.compile('<br/><iframe.+?src="(.+?)" id="innerIframe"').findall(link)[0]
            embed=re.compile('<iframe[^<]+?src="([^"]+?)" id="innerIframe"').findall(link)[0]
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}            
            urlembed=TVCoresURL + embed
            urlembed=urlembed.replace('http://tvfree.mehttp://antena.tvfree2.me/','http://antena.tvfree2.me/')
            html = abrir_url_tommy(urlembed,ref_data)
            descobrirresolver(urlembed,nomecanal,html,zapping,nomeserver)
            

        #### ALIVE REMOVER DEPOIS ####

        #elif re.search('file=myStream.sdp',link) or re.search('ec21.rtp.pt',link):
        #    marcador="Catcher: RTP Proprio"; print marcador
        #    #link=abrir_url_cookie(url_frame)
            #urlalive=re.compile('<iframe src="(.+?)".+?></iframe>').findall(link)[0]
            #import cookielib
            #cookie = cookielib.CookieJar()
            #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
            #opener.addheaders = [('Host','www.rtp.pt'), ('User-Agent', user_agent), ('Referer',url_frame)]
            #linkfinal = opener.open(urlalive).read()
        #    rtmpendereco=re.compile('streamer=(.+?)&').findall(link)[0]
        #    filepath=re.compile('file=(.+?)&').findall(link)[0]
        #    filepath=filepath.replace('.flv','')
        #    swf="http://player.longtailvideo.com/player.swf"
        #    streamurl=rtmpendereco + ' playPath=' + filepath + ' swfUrl=' + swf + ' live=1 timeout=15 pageUrl=' + url_frame
        #    comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('04stream',link):
            marcador="Catcher: 04stream"; print marcador
            try:rtmp=re.compile('file=(.+?)"').findall(link)[0]
            except: rtmp=re.compile('file=(.+?)&amp;').findall(link)[0]
            try:swf=re.compile('type="application/x-shockwave-flash" class=".+?" src="(.+?)"').findall(link)[0]
            except:swf=re.compile('src="([^"]+?)" class=".+?" type="application/x-shockwave-flash"').findall(link)[0]
            
            streamurl=rtmp + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=http://www.04stream.com'
            comecarvideo(streamurl,nomecanal,True,zapping)


        elif re.search('720Cast',link) or re.search('ilive',link):
            marcador="Catcher: ilive"; print marcador
            setecast=re.compile("fid='(.+?)';.+?></script>").findall(link)
            
            if not setecast: setecast=re.compile('file: ".+?/app/(.+?)/.+?",').findall(link)
            if not setecast: setecast=re.compile('flashvars="file=(.+?)&').findall(link)
            if not setecast: setecast=re.compile('src="/ilive.tv.php.+?id=(.+?)" id="innerIframe"').findall(link)
            if not setecast: setecast=re.compile('http://www.ilive.to/embed/(.+?)&').findall(link)
            if not setecast: setecast=re.compile('http://www.ilive.to/embedplayer.php.+?&channel=(.+?)&').findall(link)
            for chname in setecast:
                embed='http://www.ilive.to/embedplayer.php?width=640&height=400&channel=' + chname + '&autoplay=true'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                if '<script language=javascript>c="' in html:
                    from resources.lib import ioncube
                    html=ioncube.ioncube1(html)
                    
                tempomili=str(millis())
                urltoken=re.compile(""".*getJSON\("([^'"]+)".*""").findall(html)[0] + '&_='+ tempomili
                urltoken2= abrir_url_tommy(urltoken,ref_data)
                token=re.compile('"token":"(.+?)"').findall(urltoken2)[0]
                rtmp=re.compile('streamer: "(.+?)",').findall(html)[0].replace('\\','')
                filelocation=re.compile('file: "(.+?).flv",').findall(html)[0]
                swf=re.compile("type: 'flash', src: '(.+?)'").findall(html)[0]
                app=re.compile('rtmp://[\.\w:]*/([^\s]+)').findall(rtmp)[0]
                streamurl=rtmp + ' app=' + app+' playPath=' + filelocation + ' swfUrl=' + swf + ' token='+ token +' swfVfy=1 live=1 timeout=15 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('2caster',link) or re.search('4caster',link):
            marcador="Catcher: 2caster"; print marcador
            try:
                rtmp=re.compile('streamer=(.+?)&').findall(url_frame)[0]
                filep=re.compile('file=(.+?)&').findall(url_frame)[0]
            except:
                rtmp=re.compile('streamer=(.+?)&').findall(link)[0]
                filep=re.compile('file=(.+?)&').findall(link)[0]
            streamurl=rtmp + ' playPath=' + filep + ' live=true timeout=15 swfUrl=http://player.longtailvideo.com/player.swf pageUrl=' + url_frame
                #streamurl='http://live.2caster.com:1935/live/' + filep + '/playplist.m3u8'
            #else:
            #    swf=re.compile('<param name="src" value="(.+?)\?').findall(link)[0]
            #    streamurl=filep.replace('rtmp://live.2caster.com/live/','http://live.2caster.com:1935/live/') + '/playplist.m3u8'
        
            
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('9stream',link):
            marcador="Catcher: 9stream"; print marcador
            stream=re.compile('src="http://www.9stream.com/embed/(.+?)&').findall(link)
            for chid in stream:
                embed='http://www.9stream.com/embedplayer.php?width=650&height=400&channel=' + chid + '&autoplay=true'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                if '<script language=javascript>c="' in html:
                    from resources.lib import ioncube
                    html=ioncube.ioncube1(html)
                    #if re.search('window.open\("http://www.direct2watch.com',html):
                    #    frame=re.compile('window.open\("http://www.direct2watch.com(.+?)"\)').findall(html)[0]
                    #    ref_data = {'Referer': embed,'User-Agent':user_agent}
                    #    html= abrir_url_tommy('http://www.direct2watch.com' + frame,ref_data)
                    #    html=ioncube.ioncube1(html)
                    #    print html
                tempomili=str(millis())
                urltoken=re.compile(""".*getJSON\("([^'"]+)".*""").findall(html)[0] + '&_='+ tempomili
                urltoken2= abrir_url_tommy(urltoken,ref_data)
                
                token=re.compile('"token":"(.+?)"').findall(urltoken2)[0]
                try:rtmp=re.compile("""'streamer': "(.+?)",""").findall(html)[0].replace('\\','')
                except:rtmp=re.compile('streamer: "(.+?)",').findall(html)[0].replace('\\','')
                try:filelocation=re.compile("'file': '(.+?).flv',").findall(html)[0]
                except:filelocation=chid
                try:swf=re.compile('flashplayer: "(.+?)"').findall(html)[0]
                except:swf=re.compile("type: 'flash', src: '(.+?)'").findall(html)[0]
                app=re.compile('rtmp://[\.\w:]*/([^\s]+)').findall(rtmp)[0]
                streamurl=rtmp + ' app=' + app+' playPath=' + filelocation + ' swfUrl=' + swf + ' token='+ token +' swfVfy=1 live=1 timeout=15 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)
                
        elif re.search('abcast', link):
            marcador="Catcher: abcast"; print marcador
            flex=re.compile("file='(.+?)';.+?></script>").findall(link)
            for chid in flex:
                embed='http://abcast.net/embed.php?file='+chid+'&width=650&height=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                rtmp=re.compile("&streamer=(.+?)&").findall(html)[0]#.replace('redirect','live')
                playpath=re.compile("file=(.+?)&").findall(html)[0]
                swf=re.compile('object data="(.+?)"').findall(html)[0]
                streamurl=rtmp + ' playPath=' + playpath + ' swfUrl=http://abcast.net/'+swf+' live=true timeout=15 swfVfy=1 conn=S:OK pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('aliez',link):
            marcador="Catcher: aliez"; print marcador
            aliez=re.compile('src="http://emb.aliez.tv/player/live.php.+?id=(.+?)&').findall(link)
            for chid in aliez:
                embed='http://emb.aliez.tv/player/live.php?id=' + chid + '&w=700&h=420'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile('swfobject.embedSWF\("([^"]+)"').findall(html)[0]
                rtmp=urllib.unquote(re.compile('"file":\s."([^"]+)"').findall(html)[0])
                streamurl=rtmp + ' live=true swfVfy=1 swfUrl=' + swf + ' pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('castalba', link):
            marcador="Catcher: castalba"; print marcador
            castalba=re.compile('<script type="text/javascript"> id="(.+?)";.+?></script>').findall(link)
            for chname in castalba:
                embed='http://castalba.tv/embed.php?cid=' + chname + '&wh=640&ht=385&r=cdn.thesporttv.eu'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("""flashplayer': "(.+?)",""").findall(html)[0]
                filelocation=re.compile("'file': '(.+?)',").findall(html)[0]
                rtmpendereco=re.compile("'streamer': '(.+?)',").findall(html)[0]
                streamurl=rtmpendereco + ' playPath=' + filelocation + '?id=' + ' swfUrl=http://www.udemy.com/static/flash/player5.9.swf live=true timeout=15 swfVfy=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('cast247',link):
            marcador="Catcher: cast247"; print marcador
            castamp=re.compile('fid="(.+?)".+?</script>').findall(link)
            for chname in castamp:
                #embed='http://www.cast247.tv/embed.php?channel='+chname+'&width=650&height=500&domain='+url_frame
                #ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                #html= abrir_url_tommy(embed,ref_data)
                #if re.search('Channel does not exist',html):
                #ja nao existe
                if activado==False: mensagemok('TV Portuguesa','Stream está offline.')
                return
                token=re.compile('var sURL = "(.+?)";').findall(html)[0]
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                tokeninfo= abrir_url_tommy('http://www.cast247.tv/' + token,ref_data)
                swf=re.compile('flashplayer: "(.+?)",').findall(html)[0]
                filelocation=re.compile('file: "(.+?)",').findall(html)[0]
                rtmpendereco=re.compile('streamer: "(.+?)"').findall(html)[0]
                streamurl=rtmpendereco + ' playPath=' + filelocation + ' swfUrl=http://www.cast247.tv/' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)


        elif re.search('castamp',link):
            marcador="Catcher: castamp"; print marcador
            castamp=re.compile('channel="(.+?)".+?</script>').findall(link)
            for chname in castamp:
                embed='http://castamp.com/embed.php?c='+chname
                ref_data = {'Referer': 'http://www.zuuk.net','User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("""flashplayer': "(.+?)",""").findall(html)[0]
                filelocation=re.compile("'file': '(.+?)',").findall(html)[0]
                rtmpendereco=re.compile("'streamer': '(.+?)',").findall(html)[0]
                streamurl=rtmpendereco + ' playPath=' + filelocation + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search("abouttext: 'CanalHD.TV'",link):
            marcador="Catcher: canalhd.tv"; print marcador
            rtmp=re.compile("file: '(.+?)'").findall(link)[0]
            if re.search('rtmp',link):
                chid=''.join((rtmp.split('/'))[-1:])
                swf='http://canalhd.tv/tv/jwplayer/jwplayer.flash.swf'
                streamurl=rtmp.replace(chid,'') + ' playPath='+chid+' swfUrl=' + swf + ' live=true swfVfy=true pageUrl=' + url_frame
            else: streamurl=rtmp + '|User-agent=Mozilla%2F5.0%20(Linux%3B%20Android%205.0.1%3B%20Nexus%20)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F38.0.1847.114%20Mobile%20Safari%2F537.36'
            comecarvideo(streamurl,nomecanal,True,zapping)
        
        elif re.search('cast3d', link): ##nao esta
            marcador="Catcher: cast3d"; print marcador
            cast3d=re.compile('fid="(.+?)";.+?></script>').findall(link)
            for chname in cast3d:
                embed='http://www.cast3d.tv/embed.php?channel=' + '&vw=640&vh=385&domain=lsh.lshunter.tv'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("""flashplayer': "(.+?)",""").findall(html)
                filelocation=re.compile("'file': '(.+?)',").findall(html)
                rtmpendereco=re.compile("'streamer': '(.+?)',").findall(html)
                streamurl=rtmpendereco[0] + ' playPath=' + filelocation[0] + '?id=' + ' swfUrl=' + swf[0] + ' live=true timeout=15 swfVfy=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('castto.me',link):
            marcador="Catcher: castto.me"; print marcador
            castamp=re.compile('fid="(.+?)".+?</script>').findall(link)
            for chname in castamp:
                embed='http://static.castto.me/embed.php?channel='+chname+'&vw=650&vh=500&domain='+url_frame
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                if re.search('Channel does not exist',html):
                    if activado==False: mensagemok('TV Portuguesa','Stream está offline.')
                    return
                swf=re.compile("SWFObject.+?'(.+?)'").findall(html)[0]
                filelocation=re.compile("so.addVariable.+?file.+?'(.+?)'").findall(html)[0]
                rtmpendereco=re.compile("so.addVariable.+?streamer.+?'(.+?)'").findall(html)[0]
                streamurl=rtmpendereco + ' playPath=' + filelocation + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 token=#ed%h0#w@1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('clubbingtv.live',link):
            marcador="Catcher: clubbingtv oficial"; print marcador
            rtmp=re.compile('file: "(.+?)"').findall(link)[0].replace('flv:','//')
            swf=re.compile('flashplayer: "(.+?)"').findall(link)[0]
            streamurl=rtmp + ' swfUrl=' + swf + ' live=true timeout=15 pageUrl=' + url_frame
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('ChelTV',link) or re.search('visionip',link):
            marcador="Catcher: cheltv"; print marcador
            chelsea=re.compile("file=(.+?).flv&streamer=(.+?)&").findall(link)
            try:swf=re.compile('flashvars=.+?src="(.+?)" type="application/x-shockwave-flash">').findall(link)[0]
            except:swf=re.compile("src='(.+?)' allowfullscreen=").findall(link)[0]
            streamurl=chelsea[0][1] + ' playPath=' + chelsea[0][0] + ' swfUrl=' + swf + ' live=true pageUrl=http://www.casadossegredos.tv'
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('www.dcast.tv',link):
            marcador="Catcher: dcast"; print marcador
            dcastfid=re.compile('<script type="text/javascript">fid="([^"]+)";').findall(link)[0]
            embed ="http://www.dcast.tv/embed.php?u="+dcastfid+"&vw=600&vh=450"
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            html= abrir_url_tommy(embed,ref_data)
            streamurl='rtmpe://strm.dcast.tv/redirect playPath=' + dcastfid + ' swfUrl=http://www.dcast.tv/player/player.swf live=true timeout=15 pageUrl=http://www.dcast.tv/embed.php'
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('cdn.livestation',link):
            marcador="Catcher: livestation"; print marcador
            if re.search('&abouttext=http://www.estadiofutebol.com/euronews',link):
                embed='http://www.livestation.com/en/euronews/pt'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                filepath=re.compile('{&quot;file&quot;:&quot;(.+?)&quot;,&quot;bitrate').findall(html)[0]
                swf=re.compile('&quot;flash&quot;,&quot;src&quot;:&quot;(.+?)&quot;').findall(html)[0]
                rtmp=re.compile('&quot;streamer&quot;:&quot;(.+?);').findall(html)[0]
                streamurl=rtmp + ' playPath=' + filepath + ' swfUrl=' + swf + ' live=true swfVfy=true pageUrl=' + embed
            else:
                hdmi=re.compile('src="([^"]+?).swf.+?streamer=(.+?)&file=(.+?)&').findall(link)[0]
                streamurl=hdmi[1] + ' playPath=' + hdmi[2] + ' swfUrl=' + swf + ' live=true swfVfy=true pageUrl=http://www.livestation.com'
                
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('ezcast', link):
            marcador="Catcher: ezcast"; print marcador
            ezcast=re.compile("channel='(.+?)',.+?</script>").findall(link)
            if not ezcast: ezcast=re.compile('src="/ezcast.tv.php.+?id=(.+?)" id="innerIframe"').findall(link)
            if not ezcast: ezcast=re.compile('channel="(.+?)",.+?</script>').findall(link)
            for chname in ezcast:
                embed='http://www.ezcast.tv/embedded/' + chname + '/1/555/435'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                link=abrir_url('http://www.ezcast.tv:1935/loadbalancer')
                rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)[0]
                swf=re.compile('SWFObject\("(.+?)"').findall(html)[0]
                idnum=re.compile("'FlashVars'.+?id=(.+?)&s=.+?&").findall(html)[0]
                chnum=re.compile("'FlashVars'.+?id=.+?&s=(.+?)&").findall(html)[0]
                streamurl='rtmp://' + rtmpendereco + '/live playPath=' + chnum + '?id=' + idnum + ' swfUrl=http://www.ezcast.tv' + swf + ' live=true conn=S:OK swfVfy=1 timeout=14 ccommand=iUsteJaSakamCarevataKerka;TRUE;TRUE pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('.f4m&', link):
            marcador="Catcher f4m file"; print marcador
            streamurl='http://' + clean(re.compile('src=http://(.+?).f4m&').findall(link)[0]) + '.f4m' #rtp1
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('fcast', link):
            marcador="Catcher: fcast"; print marcador
            fcast=re.compile("fid='(.+?)';.+?></script>").findall(link)
            if not fcast: fcast=re.compile("e-fcast.tv.php.+?fid=(.+?).flv").findall(link)
            for chname in fcast:
                embed='http://www.fcast.tv/embed.php?live=' + chname + '&vw=600&vh=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("SWFObject.+?'(.+?)'").findall(html)
                filelocation=re.compile("so.addVariable.+?file.+?'(.+?)'").findall(html)
                rtmpendereco=re.compile("so.addVariable.+?streamer.+?'(.+?)'").findall(html)
                streamurl=rtmpendereco[0] + ' playPath=' + filelocation[0] + ' swfUrl=' + swf[0] + ' live=true timeout=14 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('flashi', link):
            marcador="Catcher: flashi"; print marcador
            flashi=re.compile('fid="(.+?)";.+?></script>').findall(link)
            for chname in flashi:
                embed='http://www.flashi.tv/embed.php?v=' + chname +'&vw=640&vh=490&typeplayer=0&domain=f1-tv.info'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                if re.search('This Channel is not Existed !',html):
                    if activado==False: mensagemok('TV Portuguesa','Stream indisponivel')
                    return
                swf=re.compile("new SWFObject.+?'(.+?)'").findall(html)[0]
                filename=re.compile("so.addVariable.+?'file'.+?'(.+?)'").findall(html)
                #rtmpendereco=re.compile("so.addVariable.+?'streamer'.+?'(.+?)'").findall(link)
                streamurl='rtmp://flashi.tv:1935/lb' + ' playPath=' + filename[0] + ' swfUrl=http://www.flashi.tv/' + swf + ' live=true timeout=15 swfVfy=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('flashstreaming.mobi',link):
            marcador="Catcher: flashstreaming.mobi"; print marcador
            flex=re.compile("channel='(.+?)',.+?></script>").findall(link)
            for chid in flex:
                js=re.compile('http://flashstreaming.mobi/(.+?).js').findall(link)[0]
                temp=abrir_url('http://flashstreaming.mobi/%s.js' % js)
                embed=re.compile("src=(.+?)'").findall(temp)[0]+chid+'&w=600&h=400'
                #embed='http://flashstreaming.mobi/embed/embed.php?channel='+chid+'&w=600&h=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                try:swf=re.compile("new SWFObject\('(.+?)'").findall(html)[0]
                except:swf=re.compile("src='(.+?)'").findall(html)[0]
                try:playp=re.compile('file=(.+?)&').findall(html)[0]
                except:playp=re.compile("'file', '(.+?)'").findall(html)[0]
                try:rtmp=re.compile('streamer=(.+?)&').findall(html)[0]
                except:rtmp=re.compile("'streamer', '(.+?)'").findall(html)[0]
                streamurl=rtmp + ' playPath=' + playp + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)
            
        elif re.search('flashtv.co', link):
            marcador="Catcher: flashtv.co"; print marcador
            stream4u=re.compile("fid='(.+?)';.+?></script>").findall(link)
            for chid in stream4u:
                embed='http://www.flashtv.co/embed.php?live='+chid+'&vw=650&vh=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("SWFObject\('(.+?)'").findall(html)[0]
                rtmp=re.compile("'streamer','(.+?)'").findall(html)[0]
                streamurl=rtmp + ' playPath=' + chid + ' swfUrl=http://www.flashtv.co' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('flexstream', link):
            marcador="Catcher: flexstream"; print marcador
            flex=re.compile("file='(.+?)';.+?></script>").findall(link)
            for chid in flex:
                embed='http://flexstream.net/embed.php?file='+chid+'&width=650&height=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                rtmp=re.compile("file: '(.+?)'").findall(html)[0].replace(chid,'')
                streamurl=rtmp + ' playPath=' + chid + ' swfUrl=http://p.jwpcdn.com/6/8/jwplayer.flash.swf live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('fxstream.biz', link):
            marcador="Catcher: fxstream.biz"; print marcador
            flex=re.compile("file='(.+?)';.+?></script>").findall(link)
            for chid in flex:
                embed='http://fxstream.biz/embed.php?file='+chid+'&width=650&height=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                rtmp=re.compile("file: '(.+?)'").findall(html)[0].replace(chid,'')
                token=re.compile('securetoken: "(.+?)"').findall(html)[0].replace(chid,'')
                streamurl=rtmp + ' playPath=' + chid + ' swfUrl=http://p.jwpcdn.com/6/11/jwplayer.flash.swf token='+token+' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)


        elif re.search('freebroadcast.pw', link):
            marcador="Catcher: freebroadcast.pw"; print marcador
            flive=re.compile("channel='(.+?)',.+?></script>").findall(link)
            for chid in flive:
                embed='http://freebroadcast.pw/embed/embed.php?n='+chid+'&w=650&h=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("SWFObject\('../(.+?)'").findall(html)[0]
                playp=re.compile("'file', '(.+?)'").findall(html)[0]
                rtmp=re.compile("'streamer', '(.+?)'").findall(html)[0]
                token=re.compile("'token', '(.+?)'").findall(html)[0]
                streamurl=rtmp + ' playPath=' + playp + ' swfUrl=http://freebroadcast.pw/' + swf + ' live=true token=' +token +' timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('freelivetv.tv', link):
            marcador="Catcher: freelivetv.tv"; print marcador
            flive=re.compile("channel='(.+?)',.+?></script>").findall(link)
            for chid in flive:
                embed='http://freelivetv.tv/embed/embed.php?channel='+chid+'&w=650&h=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("src='(.+?)'").findall(html)[0]
                playp=re.compile('file=(.+?)&').findall(html)[0]
                rtmp=re.compile('streamer=(.+?)&').findall(html)[0]
                streamurl=rtmp + ' playPath=' + playp + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('freetvcast', link):
            marcador="Catcher: freetvcast"; print marcador
            cenas=re.compile('freetvcast.pw/(.+?)"').findall(link)[0]
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            framesite='http://freetvcast.pw/' + cenas
            html= abrir_url_tommy(framesite,ref_data)
            embed=re.compile("var url = '(.+?)'").findall(html)[0]
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            html= abrir_url_tommy(embed,ref_data)
            swf=re.compile("SWFObject\('(.+?)'").findall(html)[0].replace('../','')
            rtmp=re.compile("'streamer', '(.+?)'").findall(html)[0].replace('redirect','live')
            filep=re.compile("'file', '(.+?)'").findall(html)[0]
            rtmp=rtmp.replace('live','redirect')
            streamurl=streamurl=rtmp + ' playPath=' + filep + ' swfUrl=http://freetvcast.pw/' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
            comecarvideo(streamurl,nomecanal,True,zapping)
        
        elif re.search('goodcast.me', link):
            marcador="Catcher: goodcast.me"; print marcador
            stream4u=re.compile("id='(.+?)';.+?></script>").findall(link)
            for chid in stream4u:
                embed='http://goodcast.me/stream.php?id='+chid+'&width=650&height=450&stretching='
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                playpath=re.compile('file=(.+?)&').findall(html)[0]
                swf=re.compile('data="(.+?)"').findall(html)[0]
                rtmp=re.compile("streamer=(.+?)&").findall(html)[0]
                abrir_url('http://goodcast.me/stream.html?id=' + playpath)
                streamurl=rtmp + ' playPath=' + playpath + ' swfUrl=' + swf + ' token=Fo5_n0w?U.rA6l3-70w47ch live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('hdcast.tv',link):
            marcador="Catcher: hdcast.tv"; print marcador
            chid=re.compile('fid=(.+?)"').findall(link)[0]
            chid=chid.replace('.flv','')
            streamurl='rtmp://origin.hdcast.tv:1935/redirect/ playPath='+chid+' swfUrl=http://www.udemy.com/static/flash/player5.9.swf live=true timeout=15 swfVfy=1 pageUrl=http://www.hdcast.tv'
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('hdcaster.net', link):
            marcador="Catcher: hdcaster"; print marcador
            hdcaster=re.compile("<script type='text/javascript'>id='(.+?)'").findall(link)
            for chid in hdcaster:
                urltemp='rtmp://188.138.121.99/hdcaster playPath=' + chid + ' swfUrl=http://hdcaster.net/player.swf pageUrl=http://hdcaster.net/player.php?channel_id=101634&width=600&height=430'
                token = '%Xr8e(nKa@#.'
                streamurl=urltemp + ' token=' + token
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('hqstream.tv', link):
            marcador="Catcher: hqstream.tv"; print marcador
            hqst=re.compile("hqstream.tv.+?streampage=(.+?)&").findall(link)
            for chid in hqst:
                embed='http://hqstream.tv/player.php?streampage=' + chid
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                fp=int(re.compile('var f =\s*([^;]+)').findall(html)[0])
                ap=int(re.compile('var a =\s*([^;]+)').findall(html)[0])/fp
                bp=int(re.compile('var b =\s*([^;]+)').findall(html)[0])/fp
                cp=int(re.compile('var c =\s*([^;]+)').findall(html)[0])/fp
                dp=int(re.compile('var d =\s*([^;]+)').findall(html)[0])/fp
                vp=re.compile("var v_part =\s*'([^']+).*").findall(html)[0]

                streamurl='rtmp://%s.%s.%s.%s%s swfUrl=http://filo.hqstream.tv/jwp6/jwplayer.flash.swf live=1 timeout=15 swfVfy=1 pageUrl=%s' % (ap,bp,cp,dp,vp,embed)
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('icasthd', link):
            marcador="Catcher: icastHD"; print marcador
            icast=re.compile('fid="(.+?)";.+?></script>').findall(link)
            for chname in icast:
                embed='http://www.icasthd.tv/embed.php?v='+chname+'&vw=575&vh=390&domain=www.ihdsports.com'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                if re.search('This Channel is not Existed !',html):
                    if activado==False: mensagemok('TV Portuguesa','Stream indisponivel')
                    return
                swf=re.compile("'flashplayer': 'http://www.icasthd.tv//(.+?)'").findall(html)[0]
                filename=re.compile("'file': '(.+?)'").findall(html)[0]
                rtmpendereco=re.compile("'streamer': '(.+?)redirect3").findall(html)[0]
                app=re.compile("Ticket=(.+?)'").findall(html)[0]
                streamurl=rtmpendereco+ 'live app=live?f=' + app + ' playPath=' + filename + ' swfUrl=http://www.icasthd.tv/' + swf + ' live=1 timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('janjua',link):
            marcador="Catcher: janjua"; print marcador
            janj=re.compile("channel='(.+?)',.+?</script>").findall(link)
            if not janj: janj=re.compile('channel="(.+?)",.+?</script>').findall(link)
            for chname in janj:
                embed='http://www.janjua.tv/embedplayer/'+chname+'/1/650/500'
                ref_data = {'Connection': 'keep-alive','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                if re.search('Channel is domain protected.',html):
                    url_frame='http://www.janjua.tv/' + chname
                    ref_data = {'Connection': 'keep-alive','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Referer': url_frame,'User-Agent':user_agent}
                    html= abrir_url_tommy(embed,ref_data)
                swf=re.compile('SWFObject.+?"(.+?)",').findall(html)
                flashvars=re.compile("so.addParam.+?'FlashVars'.+?'(.+?);").findall(html)[0]
                flashvars=flashvars.replace("')","&nada").split('l=&')
                if flashvars[1]=='nada':
                    nocanal=re.compile("&s=(.+?)&").findall(flashvars[0])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[0]
                else:
                    nocanal=re.compile("&s=(.+?)&nada").findall(flashvars[1])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[1]
                nocanal=nocanal.replace('&','')
                link=abrir_url('http://www.janjua.tv:1935/loadbalancer')
                embed='http://www.janjua.tv/embedplayer/'+chname+'/1/650/500'
                ref_data = {'Connection': 'keep-alive','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Referer': url_frame,'User-Agent':user_agent}
                rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)
                streamurl='rtmp://' + rtmpendereco[0] + '/live/ playPath=' + nocanal + '?id=' + chid + ' swfVfy=1 conn=S:OK live=true ccommand=soLagaDaSeStoriAga;FALSE swfUrl=http://www.janjua.tv' + swf[0] + ' ccommand=soLagaDaSeStoriAga;TRUE;TRUE pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('jwplayer:streamer',link):
            marcador="Catcher: jwplayer.streamer .xml"; print marcador
            rtmp=re.compile('<jwplayer:streamer>(.+?)</jwplayer:streamer>').findall(link)[0]
            try:
                filelocation=re.compile('<media:content bitrate=".+?" url="(.+?)" width=".+?"').findall(link)[0]
            except:
                filelocation= re.compile('<media:content url="(.+?)"').findall(link)[0]
                if re.search('TPAI.mp4',filelocation): url_frame='http://muntumedia.com/television/10-tpai'

            swf='http://www.tpai.tv/swf/jwplayer/player.swf'
            streamurl=rtmp + ' playPath=' + filelocation + ' swfUrl=' + swf + ' live=true pageUrl=' + url_frame
            comecarvideo(streamurl,nomecanal,True,zapping)


        elif re.search('longtail', link):
            marcador="Catcher: longtail"; print marcador
            longtail=re.compile("src='http://player.longtailvideo.com/player.swf' flashvars='file=(.+?)&streamer=(.+?)&").findall(link)
            if not longtail: longtail=re.compile('flashvars="file=(.+?)&streamer=(.+?)&').findall(link)
            if not longtail: longtail=re.compile('flashvars="file=(.+?)&.+?streamer=(.+?)&').findall(link)
            for chname,rtmp in longtail:
                chname=chname.replace('.flv','')
                streamurl=rtmp + ' playPath=' + chname + ' live=true swfUrl=http://player.longtailvideo.com/player.swf pageUrl=http://longtailvideo.com/'
                comecarvideo(streamurl,nomecanal,True,zapping)
            if not longtail:
                streamurl=re.compile('file: "(.+?)"').findall(link)[0]
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('hdm1.tv',link):
            marcador="Catcher: hdm1.tv"; print marcador
            hdmi=re.compile("fid='(.+?)';.+?></script>").findall(link)
            for chid in hdmi:
                embed='http://hdm1.tv/embed.php?live='+ chid +'&vw=600&vh=470'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("new SWFObject.+?'(.+?)'").findall(html)[0]
                filelocation=re.compile("so.addVariable.+?'file'.+?'(.+?)'").findall(html)
                rtmpendereco=re.compile("so.addVariable.+?'streamer'.+?'(.+?)'").findall(html)
                streamurl=rtmpendereco[0] + ' playPath=' + filelocation[0] + ' swfUrl=' + swf + ' live=true swfVfy=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)
            if not hdmi:
                hdmi=re.compile("src='(.+?).swf.+?file=(.+?)&streamer=(.+?)&autostart=true").findall(link)
                for swf,chid,rtmp in hdmi:
                    embed='http://hdm1.tv/embed.php?live='+ chid +'&vw=600&vh=470'
                    streamurl=rtmp + ' playPath=' + chid + ' swfUrl=' + swf + ' live=true swfVfy=true pageUrl=' + embed
                    comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('jimey',link):
            marcador="Catcher: jimey"; print marcador
            chname=re.compile("file='(.+?)';.+?</script>").findall(link)[0]
            embed= 'http://jimey.tv/player/embedplayer.php?channel=' + chname + '&width=640&height=490'
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            html= abrir_url_tommy(embed,ref_data)
            rtmp=re.compile('&streamer=(.+?)/redirect').findall(html)[0]
            streamurl= rtmp + ' playPath='+chname + " token=zyklPSak>3';CyUt%)'ONp" + ' swfUrl=http://jimey.tv/player/fresh.swf live=true timeout=15 swfVfy=1 pageUrl=' + embed
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('jw-player.html?cid=',url_frame):
            marcador="Catcher: jwplay tvfree"; print marcador
            streamurl=url_frame.replace('http://tvfree.me/jw-player.html?cid=','')
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('jwlive',link) or re.search('jw-play',link):
            marcador="Catcher: jwlive"; print marcador
            endereco=TVCoresURL + re.compile('<br/><iframe src="(.+?)" id="innerIframe"').findall(link)[0]
            if re.search('tvfree.me/jw-player.html',endereco):
                streamurl=endereco.replace('http://tvfree.me/jw-player.html?cid=','')
            else:
                link=abrir_url(endereco)
                streamurl=re.compile('file: "(.+?)"').findall(link)[0]
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('livemeans', link):
            marcador="Catcher: livemeans"; print marcador
            stream=re.compile('<embed.+?src="(.+?)" flashvars="rtserver=(.+?)&livechannel').findall(link)[0]
            rtmp=stream[1].replace('rtserver','livenlin4?ovpfv=2.1.2').replace(':80',':1935').replace('rtmpt://','rtmp://')
            swf=stream[0]
            streamurl=rtmp + ' playPath=mp4:2livepln swfVfy=1 live=true swfUrl=' + swf + ' pageUrl=' + url_frame
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('liveflash', link):
            marcador="Catcher: liveflash"; print marcador
            flashtv=re.compile("channel='(.+?)',.+?></script>").findall(link)
            if not flashtv: flashtv=re.compile('channel="(.+?)".+?</script>').findall(link)
            if not flashtv: flashtv=re.compile('iframe src="/cc-liveflash.php.+?channel=(.+?)"').findall(link)
            if not flashtv: flashtv=re.compile("window.open.+?'/e-liveflash.tv.php.+?channel=(.+?)'").findall(link)
            if not flashtv: flashtv=re.compile("http://tvph.googlecode.com/svn/players/liveflash.html.+?ver=(.+?)'").findall(link)
            if not flashtv: flashtv=re.compile("pop-liveflash.php.+?get=(.+?)'").findall(link)

            for chname in flashtv:
                embed='http://www.liveflash.tv/embedplayer/' + chname + '/1/640/460'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                if re.search('Channel is domain protected.',html):
                    url_frame='http://www.liveflash.tv/' + chname
                    ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                    html= abrir_url_tommy(embed,ref_data)
                swf=re.compile('SWFObject.+?"(.+?)",').findall(html)
                flashvars=re.compile("so.addParam.+?'FlashVars'.+?'(.+?);").findall(html)[0]
                flashvars=flashvars.replace("')","&nada").split('l=&')
                if flashvars[1]=='nada':
                    nocanal=re.compile("&s=(.+?)&").findall(flashvars[0])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[0]
                else:
                    nocanal=re.compile("&s=(.+?)&nada").findall(flashvars[1])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[1]
                nocanal=nocanal.replace('&','')
                link=abrir_url('http://www.liveflash.tv:1935/loadbalancer')
                rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)
                streamurl='rtmp://' + rtmpendereco[0] + '/stream/ playPath=' + nocanal + '?id=' + chid + ' swfVfy=1 conn=S:OK live=true swfUrl=http://www.liveflash.tv' + swf[0] + ' ccommand=kaskatijaEkonomista;TRUE;TRUE pageUrl=' + embed
                #print streamurl
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('livestreamtv', link):
            marcador="Catcher: livestreamtv"; print marcador
            flex=re.compile("file='(.+?)';.+?></script>").findall(link)
            for chid in flex:
                embed='http://livestreamtv.biz/globo.php?file='+chid+'&width=650&height=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                rtmp=re.compile('var streamer="(.+?)"').findall(html)[0]#.replace('redirect','live')
                playpath=re.compile("'file': '(.+?)'").findall(html)[0]
                swf=re.compile('var myPlayer="(.+?)"').findall(html)[0]
                streamurl=rtmp + ' playPath=' + playpath + ' swfUrl=http://livestreamtv.biz'+swf+' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)


        #elif re.search('livestream', link):
        #    marcador="Catcher: livestream"; print marcador
        #    livestream=re.compile("videoborda.+?channel=(.+?)&").findall(link)
        #    for chname in livestream:
        #        streamurl='rtmp://extondemand.livestream.com/ondemand playPath=trans/dv04/mogulus-user-files/ch'+chname+'/2009/07/21/1beb397f-f555-4380-a8ce-c68189008b89 live=true swfVfy=1 swfUrl=http://cdn.livestream.com/chromelessPlayer/v21/playerapi.swf pageUrl=http://cdn.livestream.com/embed/' + chname + '?layout=4&amp;autoplay=true'
        #        comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('master_tv', link):
            marcador="Catcher: mastertv"; print marcador
            mastertv=re.compile('src=".+?fid=(.+?)" name="frame"').findall(link)[0].replace('animax','disneyjr')
            descobrirresolver('http://tv-msn.com/' + mastertv + '.html', nomecanal,False,False,nomeserver)

        elif re.search('megatvhd',url_frame):
            marcador="Catcher: megatvhd.tv"; print marcador
            chid=re.compile('liveedge/(.+?)"').findall(link)[0]
            embed='http://megatvhd.tv/ch.php?id='+chid
            link=abrir_url(embed)
            rtmp=re.compile('file: "(.+?)"').findall(link)[0]
            rtmp=rtmp.replace('/'+chid,'')
            streamurl=rtmp + ' playPath='+chid + ' live=true swfUrl=http://player.longtailvideo.com/player.swf pageUrl='+embed
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('megom', link):
            marcador="Catcher: megom.tv"; print marcador
            megom=re.compile('HEIGHT=432 SRC="http://distro.megom.tv/player-inside.php.+?id=(.+?)&width=768&height=432"></IFRAME>').findall(link)
            for chname in megom:
                embed='http://distro.megom.tv/player-inside.php?id='+chname+'&width=768&height=432'
                link=abrir_url(embed)
                swf=re.compile(".*'flashplayer':\s*'([^']+)'.*").findall(link)[0]
                streamer=re.compile("'streamer': '(.+?)',").findall(link)[0]
                streamer=streamer.replace('live.megom.tv','37.221.172.85')
                streamurl=streamer + ' playPath=' + chname + ' swfVfy=1 swfUrl=' + swf + ' live=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('micast', link):
            marcador="Catcher: micast"; print marcador
            baseurl='http://micast.tv/chn.php?ch='
            micast=re.compile('micast.tv:1935/live/(.+?)/').findall(link)
            if not micast: micast=re.compile('ca="(.+?)".+?></script>').findall(link)
            if not micast: micast=re.compile('setTimeout.+?"window.open.+?' + "'http://micast.tv/gen.php.+?ch=(.+?)',").findall(link)
            if not micast: micast=re.compile('src="http://micast.tv/gen5.php.+?ch=(.+?)&amp;"').findall(link)
            if not micast: micast=re.compile('src="http://micast.tv/chn.php.+?ch=(.+?)"').findall(link)
            if not micast:
                if re.search('http://micast.tv/gens2.php',url_frame):
                    micast=[]
                    micast.append(url_frame.replace('http://micast.tv/gens2.php?ch=',''))
                    baseurl='http://micast.tv/gens2.php?ch='
                
            for chname in micast:
                #embed=redirect(baseurl+chname)
                embed=redirect('http://micast.tv/gens2.php?ch=cocoeranheta')
                link=abrir_url(embed)
                if re.search('refresh',link):
                    chname=re.compile('refresh" content="0; url=http://micast.tv/gen.php.+?ch=(.+?)"').findall(link)[0]                
                    link=abrir_url('http://micast.tv/gen5.php?ch='+chname)
                try:
                    final=re.compile('file=(.+?)&amp;streamer=(.+?)&amp').findall(link)[0]
                    streamurl=final[1] + ' playPath=' + final[0] + ' swfUrl=http://files.mica.st/player.swf live=true timeout=15 swfVfy=1 pageUrl=http://micast.tv/gen.php?ch='+final[0]
                except:
                    rtmp=re.compile('file: "(.+?),').findall(link)[0]
                    rtmp=rtmp.split('/')
                    rtmp[2]=rtmp[2] + ':443'
                    rtmp='/'.join(rtmp)
                    chid=re.compile('/liveedge/(.+?)"').findall(rtmp)[0]
                    chidplay=chid.replace('.flv','')
                    rtmp=rtmp.replace(chid+'"','')
                    streamurl=rtmp + ' playPath=' + chname + ' swfUrl=http://micast.tv/jwplayer/jwplayer.flash.swf live=true timeout=15 swfVfy=1 pageUrl=' + embed

                comecarvideo(streamurl,nomecanal,True,zapping)
            if not micast:
                try:
                    micast=re.compile('<iframe src="(.+?)" id="innerIframe"').findall(link)[0]
                    link=abrir_url(TVCoresURL + micast)
                    if re.search('privatecdn',link):
                        descobrirresolver(url_frame,nomecanal,link,zapping,nomeserver)
                    else:
                        micast=re.compile('//(.+?).micast.tv/').findall(link)[0]
                        linkfinal='http://' + micast+  '.micast.tv'
                        link=abrir_url(linkfinal)
                        final=re.compile('file=(.+?)&amp;streamer=(.+?)&amp').findall(link)[0]
                        #if not final: final=re.compile("file=(.+?)&streamer=(.+?)'").findall(link)[0]
                        streamurl=final[1] + ' playPath=' + final[0] + ' swfUrl=http://files.mica.st/player.swf live=true timeout=15 swfVfy=1 pageUrl=http://micast.tv/gen.php?ch='+final[0]
                        comecarvideo(streamurl,nomecanal,True,zapping)
                except: pass
                
        elif re.search('mips', link):
            marcador="Catcher: mips"; print marcador
            mips=re.compile("channel='(.+?)',.+?></script>").findall(link)
            if not mips: mips=re.compile('channel="(.+?)",.+?></script>').findall(link)
            if not mips: mips=re.compile('<iframe src="/mips.tv.php.+?fid=(.+?)" id="innerIframe"').findall(link)
            if not mips: mips=re.compile("pop-mips.php\?get=(.+?)'").findall(link)
            for chname in mips:
                embed='http://www.mips.tv/embedplayer/' + chname + '/1/500/400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                if re.search("The requested channel can't embedded on this domain name.",html):
                    source='http://www.mips.tv/' + chname
                    ref_data = {'Referer': source,'User-Agent':user_agent}
                    html= abrir_url_tommy(embed,ref_data)
                swf=re.compile('SWFObject.+?"(.+?)",').findall(html)[0]
                flashvars=re.compile("so.addParam.+?'FlashVars'.+?'(.+?);").findall(html)[0]
                flashvars=flashvars.replace("')","&nada").split('l=&')
                if flashvars[1]=='nada':
                    nocanal=re.compile("&s=(.+?)&e=").findall(flashvars[0])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[0]
                else:
                    nocanal=re.compile("&s=(.+?)&nada").findall(flashvars[1])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[1]
                nocanal=nocanal.replace('&','')
                link=abrir_url('http://www.mips.tv:1935/loadbalancer')
                rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)[0]
                streamurl='rtmp://' + rtmpendereco + '/live/ playPath=' + nocanal + '?id=' + chid + ' swfVfy=1 live=true timeout=15 conn=S:OK swfUrl=http://www.mips.tv' + swf + ' ccommand=gaolVanusPobeleVoKosata;TRUE;TRUE pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('newsko.co.uk', link): ##nao esta
            marcador="Catcher: newsko.co.uk"; print marcador
            cast3d=re.compile('fid="(.+?)";.+?></script>').findall(link)
            for chname in cast3d:
                embed='http://www.newsko.co.uk/embed.php?channel=' + chname +'&vw=640&vh=385&domain=' + url_frame
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("new SWFObject\('(.+?)',").findall(html)
                filelocation=re.compile("'file','(.+?)'").findall(html)
                rtmpendereco=re.compile("'streamer','(.+?)'").findall(html)
                streamurl=rtmpendereco[0] + ' playPath=' + filelocation[0] + '?id=' + ' swfUrl=' + swf[0] + ' live=true timeout=15 swfVfy=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('pt.euronews',link):
            marcador="Catcher: euronews pt"; print marcador
            embed='http://pt.euronews' + re.compile('src="http://pt.euronews(.+?)"').findall(link)[0]
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            html= abrir_url_tommy(embed,ref_data)
            try:streamurl=re.compile('<a href="(.+?)">watch this stream over RTSP</a>').findall(html)[0]
            except:streamurl=re.compile('file: "(.+?)"').findall(html)[0]
            comecarvideo(streamurl,nomecanal,True,zapping)
            
        elif re.search('privatecdn',link):
            marcador="Catcher: privatecdn"; print marcador
            privatecdn=re.compile('<script type="text/javascript">id="(.+?)"').findall(link)
            for chid in privatecdn:
                embed='http://privatecdn.tv/ch.php?id='+chid
                link=abrir_url(embed)
                rtmp=re.compile('file: "(.+?)"').findall(link)[0]
                rtmp=rtmp.replace('/'+chid,'')
                streamurl=rtmp + ' playPath='+chid + ' live=true swfUrl=http://player.longtailvideo.com/player.swf pageUrl='+embed
                comecarvideo(streamurl,nomecanal,True,zapping)
                
        elif re.search('putlive', link):
            marcador="Catcher: putlive"; print marcador
            putlivein=re.compile("<iframe.+?src='.+?.swf.+?file=(.+?)&.+?'.+?></iframe>").findall(link)
            if not putlivein: putlivein=re.compile("file='(.+?)'.+?</script>").findall(link)
            if not putlivein: putlivein=re.compile('src="http://www.putlive.in/e/(.+?)"></iframe>').findall(link)
            for chname in putlivein:
                streamurl='rtmpe://199.195.199.172:443/liveedge2/ playPath=' + chname + ' swfUrl=http://www.megacast.io/player59.swf live=true timeout=15 swfVfy=1 pageUrl=http://putlive.in/'
                comecarvideo(streamurl,nomecanal,True,zapping)

        ##livesoccerhd
        elif re.search('src="http://cdn.gosporttv.com',link):
            marcador="Catcher: livesoccerhd stolen sptvhd"; print marcador
            ups=re.compile('<iframe.+?src="(.+?)"').findall(link)[0]
            descobrirresolver(ups,nomecanal,False,zapping,nomeserver)
        
        elif re.search('ptcanal', link):
            marcador="Catcher: ptcanal"; print marcador
            
            try:
                link=link.replace('content="setTimeout,','<p><script language="JavaScript">setTimeout')
                #descobrirresolver(url_frame,nomecanal,link,zapping,nomeserver)
                ptcanal=re.compile('<p><a href="(.+?)" onclick="window.open').findall(link)[0]
            except:
                try:ptcanal=re.compile('<p><iframe src="(.+?)"').findall(link)[0]
                except:ptcanal=re.compile("""setTimeout\("window.open\('([^"]+?)'""").findall(link)[0]
                
            descobrirresolver(ptcanal,nomecanal,False,zapping,nomeserver)

        elif re.search('RTP Play - RTP</title>',link):
            marcador="Catcher: RTP Play"; print marcador
            match=re.compile('\"file\": \"(.+?)\",\"application\": \"(.+?)\",\"streamer\": \"(.+?)\"').findall(link)
            temp = ['rtmp://' + match[0][2] +'/' + match[0][1] + '/' + match[0][0] + ' swfUrl=' + RTPURL + '/play/player.swf live=true timeout=15']
            temp.append(re.compile('\"smil\":\"(.+?)\"').findall(link)[0])
            if activado==True: opcao=True
            else:opcao= xbmcgui.Dialog().yesno("TV Portuguesa", "Escolha um stream da lista dos disponiveis.", "", "","Stream Extra", 'Stream Principal')
            if opcao: streamurl=temp[0]
            else: streamurl=redirect(temp[1])
            comecarvideo(streamurl, nomecanal,True,zapping)

        elif re.search('rtps',link):
            marcador="Catcher: rtps"; print marcador
            ficheiro=re.compile("file='(.+?).flv'.+?</script>").findall(link)[0]
            streamurl='rtmp://ec21.rtp.pt/livetv/ playPath=' + ficheiro + ' swfUrl=http://museu.rtp.pt/app/templates/templates/swf/pluginplayer.swf live=true timeout=15 pageUrl=http://www.rtp.pt/'
            comecarvideo(streamurl, nomecanal,True,zapping)

        elif re.search('h2e.rtp.pt',link) or re.search('h2g2.rtp.pt',link) or re.search('.rtp.pt',link) or re.search('provider=adaptiveProvider.swf',link) or re.search('file=rtp1',link):
            marcador="Catcher: rtp.pt"; print marcador
            link=link.replace('\\','').replace('">',"'>")
            if re.search('<strong><u>Clique para ver a ',link):
                urlredirect=re.compile("popup\('(.+?)'\)").findall(link)[0]
                descobrirresolver(urlredirect,nomecanal,False,zapping,nomeserver)
                return
            try:streamurl=re.compile("cid=(.+?).m3u8").findall(link)[0] + '.m3u8'
            except:
                try:
                    streamurl=re.compile("file=(.+?).m3u8(.+?)&").findall(link)[0]
                    streamurl='.m3u8'.join(streamurl)
                    streamurl=streamurl.replace('&abouttext=TV ZUNE PLAYER 2013','')
                except:
                    try:streamurl=re.compile("file=(.+?).m3u8").findall(link)[0] + '.m3u8'
                    except:
                        try:
                            rtmp=re.compile('streamer=(.+?)&').findall(link)[0]
                            filep=re.compile('file=(.+?)&').findall(link)[0]
                            try:swf=re.compile(" data='(.+?).swf\?").findall(link)[0] + '.swf'
                            except:swf=re.compile('src="(.+?)"').findall(link)[0]
                            
                            streamurl=rtmp + ' playPath=' + filep + ' swfUrl=' + swf + ' swfVfy=1 live=1 pageUrl=http://tvzune.tv/'
                        except:
                            #embed=re.compile('<iframe src="/flashmedia.php\?channel=(.+?)" id="innerIframe"').findall(link)[0]
                            #ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                            #embed=TVCoresURL + '/flashmedia.php?channel=' + embed
                            
                            #html= urllib.unquote(abrir_url_tommy(embed,ref_data)).replace('//-->','.rtp.pt')
                            #descobrirresolver(embed,nomecanal,html,zapping,nomeserver)
                            streamurl=url_frame.replace('http://tvfree.me/jw-player.html?cid=','')
                            #comecarvideo(streamurl,nomecanal,True,zapping)
                            #return
            #streamurl='rtmp://ec21.rtp.pt/livetv/ playPath=' + ficheiro + ' swfUrl=http://museu.rtp.pt/app/templates/templates/swf/pluginplayer.swf live=true timeout=15 pageUrl=http://www.rtp.pt/'            
            comecarvideo(streamurl , nomecanal,True,zapping)

        elif re.search('meocanaltv.com/embed',link):
            marcador="Catcher: stolen meocanaltv from tvgente"; print marcador
            if re.search('<script type="text/javascript"> cid="',link): chid=re.compile('cid="(.+?)";.+?</script>').findall(link)[0]
            else: chid=re.compile('src="http://www.meocanaltv.com/embed/(.+?).php').findall(link)[0]
            meotv='http://www.meocanaltv.com/embed/' + chid  + '.php'
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            html= abrir_url_tommy(meotv,ref_data)
            if re.search('embedsecure.js',html):
                html+=abrir_url_tommy(re.compile('src="([^"]+?)embedsecure.js"').findall(html)[0] + 'embedsecure.js',ref_data).decode('string-escape')
            descobrirresolver(meotv,nomecanal,html,zapping,nomeserver)

        elif re.search('=myStream.sdp',link): 
            marcador="Catcher: other rtp"; print marcador
            try:
                rtmpendereco=re.compile('streamer=(.+?)&').findall(link)[0]
                filepath=re.compile('file=(.+?)&').findall(link)[0]
                filepath=filepath.replace('.flv','')
            except:
                rtmpendereco=re.compile('file=(.+?)&').findall(link)[0]
                filepath=re.compile(';id=(.+?)&').findall(link)[0]
            
            swf="http://player.longtailvideo.com/player.swf"
            streamurl=rtmpendereco + ' playPath=' + filepath + ' swfUrl=' + swf + ' live=1 timeout=15 pageUrl=' + url_frame
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('pepestream.com',link) or re.search('src="http://www.livesportshd.eu/c',link) or re.search('cricfree.sx',link) or re.search('<p><iframe src="http://bit.ly/1lrVcOr"',link) or re.search('tugastream',link) or re.search('sicnoticias_sp.php',link) or re.search('verdirectotv.com/tv',link) or re.search('look-tvs.com',link):
            marcador="Catcher: stolen streams"; print marcador
            if re.search('pepestream.com',link): stolen='http://pepestream.com/' + re.compile('src="http://pepestream.com/(.+?)"').findall(link)[0]
            elif re.search('src="http://www.livesportshd.eu/c',link): stolen='http://www.livesportshd.eu/' + re.compile('src="http://www.livesportshd.eu/c(.+?)"').findall(link)[0]
            elif re.search('cricfree.sx',link): stolen='http://cricfree.sx/' + re.compile('src="http://cricfree.sx/(.+?)"').findall(link)[0]
            elif re.search('<p><iframe src="http://bit.ly/1lrVcOr"',link):stolen='http://bit.ly/1lrVcOr'
            elif re.search('tugastream',link): stolen='http://www.tugastream.com/' + re.compile('src=".+?tugastream.com/(.+?)".+?/iframe>').findall(link)[0]
            elif re.search('sicnoticias_sp.php',link): stolen = 'http://www.tugastream.com/sicnoticias_sp.php'
            elif re.search('verdirectotv.com/tv',link): stolen='http://verdirectotv.com/tv' + re.compile('src="http://verdirectotv.com/tv(.+?)">').findall(link)[0]
            elif re.search('look-tvs.com',link):stolen='http://www.look-tvs.com/' + re.compile('src="http://www.look-tvs.com/(.+?)"').findall(link)[0]
            else: iugsdaiusdagiuasd
            descobrirresolver(stolen,nomecanal,False,zapping,nomeserver)

        elif re.search('resharetv',link): #reshare tv
            marcador="Catcher: resharetv"; print marcador
            ref_data = {'Referer': 'http://resharetv.com','User-Agent':user_agent}
            html= abrir_url_tommy(url_frame,ref_data)
            html=clean(html)
            try:
                try: streamurl=re.compile(',  file: "(.+?)"').findall(html)[0]
                except: streamurl=re.compile('file: "(.+?)"').findall(html)[0]
            except:
                try:
                    swf=re.compile('<param name="movie" value="/(.+?)"></param>').findall(html)[0]
                    rtmp=re.compile('<param name="flashvars" value="src=http%3A%2F%2F(.+?)%2F_definst_%2F.+?%2Fmanifest.f4m&loop=true.+?">').findall(html)[0]
                    play=re.compile('_definst_%2F(.+?)%2Fmanifest.f4m&loop=true.+?">').findall(html)[0]
                except:
                    try:
                        swf=re.compile('src="(.+?)" type="application/x-shockwave-flash"').findall(html)[0]
                        rtmp=re.compile('streamer=(.+?)&amp').findall(html)[0]
                        play=re.compile('flashvars="file=(.+?).flv&').findall(html)[0]
                        streamurl='rtmp://' + urllib.unquote(rtmp) + ' playPath=' + play + ' live=true timeout=15 swfVfy=1 swfUrl=' + ResharetvURL + swf + ' pageUrl=' + ResharetvURL
                    except:
                        try:
                            frame=re.compile('<iframe.+?src="(.+?)">').findall(html)[0]
                            descobrirresolver(frame,nomecanal,False,zapping,nomeserver)
                            return
                        except:
                            if activado==False: mensagemok('TV Portuguesa','Não e possível carregar stream.')
                            return
            comecarvideo(streamurl, nomecanal,True,zapping)
            
        elif re.search('sharecast',link):
            marcador="Catcher: sharecast"; print marcador
            share=re.compile('src="http://sharecast.to/embed/(.+?)"></iframe>').findall(link)
            if not share: share=re.compile('src="http://sharecast.to/embed.php.+?ch=(.+?)"').findall(link)
            for chname in share:
                embed= 'http://sharecast.to/embed/' + chname
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                if re.search('Channel not found',html):
                    if activado==False: mensagemok('TV Portuguesa','Stream offline.')
                    return
                try:
                    playpath= re.compile('file: "(.+?)",').findall(html)[0]
                    rtmp= re.compile('streamer: "(.+?)",').findall(html)[0]
                    conteudo=rtmp + ' playPath=' + playpath
                except:
                    rtmp= re.compile('file: "(.+?)",').findall(html)[0]
                    conteudo=rtmp
                
                streamurl= conteudo + ' live=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('surfline',link):
            marcador="Catcher: surfline"; print marcador
            idcam=re.compile('spotid = (.+?),').findall(link)[0]            
            streaminfo=abrir_url('http://api.surfline.com/v1/syndication/cam/'+idcam).replace('\\','')
            if re.search('"camStatus":"down"',streaminfo):
                if activado==False: mensagemok('TV Portuguesa','Stream está offline.')
                return
            streamurl=re.compile('"file":"(.+?)"').findall(streaminfo)[0]
            comecarvideo(streamurl,nomecanal,True,zapping)

        #elif re.search('p,a,c,k,e,r',link):
        #    marcador="Catcher: zuuk ruu.php"; print marcador
        #    link=link.replace('|','')
        #    tuga=re.compile('ruuphpnr(.+?)style').findall(link)[0]
        #    descobrirresolver("http://www.zuuk.net/ruu.php?nr=" + tuga,nomecanal,False,zapping,nomeserver)

        elif re.search('http://portalzuca.net',link):
            marcador="Catcher: portalzuca"; print marcador
            tuga='http://portalzuca.net/' + re.compile('src="http://portalzuca.net/(.+?)"').findall(link)[0]
            descobrirresolver(tuga,nomecanal,False,zapping,nomeserver)

        elif re.search('pontucanal.net/iframe',link):
            marcador="Catcher: pontucanal iframe"; print marcador
            embed='http://pontucanal.tv/iframe/' + re.compile('src="http://pontucanal.net/iframe/(.+?)\?W=').findall(link)[0]
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            html= abrir_url_tommy(embed,ref_data)
            descobrirresolver(embed,nomecanal,html,zapping,nomeserver)

        elif re.search('sawlive', link):
            marcador="Catcher: sawlive"; print marcador
            saw=re.compile('src="http://sawlive.tv/embed/(.+?)">').findall(link)
            for chid in saw:
                embed='http://sawlive.tv/embed/'+chid
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                link= abrir_url_tommy(embed,ref_data)
                jsU = JsUnpackerV2()
                link = urllib.unquote(jsU.unpackAll(link).replace(";Tamrzar.push('",'').replace("')",''))
                cont=re.compile('src="(.+?)"').findall(link)[0]
                ref_data = {'Referer': embed,'User-Agent':user_agent}
                html= jsU.unpackAll(abrir_url_tommy(cont,ref_data))
                swf=re.compile("SWFObject\('(.+?)',").findall(html)[0]
                filep=re.compile("'file', '(.+?)'").findall(html)[0]
                rtmp=re.compile("'streamer', '(.+?)'").findall(html)[0]
                streamurl=rtmp + ' playPath=' + filep + ' swfUrl='+swf+' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('streamcasttv', link):
            marcador="Catcher: streamcasttv"; print marcador
            scast=re.compile("file='(.+?)'.+?</script>").findall(link)
            if not scast: scast=re.compile('<iframe src="/streamcasttv.php\?file=(.+?)" id="innerIframe"').findall(link)
            for chid in scast:
                embed='http://www.streamcasttv.biz/embed.php?file='+chid+'&width=650&height=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data).encode('ascii','ignore').decode('utf-8')
                swf='http://www.streamcasttv.biz/jwplayer/jwplayer.flash.swf'
                if re.search("src='http://streamcasttv.biz/embed/",html):
                    extra=True
                    chid=re.compile("file='(.+?)';.+?</script>").findall(html)[0]
                    ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                    embed='http://www.streamcasttv.biz/embed/21r.php?file='+chid+'&width=650&height=400'
                    html= abrir_url_tommy(embed,ref_data).encode('ascii','ignore').decode('utf-8')
                    swf='http://www.streamcasttv.biz/embed/jwplayer/jwplayer.flash.swf'
                else: extra=False
                
                rtmp=re.compile("file: '(.+?)'").findall(html)[0]
                if extra==True: chid=''.join((rtmp.split('/'))[-1:]).replace('.smil','')
                rtmp='/'.join((rtmp.split('/'))[:-1]) + '/'
                streamurl=rtmp + ' playPath=' + chid + ' swfUrl='+swf+' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('streamify', link):
            marcador="Catcher: streamify"; print marcador
            flive=re.compile('channel="(.+?)",.+?></script>').findall(link)
            for chid in flive:
                embed='http://www.streamify.tv/embedplayer/'+chid+'/1/650/400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                if re.search('Channel is domain protected.',html):
                    url_frame='http://www.streamify.tv/' + chname
                    ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                    html= abrir_url_tommy(embed,ref_data)
                swf=re.compile('SWFObject.+?"(.+?)",').findall(html)
                flashvars=re.compile("so.addParam.+?'FlashVars'.+?'(.+?);").findall(html)[0]
                flashvars=flashvars.replace("')","&nada").split('l=&')
                if flashvars[1]=='nada':
                    nocanal=re.compile("&s=(.+?)&").findall(flashvars[0])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[0]
                else:
                    nocanal=re.compile("&s=(.+?)&nada").findall(flashvars[1])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[1]
                nocanal=nocanal.replace('&','')
                link=abrir_url('http://www.streamify.tv:1935/loadbalancer')
                rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)[0]
                streamurl='rtmp://' + rtmpendereco + '/live/ playPath=' + nocanal + '?id=' + chid + ' swfVfy=1 conn=S:OK live=true swfUrl=http://www.streamify.tv' + swf[0] + ' ccommand=keGoVidishStambolSoseBardovci;TRUE;TRUE pageUrl=' + embed
                #lib
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('sapo.pt',link):
            marcador="Catcher: sapo.pt"; print marcador
            #lista=re.compile('file=(.+?)&').findall(link)[0]
            #streams=abrir_url(lista + '?all=1').replace('\\','')
            #streamurl=re.compile('"hls":"(.+?)"').findall(streams)[0]
            '''            
            link=link.replace('" frameborder="0" scrolling="no"','&')#ugly
            try:
                swf='http://js.sapo.pt/Projects/Video/140708R1/flash/videojs.swf'
                try:
                    print "Method 1"
                    chname=re.compile('live/(.+?)&').findall(link)[0]
                    filepath=re.compile('file=(.+?)&').findall(link)[0]
                except:
                    print "Method 2"
                    chname=re.compile('http://videos.sapo.pt/(.+?)"').findall(link)[0]
                    info=abrir_url('http://videos.sapo.pt/'+chname)
                    filepath=re.compile('/live/(.+?)",').findall(info)[0]
                host=abrir_url('http://videos.sapo.pt/hosts_stream.html')
                hostip=re.compile('<host>(.+?)</host>').findall(host)[0]
                if re.search('playersrc="',link):
                    jslink=re.compile('playersrc="(.+?)"').findall(link)[0]
                    jslink=jslink.split('.js')
                    swf=jslink[0]
                    swf=swf.replace('Video','flash/videojs.swf')
                #else:
                
                streamurl='rtmp://' + hostip + '/live' + ' playPath=' + chname  + ' swfUrl='+swf+' live=true pageUrl=http://videos.sapo.pt/'+chname
            except:
            '''
            print "Method 3"
            swf='http://js.sapo.pt/Projects/Video/140708R1/flash/videojs.swf'
            try:
                print "Method 1"
                chname=re.compile('live/(.+?)&amp;').findall(link)[0]
                filepath=re.compile('file=(.+?)&').findall(link)[0]
                host=abrir_url('http://videos.sapo.pt/hosts_stream.html')
                hostip=re.compile('<host>(.+?)</host>').findall(host)[0]
                streamurl='rtmp://' + hostip + '/live' + ' playPath=' + chname  + ' swfUrl='+swf+' live=true pageUrl=http://videos.sapo.pt/'+chname
            except:
                lista=re.compile('file=(.+?)&').findall(link)[0]
                streams=abrir_url(lista + '?all=1').replace('\\','')
                try:
                    #rtmp
                    rtmp=re.compile('"rtmp":"(.+?)"').findall(streams)[0]
                    chname=rtmp.split('/')[-1:][0]
                    streamurl=rtmp + ' playPath=' + chname  + ' swfUrl='+swf+' live=true pageUrl=http://videos.sapo.pt/'+chname
                except:
                    #m3u8
                    streamurl=re.compile('"hls":"(.+?)"').findall(streams)[0]
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('surftotal',link):
            marcador="Catcher: surftotal"; print marcador
            try:
                try:streamurl=re.compile("""<source src="([^"]+?)" type='rtmp/mp4'>""").findall(link)[0]
                except:streamurl=re.compile('<source src="([^"]+?)" type="application/x-mpegURL">').findall(link)[0]
                comecarvideo(streamurl,nomecanal,True,zapping)
            except:                
                if activado==False: mensagemok('TV Portuguesa','Stream está offline.')
                return
            

        elif re.search('telewizja',link) or re.search('sapo.tv.php',link):
            marcador="Catcher: telewizja or sapo.tv"; print marcador
            codigo=re.compile('<br/><iframe src="(.+?)" id="innerIframe"').findall(link)[0]
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            embed=TVCoresURL + codigo
            html= abrir_url_tommy(embed,ref_data)
            descobrirresolver(embed,nomecanal,html,zapping,nomeserver)

        elif re.search('televisaofutebol',link):
            marcador="Catcher: televisaofutebol"; print marcador
            link=link.replace('\\','')
            tuga=re.compile('src="http://www.televisaofutebol.com/(.+?)".+?/iframe>').findall(link)[0]
            embed='http://www.televisaofutebol.com/' + tuga
            ref_data = {'Referer': 'http://www.estadiofutebol.com','User-Agent':user_agent}
            html= abrir_url_tommy(embed,ref_data)
            descobrirresolver(embed,nomecanal,html,zapping,nomeserver)

        elif re.search('http://tinyurl.com/',link):
            marcador="Catcher: tinyurl obfuscate"; print marcador
            embed=redirect(url_frame)
            descobrirresolver(embed,nomecanal,False,zapping,nomeserver)

        elif re.search('tvgo.be',url_frame):
            marcador="Catcher: tvbgo.be"; print marcador
            streamurl=re.compile('<a class="my-button" href="(.+?)"').findall(link)[0].replace('playlist','chunks')# + '|User-Agent=' + urllib.quote('PS3Application libhttp/4.5.5-000 (CellOS)')#Mozilla%2F5.0%20(iPad%3B%20CPU%20OS%206_0%20like%20Mac%20OS%20X)%20AppleWebKit%2​F536.26%20(KHTML%2C%20like%20Gecko)%20Version%2F6.0%20Mobile%2F10A5355d%20Safari​%2F8536.25'
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('streamago',link):
            marcador="Catcher: streamago"; print marcador
            flive=re.compile('<iframe src="http://www.streamago.tv/iframe/(.+?)/"').findall(link)
            if not flive:
                if re.search('streamago.php?id=',url_frame):
                    flive=url_frame('http://tvfree.me/streamago.php?id=','')
            for chid in flive:
                embed=redirect('http://www.streamago.tv/iframe/'+chid)
                html=abrir_url(embed)
                if re.search('the page you requested cannot be found.',html):
                    if activado==False: mensagemok('TV Portuguesa','Stream está offline.')
                    return
                swf=re.compile('swfobject.embedSWF\("(.+?)",').findall(html)[0]
                fvars=re.compile('flashvars.xml = "(.+?)"').findall(html)[0]
                dados=abrir_url(fvars)
                playpath=re.compile('<titolo id="(.+?)">').findall(dados)[0]
                rtmp=re.compile('<path><\!\[CDATA\[(.+?)\]\]></path>').findall(dados)[0]
                streamurl=rtmp + ' playPath=' + playpath + ' swfVfy=1 live=true swfUrl=http://www.streamago.tv' + swf + ' pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)
                
        elif re.search('tv-msn',link):
            marcador="Catcher: tv-msn"; print marcador
            if re.search('cdnbr.biz',link):
                link=link.replace('<img border="0" src="','')
                url_frame=re.compile('src="(.+?)"').findall(link)[0]
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                link= abrir_url_tommy(url_frame,ref_data).encode('ascii','ignore')
                swf=re.compile("<param name='movie' value='(.+?)'>").findall(link)[0]
            else:
                swf=re.compile("src='(.+?)'").findall(link)[0]

            variaveis=re.compile("file=(.+?).flv&streamer=(.+?)&").findall(link)[0]
            streamurl=variaveis[1] + ' playPath=' + variaveis[0]  + ' swfUrl='+swf+' live=true timeout=15 swfVfy=1 pageUrl='+url_frame
            
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('tvph.googlecode.com',link):
            marcador="Catcher: tvph google code"; print marcador
            if re.search('playeer.html',link):
                info=re.compile("cid=file=(.+?)&streamer=(.+?)'").findall(link)[0]
                rtmp=info[1]
                streamurl=rtmp + ' playPath='+info[0]+' swfUrl=http://www.tvzune.tv/jwplayer/jwplayer.flash.swf live=true pageUrl=' + url_frame
            else:
                streamurl=re.compile("cid=(.+?)'").findall(link)[0]
            comecarvideo(streamurl,nomecanal,True,zapping)
            

        elif re.search('TV ZUNE PLAYER 201',link):
            marcador="Catcher: player tvzune soft"; print marcador
            rtmp=re.compile('streamer=(.+?)&').findall(link)[0]
            filep=re.compile('file=(.+?)&').findall(link)[0]
            ref_data = {'User-Agent':''}
            url_frame=url_frame.replace('canais','privado')
            html= abrir_url_tommy(url_frame,ref_data)

            ref_data = {'Accept': '*/*','User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; Trident/7.0; .NET4.0E; .NET4.0C; InfoPath.3; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729)','Cookie': 'jm3x_unique_user=1','Host': 'www.tvzune.tv','Connection': 'Keep-Alive'}
            nada= re.compile('<iframe.+?src="(.+?)"').findall(limparcomentarioshtml(abrir_url_tommy(html,ref_data),html))[0]

            ref_data = {'Accept': 'image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*','User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; Trident/7.0; .NET4.0E; .NET4.0C; InfoPath.3; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729)','Host': 'fire.tvzune.org','Connection': 'Keep-Alive'}
            nada= abrir_url_tommy(nada,ref_data)
            
            swf=re.compile('src="(.+?)"').findall(link)[0]
            streamurl=rtmp + ' playPath=' + filep + ' swfUrl=' + swf + ' swfVfy=1 live=1 pageUrl=' + html
            comecarvideo(streamurl,nomecanal,True,zapping)
            
        elif re.search('player_tvzune',link):
            marcador="Catcher: player tvzune"; print marcador
            yoyo412=re.compile(yoyo115 + ' "(.+?)"').findall(link)[0]
            yoyo721='/'.join((yoyo412.split('/'))[:-1])
            yoyo721='rtmp://premium2.tvzune.org:1935/live/'
            yoyo428=re.compile('src="(.+?)"').findall(link)[0]
            yoyo683=re.compile(yoyo265 + '(.+?)"').findall(abrir_url(yoyo428))[0]
            yoyo378='/'.join((yoyo428.split('/'))[:-1]) + '/' + yoyo683
            streamurl=yoyo721 + ' playPath=' + yoyo412.split('/')[-1] + ' swfUrl=' +yoyo378 +' live=true pageUrl=' + url_frame
            comecarvideo(streamurl,nomecanal,True,zapping)
            

        elif re.search('stream4u', link):
            marcador="Catcher: stream4u"; print marcador
            stream4u=re.compile('fid="(.+?)";.+?></script>').findall(link)
            for chid in stream4u:
                embed='http://www.stream4u.eu/embed.php?v='+chid+'&vw=650&vh=400&domain='+url_frame
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("'flashplayer': '(.+?)'").findall(html)[0]
                rtmp=re.compile("'streamer': '(.+?)'").findall(html)[0]
                streamurl=rtmp + ' playPath=' + chid + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('<meta property="og:url" content="http://www.tvi.iol',link): #tvioficial
            marcador="Catcher: tvi oficial"; print marcador
            streamurl=re.compile('file: "(.+?)"').findall(link)[0]
            comecarvideo(streamurl,nomecanal,True,zapping)
            
        elif re.search('ukcast.co', link):
            marcador="Catcher: ukcast.co"; print marcador
            stream4u=re.compile('ukcast.co/.+?u=(.+?)&').findall(link)
            for chid in stream4u:
                embed='http://ukcast.co/embed.php?u='+chid+'&vw=100%&vh=100%'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                rtmp=re.compile('var str = "(.+?)";').findall(html)[0].replace('cdn','strm')
                swf=re.compile('new SWFObject\("(.+?)"').findall(html)[0]
                streamurl=rtmp + ' playPath=' + chid + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('up4free', link):
            marcador="Catcher: up4free"; print marcador
            stream4u=re.compile("id='(.+?)';.+?></script>").findall(link)
            for chid in stream4u:
                embed='http://up4free.com/stream.php?id='+chid+'&width=650&height=450&stretching='
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                descobrirresolver(embed,nomecanal,html,zapping,nomeserver)

        elif re.search('valeucara', link):
            marcador="Catcher: valeucara"; print marcador
            valeu=re.compile('<script type="text/javascript"> id="(.+?)";.+?></script>').findall(link)
            for chid in valeu:
                embed='http://www.valeucara.com/'+chid+'_s.php?width=650&height=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= limparcomentarioshtml(abrir_url_tommy(embed,ref_data),embed)
                if re.search('file: "',html):
                    streamurl=re.compile('file: "(.+?)"').findall(html)[0]
                    comecarvideo(streamurl,nomecanal,True,zapping)
                else: descobrirresolver(embed,nomecanal,html,zapping,nomeserver)


        elif re.search('veecast',link):
            marcador="Catcher: veecast"; print marcador
            valeu=re.compile('src="http://www.veecast.net/e/(.+?)">').findall(link)
            for chid in valeu:
                embed='http://www.veecast.net/e/'+chid + '?width=640&height=480'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= urllib.unquote(abrir_url_tommy(embed,ref_data))
                rtmp=re.compile('streamer=(.+?)&').findall(html)[0]
                filep=re.compile('file=(.+?)&').findall(html)[0]
                swf=re.compile('src="(.+?)" type="application/x-shockwave-flash"').findall(html)[0]
                streamurl=rtmp + ' playPath=' + filep + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + url_frame
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('vercosasgratis', link):
            marcador="Catcher: vercosasgratis"; print marcador
            try:cenas=re.compile("""vercosasgratis.com/([^"]+?)'""").findall(link)[0]
            except:cenas=re.compile('vercosasgratis.com/([^"]+?)"').findall(link)[0]
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            framesite='http://vercosasgratis.com/' + cenas
            html= abrir_url_tommy(framesite,ref_data)
            embed=re.compile("var url = '(.+?)'").findall(html)[0]
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            html= abrir_url_tommy(embed,ref_data)
            swf=re.compile("SWFObject\('(.+?)'").findall(html)[0].replace('../','')
            rtmp=re.compile("'streamer', '(.+?)'").findall(html)[0]
            filep=re.compile("'file', '(.+?)'").findall(html)[0]
            streamurl=streamurl=rtmp + ' playPath=' + filep + ' swfUrl=http://vercosasgratis.com/' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
            comecarvideo(streamurl,nomecanal,True,zapping)
            
        elif re.search('veetle',url_frame) or re.search("src='http://veetle",link) or re.search('src="http://veetle',link):
            marcador="Catcher: veetle"; print marcador
            if activado==False:
                if selfAddon.getSetting("verif-veetle3") == "false":
                    ok = mensagemok('TV Portuguesa','Necessita de instalar o addon veetle.','Este irá ser instalado já de seguida.')
                    urlfusion='http://fightnight-xbmc.googlecode.com/svn/addons/fightnight/plugin.video.veetle/plugin.video.veetle-0.3.1.zip' #v2.3
                    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
                    lib=os.path.join(path, 'plugin.video.veetle.zip')
                    downloader(urlfusion,lib)
                    addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
                    xbmc.sleep(2000)
                    dp = xbmcgui.DialogProgress()
                    #if dp.iscanceled(): dp.close()
                    dp.create("TV Portuguesa", "A instalar...")
                    try:
                        extract(lib,addonfolder,dp,type="all")
                        ok = mensagemok('TV Portuguesa','Veetle instalado / actualizado.','Necessita de reiniciar o XBMC.')
                        selfAddon.setSetting('verif-veetle3',value='true')
                    except:
                        ok = mensagemok('TV Portuguesa','Sem acesso para instalar Veetle. Instale o veetle','do repositório fightnight.','De seguida, active o Veetle nas definições do addon.')
                else:
                    ## PATCH SPTHD IN LSHD
                    if re.search('var urls = new Array',link):
                            framedupla=re.compile('new Array.+?"(.+?)".+?"(.+?)"').findall(link)[0]
                            if framedupla[0]==framedupla[1]: frame=framedupla[0]
                            else:
                                if activado==True: opcao=True
                                else:opcao= xbmcgui.Dialog().yesno("TV Portuguesa", "Escolha um stream da lista dos disponiveis.", "", "","Stream Extra", 'Stream Principal')
                                if opcao: frame=framedupla[0]
                                else: frame=framedupla[1]
                            descobrirresolver(frame, nomecanal,False,False,nomeserver)
                            return
                    
                    try:idembed=re.compile('/index.php/widget/index/(.+?)/').findall(link)[0]
                    except: idembed=re.compile('/index.php/widget#(.+?)/true/16:').findall(link)[0]
                    print "ID embed: " + idembed
                    try:
                        chname=abrir_url('http://fightnightaddons2.96.lt/tools/veet.php?id=' + idembed)
                        chname=chname.replace(' ','')
                        if re.search('DOCTYPE HTML PUBLIC',chname):
                            if activado==False: mensagemok('TV Portuguesa','Erro a obter link do stream. Tenta novamente.')
                            return
                        print "ID final obtido pelo TvM."
                    except:
                        chname=abrir_url('http://fightnight-xbmc.googlecode.com/svn/veetle/sporttvhdid.txt')
                        print "ID final obtido pelo txt."
                    print "ID final: " + chname
                    link=abrir_url('http://veetle.com/index.php/channel/ajaxStreamLocation/'+chname+'/flash')
                    if re.search('"success":false',link):
                        if activado==False: mensagemok('TV Portuguesa','O stream está offline.')
                    else:
                        streamfile='plugin://plugin.video.veetle/?channel=' + chname
                        comecarvideo(streamfile,nomecanal,True,zapping)

        elif re.search('veemi', link):
            marcador="Catcher: veemi"; print marcador
            veemi=re.compile('fid="(.+?)";.+?></script>').findall(link)
            for chid in veemi:
                embed='http://www.veemi.com/embed.php?v='+chid+'&vw=650&vh=400&domain='+url_frame
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("SWFObject\('(.+?)'").findall(html)[0]
                rtmp=re.compile("'streamer', '(.+?)'").findall(html)[0]
                streamurl=rtmp + ' playPath=' + chid + ' swfUrl=http://www.veemi.com/' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)


        elif re.search('www.wcast', link):
            marcador="Catcher: wcast"; print marcador
            wcast=re.compile("fid='(.+?)';.+?></script>").findall(link)
            for chid in wcast:
                embed='http://www.wcast.tv/embed.php?u=' + chid+ '&vw=600&vh=470'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf='http://www.wcast.tv/player/player.swf'
                filelocation=re.compile("so.addVariable.+?'file'.+?'(.+?)'").findall(html)
                rtmpendereco=re.compile("so.addVariable.+?'streamer'.+?'(.+?)'").findall(html)
                streamurl=rtmpendereco[0] + ' playPath=' + filelocation[0] + ' swfUrl=' + swf + ' live=true swfVfy=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('ucaster', link):
            marcador="Catcher: ucaster"; print marcador
            ucaster=re.compile("channel='(.+?)',.+?></script>").findall(link)
            if not ucaster: ucaster=re.compile('flashvars="id=.+?&s=(.+?)&g=1&a=1&l=').findall(link)
            if not ucaster: ucaster=re.compile('src="/ucaster.eu.php.+?fid=(.+?)" id="innerIframe"').findall(link)
            if not ucaster: ucaster=re.compile('flashvars="id=.+?&amp;s=(.+?)&amp;g=1').findall(link)
            if not ucaster: ucaster=re.compile("flashvars='id=.+?&s=(.+?)&").findall(link)
            if not ucaster: ucaster=re.compile('flashvars="id=.+?id=.+?&amp;s=(.+?)&amp;g=1').findall(link)
            if not ucaster: ucaster=re.compile('channel="(.+?)".+?g="1"').findall(link)
            #if not ucaster:
                #mensagemok('TV Portuguesa','Stream não é o do site responsável','logo não é possível visualizar.')
            for chname in ucaster:
                embed='http://www.ucaster.eu/embedded/' + chname + '/1/600/430'
                try:
                    ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                    html= abrir_url_tommy(embed,ref_data)
                    swf=re.compile('SWFObject.+?"(.+?)",').findall(html)[0]
                    flashvars=re.compile("so.addParam.+?'FlashVars'.+?'(.+?);").findall(html)[0]
                    if re.search('&a=1&l=www.tvgente.eu',flashvars): flashvars=flashvars.replace("')","&nada").split('l=www.tvgente.eu&')
                    else: flashvars=flashvars.replace("')","&nada").split('l=&')
                    if flashvars[1]=='nada':
                        nocanal=re.compile("&s=(.+?)&").findall(flashvars[0])[0]
                        chid=re.compile("id=(.+?)&s=").findall(html)[0]
                    else:
                        nocanal=re.compile("&s=(.+?)&nada").findall(flashvars[1])[0]
                        chid=re.compile("id=(.+?)&s=").findall(html)[1]
                    nocanal=nocanal.replace('&','')
                except:
                    nocanal=chname
                    chid=re.compile("flashvars='id=(.+?)&s").findall(link)[0]
                    swf=re.compile("true' src='http://www.ucaster.eu(.+?)'").findall(link)[0]
                link=abrir_url('http://www.ucaster.eu:1935/loadbalancer')
                rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)[0]
                streamurl='rtmp://' + rtmpendereco + '/live playPath=' + nocanal + '?id=' + chid + ' swfVfy=1 conn=S:OK live=true swfUrl=http://www.ucaster.eu' + swf + ' ccommand=vujkoMiLazarBarakovOdMonospitovo;TRUE;TRUE pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('xuuby',link): ##proteccao tvdez
            marcador="Catcher: xuuby"; print marcador
            xuuby=re.compile('chname="(.+?)".+?</script>').findall(link)
            if not xuuby: xuuby=re.compile('chname=(.+?)&').findall(link)
            for chname in xuuby:
                embed='http://www.xuuby.com/show2.php?chname='+chname+'&width=555&height=555&a=1'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                html=urllib.unquote(html)
                streamurl=re.compile('file: "(.+?)"').findall(html)[0]
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('youtube.com/v',link):
            marcador="Catcher: youtube"; print marcador
            idvideo=re.compile('type="application/x-shockwave-flash" src="http://www.youtube.com/v/(.+?)&.+?"></object>').findall(link)[0]
            sources=[]
            import urlresolver
            embedvideo='http://www.youtube.com/watch?v=' + idvideo
            hosted_media = urlresolver.HostedMediaFile(url=embedvideo)
            sources.append(hosted_media)
            source = urlresolver.choose_source(sources)
            if source:
                streamurl=source.resolve()
                comecarvideo(streamurl,nomecanal,True,zapping)
                    
        elif re.search('yocast', link):
            marcador="Catcher: yocast"; print marcador
            stream4u=re.compile("fid='(.+?)';.+?></script>").findall(link)
            for chid in stream4u:
                embed='http://www.yocast.tv/embed.php?s='+chid+'&width=650&height=400&domain='+url_frame
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                swf=re.compile("'flashplayer': '(.+?)'").findall(html)[0]
                rtmp=re.compile("'streamer': '(.+?)'").findall(html)[0]
                streamurl=rtmp + ' playPath=' + chid + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('youcloud', link):
            marcador="Catcher: youcloud"; print marcador
            hqst=re.compile("youcloud.tv/embed/(.+?)\?").findall(link)
            for chid in hqst:
                embed='http://youcloud.tv/player?streamname=' + chid
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                fp=int(re.compile('var f =\s*([^;]+)').findall(html)[0])
                ap=int(re.compile('var a =\s*([^;]+)').findall(html)[0])/fp
                bp=int(re.compile('var b =\s*([^;]+)').findall(html)[0])/fp
                cp=int(re.compile('var c =\s*([^;]+)').findall(html)[0])/fp
                dp=int(re.compile('var d =\s*([^;]+)').findall(html)[0])/fp
                vp=re.compile("var v_part =\s*'([^']+).*").findall(html)[0]

                streamurl='rtmp://%s.%s.%s.%s%s swfUrl=http://cdn.youcloud.tv/jwplayer.flash.swf live=1 timeout=15 swfVfy=1 pageUrl=%s' % (ap,bp,cp,dp,vp,embed)
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('yukons', link):
            marcador="Catcher: yukons"; print marcador
            yukons=re.compile('kuyo&file=(.+?)&').findall(link)
            if not yukons: yukons=re.compile("file='(.+?)'.+?</script>").findall(link)
            if not yukons: yukons=re.compile('channel="(.+?)".+?</script>').findall(link)
            if not yukons: yukons=re.compile('file=(.+?)&').findall(link)
            for chname in yukons:
                idnumb='373337303331363236323737'
                ref_data = {'Host': 'yukons.net','Connection': 'keep-alive','Accept': '*/*','Referer': url_frame,'User-Agent':user_agent,'Cache-Control': 'max-age=0','Accept-Encoding': 'gzip,deflate,sdch'}
                link= abrir_url_tommy('http://yukons.net/yaem/' + idnumb,ref_data)
                idfinal=re.compile("return '(.+?)'").findall(link)[0]
                embed='http://yukons.net/embed/'+idnumb+'/'+idfinal+'/600/450'
                ref_data = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Referer': url_frame,'User-Agent':user_agent,'Host': 'yukons.net','Cache-Control': 'max-age=0','Accept-Encoding': 'gzip,deflate,sdch','Connection': 'keep-alive'}
                html= abrir_url_tommy(embed,ref_data)
                idrtmp=re.compile('FlashVars\|id\|(.+?)\|').findall(html)[0]
                pidrtmp=re.compile('\|pid\|\|(.+?)\|').findall(html)[0]
                swfrtmp=re.compile('SWFObject\|.+?\|\|\|(.+?)\|swf\|eplayer').findall(html)[0]
                #'Referer': 'http://yukons.net/' + swfrtmp + '.swf'
                ref_data = {'Referer': embed,'User-Agent':user_agent,'Host': 'yukons.net','Connection': 'keep-alive','Accept':'*/*','Accept-Encoding': 'gzip,deflate,sdch'}
                servertmp= abrir_url_tommy('http://yukons.net/srvload/'+ idrtmp,ref_data).replace('srv=','')

                streamurl='rtmp://' + servertmp + ':443/kuyo playPath=' + chname + '?id=' + idrtmp + '&pid=' + pidrtmp + ' swfUrl=http://yukons.net/'+swfrtmp + '.swf live=true conn=S:OK timeout=14 swfVfy=true ccommand=trxuwaaLahRKnaechb;TRUE;TRUE pageUrl=' + embed
                #swf = 'http://yukons.net/'+swfrtmp + '.swf?streamer=rtmp://' + servertmp + ':443/kuyo&file='+chname+'&autostart=true&g=1&a=1&l='
                #streamurl='rtmp://' + servertmp + ':443/kuyo playPath=' + chname  + '?id=' + idrtmp + '&pid=' + pidrtmp + ' swfUrl=' + swf + ' live=true conn=S:OK timeout=14 swfVfy=true pageUrl=' + swf
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('wowcast.tv', link):
            marcador="Catcher: wowcast"; print marcador
            stream4u=re.compile('fid="(.+?)";.+?></script>').findall(link)
            for chid in stream4u:
                embed='http://www.wowcast.tv/embed.php?stream='+chid+'&vw=650&vh=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                
                swf=re.compile('SWFObject\("(.+?)"').findall(html)[0]
                rtmp=re.compile('"streamer", "(.+?)"').findall(html)[0]
                streamurl=rtmp + ' playPath=' + chid + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('yycast', link):
            marcador="Catcher: yycast"; print marcador
            yycast=re.compile('fid="(.+?)";.+?</script><script type="text/javascript" src="http://www.yycast.com/javascript/embedPlayer.js"></script>').findall(link)
            if not yycast: yycast=re.compile("file='(.+?).flv'.+?</script>").findall(link)
            if not yycast: yycast=re.compile('fid="(.+?)".+?</script>').findall(link)
            if not yycast: yycast=re.compile('channel="(.+?)".+?</script>').findall(link)
            for chname in yycast:
                embed='http://yycast.com/embedded/'+ chname + '/1/555/435'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                link=abrir_url('http://yycast.com:1935/loadbalancer')
                rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)[0]
                swf=re.compile('SWFObject.+?"(.+?)"').findall(html)[0]
                idnum=re.compile("'FlashVars', 'id=(.+?)&s=.+?'").findall(html)[0]
                chnum=re.compile("'FlashVars', 'id=.+?&s=(.+?)&").findall(html)[0]
                streamurl='rtmp://' + rtmpendereco + '/live/ playPath=' + chnum + '?id=' + idnum + ' swfVfy=1 timeout=15 conn=S:OK live=true ccommand=trajkoProkopiev;TRUE;TRUE swfUrl=http://yycast.com' + swf + ' pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('fa16bb1eb942c5c48ac3cd66aff4c32f2a015b1af198c14b88',link):
            marcador="Catcher: fa16bb hash"; print marcador
            stream4u=re.compile('id="(.+?)";.+?></script>').findall(link)
            for chid in stream4u:
                embed='http://fa16bb1eb942c5c48ac3cd66aff4c32f2a015b1af198c14b88.com/gen_s.php?id='+chid#+'&PageSpeed=noscript'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data).encode('latin-1','ignore')
                from resources.lib import unwise
                jsUW = unwise.JsUnwiser()
                if jsUW.containsWise(html):
                    html = jsUW.unwiseAll(html)
                temp=re.compile(",file:'(.+?)'").findall(html)[0]
                rtmp='/'.join(temp.split('/')[:-1])
                playpath=''.join(temp.split('/')[-1:])
                swf=re.compile('<script src="([^"]+?)/.+?html5.+?.js"></script>').findall(html)[0] + '/jwplayer.flash.swf'
                streamurl=rtmp + ' playPath=' + playpath + ' swfUrl=http://xuscacamusca.se/' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)


        elif re.search('xuscacamusca.se', link):
            marcador="Catcher: xuscacamusca.se"; print marcador
            stream4u=re.compile('id="(.+?)";.+?></script>').findall(link)
            for chid in stream4u:
                embed='http://xuscacamusca.se/?id='+chid+'&PageSpeed=noscript'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data).encode('latin-1','ignore')
                from resources.lib import unwise
                jsUW = unwise.JsUnwiser()
                if jsUW.containsWise(html):
                    html = jsUW.unwiseAll(html)
                temp=re.compile(",file:'(.+?)'").findall(html)[0]
                rtmp='/'.join(temp.split('/')[:-1])
                playpath=''.join(temp.split('/')[-1:])
                swf=re.compile('<script src="([^"]+?)/.+?html5.+?.js"></script>').findall(html)[0] + '/jwplayer.flash.swf'
                streamurl=rtmp + ' playPath=' + playpath + ' swfUrl=http://xuscacamusca.se/' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('mybeststream.xyz', link):
            marcador="Catcher: mybeststream.xyz"; print marcador
            stream4u=re.compile('id="(.+?)";.+?></script>').findall(link)
            for chid in stream4u:
                embed='http://mybeststream.xyz/?id='+chid+'&PageSpeed=noscript'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data).encode('latin-1','ignore')
                from resources.lib import unwise
                jsUW = unwise.JsUnwiser()
                if jsUW.containsWise(html):
                    html = jsUW.unwiseAll(html)
                temp=re.compile(",file:'(.+?)'").findall(html)[0]
                rtmp='/'.join(temp.split('/')[:-1])
                playpath=''.join(temp.split('/')[-1:])
                swf=re.compile('<script src="([^"]+?)/.+?html5.+?.js"></script>').findall(html)[0] + '/jwplayer.flash.swf'
                streamurl=rtmp + ' playPath=' + playpath + ' swfUrl=http://xuscacamusca.se/' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('zcast.us', link):
            marcador="Catcher: zcast"; print marcador
            zcast=re.compile('channel="(.+?)";.+?></script>').findall(link)
            for chname in zcast:
                embed='http://zcast.us/gen.php?ch=' + chname + '&width=700&height=480'
                streamurl='rtmp://gabon.zcast.us/liveedge' + ' playPath=' + url_frame + ' live=true timeout=15 swfVfy=1 swfUrl=http://player.zcast.us/player58.swf pageUrl=http://www.xuuby.com/'
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('zenex', link):
            marcador="Catcher: zenex"; print marcador
            zenex=re.compile("channel='(.+?)',.+?</script>").findall(link)
            for chname in zenex:
                embed='http://www.zenex.tv/embedplayer/' + chname + '/1/555/435'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= abrir_url_tommy(embed,ref_data)
                link=abrir_url('http://www.zenex.tv:1935/loadbalancer')
                rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)[0]
                idnum=re.compile("'FlashVars'.+?id=(.+?)&s=.+?&").findall(html)[0]
                chnum=re.compile("'FlashVars'.+?id=.+?&s=(.+?)&").findall(html)[0]
                swf=re.compile('new SWFObject\("(.+?)"').findall(html)[0]
                streamurl='rtmp://' + rtmpendereco + '/zenex playPath=' + chnum + '?id=' + idnum + ' swfUrl=http://www.zenex.tv' + swf+ ' live=true conn=S:OK swfVfy=1 timeout=14 ccommand=goVideStambolSoseBardovci;TRUE;TRUE pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)


        elif re.search('src="http://www.dailymotion.com/embed',link) or re.search('"video_stream_mode":"',link):
            marcador="Catcher: dailymotion"; print marcador
            try:idvideo=re.compile('<iframe.+?src="http://www.dailymotion.com/embed(.+?)"').findall(link)[0]
            except:idvideo=re.compile('<meta name="twitter:player".+?/embed(.+?)"').findall(link)[0]
            sources=[]
            embedvideo='http://www.dailymotion.com/embed' + idvideo
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            html= abrir_url_tommy(embedvideo,ref_data)
            if re.search('stream_live_hls_url',html):
                streamurl=redirect(re.compile('"stream_live_hls_url":"(.+?)"').findall(html)[0].replace('\\',''))
            else:
                import urlresolver
                hosted_media = urlresolver.HostedMediaFile(url=embedvideo)
                sources.append(hosted_media)
                source = urlresolver.choose_source(sources)
                if source:
                    streamurl=source.resolve()
            comecarvideo(streamurl,nomecanal,True,zapping)


        else:
            marcador="Catcher: noserver" ; print marcador
            if activado==False:
                mensagemok('TV Portuguesa','Servidor não suportado')
                mensagemprogresso.close()
            else:
                try:debug.append(nomeserver + ' - ' + marcador)
                except: pass
    except Exception:
        if activado==False:
            mensagemprogresso.close()
            mensagemok('TV Portuguesa','Servidor não suportado.')
            (etype, value, traceback) = sys.exc_info()
            print etype
            print value
            print traceback
        else:
            try:debug.append(nomeserver + ' - ' + marcador)
            except: pass
        #buggalo.onExceptionRaised()


### PRAIAS ####

def praias():
    beachcams=[]
    try:
        temp=abrir_url(BeachcamURL + 'pt/livecams/')
        beachcams=re.compile('<a href="/pt/livecams/(.+?)">(.+?)</a>').findall(temp)    
    except: print "Nao foi possivel obter as BeachCams"
    try:
        temp=abrir_url(SurflineURL + '/surf-report/portugal_2946/map/')
        beachcams+=re.compile('\tbackground-image:url./surfdata/images/icon_hdcam_blue.gif.\n\t\t\t\t\n                ;background-repeat:no-repeat;background-position:bottom left"\n                href="(.+?)">(.+?)</a>').findall(temp)
    except: print "Nao foi possivel obter as Surfline"
    try:
        temp=re.compile('Report<b class="caret">(.+?)</li></ul></li>').findall(abrir_url(SurftotalURL))[0]
        beachcams+=re.compile('<a href="(.+?)" >(.+?)</a>').findall(temp)
    except: print "Nao foi possivel obter as Surftotal"
    beachcams.sort(key=lambda t: t[1])
    for end,nome in beachcams:
        nome=nome.replace('&#227;','ã').replace('&#231;','ç').replace('&#237;','í').replace('&#180;','á')
        if re.search('surf-report',end):
            end=SurflineURL + end
            nome= '[B]%s[/B] (Surfline)' % nome
        elif re.search('camaras-report',end):
            end=SurftotalURL + end
            nome= '[B]%s[/B] (Surftotal)' % nome
        else:
            end=BeachcamURL + 'pt/livecams/' + end
            nome= '[B]%s[/B] (Beachcam.pt)' % nome
        addDir(nome,end,27,tvporpath + art + 'versao-ver2.png',len(beachcams),'',False)
    
### PROGRAMACAO ####

def p_todos():
    if selfAddon.getSetting("prog-lista3") == "false": return ''
    else:
        try:
            dia=horaportuguesa(True)
            
            listacanais='RTP1,RTP2,SIC,TVI,SPTV1,SPTV2,SPTV3,SPTV4,SPTV5,SLB,SLB2,PORTO,CMTV,RTPIN,SICK,SICM,SICN,SICR,TVI24,TVIFIC,HOLLW,AXN,AXNBL,AXNWH,FOX,FOXCR,FLIFE,FOXM,SYFY,DISNY,PANDA,MOTOR,DISCV,ODISS,HIST,NGC,EURSP,FASH,VH1,MTV,ABOLA,RTPAC,RTPA,RTPM,RTPMD,BIGGS,ETVHD,DISNYJ,CHELS,CAÇAP,TOROTV,DISCT,GLOBO,TVREC,EURS2,SCP,TPA,EURN,ARTV,TRACE'
            url='http://services.sapo.pt/EPG/GetChannelListByDateInterval?channelSiglas='+listacanais+'&startDate=' + dia +':01&endDate='+ dia + ':02'
            link=clean(abrir_url(url,erro=False))
            
            listas=re.compile('<Sigla>(.+?)</Sigla>.+?<Title>(.+?)</Title>.+?<Description>(.+?)</Description>').findall(link)
            canais={}
            for nomecanal, nomeprog, descricao in listas:
                canais[nomecanal]={'nomeprog':'(' + nomeprog + ')','descprog':descricao}
            return canais
        except: pass

def p_umcanal(listas,desejado,desc):
    try: return listas[desejado][desc]
    except: return ''

def programacao_canal():
    titles=[]
    sigla=name.replace('[','-')
    sigla=re.compile('B](.+?)/B]').findall(sigla)[0]
    siglacanal=sigla.replace('SPORTTV 1-','SPTV1').replace('SPORTTV 2-','SPTV2').replace('SPORTTV 3-','SPTV3').replace('SPORTTV 4-','SPTV4').replace('SPORTTV 5-','SPTV5').replace('SPORTTV LIVE-','SPTVL').replace('Discovery Channel-','DISCV').replace('AXN Black-','AXNBL').replace('AXN White-','AXNWH').replace('FOX Crime-','FOXCR').replace('FOX Life-','FLIFE').replace('FOX Movies-','FOXM').replace('Eurosport-','EURSP').replace('Hollywood-','HOLLW').replace('Canal Panda-','PANDA').replace('Benfica TV 1-','SLB').replace('Benfica TV 2-','SLB2').replace('Porto Canal-','PORTO').replace('SIC K-','SICK').replace('SIC Mulher-','SICM').replace('SIC Noticias-','SICN').replace('SIC Radical-','SICR').replace('TVI24-','TVI24').replace('TVI Ficção-','TVIFIC').replace('Mais TVI-','SEM').replace('Syfy-','SYFY').replace('Odisseia-','ODISS').replace('História-','HIST').replace('National Geographic Channel-','NGC').replace('MTV-','MTV').replace('CM TV-','CMTV').replace('RTP Informação-','RTPIN').replace('Disney Channel-','DISNY').replace('Motors TV-','MOTOR').replace('ESPN America-','SEM').replace('Fashion TV-','FASH').replace('MOV-','SEM').replace('A Bola TV-','ABOLA').replace('Panda Biggs-','BIGGS').replace('RTP 1-','RTP1').replace('RTP 2-','RTP2').replace('RTP Açores-','RTPAC').replace('RTP Madeira-','RTPMD').replace('RTP Memória-','RTPM').replace('Disney Junior-','DISNYJ').replace('RTP Africa-','RTPA').replace('Económico TV-','ETVHD').replace('Chelsea TV-','CHELS').replace('TV Globo-','GLOBO').replace('TV Record-','TVREC').replace('Eurosport 2-','EURS2').replace('Discovery Turbo-','DISCT').replace('Toros TV-','TOROTV').replace('Caça e Pesca-','CAÇAP').replace('Sporting TV-','SCP').replace('TPA Internacional-','TPA')
    siglacanal=siglacanal.replace('-','')
    dia=horaportuguesa(True)
    diaseguinte=horaportuguesa('diaseguinte')
    url='http://services.sapo.pt/EPG/GetChannelListByDateIntervalJson?channelSiglas='+siglacanal+'&startDate=' + dia +':01&endDate='+ diaseguinte + ':02'
    ref=int(0)
    link=abrir_url(url)
    titles.append('No ar: %s\n\n[B][COLOR white]Programação:[/COLOR][/B]' % name)

    programas=re.compile('{"Actor":.+?"Description":"(.+?)".+?"StartTime":".+?-.+?-(.+?) (.+?):(.+?):.+?".+?"Title":"(.+?)"').findall(link)
    for descprog,dia, horas,minutos, nomeprog in programas:
        ref=ref+1
        if dia==datetime.datetime.now().strftime('%d'): dia='Hoje'
        else: dia='Amanhã'
        titles.append('\n[B][COLOR blue]%s %s:%s[/COLOR][/B] - [B][COLOR gold]%s[/COLOR][/B] - %s' % (dia,horas,minutos,nomeprog,descprog))
    programacao='\n'.join(titles)
    
    try:
        xbmc.executebuiltin("ActivateWindow(10147)")
        window = xbmcgui.Window(10147)
        xbmc.sleep(100)
        window.getControl(1).setLabel('TV Portuguesa')
        window.getControl(5).setText(programacao)
    except: pass

### RADIOS ####

def radios():
    addDir('[COLOR blue][B]Radios Locais[/B][/COLOR]','nada',20,tvporpath + art + 'radios-v1.png',1,'',True)
    addLink("",'','')
    link=clean(abrir_url(RadiosNacionaisURL))
    nacionais=re.compile('<div class="radiostation boxgrid">(.+?)</div>').findall(link)
    for radioindividual in nacionais:
        radiosnacionais=re.compile('<a href="http://www.radioonline.com.pt/#(.+?)".+?<img.+?src="(.+?)".+?alt="(.+?)"').findall(radioindividual)
        for idradio,imagemradio,nomeradio in radiosnacionais:
            nomeradio=nomeradio.replace('Radio ','')
            addDir(nomeradio,idradio,21,imagemradio,len(radiosnacionais),'',False)

def radioslocais():
    link=clean(abrir_url(RadiosURL))
    #addDir('Pesquisar (exclui nacionais)',RadiosURL + '?distrito=0&concelho=0&tipo=0&text=',16,'',1,'',True)
    distritos=re.compile('id="DirectorioPesquisa1_ddlDistritos">(.+?)</select>').findall(link)[0]
    distritos=distritos.replace('<option value="0"></option>','<option value="0">Todos as rádios locais</option>')
    lista=re.compile('<option value="(.+?)">(.+?)</option>').findall(distritos)
    for iddistrito,nomedistrito in lista:
        addDir(nomedistrito,RadiosURL + '?distrito=' + iddistrito + '&concelho=0&tipo=0',24,'',len(lista),'',True)
    xbmc.executebuiltin("Container.SetViewMode(501)")

def listar_radios(name,url):
    link=clean(abrir_url(url))
    radios=re.compile('<td><a href="/portalradio/conteudos/ficha/.+?radio_id=(.+?)">(.+?)</a></td><td>(.+?)</td>.+?<td align="center">').findall(link)
    for idradio,nomeradio,concelho in radios:
        addDir('[B]'+nomeradio+'[/B] ('+concelho+')',RadiosURL + 'Sintonizador/?radio_id=' + idradio + '&scope=0',21,'http://www.radio.com.pt/APR.ROLI.WEB/Images/Logos/'+ idradio +'.gif',len(radios),'',False)
    xbmc.executebuiltin("Container.SetViewMode(501)")
    paginasradios(url,link)

def paginasradios(url,link):
    try:
        pagina=re.compile('<div id="DirectorioPesquisa1_divPageSelector">.+?<b> (.+?)</b>  <a href=/portalradio/(.+?)>').findall(link)[0]
        nrpag=int(pagina[0])+1
        nrpag=str(nrpag)
        addDir('[COLOR blue]Próxima página (' + nrpag + ') >>>[/COLOR]',RadiosURL + pagina[1],24,'',1,'',True)
    except: pass

def radiosobterurlstream(name,url):
    GA("None","Radio - " + name)
    mensagemprogresso.create('TV Portuguesa','A carregar...')
    mensagemprogresso.update(0)
    if re.search('www.radios.pt',url):
        link=abrir_url(url)
        try:
            endereco=re.compile('<param name="url" value="(.+?)"').findall(link)[0]
        except:
            xbmc.executebuiltin("XBMC.Notification(Fightnight Music,Não é possível ouvir esta rádio.,'500000',)")
            return
        idradio=url.replace('http://www.radios.pt/portalradio/Sintonizador/?radio_id=','').replace('&scope=0','')
        thumbnail='http://www.radio.com.pt/APR.ROLI.WEB/Images/Logos/'+ idradio +'.gif'
    else:
        urlfinal='http://www.radioonline.com.pt/ajax/player.php?clear_s_name=' + url
        link=clean(abrir_url(urlfinal))
        try: player=re.compile('soundManager.createSound\({(.+?)autoLoad').findall(link)[0]
        except: player=False
        try:
            endereco=re.compile('url: "(.+?)"').findall(player)[0].replace(';','')
            if re.search('serverURL',player):
                rtmp=re.compile('serverURL: "(.+?)"').findall(player)[0]
                #rtmp=rtmp.replace('rtmp://195.23.102.206','rtmp://195.23.102.209') #tempfix
                rtmp=rtmp.replace(':1936','') #tempfix
                endereco=rtmp + ' playPath=' + endereco
                
        except:endereco=False
        if not endereco:
            try:endereco=re.compile('<param name="URL" value="(.+?)"').findall(link)[0]
            except:
                try: endereco=re.compile('<object data="(.+?)"').findall(link)[0]
                except: endereco=False

        if not endereco:
            xbmc.executebuiltin("XBMC.Notification(TV Portuguesa,Não é possível ouvir esta rádio.,'500000',)")
            mensagemprogresso.close()
            return
        
        try:thumbnail=re.compile('<img id="station-logo-player" src="(.+?)"').findall(link)[0]
        except: thumbnail=''
        if re.search('.asx',endereco):
            nomeasx='stream.asx'
            path = xbmc.translatePath(os.path.join(pastaperfil))
            lib=os.path.join(path, nomeasx)
            downloader(endereco,lib)
            texto=openfile(nomeasx)
            endereco = xbmc.PlayList(1)
            endereco.clear()
            streams=re.compile('<ref.+?"(.+?)"/>').findall(texto)
            for musica in streams:
                listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
                listitem.setInfo("music", {"Title":name})
                endereco.add(musica,listitem)
        else: pass
    mensagemprogresso.close()
    listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
    listitem.setInfo("music", {"Title":name})
    xbmc.Player().play(endereco,listitem)

### MENSAGENS ###

def mensagemaviso():
    try:
        xbmc.executebuiltin("ActivateWindow(10147)")
        window = xbmcgui.Window(10147)
        xbmc.sleep(100)
        window.getControl(1).setLabel( "%s - %s" % ('AVISO','TV Portuguesa',))
        window.getControl(5).setText("[COLOR red][B]Termos:[/B][/COLOR]\nEste addon não aloja quaisquer conteúdos. O conteúdo apresentado é da responsabilidade dos servidores e em nada está relacionado com este addon.\n\nEste plugin não pretende substituir o acesso aos serviços de televisão pagos. Apenas funciona como extra a esses serviços.\n\nEste plugin apenas indexa links de outros sites, não alojando quaisquer conteúdos.\n\nEste plugin não pretende substituir o acesso aos sites de streaming, mas sim facilitar o acesso a estes via plataformas móveis (RPi, android, etc.)\n\nVisitem os sites oficiais e suportem os sites clicando na publicidade.\n\nUm obrigado a todos eles. (www.desportogratis.com, www.rtp.pt, www.tugastream.com, www.tvfree.me, www.tvgente.eu, www.tvdez.com).\n\nReplay TV (techdealer), Eventos (Cesarix/Rominhos), Listas (Cesarix, Mafarricos, Benfiquista), Grafismo (Rukanito), Radios (www.radios.pt e www.radioonline.com.pt), Streams f4m (shani_08), Veetle (TvM) \n\n[COLOR red][B]É necessário actualizar o libRTMP do XBMC para alguns streams funcionarem a 100%.\nMais informações em: [/B][/COLOR] http://bit.ly/fightnightaddons\n\n[B]Data de actualização do aviso: [/B] 22 de Maio de 2014")
    except: pass

def sintomecomsorte():
    if selfAddon.getSetting("mensagemgratis3") == "true":
        d = lolbaza("lolbaza.xml" , tvporpath, "Default")
        d.doModal()
        del d
        selfAddon.setSetting('mensagemgratis3',value='false')

def librtmpwindow():
    if selfAddon.getSetting("rtmp-lib0001") == "false":
        d = lolbaza("librtmp.xml" , tvporpath, "Default")
        d.doModal()
        del d

class lolbaza(xbmcgui.WindowXMLDialog):

    def __init__( self, *args, **kwargs ):
          xbmcgui.WindowXML.__init__(self)

    def onInit(self):
        pass
          
    def onClick(self,controlId):
        if controlId == 2001: self.close()

def testejanela():
    d = menulateral("menulateral.xml" , tvporpath, "Default")
    d.doModal()
    del d

class menulateral(xbmcgui.WindowXMLDialog):

    def __init__( self, *args, **kwargs ):
            xbmcgui.WindowXML.__init__(self)
            self.finalurl = kwargs[ "finalurl" ]
            self.siglacanal = kwargs[ "siglacanal" ]
            self.name = kwargs[ "name" ]
            self.directo = kwargs[ "directo" ]

    def onInit(self):
        self.updateChannelList()

    def onAction(self, action):
        if action.getId() in [9, 10, 92, 117]:
            self.close()
            return

    def onClick(self, controlId):
        if controlId == 4001:
            self.close()
            request_servidores('','[B]%s[/B]' %(self.name))

        elif controlId == 40010:
            self.close()
            iniciagravador(self.finalurl,self.siglacanal,self.name,self.directo)

        elif controlId == 203:
            #xbmc.executebuiltin("XBMC.PlayerControl(stop)")
            self.close()

        elif controlId == 6000:
            listControl = self.getControl(6000)
            item = listControl.getSelectedItem()
            nomecanal=item.getProperty('chname')
            self.close()
            request_servidores('',nomecanal)

        
        #else:
        #    self.buttonClicked = controlId
        #    self.close()

    def onFocus(self, controlId):
        pass

    def updateChannelList(self):
        idx=-1
        listControl = self.getControl(6000)
        listControl.reset()
        canaison=openfile('canaison')
        canaison=canaison.replace('[','')
        lista=re.compile('B](.+?)/B]').findall(canaison)
        for nomecanal in lista:
            idx=int(idx+1)
            if idx==0: idxaux=' '
            else:
                idxaux='%4s.' % (idx)
                item = xbmcgui.ListItem(idxaux + ' %s' % (nomecanal), iconImage = '')
                item.setProperty('idx', str(idx))
                item.setProperty('chname', '[B]' + nomecanal + '[/B]')
                listControl.addItem(item)
        
    def updateListItem(self, idx, item):
        channel = self.channelList[idx]
        item.setLabel('%3d. %s' % (idx+1, channel.title))
        item.setProperty('idx', str(idx))

    def swapChannels(self, fromIdx, toIdx):
        if self.swapInProgress: return
        self.swapInProgress = True

        c = self.channelList[fromIdx]
        self.channelList[fromIdx] = self.channelList[toIdx]
        self.channelList[toIdx] = c

        # recalculate weight
        for idx, channel in enumerate(self.channelList):
            channel.weight = idx

        listControl = self.getControl(6000)
        self.updateListItem(fromIdx, listControl.getListItem(fromIdx))
        self.updateListItem(toIdx, listControl.getListItem(toIdx))

        listControl.selectItem(toIdx)
        xbmc.sleep(50)
        self.swapInProgress = False


### LISTAS ###

def listascanais():
    addDir("[B]Desporto[/B] (cesarix)",'http://dl.dropboxusercontent.com/u/266138381/Desporto.xml',5,tvporpath + art + 'ces-desp-ver1.png',1,'',True)
    addDir("[B]Desporto/Global[/B] (vdubt25)",'http://bit.ly/vdubt25',5,tvporpath + art + 'listas-ver2.png',1,'',True)
    addDir("[B]Global[/B] (magellan)",'http://goo.gl/aOLLyX',5,tvporpath + art + 'listas-ver2.png',1,'',True)
    addDir("[B]Global[/B] (boxcenter)",'http://boxcenter.altervista.org/oficial.m3u',5,tvporpath + art + 'listas-ver2.png',1,'',True)
    addDir("[B]Música[/B] (cesarix)",'http://dl.dropboxusercontent.com/u/266138381/Musica.xml',5,tvporpath + art + 'ces-mus-ver1.png',1,'',True)
    addDir("[B]Ciências[/B] (cesarix)",'http://dl.dropboxusercontent.com/u/266138381/Tv%20Ciencia.xml',5,tvporpath + art + 'ces-ciencia-ver1.png',1,'',True)
    addDir("[B]Alemanha[/B] (cesarix)",'http://dl.dropboxusercontent.com/u/266138381/Tv%20Alema.xml',5,tvporpath + art + 'ces-alem-ver1.png',1,'',True)
    addDir("[B]Espanha[/B]",'http://dl.dropboxusercontent.com/u/266138381/Tv%20Espanhola.xml',5,tvporpath + art + 'ces-espa-ver1.png',1,'',True)
    addDir("[B]UK[/B] (cesarix)",'http://dl.dropboxusercontent.com/u/266138381/Tv%20UK.xml',5,tvporpath + art + 'ces-uk-ver1.png',1,'',True)
    addDir("[B]USA[/B] (cesarix)",'http://dl.dropboxusercontent.com/u/266138381/Tv%20USA.xml',5,tvporpath + art + 'ces-usa-ver1.png',1,'',True)
    addDir("[B]Global[/B] (mafarricos)",'http://dl.dropbox.com/u/88295111/pissos13.xml',5,tvporpath + art + 'pissos-ver1.png',1,'',True)
    addDir("[B]Portugal[/B]",'http://dl.dropboxusercontent.com/s/h9s0oiop70tjwe8/TV%20PORTUGUESA.txt',5,tvporpath + art + 'vercanais-ver2.png',1,'',True)
    addDir("[B]Filmes[/B]",'http://dl.dropboxusercontent.com/s/kk79s083x208zug/xml%20pt%20tv%20-%20nova.txt',5,tvporpath + art + 'vercanais-ver2.png',1,'',True)
    addDir("[B]Infantil[/B]",'http://dl.dropboxusercontent.com/s/kbly079op7kwaz2/INFANTIL%20TV%20POR.txt',5,tvporpath + art + 'vercanais-ver2.png',1,'',True)
    addDir("[B]Brasil[/B]",'http://dl.dropboxusercontent.com/s/9ilbiv4d83dlcrr/TV%20BRASILEIRA%20POR.txt',5,tvporpath + art + 'vercanais-ver2.png',1,'',True)
    #addLink("",'',tvporpath + art + 'listas-ver2.png')
    if selfAddon.getSetting("listasextra") == "true":
        try:listasextras()
        except:pass
    
    addDir("[B][COLOR white]A tua lista aqui?[/COLOR][/B]",'nada',14,tvporpath + art + 'versao-ver2.png',1,'',False)
    #xbmc.executebuiltin("Container.SetViewMode(500)")

def listasextras():
    iptvurl='http://01.gen.tr/HasBahCa_IPTV/'
    link=clean(abrir_url(iptvurl))
    streams=re.compile('<a class="autoindex_a" href="./(.+?)">.+?<td class="autoindex_td_right">.+?</td.+?td class="autoindex_td_right">(.+?)</td>').findall(link)
    for nomepasta,act in streams:
        if re.search('.m3u',nomepasta):
            titulo=nomepasta.replace('.m3u','').replace('_',' ').title()
            addDir("[B]%s[/B] (act.%s)" % (titulo,act[2:-2]),iptvurl + nomepasta,5,tvporpath + art + 'listas-ver2.png',1,'',True)

def parseM3U(infile,link=False):
    if link==False: inf=abrir_url(infile).splitlines( )
    else: inf=link.splitlines( )
    
    playlist=[]
    musica=[]
    titulo=''
    urlstream=''
    for line in inf:
        line=line.strip()
        if line.startswith('#EXTINF:'):
            #stupid guys with spaces and common errors
            try:titulo=line.split('#EXTINF:')[1].split(',  ',1)[1]
            except:                
                try:titulo=line.split('#EXTINF:')[1].split(', ',1)[1]
                except:
                    try:titulo=line.split('#EXTINF:')[1].split(',',1)[1]
                    except:titulo=line.split('#EXTINF:')[1].split('" ',1)[1]
        elif re.search('#EXTM3U',line):
            pass
        elif (len(line) != 0):
            line=line.replace('rtmp://$OPT:rtmp-raw=','')
            urlstream=line
            musica.append(titulo)
            musica.append(urlstream)
            musica.append(tvporpath + art + 'vercanais-ver2.png')#fakethumb
            playlist.append(musica)
            musica=[]
            titulo=''
            urlstream=''
            

    return playlist
    
def obter_lista(name,url):
    GA("None",name)
    titles = []; ligacao = []; thumb=[]
    link=abrir_url(url)
    if re.search('.m3u',url) or re.search('#EXTM3U',link):
        listas=parseM3U(url,link)
    else:
        link2=clean(link)
        listas=re.compile('<title>(.+?)</title>(.+?)<thumbnail>(.+?)</thumbnail>').findall(link2)

    for nomecanal,streams,thumbcanal in listas:
        if re.search('<link>',streams):
            streams2=re.compile('<link>(.+?)</link>').findall(streams)
        else:
            streams2=[]
            streams2.append(streams)#ugly
            
        for rtmp in streams2:
#            if re.search('$doregex',rtmp):
#                #parametros=re.compile('<regex></regex>').findall(rtmp)
#                doRegexs = re.compile('\$doregex\[([^\]]*)\]').findall(rtmp)
#                    for k in doRegexs:
#                    
#                        if k in regexs:
#                            m = regexs[k]
#                            #if m['page'] in cachedPages:
#                            #    link = cachedPages[m['page']]
#                            #else:
#                            page=re.compile('<page>(.+?)</page>').findall(streams2)[0]
#                            req = urllib2.Request(page)
#                            req.add_header('User-Agent', user_agent)
#                            if re.search('<referer>',streams2):
#                                referer=re.compile('<referer>(.+?)</referer>').findall(streams2)[0]
#                                req.add_header('Referer', referer)
#                            response = urllib2.urlopen(req)
#                            link = response.read()
#                            response.close()
#                            expres=re.compile("""<expres>'file':'([^']*)<expres>""").findall(streams2)[0]
#                            reg = re.compile(expres).search(link)
#                            rtmp = url.replace("$doregex[" + k + "]", reg.group(1).strip())
                        

            if name=='[B][COLOR white]Eventos[/COLOR][/B] (Cesarix/Rominhos)':
                titles.append(nomecanal)
                ligacao.append(rtmp)
                thumb.append(thumbcanal)
            else:
                addCanal(nomecanal,rtmp,17,thumbcanal,len(listas),'')
                xbmcplugin.setContent(int(sys.argv[1]), 'Movies')

                    
    if name=='[B][COLOR white]Eventos[/COLOR][/B] (Cesarix/Rominhos)':
        if len(ligacao)==0: ok=mensagemok('TV Portuguesa', 'Sem eventos disponiveis.'); return
        else:
            if len(ligacao)==1: index=0
            else:index = xbmcgui.Dialog().select('Escolha o servidor', titles)
            if index > -1:
                urlescolha=ligacao[index]
                nomecanal=titles[index]
                #thumb123=thumbcanal[index]
                #print thumb123
                comecarvideo(urlescolha,nomecanal,'listas',False,thumb=tvporpath + art + 'vercanais-ver2.png')

### PLAYER ####

def comecarvideo(finalurl,name,directo,zapping,thumb=''):
    if activado==True: activadoextra.append(finalurl)
    else: comecarvideo2(finalurl,name,directo,zapping,thumb='')

def comecarvideo2(finalurl,name,directo,zapping,thumb=''):
    if thumb=='':thumb=tvporpath + art + 'vercanais-ver2.png'
    listacanaison=selfAddon.getSetting("listacanais2")
    siglacanal=''
    namega=name.replace('-','')
    GA("player",namega)
    if directo==True:
        thumb=name.replace('Mais TVI-','maistvi-ver2.png').replace('AXN-','axn-ver2.png').replace('FOX-','fox-ver2.png').replace('RTP 1-','rtp1-ver2.png').replace('RTP 2-','rtp2-ver2.png').replace('SIC-','sic-ver3.png').replace('SPORTTV 1-','sptv1-ver2.png').replace('SPORTTV 1 HD-','sptvhd-ver2.png').replace('SPORTTV 2-','sptv2-ver2.png').replace('SPORTTV 3-','sptv3-ver2.png').replace('SPORTTV 4-','sptv4-ver2.png').replace('SPORTTV 5-','sptv5-ver2.png').replace('SPORTTV LIVE-','sptvlive-ver1.png').replace('TVI-','tvi-ver2.png').replace('Discovery Channel-','disc-ver2.png').replace('AXN Black-','axnb-ver2.png').replace('AXN White-','axnw-ver2.png').replace('FOX Crime-','foxc-ver2.png').replace('FOX Life-','foxl-ver3.png').replace('FOX Movies-','foxm-ver2.png').replace('Eurosport-','eusp-ver2.png').replace('Hollywood-','hwd-ver2.png').replace('MOV-','mov-ver2.png').replace('Canal Panda-','panda-ver2.png').replace('VH1-','vh1-ver2.png').replace('Benfica TV 1-','btv1-ver1.png').replace('Benfica TV 2-','btv2-ver1.png').replace('Porto Canal-','pcanal-ver2.png').replace('Big Brother VIP-','bbvip-ver2.png').replace('SIC K-','sick-ver2.png').replace('SIC Mulher-','sicm-ver3.png').replace('SIC Noticias-','sicn-ver2.png').replace('SIC Radical-','sicrad-ver2.png').replace('TVI24-','tvi24-ver2.png').replace('TVI Ficção-','tvif-ver2.png').replace('Syfy-','syfy-ver1.png').replace('Odisseia-','odisseia-ver1.png').replace('História-','historia-ver1.png').replace('National Geographic Channel-','natgeo-ver1.png').replace('MTV-','mtv-ver1.png').replace('CM TV-','cmtv-ver1.png').replace('RTP Informação-','rtpi-ver1.png').replace('Disney Channel-','disney-ver1.png').replace('Motors TV-','motors-ver1.png').replace('ESPN-','espn-ver1.png').replace('Fashion TV-','fash-ver1.png').replace('A Bola TV-','abola-ver1.png').replace('Casa dos Segredos 5-','casadseg-ver1.png').replace('RTP Açores-','rtpac-ver1.png').replace('RTP Internacional-','rtpint-ver1.png').replace('RTP Madeira-','rtpmad-ver1.png').replace('RTP Memória-','rtpmem-ver1.png').replace('RTP Africa-','rtpaf-ver1.png').replace('Panda Biggs-','pbiggs-ver1.png').replace('TV Record-','record-v1.png').replace('TV Globo-','globo-v1.png').replace('Eurosport 2-','eusp2-ver1.png').replace('Discovery Turbo-','discturbo-v1.png').replace('Toros TV-','toros-v1.png').replace('Chelsea TV-','chel-v1.png').replace('Disney Junior-','djun-ver1.png').replace('Económico TV-','econ-v1.png').replace('Caça e Pesca-','cacapesca-v1.png').replace('Sporting TV-','scptv-ver1.png').replace('Euronews-','euronews-ver1.png').replace('TPA Internacional-','tpa-ver1.png').replace('ARTV-','artv-ver1.png').replace('TRACE Urban-','traceu.png').replace('Virgin Radio TV-','virginr.png').replace('DJing TV-','djingtv.png')
        name=name.replace('-','')
        progname=name

        siglacanal=name.replace('SPORTTV 1','SPTV1').replace('SPORTTV 2','SPTV2').replace('SPORTTV 3','SPTV3').replace('SPORTTV 4','SPTV4').replace('SPORTTV 5','SPTV5').replace('SPORTTV LIVE','SPTVL').replace('Discovery Channel','DISCV').replace('AXN Black','AXNBL').replace('AXN White','AXNWH').replace('FOX Crime','FOXCR').replace('FOX Life','FLIFE').replace('FOX Movies','FOXM').replace('Eurosport','EURSP').replace('Hollywood','HOLLW').replace('Canal Panda','PANDA').replace('Benfica TV 1','SLB').replace('Benfica TV 2','SLB2').replace('Porto Canal','PORTO').replace('SIC K','SICK').replace('SIC Mulher','SICM').replace('SIC Noticias','SICN').replace('SIC Radical','SICR').replace('TVI24','TVI24').replace('TVI Ficção','TVIFIC').replace('Mais TVI','SEM').replace('Syfy','SYFY').replace('Odisseia','ODISS').replace('História','HIST').replace('National Geographic Channel','NGC').replace('MTV','MTV').replace('CM TV','CMTV').replace('RTP Informação','RTPIN').replace('Disney Channel','DISNY').replace('Motors TV','MOTOR').replace('ESPN America','SEM').replace('Fashion TV','FASH').replace('MOV','SEM').replace('A Bola TV','ABOLA').replace('Panda Biggs','BIGGS').replace('RTP 1','RTP1').replace('RTP 2','RTP2').replace('RTP Açores','RTPAC').replace('RTP Madeira','RTPMD').replace('RTP Memória','RTPM').replace('Disney Junior','DISNYJ').replace('RTP Africa','RTPA').replace('Económico TV','ETVHD').replace('Chelsea TV','CHELS').replace('TV Globo','GLOBO').replace('TV Record','TVREC').replace('Eurosport 2','EURS2').replace('Discovery Turbo','DISCT').replace('Toros TV','TOROTV').replace('Caça e Pesca','CAÇAP').replace('Sporting TV','SCP').replace('TPA Internacional','TPA')
        listitem = xbmcgui.ListItem(progname, iconImage="DefaultVideo.png", thumbnailImage=tvporpath + art + thumb)
    else: listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumb)
    if zapping==True and not re.search('.f4m',finalurl):
        #conteudoficheiro=openfile(('zapping'))
        #savefile(('zapping', conteudoficheiro + '_comeca_' + name + '_nomecanal_' + finalurl + '_thumb_' + thumb + '_acaba_'))
        iniciagravador(finalurl,siglacanal,name,directo)
    else:

        if re.search('.f4m',finalurl):
            from resources.lib.proxyf4m import f4mProxyHelper
            helper=f4mProxyHelper()
            finalurl,spscpid = helper.start_proxy(finalurl, name)
        else:
            #finalurl,spscpid=libalternativo(finalurl)
            spscpid='nada'
        
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('IsPlayable', 'true')
        if finalurl=='http://live.2caster.com:1935/live/sica/playplist.m3u8':finalurl=''
        playlist.add(finalurl, listitem)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,listitem)
        mensagemprogresso.close()
        dialogWait = xbmcgui.DialogProgress()
        dialogWait.create('TV Portuguesa', 'A carregar...')
        dialogWait.close()
        del dialogWait
        
        player = Player(finalurl=finalurl,name=name,siglacanal=siglacanal,directo=directo,spscpid=spscpid)
        if "RunPlugin" in finalurl:
            xbmc.executebuiltin(finalurl)
        else:

            player.play(playlist)
            lat123 = menulateral("menulateral.xml" , tvporpath, "Default",finalurl=finalurl,name=name,siglacanal=siglacanal,directo=directo)
        
            while player.is_active:
                if listacanaison == "true":
                    if xbmc.getCondVisibility('Window.IsActive(videoosd)') and directo==True:
                        xbmc.executebuiltin('XBMC.Control.Move(videoosd,9999)')
                        lat123.doModal()
                        while xbmc.getCondVisibility('Window.IsActive(videoosd)'): pass
                player.sleep(1000)
            
            #if not player.is_active:
            #    print "Parou. Saiu do ciclo."
            #    sys.exit(0)
                
                #player.sleep(10000)
            #print "ERRO"

class Player(xbmc.Player):
      def __init__(self,finalurl,name,siglacanal,directo,spscpid):
            if selfAddon.getSetting("playertype") == "0": player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
            elif selfAddon.getSetting("playertype") == "1": player = xbmc.Player(xbmc.PLAYER_CORE_MPLAYER)
            elif selfAddon.getSetting("playertype") == "2": player = xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER)
            elif selfAddon.getSetting("playertype") == "3": player = xbmc.Player(xbmc.PLAYER_CORE_PAPLAYER)
            else: player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
            self.is_active = True
            self._refInfo = True
            self._totalTime = 999999
            self._finalurl=finalurl
            self._name=name
            self._siglacanal=siglacanal
            self._directo=directo
            self._spscpid=spscpid
            print "Criou o player"
            #player.stop()

      def onPlayBackStarted(self):
            print "Comecou o player"
                              
      def onPlayBackStopped(self):
            print "Parou o player"
            self.is_active = False
            if re.search('.f4m',self._finalurl): self._spscpid.set()
            #import newrtmp
            #newrtmp.stop_stream(self._spscpid)
            #opcao= xbmcgui.Dialog().yesno("TV Portuguesa", "Este stream funciona? ", "(exemplificação / ainda não funciona)", "",'Sim', 'Não')
            ###### PERGUNTAR SE O STREAM E BOM #####            

      def onPlayBackEnded(self):              
            self.onPlayBackStopped()
            print 'Chegou ao fim. Playback terminou.'


      def sleep(self, s): xbmc.sleep(s) 

class PlaybackFailed(Exception):
      '''XBMC falhou a carregar o stream'''

### GRAVADOR ###

def iniciagravador(finalurl,siglacanal,name,directo):
    print "A iniciar gravador 1/2"
    if downloadPath=='':
        xbmcgui.Dialog().ok('TV Portuguesa','Necessitas de introduzir a pasta onde vão ficar','as gravações. Escolhe uma pasta com algum espaço','livre disponível.')
        dialog = xbmcgui.Dialog()
        pastafinal = dialog.browse(int(3), "Escolha pasta para as gravações", 'files')
        selfAddon.setSetting('pastagravador',value=pastafinal)
        return
    if directo==True:
        if re.search('rtmp://',finalurl) or re.search('rtmpe://',finalurl):
        #if re.search('rtmp://',finalurl):
            finalurl=finalurl.replace('playPath=','-y ').replace('swfVfy=1','').replace('conn=','-C ').replace('live=true','-v').replace('swfUrl=','-W ').replace('pageUrl=','-p ').replace(' token=','-T ').replace('app=','-a ').replace('  ',' ').replace('timeout=','-m ')
            verifica_so('-r ' + finalurl,name,siglacanal,directo)
        else: xbmc.executebuiltin("XBMC.Notification(TV Portuguesa, Stream não gravável. Escolha outro.,'100000'," + tvporpath + art + "icon32-ver1.png)")

def verifica_so(args,nomecanal,siglacanal,directo):
    print "A iniciar gravador 2/2"
    mensagemprogresso.create('TV Portuguesa','A carregar gravador...')
    #correrdump(args,nomecanal,'windows',siglacanal,directo)
    if selfAddon.getSetting('rtmpdumpalternativo')=='':
        if xbmc.getCondVisibility('system.platform.windows'): correrdump(args,nomecanal,'gravador-windows',siglacanal,directo)
        elif xbmc.getCondVisibility('system.platform.osx'): correrdump(args,nomecanal,'gravador-mac86atv1',siglacanal,directo)
        elif xbmc.getCondVisibility('system.platform.linux'):
            if os.uname()[4] == "armv6l":
                pasta=os.path.join(gravadorpath,'rpi')
                basescript='#!/bin/sh\nexport LD_LIBRARY_PATH="%s"\n' % (pasta)
                correrdump(args,nomecanal,'gravador-rpi',siglacanal,directo,script=basescript)
            elif os.uname()[4] == "x86_64":
                pasta=os.path.join(gravadorpath,'linux64')
                basescript='#!/bin/sh\nexport LD_LIBRARY_PATH="%s"\n' % (pasta)
                correrdump(args,nomecanal,'gravador-linux64',siglacanal,directo,script=basescript)
            else:
                pasta=os.path.join(gravadorpath,'linux86')
                basescript='#!/bin/sh\nexport LD_LIBRARY_PATH="%s"\n' % (pasta)
                correrdump(args,nomecanal,'gravador-linux86',siglacanal,directo,script=basescript)
    else: correrdump(args,nomecanal,'alternativo',siglacanal,directo)
        
def correrdump(args,nomecanal,pathso,siglacanal,directo,script=False):
    import subprocess
    from datetime import timedelta
    info=infocanal(siglacanal)
    escolha=0 #### inicializador
    mensagemprogresso.close()
    if info!=False and directo!='listas': escolha=listadeprogramas(info) #### se ha programacao, mostra lista
    if escolha==0:
        if info!=False and directo!='listas': #### ha programacao
            fimprograma=calculafinalprograma(info)
            tituloprograma=' - '+ re.compile('<Title>(.+?)</Title>').findall(info)[0]
            #nomecanal = nomecanal + tituloprograma
            minutosrestantes=fimprograma / 60
            opcao= xbmcgui.Dialog().yesno("TV Portuguesa", 'Faltam ' + str(minutosrestantes) + ' minutos para o fim do programa', "Deseja gravar o resto do programa ou", "definir um tempo de gravação?",'Definir tempo', 'Gravar restante')
            if opcao==1:
                if selfAddon.getSetting("acrescentogravacao") == "0": segundos=fimprograma
                elif selfAddon.getSetting("acrescentogravacao") == "1": segundos=fimprograma+120
                elif selfAddon.getSetting("acrescentogravacao") == "2": segundos=fimprograma+300
                elif selfAddon.getSetting("acrescentogravacao") == "3": segundos=fimprograma+600
                else: segundos=fimprograma + 120
                minutos=segundos/60
            else:
                minutos = -1
                while minutos < 1: minutos = int(xbmcgui.Dialog().numeric(0,"Num de minutos de gravacao"))
                segundos=minutos*60
        else:
            minutos = -1
            while minutos < 1: minutos = int(xbmcgui.Dialog().numeric(0,"Num de minutos de gravacao"))
            segundos=minutos*60
        nomecanal = limpar(re.sub('[^-a-zA-Z0-9_.()\\\/ ]+', '',  nomecanal))
        horaactual=horaportuguesa(False)

        if pathso=='alternativo': caminhodump=selfAddon.getSetting("rtmpdumpalternativo")
        else: caminhodump=os.path.join(gravadorpath,pathso)
        
        if xbmc.getCondVisibility('system.platform.linux'):
            st = os.stat(caminhodump)
            os.chmod(caminhodump, st.st_mode | stat.S_IEXEC)

        args=args.split(' ')
        typeargs=[]
        for types in args:
            if len(types) != 2: typeargs.append('"' + types + '"')
            else: typeargs.append(types)
        args=' '.join(typeargs)

        argumentos=args + ' -o "' + downloadPath + horaactual + ' - ' + nomecanal + '.flv" -B ' + str(segundos)
        #argumentos=args + ' -o "' + downloadPath + horaactual + '.flv" -B ' + str(segundos)

        if script:
            conteudoscript=script + xbmc.translatePath(os.path.join(gravadorpath,pathso))+ ' $1 ' + argumentos
            savefile('script.sh', conteudoscript ,pastafinal=gravadorpath)
            caminhodump=xbmc.translatePath(os.path.join(gravadorpath,'script.sh'))
            st = os.stat(caminhodump)
            os.chmod(caminhodump, st.st_mode | stat.S_IEXEC)
        try:
            #proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if script:
                proc = subprocess.Popen(caminhodump, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                #proc = subprocess.Popen(argumentos, executable=caminhodump + '.exe', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                cmd = '"%s" %s' % (caminhodump, argumentos)
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print "RTMPDump comecou a funcionar"
            xbmc.executebuiltin("XBMC.Notification(TV Portuguesa, Gravação de "+str(minutos)+" minutos iniciou,'10000'," + tvporpath + "/resources/art/icon32-ver1.png)")
            (stdout, stderr) = proc.communicate()
            print "RTMPDump parou de funcionar"
            stderr = normalize(stderr)
            if u'Download complete' in stderr:
                print 'stdout: ' + str(stdout)
                print 'stderr: ' + str(stderr)
                print "Download Completo!"
                xbmc.executebuiltin("XBMC.Notification(TV Portuguesa, Gravação efectuada com sucesso,'10000'," + tvporpath + "/resources/art/icon32-ver1.png)")
            else:
                print 'stdout: ' + str(stdout)
                print 'stderr: ' + str(stderr)
                print "Download Falhou!"
                xbmc.executebuiltin("XBMC.Notification(TV Portuguesa, Gravação falhou,'10000'," + tvporpath + "/resources/art/icon32-ver1.png)")
        except Exception:
            print ("Nao conseguiu abrir o programa")
            xbmc.executebuiltin("XBMC.Notification(TV Portuguesa, Erro ao abrir programa de gravação,'10000'," + tvporpath + "/resources/art/icon32-ver1.png)")
            (etype, value, traceback) = sys.exc_info()
            print "Erro etype: " + str(etype)
            print "Erro valor: " + str(value)
            print "Erro traceback: " + str(traceback)

def infocanal(siglacanal):
    if siglacanal=='SEM':
        print "Canal sem programacao."
        return False
    try:
        dia=horaportuguesa(True)
        diaseguinte=horaportuguesa('diaseguinte')
        url='http://services.sapo.pt/EPG/GetChannelListByDateInterval?channelSiglas='+siglacanal+'&startDate=' + dia +':01&endDate='+ diaseguinte + ':02'
        link=clean(abrir_url(url))
        return link
    except:
        print "Nao conseguiu capturar programacao."
        return False

def listadeprogramas(link):
    titles=[]
    ligacao=[]
    ref=int(0)
    programas=re.compile('<Title>(.+?)</Title>.+?<StartTime>.+?-.+?-(.+?) (.+?):(.+?):.+?</StartTime>').findall(link)
    for nomeprog,dia, horas,minutos in programas:
        ref=ref+1
        if dia==datetime.datetime.now().strftime('%d'): dia='Hoje'
        else: dia='Amanhã'
        if ref==2:
            titles.append('')
            titles.append('[COLOR red]A seguir: (não dá para gravar)[/COLOR]')
        if ref!=1:  titles.append(dia + ' ' + horas + ':' + minutos + ' - ' +nomeprog)
        else: titles.append(dia + ' ' + horas + ':' + minutos + ' - ' +nomeprog)
        ligacao.append('')
    index = xbmcgui.Dialog().select('Escolha o programa a gravar', titles)
    return index

def calculafinalprograma(link):
    fim=re.compile('<EndTime>(.+?)-(.+?)-(.+?) (.+?):(.+?):.+?</EndTime>').findall(link)[0]
    agora=horaportuguesa(False)
    inicio=re.compile('(.+?)-(.+?)-(.+?) (.+?)-(.+?)-').findall(agora)[0]
    start = datetime.datetime(year=int(inicio[0]), month=int(inicio[1]), day=int(inicio[2]), hour=int(inicio[3]), minute=int(inicio[4]))
    end = datetime.datetime(year=int(fim[0]), month=int(fim[1]), day=int(fim[2]), hour=int(fim[3]), minute=int(fim[4]))
    diff = end - start
    segundos= (diff.microseconds + (diff.seconds + diff.days * 24 * 3600) * 10**6) / 10**6
    return segundos

### TESTES ###
    
def libalternativo(finalurl):
    if xbmc.getCondVisibility('system.platform.windows'):
        import newrtmp
        finalurl,spsc=newrtmp.start_stream(rtmp=finalurl)
    else: spsc=''
    return finalurl,spsc

### REQUESTS ###

def abrir_url(url,erro=True):
    print "A fazer request normal de: " + url
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', user_agent)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link
    except urllib2.HTTPError, e:
        if erro==True and activado==False:
            host='http://' + url.split('/')[2]
            mensagemok('TV Portuguesa',str(urllib2.HTTPError(e.url, e.code, "Erro na página.", e.hdrs, e.fp)),'Verifique manualmente se a página está operacional.',host)
            sys.exit(0)
    except urllib2.URLError, e:
        if erro==True and activado==False:
            mensagemok('TV Portuguesa',"Erro na página. Verifique manualmente",'se a página está operacional. ' + url)
            sys.exit(0)

def abrir_url_cookie(url,erro=True,forcedns=False):
    print "A fazer request com cookie de: " + url
    try:
        if forcedns==False:
            hdr = {'User-Agent': user_agent, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
            req = urllib2.Request(url, headers=hdr)
            page = urllib2.urlopen(req)
            content = page.read()
            return content
        else:
            from resources.lib import dnsrequest
            content=dnsrequest.request(url)
            return content            
    except urllib2.HTTPError, e:
        if erro==True and activado==False:
            host='http://' + url.split('/')[2]
            mensagemok('TV Portuguesa',str(urllib2.HTTPError(e.url, e.code, "Erro na página.", e.hdrs, e.fp)),'Verifique manualmente se a página está operacional.',host)
            sys.exit(0)
    except urllib2.URLError, e:
        if erro==True and activado==False:
            host='http://' + url.split('/')[2]
            mensagemok('TV Portuguesa',"Erro na página. Verifique manualmente",'se a página está operacional.',host)
            sys.exit(0)

def abrir_url_tommy(url,referencia,form_data=None,erro=True,forcedns=False):
    print "A fazer request tommy de: " + url
    #method 1
    try:
        if form_data==None:
            if forcedns==False:
                link = net.http_GET(url,referencia).content
            else:
                from resources.lib import dnsrequest
                link=dnsrequest.request(url)
        else:link= net.http_POST(url,form_data=form_data,headers=referencia).content.encode('latin-1','ignore')
        return link
    #method 2
    #try:
    #    if form_data==None:link = requests.get(url,headers=referencia).text
    #    else:link= requests.post(url,params=form_data,headers=referencia).text
    #    return link

    except urllib2.HTTPError, e:
        if erro==True and activado==False:
            host='http://' + url.split('/')[2]
            mensagemok('TV Portuguesa',str(urllib2.HTTPError(e.url, e.code, "Erro na página.", e.hdrs, e.fp)),'Verifique manualmente se a página está operacional.',host)
            sys.exit(0)
    except urllib2.URLError, e:
        if erro==True and activado==False:
            host='http://' + url.split('/')[2]
            mensagemok('TV Portuguesa',"Erro na página. Verifique manualmente",'se a página está operacional. ' + host)
            sys.exit(0)


### OTHERS ###

class JsUnpacker:

    def unpackAll(self, data):
        sPattern = '(eval\(function\(p,a,c,k,e,d\)\{while.*?)\s*</script>'
        return re.sub(sPattern, lambda match: self.unpack(match.group(1)), data)
    
    def containsPacked(self, data):
        return 'p,a,c,k,e,d' in data
        
    def unpack(self, sJavascript):
        aSplit = sJavascript.split(";',")
        p = str(aSplit[0])
        aSplit = aSplit[1].split(",")
        a = int(aSplit[0])
        c = int(aSplit[1])
        k = aSplit[2].split(".")[0].replace("'", '').split('|')
        e = ''
        d = ''
        sUnpacked = str(self.__unpack(p, a, c, k, e, d))
        return sUnpacked.replace('\\', '')
    
    def __unpack(self, p, a, c, k, e, d):
        while (c > 1):
            c = c -1
            if (k[c]):
                p = re.sub('\\b' + str(self.__itoa(c, a)) +'\\b', k[c], p)
        return p
    
    def __itoa(self, num, radix):
        result = ""
        while num > 0:
            result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result
            num /= radix
        return result

class JsUnpackerV2:

    def unpackAll(self, data):
        try:
            in_data=data
            sPattern = '(eval\\(function\\(p,a,c,k,e,d.*)'
            enc_data=re.compile(sPattern).findall(in_data)
            #print 'enc_data',enc_data, len(enc_data)
            if len(enc_data)==0:
                sPattern = '(eval\\(function\\(p,a,c,k,e,r.*)'
                enc_data=re.compile(sPattern).findall(in_data)
                #print 'enc_data packer...',enc_data

            for enc_val in enc_data:
                unpack_val=self.unpack(enc_val)
                in_data=in_data.replace(enc_val,unpack_val)
            return in_data
        except: 
            traceback.print_exc(file=sys.stdout)
            return data
        
        
    def containsPacked(self, data):
        return 'p,a,c,k,e,d' in data or 'p,a,c,k,e,r' in data
        
    def unpack(self,sJavascript,iteration=1, totaliterations=1  ):

        aSplit = sJavascript.split("rn p}('")

        p1,a1,c1,k1=('','0','0','')
        ss="p1,a1,c1,k1=(\'"+aSplit[1].split(".spli")[0]+')' 
        exec(ss)
        
        k1=k1.split('|')
        aSplit = aSplit[1].split("))'")
        e = ''
        d = ''#32823
        sUnpacked1 = str(self.__unpack(p1, a1, c1, k1, e, d,iteration))
        if iteration>=totaliterations:
            return sUnpacked1
        else:
            return self.unpack(sUnpacked1,iteration+1)

    def __unpack(self,p, a, c, k, e, d, iteration,v=1):
        while (c >= 1):
            c = c -1
            if (k[c]):
                aa=str(self.__itoaNew(c, a))
                p=re.sub('\\b' + aa +'\\b', k[c], p)# THIS IS Bloody slow!
        return p

    def __itoa(self,num, radix):

        result = ""
        if num==0: return '0'
        while num > 0:
            result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result
            num /= radix
        return result
        
    def __itoaNew(self,cc, a):
        aa="" if cc < a else self.__itoaNew(int(cc / a),a) 
        cc = (cc % a)
        bb=chr(cc + 29) if cc> 35 else str(self.__itoa(cc,36))
        return aa+bb


def savefile(filename, contents,pastafinal=pastaperfil):
    try:
        destination = os.path.join(pastafinal,filename)
        fh = open(destination, 'wb')
        fh.write(contents)  
        fh.close()
    except: print "Nao gravou os temporarios de: %s" % filename

def openfile(filename,pastafinal=pastaperfil):
    try:
        destination = os.path.join(pastafinal, filename)
        fh = open(destination, 'rb')
        contents=fh.read()
        fh.close()
        return contents
    except:
        print "Nao abriu os temporarios de: %s" % filename
        return None

def menugravador():
    if downloadPath=='':
        xbmcgui.Dialog().ok('TV Portuguesa','Necessitas de introduzir a pasta onde vão ficar','as gravações. Escolhe uma pasta com algum espaço','livre disponível.')
        dialog = xbmcgui.Dialog()
        pastafinal = dialog.browse(int(3), "Escolha pasta para as gravações", 'files')
        selfAddon.setSetting('pastagravador',value=pastafinal)
        return
    xbmc.executebuiltin("ReplaceWindow(VideoFiles," + downloadPath + ")")

def vista_canais():
      menuview=selfAddon.getSetting('vistacanais')
      if menuview == "0": xbmc.executebuiltin("Container.SetViewMode(500)")#miniatura
      elif menuview == "1": xbmc.executebuiltin("Container.SetViewMode(560)")#guia
      elif menuview == "2": xbmc.executebuiltin("Container.SetViewMode(50)")#lista
      elif menuview == "3": xbmc.executebuiltin("Container.SetViewMode(51)")#lista grande

def versao_disponivel():            
    try:
        link=abrir_url('http://fightnight-xbmc.googlecode.com/svn/addons/fightnight/plugin.video.tvpor/addon.xml')
        match=re.compile('name="TV Portuguesa"\r\n       version="(.+?)"\r\n       provider-name="fightnight">').findall(link)[0]
    except:
        ok = mensagemok('TV Portuguesa','Addon não conseguiu conectar ao servidor','de actualização. Verifique a situação.','')
        match='Erro. Verificar origem do erro.'
    return match

def checker():
    if selfAddon.getSetting('ga_visitor')=='':
        from random import randint
        selfAddon.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
    checkGA()

def limparcomentarioshtml(link,url_frame):
    print "A limpar: " + url_frame
    if re.search('Sporttv1-veetle-iframe',url_frame) or re.search('Sporttv2-veetle-iframe',url_frame):
        return link
    else:
        link=clean(link)
        htmlcomments=re.compile('<!--(?!<!)[^\[>].*?-->').findall(link)
        for comentario in htmlcomments:
            if comentario[-5:]=='//-->': pass
            else:link=link.replace(comentario,'oioioioi')
        return link

def clean(text):
    command={'\r':'','\n':'','\t':'','&nbsp;':'','&#231;':'ç','&#201;':'É','&#233;':'é','&#250;':'ú','&#227;':'ã','&#237;':'í','&#243;':'ó','&#193;':'Á','&#205;':'Í','&#244;':'ô','&#224;':'à','&#225;':'á','&#234;':'ê','&#211;':'Ó','&#226;':'â'}
    regex = re.compile("|".join(map(re.escape, command.keys())))
    return regex.sub(lambda mo: command[mo.group(0)], text)

def redirect(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent)
    response = urllib2.urlopen(req)
    gurl=response.geturl()
    return gurl

def millis():
      import time as time_
      return int(round(time_.time() * 1000))

def horaportuguesa(sapo):
    if sapo==True or sapo=='diaseguinte': fmt = '%Y-%m-%d%%20%H:%M'
    else: fmt = '%Y-%m-%d %H-%M-%S'

    if selfAddon.getSetting('horaportuguesa') == 'true':
        dt  = datetime.datetime.now()
        if sapo=='diaseguinte':
            dts = dt.strftime('%Y-%m-') + str(int(dt.strftime('%d')) + 1) +dt.strftime('%%20%H:%M')
            #special dia seguinte case
        else: dts = dt.strftime(fmt)
        return dts
    else:
        from resources.lib import pytzimp
        dt  = datetime.datetime.now()
        timezona= selfAddon.getSetting('timezone2')
        terradamaquina=str(pytzimp.timezone(pytzimp.all_timezones[int(timezona)]))
        if sapo=='diaseguinte': dia=int(dt.strftime('%d')) + 1
        else: dia=int(dt.strftime('%d'))
        d = pytzimp.timezone(terradamaquina).localize(datetime.datetime(int(dt.strftime('%Y')), int(dt.strftime('%m')), dia, hour=int(dt.strftime('%H')), minute=int(dt.strftime('%M'))))
        lisboa=pytzimp.timezone('Europe/Lisbon')
        convertido=d.astimezone(lisboa)

        dts=convertido.strftime(fmt)
        return dts

def extract(_in,_out,dp=None,type='all'):
    import zipfile
    if type=='all':
        if dp:
            return allWithProgress(_in, _out, dp)

        return allNoProgress(_in, _out)
            
    elif type=='allNoProgress':
        try:
            zin = zipfile.ZipFile(_in, 'r')
            zin.extractall(_out)
        except Exception, e:
            print str(e)
            return False
        return True

    elif type=='allWithProgress':
        zin = zipfile.ZipFile(_in,  'r')
        nFiles = float(len(zin.infolist()))
        count  = 0
        try:
            for item in zin.infolist():
                count += 1
                update = count / nFiles * 100
                dp.update(int(update))
                zin.extract(item, _out)
        except Exception, e:
            print str(e)
            return False
        return True

def normalize(text):
    if isinstance(text, str):
        try:
            text = text.decode('utf8')
        except:
            try:
                text = text.decode('latin1')
            except:
                text = text.decode('utf8', 'ignore')
    import unicodedata
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore')

def limpar(text):
    command={'(':'- ',')':''}
    regex = re.compile("|".join(map(re.escape, command.keys())))
    return regex.sub(lambda mo: command[mo.group(0)], text)


### DOWNLOADER ###

def downloader(url,dest, mensagem="A fazer download...",useReq = False):
    dp = xbmcgui.DialogProgress()
    dp.create("TV Portuguesa",mensagem,'')

    if useReq:
        import urllib2
        req = urllib2.Request(url)
        req.add_header('Referer', 'http://wallpaperswide.com/')
        f       = open(dest, mode='wb')
        resp    = urllib2.urlopen(req)
        content = int(resp.headers['Content-Length'])
        size    = content / 100
        total   = 0
        while True:
            if dp.iscanceled(): 
                raise Exception("Canceled")                
                dp.close()

            chunk = resp.read(size)
            if not chunk:            
                f.close()
                break

            f.write(chunk)
            total += len(chunk)
            percent = min(100 * total / content, 100)
            dp.update(percent)       
    else:
        urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))

def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled(): 
        raise Exception("Canceled")
        dp.close()

### GA ###

def parseDate(dateString):
    try: return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except: return datetime.datetime.today() - datetime.timedelta(days = 1) #force update

def checkGA():
    secsInHour = 60 * 60
    threshold  = 2 * secsInHour
    now   = datetime.datetime.today()
    prev  = parseDate(selfAddon.getSetting('ga_time'))
    delta = now - prev
    nDays = delta.days
    nSecs = delta.seconds
    doUpdate = (nDays > 0) or (nSecs > threshold)
    if not doUpdate: return
    selfAddon.setSetting('ga_time', str(now).split('.')[0])
    APP_LAUNCH()    
    
                    
def send_request_to_google_analytics(utm_url):
    try:
        req = urllib2.Request(utm_url, None,{'User-Agent':user_agent})
        response = urllib2.urlopen(req).read()
    except:
        print ("GA fail: %s" % utm_url)         
    return response
       
def GA(group,name):
        try:
            try:
                from hashlib import md5
            except:
                from md5 import md5
            from random import randint
            import time
            from urllib import unquote, quote
            from os import environ
            from hashlib import sha1
            VISITOR = selfAddon.getSetting('ga_visitor')
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            if not group=="None":
                    utm_track = utm_gif_location + "?" + \
                            "utmwv=" + versao + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmt=" + "event" + \
                            "&utme="+ quote("5("+PATH+"*"+group+"*"+name+")")+\
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
                    try:
                        print "============================ POSTING TRACK EVENT ============================"
                        send_request_to_google_analytics(utm_track)
                    except:
                        print "============================  CANNOT POST TRACK EVENT ============================" 
            if name=="None":
                    utm_url = utm_gif_location + "?" + \
                            "utmwv=" + versao + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
            else:
                if group=="None":
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + versao + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                else:
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + versao + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+group+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                                
            print "============================ POSTING ANALYTICS ============================"
            send_request_to_google_analytics(utm_url)
            
        except:
            print "================  CANNOT POST TO ANALYTICS  ================" 
            
            
def APP_LAUNCH():
        versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
        print versionNumber
        if versionNumber < 12:
            if xbmc.getCondVisibility('system.platform.osx'):
                if xbmc.getCondVisibility('system.platform.atv2'):
                    log_path = '/var/mobile/Library/Preferences'
                else:
                    log_path = os.path.join(os.path.expanduser('~'), 'Library/Logs')
            elif xbmc.getCondVisibility('system.platform.ios'):
                log_path = '/var/mobile/Library/Preferences'
            elif xbmc.getCondVisibility('system.platform.windows'):
                log_path = xbmc.translatePath('special://home')
                log = os.path.join(log_path, 'xbmc.log')
                logfile = open(log, 'r').read()
            elif xbmc.getCondVisibility('system.platform.linux'):
                log_path = xbmc.translatePath('special://home/temp')
            else:
                log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        elif versionNumber > 11:
            print '======================= more than ===================='
            if versionNumber < 14: filename='xbmc.log'
            else: filename='kodi.log'
            log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, filename)
            logfile = open(log, 'r').read()
            if versionNumber < 14: match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
            else: match=re.compile('Starting Kodi \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        else:
            logfile='Starting XBMC (Unknown Git:.+?Platform: Unknown. Built.+?'
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        print '==========================   '+PATH+' '+versao+'  =========================='
        try:
            from hashlib import md5
        except:
            from md5 import md5
        from random import randint
        import time
        from urllib import unquote, quote
        from os import environ
        from hashlib import sha1
        import platform
        VISITOR = selfAddon.getSetting('ga_visitor')
        for build, PLATFORM in match:
            if re.search('12',build[0:2],re.IGNORECASE): 
                build="Frodo" 
            if re.search('11',build[0:2],re.IGNORECASE): 
                build="Eden" 
            if re.search('13',build[0:2],re.IGNORECASE): 
                build="Gotham" 
            print build
            print PLATFORM
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            utm_track = utm_gif_location + "?" + \
                    "utmwv=" + versao + \
                    "&utmn=" + str(randint(0, 0x7fffffff)) + \
                    "&utmt=" + "event" + \
                    "&utme="+ quote("5(APP LAUNCH*"+build+"*"+PLATFORM+")")+\
                    "&utmp=" + quote(PATH) + \
                    "&utmac=" + UATRACK + \
                    "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
            try:
                print "============================ POSTING APP LAUNCH TRACK EVENT ============================"
                send_request_to_google_analytics(utm_track)
            except:
                print "============================  CANNOT POST APP LAUNCH TRACK EVENT ============================" 

### PASTAS E AFINS ###

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]                         
    return param

def addLink(name,url,iconimage):
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
    try:
        if re.search('HD',name) or re.search('1080P',name) or re.search('720P',name):liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 1280, 'height': 720 } )
        else: liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 600, 'height': 300 } )
    except: pass    
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def addCanal(name,url,mode,iconimage,total,descricao):
    cm=[]
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)#+"&thumb="+urllib.quote_plus(iconimage)
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "overlay":6 ,"plot":descricao} )
    liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
    try:
        if re.search('HD',name) or re.search('1080P',name) or re.search('720P',name):liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 1280, 'height': 720 } )
        else: liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 600, 'height': 300 } )
    except: pass
    cm.append(('Gravar canal', "XBMC.RunPlugin(%s?mode=%s&name=%s&url=%s)"%(sys.argv[0],30,name,url)))
    cm.append(('Ver programação', "XBMC.RunPlugin(%s?mode=%s&name=%s&url=%s)"%(sys.argv[0],31,name,url)))
    liz.addContextMenuItems(cm, replaceItems=False)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=total)

def addDir(name,url,mode,iconimage,total,descricao,pasta):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "overlay":6 ,"plot":descricao} )
    liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

params=get_params()
url=None
thumb=None
name=None
mode=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: thumb=urllib.unquote_plus(params["thumb"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Thumb: "+str(url)
checker()

if mode==None or url==None or len(url)<1:
    print "Versao Instalada: v" + versao
    if selfAddon.getSetting('termos') == 'true':
        mensagemaviso()
        selfAddon.setSetting('termos',value='false')
    canais()
if mode==1: menu_principal()
elif mode==2: replaytv()
elif mode==3: replaytv_lista(name,url)
elif mode==4: replaytv_progs(name,url)
elif mode==5: obter_lista(name,url)
elif mode==6: listascanais()
elif mode==7: descobrirresolver(url,nomecanal,linkrecebido,zapping)
elif mode==8: replaytv_play(name,url)
elif mode==9: xbmc.executebuiltin("Container.NextViewMode")
elif mode==10: replaytv_pesquisa()
elif mode==11: obter_lista(name,url)
elif mode==12: menugravador()
elif mode==13: abrir_lista_canais()
elif mode==14: ok = mensagemok('TV Portuguesa','[B][COLOR white]Queres adicionar a tua lista (XML)?[/COLOR][/B]','Visita [B]http://bit.ly/fightnightaddons[/B]','ou contacta "fightnight.addons@gmail.com')
elif mode==15: ok = mensagemok('TV Portuguesa','A actualizacao é automática. Caso nao actualize va ao','repositorio fightnight e prima c ou durante 2seg','e force a actualizacao. De seguida, reinicie o XBMC.')
elif mode==16: request_servidores(url,name)
elif mode==17: comecarvideo(url,name,'listas',False,thumb=thumb)
elif mode==18: entraraddon()
elif mode==19: radios()
elif mode==20: radioslocais()
elif mode==21: radiosobterurlstream(name,url)
elif mode==22: selfAddon.openSettings()
elif mode==23: mensagemaviso()
elif mode==24: listar_radios(name,url)
elif mode==25: sportsdevil()
elif mode==26: praias()
elif mode==27: _descobrirresolver(url,name,False,False,'Praias')
elif mode==28: eventosdesportivos()
elif mode==29: firstrow()
elif mode==30: request_servidores(url,name,gravador=True)
elif mode==31: programacao_canal()
elif mode==2013: testejanela()
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
