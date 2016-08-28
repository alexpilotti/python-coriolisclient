# Copyright (c) 2016 Cloudbase Solutions Srl
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from coriolisclient import base
from coriolisclient.v1 import common
from coriolisclient.v1 import replica_executions


class Replica(base.Resource):
    _tasks = None

    @property
    def origin(self):
        return common.Origin(None, self._info.get("origin"), loaded=True)

    @property
    def destination(self):
        return common.Destination(None, self._info.get("destination"),
                                  loaded=True)

    @property
    def executions(self):
        if self._info.get('executions') is None:
            self.get()
        return [common.TasksExecution(None, d, loaded=True) for d in
                self._info.get('executions', [])]


class ReplicaManager(base.BaseManager):
    resource_class = Replica

    def __init__(self, api):
        super(ReplicaManager, self).__init__(api)

    def list(self):
        return self._list('/replicas/detail', 'replicas')

    def get(self, replica):
        return self._get('/replicas/%s' % base.getid(replica), 'replica')

    def create(self, origin_type, origin_connection_info, destination_type,
               destination_connection_info, target_environment, instances):
        data = {
            "replica": {
                "origin": {
                    "type": origin_type,
                    "connection_info": origin_connection_info,
                },
                "destination": {
                    "type": destination_type,
                    "connection_info": destination_connection_info,
                    "target_environment": target_environment,
                },
                "instances": instances,
            }
        }
        return self._post('/replicas', data, 'replica')

    def delete(self, replica):
        return self._delete('/replicas/%s' % base.getid(replica))

    def delete_disks(self, replica):
        response = self.client.post(
            '/replicas/%s/actions' % base.getid(replica),
            json={'delete-disks': None})

        return replica_executions.ReplicaExecution(
            self, response.json().get("execution"), loaded=True)