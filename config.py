import pymysql
pymysql.install_as_MySQLdb()

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Gayathri%40123@localhost:3306/igniteher'
    SQLALCHEMY_TRACK_MODIFICATIONS = False