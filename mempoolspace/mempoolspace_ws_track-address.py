# https://mempool.space/docs/api/websocket
#
# To solve the error:
#
# [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate
#
# run from finder: ~/Python 3.10/Install Certificates.command
#

import websocket
import _thread
import time
import rel
import json

rel.safe_read()


def on_message(ws, message):
    print(json.loads(message))


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    message = {"action": "init"}
    ws.send(json.dumps(message))
    message = { 'track-address': 'bc1qp7s43q92tg7d8s84ch938ywyxc848a6l6xj30n' }
    ws.send(json.dumps(message))


if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://mempool.space/api/v1/ws",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
