# Copyright (c) 2024, Quantbit Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import math

class QuotationSheet(Document):
	def before_save(self):
		self.validate_shape_and_state()
		self.calculate_quotation_cost()

	def validate_shape_and_state(self):
		if self.is_machining_required: 
			if not self.operation_details:
				frappe.throw("Operation Details are required when Machining is checked")
			if (self.total_wastage_in_kg or 0) <= 0:
				frappe.throw("Total Wastage in Kg should be greater than 0")
    
	
	def calculate_quotation_cost(self):
		if self.shape == "Circle":
			initial_volume = math.pi * self.height * ((self.outer_diameter / 2) ** 2 - (self.inner_diameter / 2) ** 2)
			adjusted_volume = initial_volume / (1 - (self.shrinkage_factor / 100))
			raw_material_weight = (self.density * adjusted_volume) / 1000 
			self.weight = raw_material_weight + self.total_wastage_in_kg
			self.finished_material_weight_in_kg = (self.density * initial_volume) / 1000 
			machining_cost = sum(i.machine_cost or 0 for i in self.get("operation_details"))
			self.cost = ((self.raw_item_rate or 0) * (self.weight or 0)) + machining_cost
  
		elif self.shape == "Rectangle" and self.is_strip:
			finished_strip_volume = (self.length * 100) * (self.breadth * 100) * (self.height * 100)
			adjusted_volume = (finished_strip_volume + self.total_wastage_in_kg) / (1 - (self.shrinkage_factor / 100))
			raw_material_weight = (self.density * adjusted_volume) / 1000
			self.weight = raw_material_weight + self.total_wastage_in_kg
			self.finished_material_weight_in_kg = (self.density * finished_strip_volume) / 1000
			machining_cost = sum(i.machine_cost or 0 for i in self.get("operation_details"))
			self.cost = ((self.raw_item_rate or 0) * (self.weight or 0)) + machining_cost

		elif self.shape == "Rectangle":
			initial_volume = self.length * self.breadth * self.height
			adjusted_volume = initial_volume / (1 - (self.shrinkage_factor / 100))
			raw_material_weight = (self.density * adjusted_volume) / 1000 
			self.weight = raw_material_weight + self.total_wastage_in_kg
			self.finished_material_weight_in_kg = (self.density * initial_volume) / 1000 
			machining_cost = sum(i.machine_cost or 0 for i in self.get("operation_details"))
			self.cost = ((self.raw_item_rate or 0) * (self.weight or 0)) + machining_cost
