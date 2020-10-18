import pytest
import os
import sys
import re
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
os.environ['SENTINEL_ENV'] = 'test'
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../lib')))
import config
from xazab_config import XazabConfig


@pytest.fixture
def xazab_conf(**kwargs):
    defaults = {
        'rpcuser': 'xazabrpc',
        'rpcpassword': 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk',
        'rpcport': 29241,
    }

    # merge kwargs into defaults
    for (key, value) in kwargs.items():
        defaults[key] = value

    conf = """# basic settings
testnet=1 # TESTNET
server=1
rpcuser={rpcuser}
rpcpassword={rpcpassword}
rpcallowip=127.0.0.1
rpcport={rpcport}
""".format(**defaults)

    return conf


def test_get_rpc_creds():
    xazab_config = xazab_conf()
    creds = XazabConfig.get_rpc_creds(xazab_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'xazabrpc'
    assert creds.get('password') == 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk'
    assert creds.get('port') == 29241

    xazab_config = xazab_conf(rpcpassword='s00pers33kr1t', rpcport=8000)
    creds = XazabConfig.get_rpc_creds(xazab_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'xazabrpc'
    assert creds.get('password') == 's00pers33kr1t'
    assert creds.get('port') == 8000

    no_port_specified = re.sub('\nrpcport=.*?\n', '\n', xazab_conf(), re.M)
    creds = XazabConfig.get_rpc_creds(no_port_specified, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'xazabrpc'
    assert creds.get('password') == 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk'
    assert creds.get('port') == 41414


def test_slurp_config_file():
    import tempfile

    xazab_config = """# basic settings
#testnet=1 # TESTNET
server=1
printtoconsole=1
txindex=1 # enable transaction index
"""

    expected_stripped_config = """server=1
printtoconsole=1
txindex=1 # enable transaction index
"""

    with tempfile.NamedTemporaryFile(mode='w') as temp:
        temp.write(xazab_config)
        temp.flush()
        conf = XazabConfig.slurp_config_file(temp.name)
        assert conf == expected_stripped_config
