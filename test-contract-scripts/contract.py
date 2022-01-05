from terra_sdk.client.localterra import LocalTerra
from terra_sdk.util.contract import read_file_as_b64, get_code_id, get_contract_address
from terra_sdk.core.auth import StdFee
from terra_sdk.core.wasm import MsgStoreCode, MsgInstantiateContract

from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.client.lcd import LCDClient

terra = LCDClient("https://bombay-lcd.terra.dev", "bombay-12")

mk = MnemonicKey(mnemonic = "nut mouse enlist brief spin empower coin brother actual unveil ticket diesel traffic quiz useless oil swing artefact tomato tennis topple betray banana gate")

# deployer = lt.wallets["test1"]
deployer = terra.wallet(mk)

def store_contract(contract_name: str, sequence) -> str:
    contract_bytes = read_file_as_b64(f"artifacts/{contract_name}.wasm")
    store_code = MsgStoreCode(
        deployer.key.acc_address,
        contract_bytes
    )

    tx = deployer.create_and_sign_tx(
        msgs = [store_code], fee=StdFee(400000000, "10000000uluna"), sequence=sequence
    )

    result = terra.tx.broadcast(tx)
    code_id = get_code_id(result)

    return code_id

def instantiate_contract(code_id: str, init_msg, sequence) -> str:
    instantiate = MsgInstantiateContract(
        admin=deployer.key.acc_address, sender=deployer.key.acc_address , code_id=code_id, init_msg=init_msg
    )
    tx = deployer.create_and_sign_tx(
        msgs=[instantiate], fee=StdFee(400000000, "10000000uluna"), sequence=sequence
    )
    result = terra.tx.broadcast(tx)
    contract_address = get_contract_address(result)
    # contract_address = result.logs[0].events_by_type[
    #     "instantiate_contract"
    # ]["contract_address"][0]

    print(contract_address)

    return contract_address

# we need to increase the sequence cuz it runs too fast. the sequence overlaps
sequence = terra.auth.account_info(deployer.key.acc_address).sequence

code_id = store_contract("cw20_base", sequence)
contract_address =instantiate_contract(code_id, {"name":"real_token","symbol":"SYMBOL","decimals": 3,"initial_balances":[{"address":"terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v","amount":"10000"},{"address":"terra17lmam6zguazs5q5u6z5mmx76uj63gldnse2pdp","amount":"10000"}]}, sequence+1)
# print(terra.wasm.contract_query(contract_address, {"balance":{"address": "terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v"}}))