from odoo import models, api, _
from odoo.exceptions import UserError
import io
import base64
import xlsxwriter
import logging

_logger = logging.getLogger(__name__)

class SaleReport(models.Model):
    _inherit = "sale.report"

    @api.model
    def export_to_excel(self):
        # Obtener los registros seleccionados
        active_ids = self.env.context.get('active_ids', [])
        records = self.env['sale.report'].browse(active_ids)
    
        # Crear un archivo Excel en memoria
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    
        # Hoja de datos
        data_sheet = workbook.add_worksheet("Datos")
        headers = ["Sucursal", "Categoria", "Producto", "Cantidad", "Neto", "Total"]
        for col_num, header in enumerate(headers):
            data_sheet.write(0, col_num, header)
    
        # Agregar los datos base
        for row_num, record in enumerate(records, start=1):
            data_sheet.write(row_num, 0, record.company_id.name or '')
            data_sheet.write(row_num, 1, record.product_id.categ_id.name or '')
            data_sheet.write(row_num, 2, record.product_id.display_name or '')
            data_sheet.write(row_num, 3, record.product_uom_qty or 0)
            data_sheet.write(row_num, 4, record.price_subtotal or 0.0)
            data_sheet.write(row_num, 5, record.price_total or 0.0)
    
        # Hoja para la tabla dinámica
        pivot_sheet = workbook.add_worksheet("Tabla Dinámica")
    
        # Configurar el rango de datos para la tabla dinámica
        pivot_data_range = f"'Datos'!A1:F{len(records) + 1}"
    
        # Crear la tabla dinámica
        pivot_table = {
            'data': pivot_data_range,
            'row_fields': [{'name': 'Sucursal'}, {'name': 'Categoria'}, {'name': 'Producto'}],
            'data_fields': [
                {'name': 'Cantidad', 'function': 'sum'},
                {'name': 'Neto', 'function': 'sum'},
                {'name': 'Total', 'function': 'sum'}
            ],
        }
        workbook.add_pivot_table(f"'Tabla Dinámica'!A1", pivot_table)
    
        # Cerrar el workbook
        workbook.close()
        output.seek(0)
    
        # Codificar el archivo para guardarlo como adjunto
        file_content_base64 = base64.b64encode(output.getvalue()).decode('utf-8')
        output.close()
    
        # Crear un adjunto en Odoo
        attachment = self.env['ir.attachment'].create({
            'name': "Reporte_Ventas_Tabla_Dinamica.xlsx",
            'type': 'binary',
            'datas': file_content_base64,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })
    
        # Retornar la acción para descargar el archivo
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }
