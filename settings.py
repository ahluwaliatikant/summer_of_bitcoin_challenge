MAX_WEIGHT = 4000000

INPUT_FILE = 'mempool.csv'
OUTPUT_FILE = 'block.txt'

dummy_transactions = [
        {
            'txid': '2e3da8fbc1eaca8ed9b7c2db9e6545d8ccac3c67deadee95db050e41c1eedfc0',
            'fee': 452,
            'weight': 110,
            'parents': ['2e3da8fbc1eaca8ed9b7c2db9e6545d8ccac3c67deadee95db050e41c1eedfc1', '2e3da8fbc1eaca8ed9b7c2db9e6545d8ccac3c67deadee95db050e41c1eedfc2']
        },
        {
            'txid': '2e3da8fbc1eaca8ed9b7c2db9e6545d8ccac3c67deadee95db050e41c1eedfc1',
            'fee': 453,
            'weight': 1150,
            'parents': []
        },
        {
            'txid': '2e3da8fbc1eaca8ed9b7c2db9e6545d8ccac3c67deadee95db050e41c1eedfc2',
            'fee': 454,
            'weight': 190,
            'parents': []
        }
]
