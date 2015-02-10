# -*- coding: utf-8 -*-
import re,math


def ioncube1(bodi):
 p = re.compile(ur'<script language=javascript>(c=".*?)<\/script>')
 result=re.findall(p, bodi)
 p = re.compile(ur'eval\(unescape\(\'?"?"(.*?)\'?"?\)\)')
 result=re.findall(p, str(result))
 import urllib
 result = urllib.unquote_plus(str(result))
 p = re.compile(ur'c="([^"]+)')
 valc=re.findall(p, bodi);valc=valc[0];
 
 p = re.compile(ur'x\("([^"]+)')
 valx=re.findall(p, bodi);valx=valx[0];
 d="";int1 = 0;
 while int1 < len(valc):
  if int1%3==0:
   d+="%";
  else:
   d+=valc[int1];
  int1 += 1
 valc=urllib.unquote_plus(d)
 valt=re.compile('t=Array\(([0-9,]+)\)').findall(valc)[0];
 
 valz=valez(valx,valt);
 return valz

def valez(valx,tS,b=1024,p=0,s=0,w=0):
		#print "TTTTSSSSS = "+tS
		l=len(valx); valt=tS.split(','); valr=[]
		#print "VALT = "+str(valt)
		for j in range(int(math.ceil(l/b)),0, -1):
			for i in range(min(l,b),0, -1):
				w |= int(valt[ord(valx[p])-48]) << s
				#print "WWW = "+str(w)
				p += 1
				if (s):
					valr.append(chr(165 ^ w & 255))
					#valu=chr(165 ^ w & 255);print "\n"+valu
					#print "VALR NOW = "+str(valr)
					w >>= 8
					s -= 2
				else:
					s = 6
			l -=1
		valr = ''.join(valr)
		#print "VALR FINAL = "+str(valr)
		return valr
#6ik3cdsewu48nt1
