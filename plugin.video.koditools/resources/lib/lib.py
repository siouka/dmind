#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2014 Anonymous

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os,sys,time,subprocess,shutil,hashlib,zipfile,ctypes
h = HTMLParser.HTMLParser()

addon_id = 'plugin.video.xbmctools'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
if not os.path.exists(addonfolder): addonfolder = addonfolder.decode('utf-8')
artfolder = addonfolder + '/resources/img/'
dialog = xbmcgui.Dialog()
xbmc_version = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
traducaoma= selfAddon.getLocalizedString

def traducao(texto):
	return traducaoma(texto).encode('utf-8')

class librtmp:

	def VersionChecker(self,system):
		if system == "ios":
			#librtmp_path = os.path.join(xbmc.translatePath("special://xbmc").replace('XBMCData/XBMCHome','Frameworks'),"librtmp.0.dylib")
			librtmp_path = os.path.join(xbmc.translatePath("special://frameworks"),"librtmp.0.dylib")
			md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/ios.xml.md5")
		elif system == "macos":
			#librtmp_path = os.path.join(xbmc.translatePath("special://xbmc").replace('Resources/XBMC','Libraries'),"librtmp.0.dylib")
			librtmp_path = os.path.join(xbmc.translatePath("special://frameworks"),"librtmp.0.dylib")
			if selfAddon.getSetting('mac_bits') == "0": md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/macos_x86.xml.md5")
			elif selfAddon.getSetting('mac_bits') == "1": md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/macos_x64.xml.md5")
			else: return
		elif system == "windows":
			librtmp_path = os.path.join(xbmc.translatePath("special://xbmc"), "system/players/dvdplayer/librtmp.dll")
			md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/windows.xml.md5")
		elif system == "android":
			xbmc_path = self.android_xbmc_path()
			librtmp_path = os.path.join(xbmc_path, "lib","librtmp.so")
			aux = os.path.join(xbmc_path, "lib", "libxbrtmp.so")
			if os.path.exists(aux): librtmp_path = aux
			md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/android.xml.md5")
		elif system == "openelec":
			md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/raspberry.xml.md5")
			librtmp_path = "/storage/lib/librtmp.so.0"
		elif system == "openelec pc":
			if os.uname()[4] == "i686" or os.uname()[4] == "i386": md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x86.xml.md5")
			elif os.uname()[4] == "x86_64": md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x64.xml.md5")
			else: return
			librtmp_path = "/storage/lib/librtmp.so.0"
		elif system == "linux" or system == "raspberry":
			librtmp_path, lib = self._librtmp_path()
			if system == "raspberry": md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/raspberry.xml.md5")
			elif system == "linux": 
				if os.uname()[4] == "i686" or os.uname()[4] == "i386": md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x86.xml.md5")
				elif os.uname()[4] == "x86_64": md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x64.xml.md5")
				else: return
				
		if self.md5sum_verified(librtmp_path) == md5: self.addLink("[B][COLOR blue]"+traducao(2049)+"[/COLOR][/B]",'',artfolder + "check.png")
		else: self.addLink("[B][COLOR red]"+traducao(2050)+"[/COLOR][/B]",'',artfolder + "check.png")

	def keyboard(self,url):
		dialog.ok(traducao(2009), traducao(2010))
		if url == "windows":
			self.addDir("QWERTY","qwerty windows",2,artfolder + "keyboard.png",False)
			self.addDir("ABCDE","abcde windows",2,artfolder + "keyboard.png",False)
		elif url == "android":
			self.addDir("QWERTY","qwerty android",2,artfolder + "keyboard.png",False)
			self.addDir("ABCDE","abcde android",2,artfolder + "keyboard.png",False)
		elif url == "linux":
			self.addDir("QWERTY","qwerty",6,artfolder + "keyboard.png",False)
			self.addDir("ABCDE","abcde",6,artfolder + "keyboard.png",False)
			
	#########################################	LINUX

	def _librtmp_path(self):
		file_path = selfAddon.getSetting('librtmp_path')
		if "librtmp.so.0" in file_path: lib = "librtmp.so.0"
		elif "librtmp.so.1" in file_path: lib = "librtmp.so.1"
		else: 
			file_path = "erro"
			lib = "erro"
		return file_path,lib

	def set_librtmp_path(self):
		if selfAddon.getSetting('librtmp_path') != "": return
		mensagemprogresso = xbmcgui.DialogProgress()
		mensagemprogresso.create('XBMC Tools', traducao(3031),traducao(2013))
		mensagemprogresso.update(33)
		file_path = self.find_abs_path("librtmp.so.0","/lib/")
		if file_path == "erro": file_path = self.find_abs_path("librtmp.so.1","/lib/")
		mensagemprogresso.update(66)
		selfAddon.setSetting('librtmp_path',value=file_path)
		mensagemprogresso.update(100)
		mensagemprogresso.close()

	def file_name(self,path):
		import ntpath
		head, tail = ntpath.split(path)
		return tail or ntpath.basename(head)

	def find_abs_path(self,str_path, search_str = ""):
		p = subprocess.Popen('find / | grep ' + str_path, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
		p_status = p.wait()
		
		aux = ""
		paths = []
		letra = False
		
		for x in range(0, len(output)):
			if not letra:
				if output[x] == " " or output[x] == "\n": continue
				else:
					aux = aux + output[x]
					letra = True
			else:
				if output[x] == " " or output[x] == "\n":
					try:
						if output[x+1] == "/" or output[x+1] == " " or output[x+1] == "\n":
							paths.append(aux)
							aux = ""
							letra = False
						else: aux = aux + output[x]
					except: paths.append(aux)
				else: aux = aux + output[x]
		
		if len(paths) == 1:
			if self.file_name(paths[0]) == str_path: return paths[0]
			else: return "erro"
		if search_str != "":
			for x in range(0, len(paths)):
				if search_str in paths[x] and self.file_name(paths[x]) == str_path: return paths[x]
			return "erro"
		return paths

	def librtmp_openelec(self,url,autorun=False):
		if url == "raspberry":
			md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/raspberry.xml.md5")
			url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/RaspberryPI/librtmp.so.0"
		else:
			if os.uname()[4] == "i686" or os.uname()[4] == "i386": 
				url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Linux/x86&ATV1/librtmp.so.0"
				md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x86.xml.md5")
			elif os.uname()[4] == "x86_64": 
				url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Linux/x64/librtmp.so.0"
				md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x64.xml.md5")
			else:
				ret = dialog.select(traducao(2030), ['x86', 'x64'])
				if ret == 0:
					url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Linux/x86&ATV1/librtmp.so.0"
					md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x86.xml.md5")
				elif ret == 1: 
					url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Linux/x64/librtmp.so.0"
					md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x64.xml.md5")
				else: return
			
		if self.md5sum_verified("/storage/lib/librtmp.so.0") == md5:
			if autorun: return
			if not dialog.yesno(traducao(2016),traducao(2044),traducao(2045)): return
		
		if autorun:
			if not dialog.yesno(traducao(2016),traducao(2060),traducao(2061)): return
		
		my_tmp = os.path.join(addonfolder,"resources","temp","librtmp.so.0")
		
		if not self.download(my_tmp,url_download):
			dialog.ok(traducao(2014), traducao(2015))
			return;
			
		if os.path.exists("/storage/lib/librtmp.so.0") and os.path.exists("/var/tmp/libhack/3rdparty/librtmp.so.0"):
			if not dialog.yesno(traducao(2016),traducao(2053),traducao(2054)):
				subprocess.call("rm /storage/lib/librtmp.so.0", shell=True)
				subprocess.call("cp " + my_tmp + " /storage/lib/librtmp.so.0", shell=True)
				subprocess.call("chmod 755 /storage/lib/librtmp.so.0", shell=True)
				subprocess.call("rm " + my_tmp, shell=True)
				
				if self.md5sum_verified("/storage/lib/librtmp.so.0") != md5: dialog.ok(traducao(2014),traducao(2042),traducao(2043))
				
				dialog.ok(traducao(2016),traducao(2017))
				subprocess.call("reboot", shell=True)
				return
		
		mensagemprogresso = xbmcgui.DialogProgress()
		mensagemprogresso.create('XBMC Tools', traducao(2012),traducao(2013))
		subprocess.call("mkdir -p /storage/lib", shell=True)
		mensagemprogresso.update(13)
		subprocess.call("curl -L http://is.gd/kBaTzY -o /storage/.config/autostart.sh", shell=True)
		mensagemprogresso.update(26)
		subprocess.call("curl -L http://is.gd/yQUqNm -o /storage/.config/hacklib", shell=True)
		mensagemprogresso.update(39)
		subprocess.call("curl -L http://is.gd/GJdaEY -o /storage/.config/mktmplib", shell=True)
		mensagemprogresso.update(52)
		subprocess.call("cp " + my_tmp + " /storage/lib/librtmp.so.0", shell=True)
		mensagemprogresso.update(65)
		subprocess.call("chmod 755 /storage/lib/librtmp.so.0", shell=True)
		mensagemprogresso.update(78)
		subprocess.call("ln -s /storage/lib/librtmp.so.0 /storage/lib/librtmp.so", shell=True)
		mensagemprogresso.update(90)
		subprocess.call("rm " + my_tmp, shell=True)
		mensagemprogresso.update(100)
		mensagemprogresso.close()
		
		if self.md5sum_verified("/storage/lib/librtmp.so.0") != md5: dialog.ok(traducao(2014),traducao(2042),traducao(2043))
		
		dialog.ok(traducao(2016),traducao(2017))
		subprocess.call("reboot", shell=True)

	def is_admin(self):
		return ctypes.windll.shell32.IsUserAnAdmin() != 0
		
	def backup(self,url):
		self.addDir("Backup",url + " backup",10,artfolder + "backup.png",False)
		self.addDir("Restore",url + " restore",10,artfolder + "backup.png",False)
		self.addDir(traducao(2063),url + " remove",10,artfolder + "backup.png",False)
		
	def backup_(self,url):
		if "backup" in url:
			if not dialog.yesno(traducao(2016), traducao(2018),traducao(2019)): return
		elif "remove" in url:
			if not dialog.yesno(traducao(2016), traducao(2020),traducao(2019)): return
		elif "restore" in url:
			if not dialog.yesno(traducao(2016), traducao(2021),traducao(2019)): return

		if "linux" in url or "raspberry" in url or "openelec" in url:
			if "openelec" in url: 
				librtmp_path = "/storage/lib/librtmp.so.0"
				lib = "librtmp.so.0"
			else:
				librtmp_path, lib = self._librtmp_path()
			
			if os.path.exists(librtmp_path) is False:
				dialog.ok(traducao(2014), traducao(2022))
				return
				
			if ("remove" in url or "restore" in url) and not os.path.exists(librtmp_path.replace(lib,lib+".bak")): 
				dialog.ok(traducao(2016), traducao(2023))
				return
			
			if "linux" in url or "raspberry" in url:
				if self.verifica_pass(""): password = ""
				else:
					keyb = xbmc.Keyboard('', traducao(2024)) 
					keyb.setHiddenInput(True)
					keyb.doModal()
					if (keyb.isConfirmed()): password = keyb.getText()
					else: return
					
					if self.verifica_pass(password) is False: 
						dialog.ok(traducao(2014), traducao(2025))
						return
			if "openelec" in url:
				if "remove" in url or "backup" in url: subprocess.call("rm " + librtmp_path.replace("librtmp.so.0","librtmp.so.0.bak"), shell=True)
				if "backup" in url: subprocess.call("cp " + librtmp_path + " " + librtmp_path.replace("librtmp.so.0","librtmp.so.0.bak"), shell=True)
				if "restore" in url: 
					subprocess.call("rm " + librtmp_path, shell=True)
					subprocess.call("cp " + librtmp_path.replace("librtmp.so.0","librtmp.so.0.bak") + " " + librtmp_path, shell=True)
					subprocess.call("rm " + librtmp_path.replace("librtmp.so.0","librtmp.so.0.bak"), shell=True)
					subprocess.call("chmod 755 " + librtmp_path, shell=True)
				dialog.ok(traducao(2026),traducao(2027))
				return
			
			if "remove" in url or "backup" in url:		
				p = subprocess.Popen("sudo -S rm " + librtmp_path.replace(lib,lib+".bak"), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				p.communicate(password+"\n") 
			if "backup" in url:
				p = subprocess.Popen("sudo -S cp " + librtmp_path + " " + librtmp_path.replace(lib,lib+".bak"), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				p.communicate(password+"\n")
			if "restore" in url:
				p = subprocess.Popen("sudo -S rm " + librtmp_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				p.communicate(password+"\n") 
				p = subprocess.Popen("sudo -S cp " + librtmp_path.replace(lib,lib+".bak") + " " + librtmp_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				p.communicate(password+"\n")
				p = subprocess.Popen("sudo -S rm " + librtmp_path.replace(lib,lib+".bak"), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				p.communicate(password+"\n") 
				p = subprocess.Popen("sudo -S chmod 755 " + librtmp_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				p.communicate(password+"\n") 
			dialog.ok(traducao(2026),traducao(2027))
			return
			
		if "windows" in url or "ios" in url or "macos" in url or "armv7" in url:
			xbmc_folder = xbmc.translatePath("special://xbmc")
			if "windows" in url:
				if not self.is_admin():
					dialog.ok(traducao(2014),traducao(2028))
					return
				librtmp_path = os.path.join(xbmc_folder, "system/players/dvdplayer/librtmp.dll")
				bak_path = os.path.join(xbmc_folder, "system/players/dvdplayer/librtmp.dll.bak")
			if "ios" in url:
				#librtmp_path = os.path.join(xbmc_folder.replace('XBMCData/XBMCHome','Frameworks'),"librtmp.0.dylib")
				#bak_path = os.path.join(xbmc_folder.replace('XBMCData/XBMCHome','Frameworks'),"librtmp.0.dylib.bak")
				librtmp_path = os.path.join(xbmc.translatePath("special://frameworks"),"librtmp.0.dylib")
				bak_path = os.path.join(xbmc.translatePath("special://frameworks"),"librtmp.0.dylib.bak")
			if "macos" in url:
				#librtmp_path = os.path.join(xbmc_folder.replace('Resources/XBMC','Libraries'),"librtmp.0.dylib")
				#bak_path = os.path.join(xbmc_folder.replace('Resources/XBMC','Libraries'),"librtmp.0.dylib.bak")
				librtmp_path = os.path.join(xbmc.translatePath("special://frameworks"),"librtmp.0.dylib")
				bak_path = os.path.join(xbmc.translatePath("special://frameworks"),"librtmp.0.dylib.bak")
			if "armv7" in url:
				librtmp_path, lib = _librtmp_path()
				bak_path = librtmp_path.replace(lib,lib+'.bak')
			
			if os.path.exists(librtmp_path) is False:
				dialog.ok(traducao(2014), traducao(2022))
				return
			
			if ("remove" in url or "restore" in url) and not os.path.exists(bak_path): 
				dialog.ok(traducao(2016), traducao(2023))
				return
			
			if "remove" in url or "backup" in url: 
				if not self.remove_ficheiro(bak_path): return
			if "backup" in url: shutil.copy(librtmp_path,bak_path)
			if "restore" in url:
				if not self.remove_ficheiro(librtmp_path): return
				shutil.copy(bak_path,librtmp_path)
				self.remove_ficheiro(bak_path)
				if "windows" in url: os.chmod(librtmp_path,755)
			dialog.ok(traducao(2026),traducao(2027))
			return
			
		if "android" in url:
			xbmc_path = self.android_xbmc_path()
			librtmp_path = os.path.join(xbmc_path, "lib/librtmp.so")
			bak_path = os.path.join(xbmc_path, "lib/librtmp.so.bak")
			
			aux = os.path.join(xbmc_path, "lib", "libxbrtmp.so")
			if os.path.exists(aux): 
				librtmp_path = aux
				bak_path = os.path.join(xbmc_path, "lib/libxbrtmp.so.bak")
			
			if ("remove" in url or "restore" in url) and not os.path.exists(bak_path): 
				dialog.ok(traducao(2016), traducao(2023))
				return
			
			if not self.checksu():
				dialog.ok(traducao(2014),traducao(2029))
				return
				
			if "remove" in url or "backup" in url: os.system("su -c 'rm "+bak_path+"'")
			if "backup" in url: os.system("su -c 'cat "+librtmp_path+" > "+bak_path+"'")
			if "restore" in url:
				os.system("su -c 'rm "+librtmp_path+"'")
				os.system("su -c 'cat "+bak_path+" > "+librtmp_path+"'")
				os.system("su -c 'rm "+bak_path+"'")
				os.system("su -c 'chmod 755 "+librtmp_path+"'")
			dialog.ok(traducao(2026),traducao(2027))
			return
			
	def librtmp_linux(self,url,autorun=False):
		
		if url == "raspberry":
			url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/RaspberryPI/librtmp.so.0"
			md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/raspberry.xml.md5")
		elif url == "linux":
			if os.uname()[4] == "i686" or os.uname()[4] == "i386": 
				url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Linux/x86&ATV1/librtmp.so.0"
				md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x86.xml.md5")
			elif os.uname()[4] == "x86_64": 
				url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Linux/x64/librtmp.so.0"
				md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x64.xml.md5")
			else:
				ret = dialog.select(traducao(2030), ['x86', 'x64'])
				if ret == 0:
					url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Linux/x86&ATV1/librtmp.so.0"
					md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x86.xml.md5")
				elif ret == 1: 
					url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Linux/x64/librtmp.so.0"
					md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x64.xml.md5")
				else: return
		else: return
			
		file_path, lib = self._librtmp_path()

		if os.path.exists(file_path) is False:
			if autorun and file_path == "":
				self.set_librtmp_path()
				file_path, lib = self._librtmp_path()
			else:
				dialog.ok(traducao(2014), traducao(2022))
				return

		librtmp_path = file_path.replace(lib,"")
		my_tmp = os.path.join(addonfolder,"resources","temp",lib)
		
		if self.md5sum_verified(file_path) == md5:
			if autorun: return
			if not dialog.yesno(traducao(2016),traducao(2044),traducao(2045)): return
			
		if autorun:
			if not dialog.yesno(traducao(2016),traducao(2060),traducao(2061)): return
		
		if self.verifica_pass(""): password = ""
		else:
			keyb = xbmc.Keyboard('', traducao(2024)) 
			keyb.setHiddenInput(True)
			keyb.doModal()
			if (keyb.isConfirmed()): password = keyb.getText()
			else: return
			
			if self.verifica_pass(password) is False: 
				dialog.ok(traducao(2014), traducao(2025))
				return

		if self.download(my_tmp,url_download):
			p = subprocess.Popen("sudo -S rm " + file_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			p.communicate(password+"\n") 
			p = subprocess.Popen("sudo -S cp " + my_tmp + " " + librtmp_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			p.communicate(password+"\n") 
			self.remove_ficheiro(my_tmp)
			p = subprocess.Popen("sudo -S chmod 755 " + file_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			p.communicate(password+"\n") 
			if self.md5sum_verified(file_path) == md5: 
				dialog.ok(traducao(2016), traducao(2026),traducao(2032))
				xbmc.executebuiltin("Container.Refresh")
			else: dialog.ok(traducao(2014),traducao(2042),traducao(2043))
		else: dialog.ok(traducao(2014), traducao(2015))
		

	def verifica_pass(self,password):
		p = subprocess.Popen("sudo -S su ", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		(output, err) = p.communicate(password+"\n") 
		rc = p.returncode
		if rc == 0: return True
		return False

	def change_keyboard_linux(self,url):
		mensagemprogresso = xbmcgui.DialogProgress()
		mensagemprogresso.create('XBMC Tools', traducao(3031),traducao(2013))
		mensagemprogresso.update(50)
		file_path = self.find_abs_path("DialogKeyboard.xml","skin.confluence/720p/")
		
		if (os.path.exists(file_path) and "skin.confluence/720p/DialogKeyboard.xml" in file_path) is False:
			mensagemprogresso.close()
			dialog.ok(traducao(2014), traducao(2034))
			return
		
		keyboard_path = file_path.replace("DialogKeyboard.xml","")
		my_tmp = os.path.join(addonfolder,"resources","temp","DialogKeyboard.xml")
		mensagemprogresso.update(100)
		mensagemprogresso.close()
		
		if self.verifica_pass(""): password = ""
		else:
			keyb = xbmc.Keyboard('', traducao(2024)) 
			keyb.setHiddenInput(True)
			keyb.doModal()
			if (keyb.isConfirmed()): password = keyb.getText()
			else: return
			
			if self.verifica_pass(password) is False: 
				dialog.ok(traducao(2014), traducao(2025))
				return
		
		if url == "qwerty": url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/keyboard/qwerty/DialogKeyboard.xml"
		elif url == "abcde": url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/keyboard/abcd/DialogKeyboard.xml"
		
		if self.download(my_tmp,url_download):
			p = subprocess.Popen("sudo -S rm " + file_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			p.communicate(password+"\n") 
			p = subprocess.Popen("sudo -S cp " + my_tmp + " " + keyboard_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			p.communicate(password+"\n")
			self.remove_ficheiro(my_tmp)
			dialog.ok(traducao(2026),traducao(2027))
			xbmc.executebuiltin('ReloadSkin()')
		else: dialog.ok(traducao(2014), traducao(2015))

	#########################################	ANDROID
		
	def checksu(self):
		if os.system("su -c ''") == 0: return True
		return False
		
	def librtmp_android(self,autorun = False):
		my_librtmp = os.path.join(addonfolder,"resources","temp","librtmp.so")
		xbmc_path = self.android_xbmc_path()
		librtmp_path = os.path.join(xbmc_path, "lib", "librtmp.so")
		aux = os.path.join(xbmc_path, "lib", "libxbrtmp.so")
		if os.path.exists(aux): librtmp_path = aux
			
		md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/android.xml.md5")
		
		if os.path.exists(librtmp_path) is False:
			dialog.ok(traducao(2014), traducao(2022))
			return
		if self.md5sum_verified(librtmp_path) == md5:
			if autorun: return
			if not dialog.yesno(traducao(2016),traducao(2044),traducao(2045)): return 
		if autorun:
			if not dialog.yesno(traducao(2016),traducao(2060),traducao(2061)): return 
		if not autorun:
			if not dialog.yesno(traducao(2016), traducao(2033),traducao(2019)): return
		if not self.checksu():
			dialog.ok(traducao(2014),traducao(2029))
			return
		
		print "////////ANDROID////////"
		print "my_librtmp: " + my_librtmp
		print "librtmp_path: " + librtmp_path
		
		if self.download(my_librtmp,"http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Android/librtmp.so"):
			if selfAddon.getSetting('android_hack') == "true":
				librtmp_hack_path = os.path.join(addonfolder,"resources","android_hack","librtmp.so")
				os.system("su -c 'rm "+librtmp_hack_path+"'")
				os.system("su -c 'cat "+my_librtmp+" > "+librtmp_hack_path+"'")
			c1 = os.system("su -c 'rm "+librtmp_path+"'")
			c2 = os.system("su -c 'cat "+my_librtmp+" > "+librtmp_path+"'")
			c3 = os.system("su -c 'chmod 755 "+librtmp_path+"'")
			self.remove_ficheiro(my_librtmp)
			if self.md5sum_verified(librtmp_path) == md5: 
				dialog.ok(traducao(2016), traducao(2026),traducao(2032))
				xbmc.executebuiltin("Container.Refresh")
			else: dialog.ok(traducao(2014),traducao(2042),traducao(2043))
			print "Return: " + str(c1) +" "+ str(c2) +" "+ str(c3)
		else: dialog.ok(traducao(2014), traducao(2015))
	
	def android_hack_checker(self):
		if selfAddon.getSetting('android_hack') == "false": return False
		my_librtmp = os.path.join(addonfolder,"resources","android_hack","librtmp.so")
		if not os.path.exists(my_librtmp):
			selfAddon.setSetting('android_hack',value='false')
			return False
		return True
	
	def android_hack_on(self):
		if not dialog.yesno(traducao(2016), traducao(2033),traducao(2019)): return
		if not self.checksu():
			dialog.ok(traducao(2014),traducao(2029))
			return
		my_librtmp = os.path.join(addonfolder,"resources","android_hack","librtmp.so")
		self.remove_ficheiro(my_librtmp)
		if self.download(my_librtmp,"http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Android/librtmp.so"):
			selfAddon.setSetting('android_hack',value='true')
			xbmc.executebuiltin("Container.Refresh")
			
	def android_hack_off(self):
		my_librtmp = os.path.join(addonfolder,"resources","android_hack","librtmp.so")
		self.remove_ficheiro(my_librtmp)
		selfAddon.setSetting('android_hack',value='false')
		xbmc.executebuiltin("Container.Refresh")
		
	'''def xbmc_android_hack(self):
		my_librtmp = os.path.join(addonfolder,"resources","temp","librtmp.so")
		my_apk = os.path.join(addonfolder,"resources","temp","xbmc.apk")
		app_lib = self.get_xbmb_applib()
		xbmc_apk = self.get_xbmb_apk()
		if xbmc_apk == "erro" or app_lib == "erro": return
		if self.download(my_librtmp,"http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Android/librtmp.so"):
			#os.system("su -c 'cat "+my_librtmp+" > "+os.path.join(app_lib,"librtmp.so")+"'")
			#os.system("su -c 'chmod 755 "+os.path.join(app_lib,"librtmp.so")+"'")
			os.system("su -c 'chmod 755 "+my_librtmp+"'")
			os.system("su -c 'cat "+xbmc_apk+" > "+my_apk+"'")
			if not self.change_from_apk(my_apk, my_librtmp): return
			#os.system("su -c 'rm "+xbmc_apk+"'")
			#os.system("su -c 'cat "+my_apk+" > "+xbmc_apk+"'")
			self.remove_ficheiro(my_apk)
			#self.remove_ficheiro(my_librtmp)
			#os.system("su -c 'chown system.system "+xbmc_apk+"'")
			#os.system("su -c 'chmod 644 "+xbmc_apk+"'")
			os.system("su -c 'rm /data/dalvik-cache/*'")
			os.system("su -c 'rm /cache/dalvik-cache/*'")
			dialog.ok("Concluido","O Android vai reiniciar...")
			if os.system("su -c 'reboot'"):	xbmc.executebuiltin('Reboot')
		else: dialog.ok(traducao(2014), traducao(2015))
		
	def get_xbmb_applib(self):
		output = os.popen("su -c 'ls /data/app-lib/'").read()
		paths = output.replace(" ","").split("\n")
		try:
			for x in range(0,len(paths)):
				if "xbmc" in paths[x]: return os.path.join("/data","app-lib",paths[x])
		except: pass
		return "erro"
	
	def get_xbmb_apk(self):
		output = os.popen("su -c 'ls /data/app/'").read()
		paths = output.replace(" ","").split("\n")
		try:
			for x in range(0,len(paths)):
				if "xbmc" in paths[x]: return os.path.join("/data","app",paths[x])
		except: pass
		return "erro"

	def change_from_apk(self,apkpath, filepath):
		if not os.path.exists(apkpath): return False
		mensagemprogresso = xbmcgui.DialogProgress()
		mensagemprogresso.create('XBMC Tools', traducao(3031),traducao(2013))
		tempname = os.path.join(addonfolder,"resources","temp", 'new_temp.apk')
		flag = False
		try:
			zipread=zipfile.ZipFile(apkpath, 'r')
			zipwrite=zipfile.ZipFile(tempname, 'w')
			total =len(zipread.infolist())
			i = 1
			for item in zipread.infolist():
				if self.file_name(filepath) not in item.filename:
					data = zipread.read(item.filename)
					zipwrite.writestr(item, data)
				else:
					data = open(filepath, "rb").read()
					zipwrite.writestr(item, data)
				mensagemprogresso.update(int((i/float(total))*100.0))
				i = i+1
			shutil.move(tempname, apkpath)
			flag = True;
		except: pass
		mensagemprogresso.close()
		return flag'''
		
	def xbmc_restart(self):
			xbmc.executebuiltin("XBMC.RestartApp()")
			if os.environ.get("OS", "win32") == "win32":
				os.startfile(os.path.join(addonfolder,"resources","lib","windows.bat"))
		
	def android_xbmc_path(self):	#Obrigado enen92!
		xbmcfolder=xbmc.translatePath(addonfolder).split("/")
		i = 0
		found = False
		
		for folder in xbmcfolder:
			if folder.count('.') >= 2 and folder != addon_id :
				found = True
				break
			else:
				i+=1

		if found == True:
			uid = os.getuid()
			app_id = xbmcfolder[i]
			xbmc_data_path = os.path.join("/data", "data", app_id)
			if os.path.exists(xbmc_data_path) and uid == os.stat(xbmc_data_path).st_uid: return xbmc_data_path
		return "erro"
		
	def get_mediafire_url(self,url):
		codigo_fonte = self.abrir_url(url).replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')    
		try: return re.compile('kNO = "(.+?)"').findall(codigo_fonte)[0]
		except: return "erro"
		
	def download_apk(self):
		dir = dialog.browse(int(3), traducao(2047), 'files')
		if dir == "": return
		if not os.path.exists(dir):
			dialog.ok(traducao(2014),traducao(2046))
			return
		url = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/apk/url.txt")
		url = self.get_mediafire_url(url)
		if url == "erro":
			dialog.ok(traducao(2014), traducao(2015))
			return
		if self.download(os.path.join(dir,self.file_name(url)),url): dialog.ok(traducao(2026),traducao(2048))
		else: dialog.ok(traducao(2014), traducao(2015))
		
	#########################################	WINDOWS, IOS e MAC OSX
	
	def _version(self):
		try: ver = int(xbmc.getInfoLabel("System.BuildVersion")[0:2])
		except: ver = -1
		return ver
	
	def xbmc_bit_version(self):
		log_path = xbmc.translatePath('special://logpath')
		if self._version() < 14: log = os.path.join(log_path, 'xbmc.log')
		else: log = os.path.join(log_path, 'kodi.log')
		f = open(log,"r")
		aux = f.readlines()
		f.close()
		try: 
			bits = re.compile('XBMC (.+?) build').findall(aux[3])[0]
			if bits == "x32" or bits == "x64": return bits
		except: pass
		try: 
			bits = re.compile('Kodi (.+?) build').findall(aux[3])[0]
			if bits == "x32" or bits == "x64": return bits
		except: pass
		try:
			i = aux[3].find("-bit version", 0)
			bits = "x"+aux[3][i-2]+aux[3][i-1]
			if bits == "x32" or bits == "x64": return bits
		except: pass
		return "erro"

	def librtmp_updater(self,url,autorun = False):
		xbmc_folder = xbmc.translatePath("special://xbmc")
		if url == "windows": 
			if not self.is_admin() and not autorun:
				dialog.ok(traducao(2014),traducao(2028))
				return
			librtmp_path = os.path.join(xbmc_folder, "system/players/dvdplayer/librtmp.dll")
			my_librtmp = os.path.join(addonfolder,"resources","temp","librtmp.dll")
			download_url = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Windows/librtmp.dll"
			md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/windows.xml.md5")
		elif url == "ios":
			#librtmp_path = os.path.join(xbmc_folder.replace('XBMCData/XBMCHome','Frameworks'),"librtmp.0.dylib")
			librtmp_path = os.path.join(xbmc.translatePath("special://frameworks"),"librtmp.0.dylib")
			my_librtmp = os.path.join(addonfolder,"resources","temp","librtmp.0.dylib")
			download_url = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/iOS/librtmp.0.dylib"
			md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/ios.xml.md5")
		elif url == "macos":
			if selfAddon.getSetting('mac_bits') == "0":
				download_url = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/macOS/x86/librtmp.0.dylib"
				md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/macos_x86.xml.md5")
			elif selfAddon.getSetting('mac_bits') == "1":
				download_url = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/macOS/x64/librtmp.0.dylib"
				md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/macos_x64.xml.md5")
			else: return
			#librtmp_path = os.path.join(xbmc_folder.replace('Resources/XBMC','Libraries'),"librtmp.0.dylib")
			librtmp_path = os.path.join(xbmc.translatePath("special://frameworks"),"librtmp.0.dylib")
			my_librtmp = os.path.join(addonfolder,"resources","temp","librtmp.0.dylib")
		elif url == "armv7":
			download_url = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/RaspberryPI/librtmp.so.0"
			md5 = self.abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/raspberry.xml.md5")
			librtmp_path, lib = self._librtmp_path()
			my_librtmp = os.path.join(addonfolder,"resources","temp",lib)
		else: return
		
		if os.path.exists(librtmp_path) is False:
			dialog.ok(traducao(2014), traducao(2022))
			return
			
		if self.md5sum_verified(librtmp_path) == md5:
			if autorun: return
			if not dialog.yesno(traducao(2016),traducao(2044),traducao(2045)): return
		if autorun:
			if not dialog.yesno(traducao(2016),traducao(2060),traducao(2061)): return
			if url == "windows": 
				if not self.is_admin():
					dialog.ok(traducao(2014),traducao(2028))
					return
			
		if self.download(my_librtmp,download_url):
			if not self.remove_ficheiro(librtmp_path): return
			shutil.copy(my_librtmp,librtmp_path)
			self.remove_ficheiro(my_librtmp)
			if url == "windows" or url == "armv7": os.chmod(librtmp_path,755)
			if self.md5sum_verified(librtmp_path) == md5: 
				dialog.ok(traducao(2016), traducao(2026),traducao(2032))
				xbmc.executebuiltin("Container.Refresh")
			else: dialog.ok(traducao(2014),traducao(2042),traducao(2043))
		else: dialog.ok(traducao(2014), traducao(2015))
		
	def change_keyboard(self,url):
		if "windows" in url: 
			if not self.is_admin():
				dialog.ok(traducao(2014),traducao(2028))
				return
			keyboard_path = os.path.join(xbmc.translatePath("special://xbmc"), "addons/skin.confluence/720p/DialogKeyboard.xml")
		elif "android" in url: keyboard_path = os.path.join(self.android_xbmc_path(), "cache/apk/assets/addons/skin.confluence/720p/DialogKeyboard.xml")
		else: return
		
		my_tmp = os.path.join(addonfolder,"resources","temp","DialogKeyboard.xml")
		if os.path.exists(keyboard_path) is False:
			dialog.ok(traducao(2014), traducao(2034))
			return
			
		if "qwerty" in url: url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/keyboard/qwerty/DialogKeyboard.xml"
		elif "abcde" in url: url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/keyboard/abcd/DialogKeyboard.xml"
		else: return
			
		if self.download(my_tmp,url_download):
			if not self.remove_ficheiro(keyboard_path): return
			shutil.copy(my_tmp,keyboard_path)
			self.remove_ficheiro(my_tmp)
			dialog.ok(traducao(2026),traducao(2027))
			xbmc.executebuiltin('ReloadSkin()')
		else: dialog.ok(traducao(2014), traducao(2015))

	def md5sum_verified(self,path):	#Obrigado Mafarricos!
		if not os.path.exists(path): return "erro"
		BLOCK_SIZE = 65536
		hasher = hashlib.md5()
		f = open(path,'rb')
		done = 0
		size = os.path.getsize(path)
		while done < size:
			data = f.read(BLOCK_SIZE)
			done += len(data)
			hasher.update(data)
			if not data: break		
		md5sum = hasher.hexdigest()
		return md5sum

	def remove_ficheiro(self,file_path):
		while os.path.exists(file_path): 
				try: os.remove(file_path); break 
				except:	
					dialog = xbmcgui.Dialog()
					if dialog.yesno(traducao(2014), traducao(2039)): pass
					else: return False
		return True
		
	def download(self,mypath,url,md5 = ''):
		if os.path.isfile(mypath) is True:
			if not self.remove_ficheiro(mypath):
				dialog.ok(traducao(2014),traducao(2038))
				return False

		dp = xbmcgui.DialogProgress()
		dp.create('Download')
		start_time = time.time()		# url - url do ficheiro    mypath - localizacao ex: c:\file.mp3
		try: urllib.urlretrieve(url, mypath, lambda nb, bs, fs: self.dialogdown(nb, bs, fs, dp, start_time))
		except:
			while os.path.exists(mypath): 
				try: os.remove(mypath); break 
				except: pass
			dp.close()
			return False
		dp.close()
		print "MD5: " + self.md5sum_verified(mypath)
		if not os.path.isfile(mypath): return False
		if md5 == '': return True
		if md5 == self.md5sum_verified(mypath): return True
		return False

	def dialogdown(self,numblocks, blocksize, filesize, dp, start_time):
		  try:
				percent = min(numblocks * blocksize * 100 / filesize, 100)
				currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
				kbps_speed = numblocks * blocksize / (time.time() - start_time) 
				if kbps_speed > 0: eta = (filesize - numblocks * blocksize) / kbps_speed 
				else: eta = 0 
				kbps_speed = kbps_speed / 1024 
				total = float(filesize) / (1024 * 1024) 
				mbs = '%.02f MB %s %.02f MB' % (currently_downloaded,traducao(2040), total) 
				e = ' (%.0f Kb/s) ' % kbps_speed 
				tempo = traducao(2041) + ' %02d:%02d' % divmod(eta, 60) 
				dp.update(percent, mbs + e,tempo)
		  except: 
				percent = 100 
				dp.update(percent) 
		  if dp.iscanceled(): 
				dp.close()
				raise StopDownloading('Stopped Downloading')

	class StopDownloading(Exception):
		  def __init__(self, value): self.value = value 
		  def __str__(self): return repr(self.value)

	def abrir_url(self,url):
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link

	def addLink(self,name,url,iconimage,total=1):
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
		liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
		liz.setInfo( type="Video", infoLabels={ "Title": name } )
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,totalItems=total)
		return ok

	def addDir(self,name,url,mode,iconimage,pasta = True,total=1):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
		return ok