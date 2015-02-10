@ECHO OFF
CLS
COLOR 1B

::SET WINDOW TITLE
TITLE Restarting XBMC ...

ECHO ---------------------------------------------------------------------------
echo                         :                                                  
echo                        :::                                                 
echo                        ::::                                                
echo                        ::::                                                
echo    :::::::       :::::::::::::::::        ::::::      ::::::        :::::::
echo    :::::::::   ::::::::::::::::::::     ::::::::::  ::::::::::    :::::::::
echo     ::::::::: ::::::::::::::::::::::   ::::::::::::::::::::::::  ::::::::: 
echo          :::::::::     :::      ::::: :::::    ::::::::    :::: :::::      
echo           ::::::      ::::       :::: ::::      :::::       :::::::        
echo           :::::       ::::        :::::::       :::::       ::::::         
echo           :::::       :::         ::::::         :::        ::::::         
echo           ::::        :::         ::::::        ::::        ::::::         
echo           ::::        :::        :::::::        ::::        ::::::         
echo          :::::        ::::       :::::::        ::::        ::::::         
echo         :::::::       ::::      ::::::::        :::         :::::::        
echo     :::::::::::::::    :::::  ::::: :::         :::         :::::::::      
echo  :::::::::  :::::::::  :::::::::::  :::         :::         ::: :::::::::  
echo  ::::::::    :::::::::  :::::::::   :::         :::         :::  ::::::::  
echo ::::::         :::::::    :::::     :            ::          ::    ::::::  

ECHO ---------------------------------------------------------------------------
::FORCE XBMC TO CLOSE
::tasklist /fi "Imagename eq XBMC.exe"
ECHO Closing XBMC ...
TaskKill /IM:XBMC.exe /F

::XBMC CHANGE %CD% FROM BAT TO XBMC ROOT FOLDER.
SET xbmcPath=%CD%
IF NOT EXIST "%xbmcPath%\XBMC.exe" (
    SET xbmcPath=C:\Program Files\XBMC
)

ECHO ---------------------------------------------------------------------------
ECHO Starting XBMC ...
:: SLEEP 7 SECONDS
PING -n 7 localhost > NUL
:: START XBMC
START /D"%xbmcPath%" XBMC.exe

::PAUSE > NUL