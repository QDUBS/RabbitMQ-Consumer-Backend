import sys
import os
import ssl
import odoorpc
from dotenv import load_dotenv, find_dotenv
from pprint import pprint as pp

ssl._create_default_https_context = ssl._create_unverified_context
load_dotenv()


def connect():
    try:
        odoo = odoorpc.ODOO(host=os.environ.get('ODOO_HOST'), protocol=os.environ.get(
            'ODOO_PROTOCOL'), port=os.environ.get('ODOO_PORT'))
        odoo.login(os.environ.get('ODOO_DATABASE'), os.environ.get(
            'ODOO_USERNAME'), os.environ.get('ODOO_PASSWORD'))
        return odoo
    except odoorpc.error.RPCError as exc:
        pp(exc.info)


api = connect()
