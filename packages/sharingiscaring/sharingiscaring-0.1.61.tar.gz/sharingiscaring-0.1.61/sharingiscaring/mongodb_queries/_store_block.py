import pymongo
from dateutil.parser import isoparse
from ..transaction import Transaction
from sharingiscaring.block import ConcordiumBlockInfo, ConcordiumBlock
from sharingiscaring.transaction import ClassificationResult
import datetime as dt
# from sharingiscaring.client import ConcordiumClient

class Mixin:
    def store_block_in_mongodb(self, block: ConcordiumBlock, client):
        if not isinstance(block.blockInfo.blockArriveTime, dt.datetime):
            block.blockInfo.blockArriveTime    = isoparse(block.blockInfo.blockArriveTime)
        if not isinstance(block.blockInfo.blockReceiveTime, dt.datetime):
            block.blockInfo.blockReceiveTime   = isoparse(block.blockInfo.blockReceiveTime)
        if not isinstance(block.blockInfo.blockSlotTime, dt.datetime):
            block.blockInfo.blockSlotTime      = isoparse(block.blockInfo.blockSlotTime)
        
        summary = block.blockSummary
        try:
            summary.updates['chainParameters']['microGTUPerEuro']['numerator'] = str(summary.updates['chainParameters']['microGTUPerEuro']['numerator'])
        except:
            pass
                
        for k, v in summary.updates.items():
            try:
                summary[k] = isoparse(v)
            except Exception:
                pass

        for item in summary.specialEvents:
            for k, v in item.items():
                try:
                    summary[k] = isoparse(v)
                except Exception:
                    pass

        mongo_block = {'blockHeight': block.blockInfo.blockHeight, '_id': block.blockInfo.blockHash, 'blockInfo': block.blockInfo, 'blockSummary': summary}
        try:
            self.mongodb.collection_blocks.insert_one(mongo_block)
        except Exception as e:
            # console.log(e)
            pass

        transactions = summary.transactionSummaries
        for tx in transactions:
            tx['blockInfo'] = block.blockInfo
            tx['_id'] = tx['hash']

        if len(transactions) > 0:
            try:
                self.mongodb.collection_transactions.insert_many(transactions)
            except:
                pass

        # finally, store account_tx_link if needed

        for tx in transactions:
            classificationResult, _ = Transaction(client).init_from_node(tx).classify_transaction_for_bot()
            if classificationResult.sender and classificationResult.receiver:
                self.store_account_tx_link(tx, classificationResult)


    def store_account_tx_link(self, tx, classificationResult: ClassificationResult):
        
        dct = {
            "tx_hash":  classificationResult.txHash,
            "sender":   classificationResult.sender,
            "receiver": classificationResult.receiver,
            "amount":   classificationResult.amount,
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