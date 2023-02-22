"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs,os,sys
import urllib
import re
import time
import zipfile
from math import trunc
from resources.lib.modules import control
from datetime import datetime
from resources.lib.modules.backtothefuture import unicode, PY2

if PY2:
    FancyURLopener = urllib.FancyURLopener
    translatePath = xbmc.translatePath
else:
    FancyURLopener = urllib.request.FancyURLopener
    translatePath = xbmcvfs.translatePath

dp           = xbmcgui.DialogProgress()
dialog       = xbmcgui.Dialog()
addonInfo    = xbmcaddon.Addon().getAddonInfo

AddonTitle="EZ Maintenance Mod"
AddonID ='script.ezmaintenancemod'


def xml_data_advSettings_old(size):
    xml_data="""<advancedsettings>
      <network>
        <curlclienttimeout>10</curlclienttimeout>
        <curllowspeedtime>20</curllowspeedtime>
        <curlretries>2</curlretries>
        <cachemembuffersize>%s</cachemembuffersize>
        <buffermode>2</buffermode>
        <readbufferfactor>20</readbufferfactor>
      </network>
</advancedsettings>""" % size
    return xml_data

def xml_data_advSettings_New(size):
    xml_data="""<advancedsettings>
      <network>
        <curlclienttimeout>10</curlclienttimeout>
        <curllowspeedtime>20</curllowspeedtime>
        <curlretries>2</curlretries>
      </network>
      <cache>
        <memorysize>%s</memorysize>
        <buffermode>2</buffermode>
        <readfactor>20</readfactor>
      </cache>
</advancedsettings>""" % size
    return xml_data

def advancedSettings():
    XML_FILE   =  translatePath(os.path.join('special://home/userdata' , 'advancedsettings.xml'))
    MEM        =  xbmc.getInfoLabel("System.Memory(total)")
    FREEMEM    =  xbmc.getInfoLabel("System.FreeMemory")
    BUFFER_F   =  re.sub('[^0-9]','',FREEMEM)
    BUFFER_F   = int(BUFFER_F) / 3
    BUFFERSIZE = trunc(BUFFER_F * 1024 * 1024)
    try: KODIV        =  float(xbmc.getInfoLabel("System.BuildVersion")[:4])
    except: KODIV = 16


    """,customlabel='Cancel'"""
    choice = dialog.yesno(AddonTitle, 'En fonction de votre mémoire libre, votre taille de tampon optimale est: \n' + str(BUFFERSIZE) + ' Octets' + ' ('  + str(round(BUFFER_F)) + ' MB)' + '\n' + 'Notez que vos paramètres avancés actuels seront écrasés!' + '\n' + 'Choisissez une option ci-dessous ou appuyez sur ESC pour abandonner.', yeslabel='Utilisation optimale',nolabel='Saisir une valeur' )
    if choice == 1:
        with open(XML_FILE, "w") as f:
            if KODIV >= 17: xml_data = xml_data_advSettings_New(str(BUFFERSIZE))
            else: xml_data = xml_data_advSettings_old(str(BUFFERSIZE))

            f.write(xml_data)
            dialog.ok(AddonTitle,'Mémoire tampon réglée à: ' + str(BUFFERSIZE) + '\n' + 'Veuillez redémarrer Kodi pour que les paramètres s\appliquent.')

    elif choice == 0:
        BUFFERSIZE = _get_keyboard( default=str(BUFFERSIZE), heading="Réglage de la mémoire tampon (Octets) ou ESC/Cancel pour annuler", cancel="-")
        if BUFFERSIZE != "-":
            with open(XML_FILE, "w") as f:
                if KODIV >= 17: xml_data = xml_data_advSettings_New(str(BUFFERSIZE))
                else: xml_data = xml_data_advSettings_old(str(BUFFERSIZE))
                f.write(xml_data)
                dialog.ok(AddonTitle,'Taille de la mémoire tampon définie à: ' + str(BUFFERSIZE) + '\n' + 'Veuillez redémarrer Kodi pour que les paramètres s\appliquent.')


def open_Settings():
    open_Settings = xbmcaddon.Addon(id=AddonID).openSettings()

def _get_keyboard( default="", heading="", hidden=False, cancel="" ):
    """ shows a keyboard and returns a value """
    if cancel == "":
        cancel=default
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText())
    return cancel


##############################    END    #########################################