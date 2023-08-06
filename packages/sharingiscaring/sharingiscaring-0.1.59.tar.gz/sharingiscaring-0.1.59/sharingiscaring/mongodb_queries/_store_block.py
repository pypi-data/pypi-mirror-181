import pymongo
from dateutil.parser import isoparse
from ..transaction import Transaction
# from sharingiscaring.client import ConcordiumClient

class Mixin:
    def store_block_in_mongodb(self, block):
        info = block['blockInfo']
        for k, v in info.items():
            try:
                info[k] = isoparse(v)
            except Exception:
                pass
        summary = block['blockSummary']
        try:
            summary['updates']['chainParameters']['microGTUPerEuro']['numerator'] = str(summary['updates']['chainParameters']['microGTUPerEuro']['numerator'])
        except:
            pass
                
        for k, v in summary.items():
            try:
                summary[k] = isoparse(v)
            except Exception:
                pass

        mongo_block = {'blockHeight': info['blockHeight'], '_id': info['blockHash'], 'blockInfo': info, 'blockSummary': summary}
        try:
            self.mongodb.collection_blocks.insert_one(mongo_block)
        except Exception as e:
            # console.log(e)
            pass

        transactions = summary.get('transactionSummaries', [])
        for tx in transactions:
            tx['blockInfo'] = info
            tx['_id'] = tx['hash']

        if len(transactions) > 0:
            try:
                self.mongodb.collection_transactions.insert_many(transactions)
            except:
                pass

    def store_account_tx_link(self, tx, classificationResult):
        
        dct = {
            "tx_hash": classificationResult.txHash,
            "sender": classificationResult.sender,
            "receiver": classificationResult.receiver,
            "amount": classificationResult.amount,
            "blockHeight": tx['blockInfo']['blockHeight']
        }
        try:
            self.collection_accounts_involved.insert_one(dct)
        except Exception as e:
            print (e)

    def search_tx_higher_than_block_height(self, block_height_start, block_height_end):
        pipeline = [
            { '$match':     { 'blockInfo.blockHeight': { '$gt': block_height_start } } },
            { '$match':     { 'blockInfo.blockHeight': { '$lt': block_height_end } } },
            
            {'$project': { 
                '_id': 1
                }
            }
        ]

        return pipeline