# Copyright (c) 2017 Cloudbase Solutions Srl
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

import json

from six.moves.urllib import parse as urlparse

from coriolisclient import base


class ReplicaSchedule(base.Resource):
    _tasks = None


class ReplicaScheduleManager(base.BaseManager):
    resource_class = ReplicaSchedule

    def __init__(self, api):
        super(ReplicaScheduleManager, self).__init__(api)

    def list(self, replica, hide_expired=False):
        query = {}
        if hide_expired:
            query["show_expired"] = hide_expired is False
        url = '/replicas/%s/schedules' % base.getid(replica)
        if query:
            url += "?" + urlparse.urlencode(query)
        return self._list(
            url, 'schedules')

    def get(self, replica, schedule):
        return self._get(
            '/replicas/%(replica_id)s/schedules/%(schedule_id)s' %
            {"replica_id": base.getid(replica),
             "schedule_id": base.getid(schedule)},
            'schedule')

    def create(self, replica, schedule, enabled, expires, shutdown_instance):
        data = {
            "schedule": schedule,
            "enabled": enabled,
            "shutdown_instance": shutdown_instance,
        }
        if expires:
            data["expiration_date"] = expires
        return self._post(
            '/replicas/%s/schedules' % base.getid(replica), data, 'schedule')

    def update(self, replica_id, schedule_id, updated_values):
        return self._put(
            '/replicas/%(replica_id)s/schedules/%(schedule_id)s' % {
                "replica_id": base.getid(replica_id),
                "schedule_id": base.getid(schedule_id)},
            updated_values, 'schedule')

    def delete(self, replica, schedule):
        return self._delete(
            '/replicas/%(replica_id)s/schedules/%(schedule_id)s' %
            {"replica_id": base.getid(replica),
             "schedule_id": base.getid(schedule)})
