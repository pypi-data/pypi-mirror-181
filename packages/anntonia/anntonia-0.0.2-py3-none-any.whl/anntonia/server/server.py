from anntonia.server.actions import *

import asyncio
import pathlib
import websockets
import bson
import numpy as np
import sys
import io
from PIL import Image


class Server():
    '''Web socket server class that handles communication with the visualizer application.'''
    
    def __init__(self, sync_state):
        self.sync_state = sync_state
        self.functions = {'RequestData': self.HandleDataRequest, 'RequestActions': self.HandleActionsRequest}
        self.send_queue = asyncio.Queue()
        self.actions = []
        
    @property
    def actions(self):
        return self.__actions
        
    @actions.setter
    def actions(self, actions):
        self.__actions = actions
        for action in actions:
            self.functions[action.name] = action.Call

    @property
    def sync_state(self):
        return self.__sync_state

    @sync_state.setter
    def sync_state(self, sync_state):
        self.__sync_state = sync_state
        self.sync_state.dirty
        
    def HandleDataRequest(self, data_request):
        print("Request: " + data_request["request"])
        response = data_request
        response["action"] = "PutData"
        if data_request["request"] == "LayerCount":
            response["LayerCount"] = self.sync_state.GetLayerCount()
        elif data_request["request"] == "LayerSize":
            response["LayerSize"] = self.sync_state.GetLayerSize(data_request["layer_index"])
        elif data_request["request"] == "NodeValues":
            response["NodeValues"] = self.sync_state.layers[data_request["layer_index"]].node_values
        elif data_request["request"] == "NodeCoordinates":
            response["NodeCoordinates"] = self.sync_state.layers[data_request["layer_index"]].node_coordinates
        elif data_request["request"] == "Connections":
            connections = [[x[0], x[1]] for x in self.sync_state.connections.keys()]
            response["Connections"] = connections
        elif data_request["request"] == "LinkValues":
            response["LinkValues"] = self.sync_state.connections[(data_request["layer_index_from"], data_request["layer_index_to"])].link_values
            response["ConnectionType"] = self.sync_state.connections[(data_request["layer_index_from"], data_request["layer_index_to"])].connection_type
            response["VisualizeOnStart"] = self.sync_state.connections[(data_request["layer_index_from"], data_request["layer_index_to"])].visualize_on_start 
            if self.sync_state.connections[(data_request["layer_index_from"], data_request["layer_index_to"])].connection_type != "AD_MATRIX":
                response["Strides"] = self.sync_state.connections[(data_request["layer_index_from"], data_request["layer_index_to"])].stride
                response["SumChannels"] = self.sync_state.connections[(data_request["layer_index_from"], data_request["layer_index_to"])].sum_channels 
        elif data_request["request"] == "NeedsDrawingPad":
            response["NeedsDrawingPad"] = self.sync_state.needs_drawing_pad
        elif data_request["request"] == "NodeMesh":
            response["NodeMesh"] = self.sync_state.layers[data_request["layer_index"]].node_mesh
        else:
            print("Unknown request for " + data_request["request"] + " was ignored.")
            return
        return response
        
    def HandleActionsRequest(self, actions_request):
        response = {}
        response["action"] = "AnnounceActions"
        response["action_list"] = []
        for action in self.actions:
            entry = {}
            entry["name"] = action.name
            if isinstance(action, SimpleAction):
                entry["type"] = "Simple"
            if isinstance(action, FloatAction):
                entry["type"] = "Float"
            if isinstance(action, NodeAction):
                entry["type"] = "Node"
            if isinstance(action, TextureAction):
                entry["type"] = "Texture"
            response["action_list"].append(entry)
        return response
        
    async def Consumer(self, message):
        data = bson.loads(message)
        print("Received action: " + data["action"])
        if data["action"] in self.functions.keys():
            response = self.functions[data["action"]](data)
            if response != None:
                await self.send_queue.put(bson.dumps(response))
        else:
            print("Unknown action was ignored.")
            
    async def Producer(self):
        message = await self.send_queue.get()
        return message
        
    async def ConsumerHandler(self, websocket, path):
        async for message in websocket:
            await self.Consumer(message)
            
    async def ProducerHandler(self, websocket, path):
        while True:
            message = await self.Producer()
            await websocket.send(message)
        
    async def Handler(self, websocket, path):
        print("New connection opened.")
        consumer_task = asyncio.ensure_future(self.ConsumerHandler(websocket, path))
        producer_task = asyncio.ensure_future(self.ProducerHandler(websocket, path))
        done, pending = await asyncio.wait([consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED)
        print("Client disconnected")
        for task in pending:
            task.cancel()

    def UpdateState(self):
        asyncio.ensure_future(self.StateUpdated())

    async def StateUpdated(self):
        print("Cleaning up state...")
        if self.sync_state.connections.dirty:
            data = {"action": "RequestData", "request": "Connections"}
            await self.Consumer(bson.dumps(data))

        if self.sync_state.layers.value_dirty:
            for layer in range(self.sync_state.GetLayerCount()):
                data = {"action": "RequestData", "request": "NodeValues", "layer_index": layer}
                await self.Consumer(bson.dumps(data))

        if self.sync_state.pad_dirty:
            data = {"action": "RequestData", "request": "NeedsDrawingPad"}
            await self.Consumer(bson.dumps(data))
        
        if self.sync_state.layers.mesh_dirty:
            for layer in range(self.sync_state.GetLayerCount()):
                data = {"action": "RequestData", "request": "NodeMesh", "layer_index": layer}
                await self.Consumer(bson.dumps(data))

        if self.sync_state.dirty and not self.sync_state.connections.dirty and not self.sync_state.layers.value_dirty \
                and not self.sync_state.layers.coords_dirty and not self.sync_state.layers.mesh_dirty:
            data = {"action": "RequestData", "request": "LayerCount"}
            await self.Consumer(bson.dumps(data))
            for layer in range(self.sync_state.GetLayerCount()):
                data = {"action": "RequestData", "request": "LayerSize", "layer_index": layer}
                await self.Consumer(bson.dumps(data))

        self.sync_state.flush()

    def SendImage(self, image, image_id="default", width=0, height=0):
        if isinstance(image, str):
            try:
                im = Image.open(image)
                image = io.BytesIO()
                im.save(image, format='PNG')
            except BaseException as err:
                print("A string was input as an image but the image at that path could not be opened.")
                return
        data = image.getvalue()
        message = {"action": "Image", "image_data": data, "image_id": image_id,
                   "image_width": width, "image_height": height}
        asyncio.ensure_future(self.send_queue.put(bson.dumps(message)))


    async def ConsoleInterface(self, loop):
        while True:
            cmd = await loop.run_in_executor(None, input)
            parts = cmd.split(" ")
            if parts[0] == "stop":
                exit()
            elif parts[0] == "send":
                message = {"message" : " ".join(parts[1:])}
                print(f"Message {message} added to queue.")
                await self.send_queue.put(bson.dumps(message))
            else:
                print(parts[0] + " is an unknown command")
    
    def Run(self, host="", port=8765):
        '''Starts handler.'''
        start_server = websockets.serve(
            self.Handler, host, port, max_size=8388608 #1048576 # max message size defaults to 1 MiB UTF8-encoded data ~ 4 MiB, 8388608 worked without pbjson
        )
    
        print("Starting server...")
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.ConsoleInterface(loop))
        loop.run_until_complete(start_server)
        loop.run_forever()
        print("Server stopped.")