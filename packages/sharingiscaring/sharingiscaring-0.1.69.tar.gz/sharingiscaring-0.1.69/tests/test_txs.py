import pytest
from pathlib import Path
import json
from unittest.mock import Mock
from sharingiscaring.transaction import Transaction
from sharingiscaring.client import ConcordiumClient
from sharingiscaring.tooter import Tooter
from sharingiscaring.cns import CNSActions

# @pytest.fixture
# def tooter():
#     return Tooter('','','','','')


@pytest.fixture
def node():
    return ConcordiumClient(Tooter('','','','',''))

def read_block_information(blockHeight):
    p = Path('tests')
    
    with open(p / 'blocks' / f'{blockHeight}' / 'blockInfo', 'r') as f:   
            blockInfo = json.load(f)
    with open(p / 'blocks' / f'{blockHeight}' / 'blockSummary', 'r') as f:    
            blockSummary = json.load(f)
    
    block = {'blockInfo': blockInfo, 'blockSummary': blockSummary}
    return block

def get_tx_at_index(node, blockHeight, index):
    block = read_block_information (blockHeight)
    if 'transactionSummaries' in block['blockSummary']:
        tx_by_index = {x['index']: x for x in  block['blockSummary']['transactionSummaries']}
        tx_at_index = tx_by_index[index]
        tx_at_index.update({'blockInfo': block['blockInfo']})
        return Transaction(node).init_from_node(tx_at_index)
    else:
        return None

def test_tx():
    block = read_block_information (3639756)
    assert block['blockInfo']['blockHeight'] == 3639756

def test_tx_cns_registration(node: ConcordiumClient):
    tx = get_tx_at_index(node, 4018850, 8)
    
    assert tx.cns_domain.domain_name == "99.ccd"
    assert tx.cns_domain.action == CNSActions.register

def test_tx_transfers(node: ConcordiumClient):
    tx = get_tx_at_index(node, 2826981, 0)
    
    assert tx.type == 'accountTransaction'
    assert tx.contents == 'transfer'
    assert tx.result['outcome'] == 'success'

def test_tx_transfer(node: ConcordiumClient):
    tx = get_tx_at_index(node, 1992437, 1)
    
    assert tx.type == 'accountTransaction'
    assert tx.contents == 'transferWithSchedule'
    assert tx.result['outcome'] == 'success'

def test_tx_delegation_decreased(node: ConcordiumClient):
    tx = get_tx_at_index(node, 3255576, 2)
    
    assert tx.type == 'accountTransaction'
    assert tx.contents == 'configureDelegation'
    assert tx.result['outcome'] == 'success'
    
    delegationResult = tx.classify_transaction_for_bot_for_delegation_and_staking()
    assert delegationResult.txHash == 'e02251ca6e4ceda0aaae0c24396418a8965dc0ff626294bae0c9bf188862b669'
    assert delegationResult.bakerId == 77032
    assert delegationResult.sender == '3g8HevPoKN7aKX8Qg2DqGPrr3m8okw3SiwJFmvmJDk5jZ5hrSs'
    assert delegationResult.message == 'Delegation target set to 77,032. Stake decreased (90.00%) to 1,000 CCD.'

def test_tx_delegation_increased(node: ConcordiumClient):
    tx = get_tx_at_index(node, 4521544, 0)
    
    assert tx.type == 'accountTransaction'
    assert tx.contents == 'configureDelegation'
    assert tx.result['outcome'] == 'success'
    
    delegationResult = tx.classify_transaction_for_bot_for_delegation_and_staking()
    assert delegationResult.txHash == '39947f650fb8432992fd9a4ea057b65c5a7deb5cd89e2c40ea3b949c185a7fcb'
    # assert delegationResult.bakerId == 77032
    assert delegationResult.sender == '2xLQhdg9YvS53uDWakiN6njrRsXuAh4BtDMaJc6JzNhrarCM1q'
    assert delegationResult.message == 'Stake increased (112.50%) to 8,500 CCD.'