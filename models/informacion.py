# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class informacion(models.Model):
    _name = 'odoo_basico.informacion'
    _description = 'odoo_basico.informacion'
    _sql_constraints = [('nomeUnico', 'unique(name)', 'Non se pode repetir o nome')]
    _order = "descripcion desc"

    name = fields.Char(required=True, size=20, string="Titulo:")
    descripcion = fields.Text(string="A descripción:")
    sexo_traducido = fields.Selection([('Hombre', 'Home'), ('Mujer', 'Muller'), ('Otros', 'Outros')], required=True, string="Sexo")
    alto_en_cms = fields.Integer(string="Alto en centimetros:")
    longo_en_cms = fields.Integer(string="Longo en centimetros:")
    ancho_en_cms = fields.Integer(string="Ancho en centimetros:")
    volume = fields.Float(digits=(6, 7), compute="_volume", store=True, string="Volume (m3):")
    peso = fields.Float(digits=(6, 2), string="Peso en Kg.s", default=2.7)
    densidade = fields.Float(compute="_densidade", store=True, string="Densidade (m3):")
    literal = fields.Char(store=False)
    autorizado = fields.Boolean(default=True, string="¿Autorizado?")

    @api.depends('alto_en_cms', 'longo_en_cms', 'ancho_en_cms')
    def _volume(self):
        for rexistro in self:
            rexistro.volume = (float(rexistro.alto_en_cms) * float(rexistro.longo_en_cms) * float(rexistro.ancho_en_cms)) / 1000000

    @api.depends('volume', 'peso')
    def _densidade(self):
        for rexistro in self:
            if rexistro.volume != 0:

                rexistro.densidade = (float(rexistro.peso) / float(rexistro.volume))

            else:

                rexistro.densidade = 0


    @api.onchange('alto_en_cms')
    def _avisoAlto(self):
        for rexistro in self:
            if rexistro.alto_en_cms > 7:
                rexistro.literal = 'O alto ten un valor posiblemente excesivo %s é maior que 7' % rexistro.alto_en_cms
            else:
                rexistro.literal = ""

    @api.constrains('peso')  # Ao usar ValidationError temos que importar a libreria ValidationError
    def _constrain_peso(self):  # from odoo.exceptions import ValidationError
        for rexistro in self:
            if rexistro.peso < 1 or rexistro.peso > 4:
                raise ValidationError('Os peso de %s ten que ser entre 1 e 4 ' % rexistro.name)