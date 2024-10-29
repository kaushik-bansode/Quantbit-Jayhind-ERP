# Copyright (c) 2024, Quantbit Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import math


class QuotationSheet(Document):
	def before_save(self):
		self.calculate_quotation_cost()
  
	def calculate_quotation_cost(self):
     
		if self.shape == "Circle":
			volume = math.pi * self.height * ((self.outer_diameter / 2) ** 2 - (self.inner_diameter / 2) ** 2)
			self.weight = (self.density * volume) / 1000
			machining_cost = sum(i.machine_cost or 0 for i in self.get("operation_details"))
			self.cost = (self.raw_item_rate * self.weight) + machining_cost
		
		elif self.shape == "Rectangle":
			volume = self.length * self.breadth * self.height
			self.weight = (self.density * volume) / 1000
			machining_cost = sum(i.machine_cost or 0 for i in self.get("operation_details"))
			self.cost = (self.raw_item_rate * self.weight) + machining_cost
			
		
