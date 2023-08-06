import requests
from rich.console import Console
console = Console()

class Mixin:
    def ql_request_tx_from_hash(self, txHash: str):
        query = "query {"
        query += f'transactionByTransactionHash(transactionHash: "{txHash}")'
        query += '{'

        query += self.standard_tx_fields()
        query += self.ql_query_tx_events()
        
        query += '}'
        try:
            r = requests.post(self.graphql_url, json={'query': query})
            if r.status_code == 200:
                return r.json()['data']['transactionByTransactionHash']
       
        except Exception as e:
            console.log(query, e)
            return None