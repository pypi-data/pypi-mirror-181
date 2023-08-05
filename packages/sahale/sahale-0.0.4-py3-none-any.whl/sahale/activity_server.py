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
import sahale_pb2
import sahale_pb2_grpc
REPLACE_ME_ACTIVITY_IMPORT
#from activities import user_activity_replace_me # will add a line here simliar to this
import json

class Sahale(sahale_pb2_grpc.SahaleServicer):

    def RunActivity(self, request, context):
        print("got request: " + request.parameters) # Q: does json serialize the parameters in order? 
        # TODO do something with the context
        parameters = json.loads(request.parameters)
        REPLACE_ME_ACTIVITY_INVOCATION
        return sahale_pb2.Reply(result=json.dumps(res))

def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1)) # what should the default be?
    sahale_pb2_grpc.add_SahaleServicer_to_server(Sahale(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
