from ntn import db

class OUI_MAL(db.Model):
    __tablename__ = "OUI_MAL"

    '''
        MA-L large or traditional sized OUIs are 24-bits in length
    '''

    assignment = db.Column(db.CHAR(6), primary_key=True)
    organization = db.Column(db.String)
    organization_address = db.Column(db.String)


class OUI_MAM(db.Model):
    __tablename__ = "OUI_MAM"

    '''
        MA-M (medium) 28-bit prefix in length
    '''

    assignment = db.Column(db.CHAR(7), primary_key=True)
    organization = db.Column(db.String)
    organization_address = db.Column(db.String)


class OUI_MAS(db.Model):
    __tablename__ = "OUI_MAS"

    '''
        MA-S (small) 36-bit prefix
    '''

    assignment = db.Column(db.CHAR(8), primary_key=True)
    organization = db.Column(db.String)
    organization_address = db.Column(db.String)


db.create_all()