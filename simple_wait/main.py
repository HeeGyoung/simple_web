import json

import pika
import memcache
import requests as requests

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from constants import (
    MEMCACHE_HOST, Q_VIRTUAL_HOST, Q_EXCHANGE, Q_URL, Q_USER,
    Q_PASS, Q_NAME, API_URL, REDIRECT_URL, WEB_STAT_AUTH,
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates/")
memcached_client = memcache.Client([(MEMCACHE_HOST, 11211)])


def get_connection():
    credential = pika.PlainCredentials(Q_USER, Q_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            virtual_host=Q_VIRTUAL_HOST, credentials=credential
        )
    )
    return connection


def send_message(connection, id, message):
    property = pika.spec.BasicProperties(message_id=id)
    channel = connection.channel()
    channel.basic_publish(
        exchange=Q_EXCHANGE, routing_key=Q_PASS,
        body=message, properties=property
    )
    channel.close()


def set_id(id, message):
    memcached_client.add(key=id, val=message, time=60*60*1)


def get_id(id):
    return memcached_client.get(key=id)


def del_id(id):
    memcached_client.delete(key=id)


def get_web_status():
    r = requests.get(f"{API_URL}/stats;csv;norefresh", auth=WEB_STAT_AUTH)
    r.close()
    csv = [line for line in r.text.strip(' #').split('\n') if line]
    fields = [f for f in csv.pop(0).split(',') if f]

    length = len(fields)
    result = {}
    for values in csv:
        line = [f for f in values.split(',')]
        key = f"{line[0]}-{line[1]}"
        result[key] = {}
        for i in range(2, length):
            result[key][fields[i]] = line[i]
    return result


def get_message(requeue=True):
    q_url = f"{Q_URL}/{Q_VIRTUAL_HOST}/{Q_NAME}"
    r = requests.post(
        f"{q_url}/get",
        auth=(Q_USER, Q_PASS),
        data=json.dumps({"count": 1, "requeue": requeue, "encoding": "auto"}),
        headers={"Content-Type": "application/json"}
    )
    r.close()
    return json.loads(r.content)[0]


@app.get("/del")
def flush_id():
    memcached_client.flush_all()


@app.get("/items/{id}", response_class=HTMLResponse)
def wait_user(request: Request, id: str):
    if not get_id(id):
        conn = get_connection()
        message = f"I'm item {id}"
        send_message(conn, id, message)
        set_id(id, message)

    result = get_web_status()
    server_limit = int(result['http-in-FRONTEND']['slim'])
    scur = int(result['http-in-FRONTEND']['scur'])
    smax = int(result['http-in-FRONTEND']['smax'])
    server_current = scur + smax
    if server_limit > server_current:
        message_info = get_message(True)
        key = message_info["properties"]["message_id"]
        if key == id:
            get_message(False)
            del_id(key)
            return RedirectResponse(f"{REDIRECT_URL}/?id={key}")

    message_info = get_message()
    message_cnt = server_current + message_info["message_count"]
    return templates.TemplateResponse(
        "item.html", {
            "request": request,
            "message": f"Have to wait {message_cnt}. Limit is {server_limit}."
        }
    )
