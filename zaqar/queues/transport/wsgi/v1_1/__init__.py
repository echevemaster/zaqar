# Copyright (c) 2013 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy
# of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

from zaqar.queues.transport.wsgi.v1_1 import claims
from zaqar.queues.transport.wsgi.v1_1 import health
from zaqar.queues.transport.wsgi.v1_1 import homedoc
from zaqar.queues.transport.wsgi.v1_1 import messages
from zaqar.queues.transport.wsgi.v1_1 import ping
from zaqar.queues.transport.wsgi.v1_1 import pools
from zaqar.queues.transport.wsgi.v1_1 import queues
from zaqar.queues.transport.wsgi.v1_1 import stats


def public_endpoints(driver):
    queue_controller = driver._storage.queue_controller
    message_controller = driver._storage.message_controller
    claim_controller = driver._storage.claim_controller

    defaults = driver._defaults

    return [
        # Home
        ('/',
         homedoc.Resource()),

        # Queues Endpoints
        ('/queues',
         queues.CollectionResource(driver._validate,
                                   queue_controller)),
        ('/queues/{queue_name}',
         queues.ItemResource(driver._validate,
                             queue_controller,
                             message_controller)),
        ('/queues/{queue_name}/stats',
         stats.Resource(queue_controller)),

        # Messages Endpoints
        ('/queues/{queue_name}/messages',
         messages.CollectionResource(driver._wsgi_conf,
                                     driver._validate,
                                     message_controller,
                                     queue_controller,
                                     defaults.message_ttl)),
        ('/queues/{queue_name}/messages/{message_id}',
         messages.ItemResource(message_controller)),

        # Claims Endpoints
        ('/queues/{queue_name}/claims',
         claims.CollectionResource(driver._wsgi_conf,
                                   driver._validate,
                                   claim_controller,
                                   defaults.claim_ttl,
                                   defaults.claim_grace)),
        ('/queues/{queue_name}/claims/{claim_id}',
         claims.ItemResource(driver._wsgi_conf,
                             driver._validate,
                             claim_controller)),

        # Health
        ('/health',
         health.Resource(driver._storage)),

        # Ping
        ('/ping',
         ping.Resource(driver._storage))
    ]


def private_endpoints(driver):
    pools_controller = driver._control.pools_controller

    return [
        ('/pools',
         pools.Listing(pools_controller)),
        ('/pools/{pool}',
         pools.Resource(pools_controller)),
    ]
