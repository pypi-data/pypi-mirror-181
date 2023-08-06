# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging
import grpc
from cakework import cakework_pb2
from cakework import cakework_pb2_grpc
import json
import importlib
# import os

class Cakework(cakework_pb2_grpc.CakeworkServicer):
    def __init__(self, user_activity):
        self.user_activity = user_activity
        # with open('cakework.json') as infile:
        #     conf = json.load(infile)
        # # self.module = os.environ['MODULE']
        # self.module = conf['module']
        # # self.activity = os.environ['ACTIVITY']
        # self.activity = conf['activity']
        # print("module: " + module)
        # print("activity: " +)
        # print("Running module: " + self.module + ", activity: " + self.activity) # TODO do proper logging
        # serve() # TODO hide the output that started a port. 

    def RunActivity(self, request, context):
        print("got request: " + request.parameters) # Q: does json serialize the parameters in order? 
        # print("importing module: " + self.module)
        # module = importlib.import_module(self.module)
        # # TODO do something with the context
        # parameters = json.loads(request.parameters)
        # activity = getattr(module, self.activity)
        parameters = json.loads(request.parameters)
        res = self.user_activity(**parameters)
        return cakework_pb2.Reply(result=json.dumps(res))

def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1)) # what should the default be?
    cakework_pb2_grpc.add_CakeworkServicer_to_server(Cakework(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()

class ActivityServer:
    def __init__(self, user_activity):
        self.user_activity = user_activity
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1)) # what should the default be?

    def start(self):        
        port = '50051'
        cakework_pb2_grpc.add_CakeworkServicer_to_server(Cakework(self.user_activity), self.server)
        self.server.add_insecure_port('[::]:' + port)
        self.server.start()
        print("Server started, listening on " + port)
        self.server.wait_for_termination()
