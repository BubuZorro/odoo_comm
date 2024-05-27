from odoo import models, fields
from lxml import etree
import base64

class TimesheetXmlReport(models.Model):
    _name = 'timesheet.xml.report'
    _description = 'Timesheet XML converter'

    reporter_ids = fields.Many2many('res.users', string='Reporter', default=lambda self: self.env.user)
    date_report_start = fields.Datetime('Start of the time frame')
    date_report_end = fields.Datetime('End of the time frame')
    employee_ids = fields.Many2many('hr.employee', string='List of Employees in the Report')            # Lista degli employees nel singolo report


    def export_xml_report(self):
        """
        Create the XML report as Zucchetti's standard
        Example:
        <Fornitura>
            <Dipendente CodAziendaUfficiale="000001" CodDipendenteUfficiale="0000003" >
                <Movimenti GenerazioneAutomaticaDaTeorico="N">
                    <Movimento>
                        ...
                    </Movimento>
                    <Movimento>
                        ...
                    </Movimento>
                </Movimenti>
            </Dipendente>
            <Dipendente CodAziendaUfficiale="000001" CodDipendenteUfficiale="0000012" >
                <Movimenti GenerazioneAutomaticaDaTeorico="N">
                    <Movimento>
                        ...
                    </Movimento>
                    <Movimento>
                        ...
                    </Movimento>
                </Movimenti>
            </Dipendente>
        </Fornitura>
        """
        for record in self:
            xml_data = etree.Element("Fornitura")

            for employee in self.employee_ids:
                employee_code = f"{int(employee.internal_code):07}"             # Per aver sempre il formato 0000001 lungo 7 caratteri
                employee_element = etree.SubElement(xml_data, "Dipendente", CodAziendaUfficiale="000001", CodDipendenteUfficiale=str(employee_code))
                movements_info_element = etree.SubElement(employee_element, "Movimenti", GenerazioneAutomaticaDaTeorico="N")
                self.get_timesheet_info(employee.id, movements_info_element)

            xml_string = etree.tostring(xml_data, pretty_print=True, encoding="UTF-8", xml_declaration=False)

            current_user = self.env.user
            if current_user not in record.reporter_ids:
                record.reporter_ids = [(4, current_user.id)]

            return [record.id, xml_string]

    def get_timesheet_info(self, employee_id, movements_info_element):
        """
        Gets the complete info for a employee
        Writes all timesheet lines converted to XML format
        Example:
        <Movimento>
            <CodGiustificativoRilPres>ORD</CodGiustificativoRilPres>
            <CodGiustificativoUfficiale>01</CodGiustificativoUfficiale>
            <Data>2024-03-01</Data>
            <NumOre>8</NumOre>
            <NumMinuti>00</NumMinuti>
            <NumMinutiInCentesimi>00</NumMinutiInCentesimi>
            <GiornoDiRiposo>N</GiornoDiRiposo>
            <GiornoChiusuraStraordinari>N</GiornoChiusuraStraordinari>
        </Movimento>
        """
        for record in self:
            employee_hours_list = self.env['account.analytic.line'].search([
                        ('date', '>=', record.date_report_start),
                        ('date', '<=', record.date_report_end),
                        ('employee_id', '=', employee_id)
                        ])

            for line in employee_hours_list:
                single_timesheet_element = etree.SubElement(movements_info_element, "Movimento")

                rilpres_code_info_element = etree.SubElement(single_timesheet_element, "CodGiustificativoRilPres")
                rilpres_code_info_element.text = 'ORD'                  # ORD messo di default
                official_code_info_element = etree.SubElement(single_timesheet_element, "CodGiustificativoUfficiale")
                official_code_info_element.text = str(line.task_id.id)   #task_id è project.task
                data_info_element = etree.SubElement(single_timesheet_element, "Data")
                data_info_element.text = str(line.date)

                time_total = line.unit_amount
                minutes = int(time_total % 60)
                seconds = int((time_total % 1) * 60)
                cents = '00'                               # TODO implementare centesimi di secondo in caso improbabile serva

                hours_info_element = etree.SubElement(single_timesheet_element, "NumOre")
                hours_info_element.text = str(minutes)
                minutes_info_element = etree.SubElement(single_timesheet_element, "NumMinuti")
                minutes_info_element.text = str(seconds)
                cents_info_element = etree.SubElement(single_timesheet_element, "NumMinutiInCentesimi")
                cents_info_element.text = str(cents)

                rest_info_element = etree.SubElement(single_timesheet_element, "GiornoDiRiposo")
                rest_info_element.text = 'N'                            # N messo di default
                closure_info_element = etree.SubElement(single_timesheet_element, "GiornoChiusuraStraordinari")
                closure_info_element.text = 'N'                         # N messo di default

        return True

    def download_xml_report(self):
        """
        Allows to download the XML report
        """

        xml_data = self.export_xml_report()
        report_id = xml_data[0]
        xml_string = xml_data[1]

        # Encode the XML string to base64
        encoded_xml = base64.b64encode(xml_string)

        # get base url
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        attachment_obj = self.env['ir.attachment']

        # create attachment
        filename = f"timesheet_report_{report_id}.xml"
        attachment_id = attachment_obj.create(
            {'name': filename,
             'datas': encoded_xml,
             #'datas_fname': filename
             })

        # prepare download url
        download_url = '/web/content/' + str(attachment_id.id) + '?download=true'

        # download
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }
