frappe.ui.form.on("Quotation Item", {
	custom_quotation_sheet:async function(frm,cdt,cdn) {
        let d = locals[cdt][cdn]
        if(d.custom_quotation_sheet) {  
            d.rate = (await frappe.db.get_value("Quotation Sheet",d.custom_quotation_sheet,"cost")).message.cost
            frm.trigger("rate")
            frm.refresh_fields()

        }
        console.log(d.rate)
	},
  
});