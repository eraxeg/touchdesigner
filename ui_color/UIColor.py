"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""
import json
import os
from TDStoreTools import StorageManager
import TDFunctions as TDF

import pprint
class UIColor:
	"""
	UIColors description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

		c = self.ownerComp
		for page in c.customPages:
			page.destroy()
		io_page = c.appendCustomPage('Save/Load')
		path = io_page.appendFile('Path')
		path.default = os.path.normpath(os.path.join(project.folder, 'colors.json'))
		path.val = path.default
		save = io_page.appendPulse('Save')
		load = io_page.appendPulse('Load')
		load.enableExpr = 'mod.os.path.isfile(me.par.Path.val)'
		for base in c.findChildren(type=baseCOMP):
			base.destroy()

		color_dict = {color: ui.colors[color] for color in ui.colors}

		nested_dict = {}
		for key, value in sorted(color_dict.items()):
			keys = key.split('.')
			insert(nested_dict, keys, value)

		nodeWidth = 160
		nodeHeight = 130
		spacing = 20
		columns = 10  # Number of columns in the grid

		nodes_list = []
		current_column = 0
		current_row = 0

		for key in sorted(nested_dict.items()):
			newOpr = c.create(baseCOMP, key[0])
			nodes_list.append(newOpr)
			
			newOpr.nodeX = current_column * (nodeWidth + spacing)
			newOpr.nodeY = -current_row * (nodeHeight + spacing)  # Negative Y for grid going downward
			
			# Move to the next column, reset to new row if we've filled the current row
			current_column += 1
			if current_column >= columns:
				current_column = 0
				current_row += 1

			first_page = newOpr.appendCustomPage(key[0])
			newOpr.currentPage = first_page
			
			if type(key[1]) == tuple:
				parname = f'{key[0]}'.capitalize()
				par = first_page.appendRGB(parname, label=f'{key[0]}')
				par.val = key[1]
			else:
				flattened = flatten_dict(key[1])
				for item in flattened.items():
					parname = f"{item[0].replace('.', '')}".capitalize()
					par = first_page.appendRGB(parname, label=f'{key[0]}.{item[0]}')
					par.val = item[1]

			# Continue to the next item in the loop
			continue

	def Save(self):
		with open(self.ownerComp.par.Path.val, 'w') as f:
			f.write(json.dumps({color: ui.colors[color] for color in ui.colors}, indent=2))
		ui.messageBox('Saved', f'Saved {self.ownerComp.par.Path.val}')

		return
	
	def Load(self):
		with open(self.ownerComp.par.Path.val, 'r') as f:
			for key, value in json.loads(f.read()).items():
				ui.colors[key] = value
		return
	
	def OnPulse(self, par):
		if par.name == 'Save':
			self.Save()
		elif par.name == 'Load':
			self.Load()

		

def insert(d, keys, value):
	"""Recursively insert value into nested dictionary based on keys."""
	if len(keys) == 1:
		d[keys[0]] = value
	else:
		if keys[0] not in d or not isinstance(d[keys[0]], dict):
			d[keys[0]] = {}
		insert(d[keys[0]], keys[1:], value)

from collections.abc import MutableMapping

def flatten_dict(d: MutableMapping, parent_key: str = '', sep: str ='.') -> MutableMapping:
	items = []
	for k, v in d.items():
		new_key = parent_key + sep + k if parent_key else k
		if isinstance(v, MutableMapping):
			items.extend(flatten_dict(v, new_key, sep=sep).items())
		else:
			items.append((new_key, v))
	return dict(items)
