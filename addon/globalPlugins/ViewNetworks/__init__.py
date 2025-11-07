# -*- coding: UTF-8 -*-

"""
Author: Edilberto Fonseca <edilberto.fonseca@outlook.com>
Copyright: (C) 2025 Edilberto Fonseca

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html

Created on: 07/08/2022
"""

import addonHandler
import globalPluginHandler
import gui
import wx
from logHandler import log
from scriptHandler import script

# imports from the View Networks addon.
from .networks import ViewNetworks
from .password import ViewPassword

# Config# Get the add-on summary contained in the manifest.
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

# Initialize translation support
addonHandler.initTranslation()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		self.create_menu()

	def create_menu(self):
		self.mainMenu = wx.Menu()
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu

		# Translators: Lists the profiles in the Wireless Network Connection interface.
		networck = self.mainMenu.Append(-1, _("&Network Profiles"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_networks, networck)

		# Translators: Search the networks and try to recover the password.
		recoverPassword = self.mainMenu.Append(-1, _("&Recover Password"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_recoverPassword, recoverPassword)

		# Translators: Creates the item in the NVDA menu.
		self.menuItem = self.toolsMenu.AppendSubMenu(self.mainMenu, "&{}...".format(ADDON_SUMMARY))

	@script(
		gesture="kb:Windows+alt+N",
		description=_("Displays the networks you have connected to."),
		category=ADDON_SUMMARY,
	)
	def script_networks(self, gesture):
		# Translators: title of the profiles dialog in the Wireless Network Connection interface.
		self.dlg = ViewNetworks(gui.mainFrame, _("Network Profiles"))
		gui.mainFrame.prePopup()
		self.dlg.Show()
		self.dlg.Centre()
		gui.mainFrame.postPopup()

	@script(
		gesture="kb:Windows+alt+P",
		description=_("Recover saved networks password."),
		category=ADDON_SUMMARY,
	)
	def script_recoverPassword(self, gesture):
		# Translators: Title of the Recover Password dialog.
		self.dlg = ViewPassword(gui.mainFrame, _("Recover Password."))
		gui.mainFrame.prePopup()
		self.dlg.Show()
		self.dlg.Centre()
		gui.mainFrame.postPopup()

	def terminate(self):
		try:
			self.toolsMenu.Remove(self.menuItem)
		except Exception as e:
			log.warning(f"Error removing Scraps and agenda organizer menu item: {e}")
