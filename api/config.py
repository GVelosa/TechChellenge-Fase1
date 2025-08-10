import os

basedir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.dirname(basedir)
data_dir = os.path.join(project_root, 'data')

os.makedirs(data_dir, exist_ok=True)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(data_dir, 'books.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False