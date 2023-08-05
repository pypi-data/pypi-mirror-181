from viggocore.database import db
from viggocore.common.subsystem import entity


class RegraFiscal(entity.Entity, db.Model):

    attributes = ['domain_org_id', 'cstcofins_id', 'csticms_id', 'cstpis_id',
                  'cfop_id', 'cstipi_id', 'descricao', 'aliq_especifica_icms',
                  'aliq_especifica_icmsst', 'aliq_reducao_base_icms',
                  'aliq_reducao_base_est', 'indice_difal', 'difal_base_dupla',
                  'icms_sob_pis_cofins', 'icms_sob_frete', 'tipo_ipi', 'icms_sob_ipi']
    attributes += entity.Entity.attributes

    domain_org_id = db.Column(
        db.CHAR(32), db.ForeignKey('domain_org.id'), nullable=False)
    cstcofins_id = db.Column(
        db.CHAR(32), db.ForeignKey('cstcofins.id'), nullable=False)
    csticms_id = db.Column(
        db.CHAR(32), db.ForeignKey('csticms.id'), nullable=False)
    cstpis_id = db.Column(
        db.CHAR(32), db.ForeignKey('cstpis.id'), nullable=False)
    cfop_id = db.Column(
        db.CHAR(32), db.ForeignKey('cfop.id'), nullable=False)
    cstipi_id = db.Column(
        db.CHAR(32), db.ForeignKey('cstipi.id'), nullable=True)

    descricao = db.Column(db.String(100), nullable=False)
    aliq_especifica_icms = db.Column(
        db.Numeric(5, 2), nullable=False, default=0, server_default="0")
    aliq_especifica_icmsst = db.Column(
        db.Numeric(5, 2), nullable=False, default=0, server_default="0")
    aliq_reducao_base_icms = db.Column(
        db.Numeric(5, 2), nullable=False, default=0, server_default="0")
    aliq_reducao_base_est = db.Column(
        db.Numeric(5, 2), nullable=False, default=0, server_default="0")
    indice_difal = db.Column(db.Boolean, nullable=False)
    difal_base_dupla = db.Column(db.Boolean, nullable=False)
    icms_sob_pis_cofins = db.Column(db.Boolean, nullable=False)
    icms_sob_frete = db.Column(db.Boolean, nullable=False)
    tipo_ipi = db.Column(db.CHAR(6), nullable=True)
    icms_sob_ipi = db.Column(db.Boolean, nullable=True)

    def __init__(self, id, domain_org_id, cstcofins_id, csticms_id,
                 cfop_id, cstipi_id, descricao, aliq_especifica_icms,
                 aliq_especifica_icmsst, aliq_reducao_base_icms,
                 aliq_reducao_base_est, indice_difal, difal_base_dupla,
                 icms_sob_pis_cofins, icms_sob_frete,  cstpis_id=None, tipo_ipi=None,
                 icms_sob_ipi=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.domain_org_id = domain_org_id
        self.cstcofins_id = cstcofins_id
        self.csticms_id = csticms_id
        self.cfop_id = cfop_id
        self.cstipi_id = cstipi_id
        self.descricao = descricao
        self.aliq_especifica_icms = aliq_especifica_icms
        self.aliq_especifica_icmsst = aliq_especifica_icmsst
        self.aliq_reducao_base_icms = aliq_reducao_base_icms
        self.aliq_reducao_base_est = aliq_reducao_base_est
        self.indice_difal = indice_difal
        self.difal_base_dupla = difal_base_dupla
        self.icms_sob_pis_cofins = icms_sob_pis_cofins
        self.icms_sob_frete = icms_sob_frete
        self.cstpis_id = cstpis_id
        self.tipo_ipi = tipo_ipi
        self.icms_sob_ipi = icms_sob_ipi
    
    def is_stable(self):
        if (self.icms_sob_ipi is True and 
            (self.tipo_ipi is False and self.cstipi_id is False)):
            return False
        return True

    @classmethod
    def individual(cls):
        return 'regra_fiscal'
