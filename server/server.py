#!/usr/bin/env python

import os, sys, argparse
sys.path.insert(0, os.path.abspath(".."))
from server.mockDataGenerator import Point

import asyncio
import websockets
from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer

from libraries.get_robot_position import *

point_list = []

count = 1


async def mocked_producer():
    while True:
        sleep(0.01)
        global point_list, count

        for i, p in enumerate(point_list):
            if count % 800 == 0:
                point_list[i] = p.set_random()
            else:
                point_list[i] = p.next()

        count += 1
        str_array = []

        for points in point_list:
            str_array.append(json.loads(points.get_json()))

        print(json.dumps(str_array))
        return json.dumps(str_array)


async def real_producer():
    while True:
        try:
            x = get_robot_position(0, camera)

            if x:
                print(x)
                return x

        except RuntimeError as e:
            print(e)
            pass


producer_name = real_producer


async def consumer(message):
    print(message)


async def handler(websocket, path):
    while True:
        listener_task = asyncio.ensure_future(websocket.recv())
        producer_task = asyncio.ensure_future(producer_name())
        done, pending = await asyncio.wait(
            [listener_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED)
        try:
            if listener_task in done:
                message = listener_task.result()
                await consumer(message)
            else:
                listener_task.cancel()

            if producer_task in done:
                message = producer_task.result()
                await websocket.send(message)
            else:
                producer_task.cancel()
        except websockets.exceptions.ConnectionClosed as error:
            # print(error)
            producer_task.cancel()
            listener_task.cancel()
            break

# Classic HTTP requests server, not in use currently
# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    def fetch_meta(self):
        ### Taille de la grille par rapport au robot
        self.send_response(200)
        message = '{"grid-size" : 1000}'
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))
        return

    # GET
    def do_GET(self):

        if self.path == "/meta":
            self.fetch_meta()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            return


def run_server():
    print('starting server...')
    server_address = ('localhost', 8765)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


def get_mode():
    parser = argparse.ArgumentParser(description='Switch between mocked and real data')
    parser.add_argument('-m', '--mockedData', help='Switch to mocked data mode', action='store_true')
    parser.add_argument('-n', '--robotNumber', help='Choose number of robots to display. Default value 1')
    args = parser.parse_args()
    robot_number = 1
    if args.robotNumber:
        robot_number = int(args.robotNumber)
    if args.mockedData:
        return robot_number
    return False


def main():
    global producer_name
    global point_list
    mode_nb = get_mode()

    if mode_nb:
        for x in range(mode_nb):
            point_list.append(Point().set_random())
        producer_name = mocked_producer
    else:
        print("Contacting camera.. ")
        global camera
        camera = contact_camera()

    print("Starting webservice..")
    start_server = websockets.serve(handler, 'localhost', 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
