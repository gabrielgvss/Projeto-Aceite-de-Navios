import os

SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URL = 'postgresql://gabrielgvss:J6dMk7FRlZry@ep-summer-mud-a5yjjyfw.us-east-2.aws.neon.tech/DB_SANA?sslmode=require'

SQLALCHEMY_TRACK_MODIFICATIONS = False
