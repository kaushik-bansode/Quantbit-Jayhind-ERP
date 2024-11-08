// Copyright (c) 2024, Quantbit Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Quotation Sheet", {
	dia_master:async function(frm) {
        if(frm.doc.dia_master){
            const dimensions = (await frappe.db.get_value("Dia Master", frm.doc.dia_master,["length_in_mm","breadth_in_mm","height_in_mm","inner_diameter_in_mm","outer_diameter_in_mm"])).message;
            frm.doc.length = dimensions.length_in_mm;
            frm.doc.breadth = dimensions.breadth_in_mm;
            frm.doc.height = dimensions.height_in_mm;
            frm.doc.inner_diameter = dimensions.inner_diameter_in_mm;
            frm.doc.outer_diameter = dimensions.outer_diameter_in_mm;
            frm.refresh_fields();           
        }
	},
});
