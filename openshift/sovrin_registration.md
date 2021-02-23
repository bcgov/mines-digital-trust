# Register your Agent on Sovrin

1. Start Agent locally with aca-py command line argument `--read-only-ledger` and `--genesis-url https://raw.githubusercontent.com/sovrin-foundation/sovrin/stable/sovrin/pool_transactions_sandbox_genesis`
    - for Sovrin MainNET use this instead `--genesis-url https://raw.githubusercontent.com/sovrin-foundation/sovrin/stable/sovrin/pool_transactions_live_genesis`
1. GET from local agent at `/wallet/did/public`, note DID and VerKey
1. Register DID and VerKey on Sovrin Ledger with `Endorser` role
    - StagingNET https://selfserve.sovrin.org/ - Set network to StagingNet and ignore Payment Address
    - MainNET,Must be registered manually by DTS Team
1. Restart Agent locally (it will error with `Ledger rejected transaction request`)
    - We must accept the Transaction Author Agreement (TAA) before writing to the ledger
1. GET from local agent at `ledger/taa` to read the TAA.
1. POST to local agent at `ledger/taa/accept` to accept TAA with dictionary as body as follows
```
    {   'text': copy from GET,
        'version': copy from GET,
        'mechanism': select the appropriate AML (Acceptance Mechanism List), use 'at_submission' by default.
    } 
```
1. remove `--read-only-ledger` argument, and start controller to register schema's on ledger
1. restart agent with `--read-only-ledger` argument for the final time. Congrats!

