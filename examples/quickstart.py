from pydantic import SecretStr

from metatrader5_wrapper import LoginCredential, MetaTrader5Client

creds = LoginCredential(login=12345678, password=SecretStr("your-password"), server="Broker-Demo")

with MetaTrader5Client() as client:
    init_result = client.initialize(creds)
    if not init_result.success:
        print("initialize failed:", init_result.error_code, init_result.error_message)
        raise SystemExit(1)

    login_result = client.login(creds)
    if not login_result.success:
        print("login failed:", login_result.error_code, login_result.error_message)
        raise SystemExit(1)

    positions_result = client.positions()
    print(positions_result)
