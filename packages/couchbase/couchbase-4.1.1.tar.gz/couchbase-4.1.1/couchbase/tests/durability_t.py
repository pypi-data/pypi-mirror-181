#  Copyright 2016-2022. Couchbase, Inc.
#  All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License")
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from datetime import timedelta

import pytest

import couchbase.subdocument as SD
from couchbase.durability import (ClientDurability,
                                  DurabilityLevel,
                                  PersistTo,
                                  PersistToExtended,
                                  ReplicateTo,
                                  ServerDurability)
from couchbase.exceptions import DocumentNotFoundException, DurabilityImpossibleException
from couchbase.options import (InsertOptions,
                               MutateInOptions,
                               RemoveOptions,
                               ReplaceOptions,
                               UpsertOptions)

from ._test_utils import (CollectionType,
                          KVPair,
                          TestEnvironment)


class DurabilityTests:
    NO_KEY = "not-a-key"

    @pytest.fixture(scope="class", name="cb_env", params=[CollectionType.DEFAULT, CollectionType.NAMED])
    def couchbase_test_environment(self, couchbase_config, request):
        cb_env = TestEnvironment.get_environment(__name__, couchbase_config, request.param, manage_buckets=True)

        if request.param == CollectionType.NAMED:
            cb_env.try_n_times(5, 3, cb_env.setup_named_collections)

        cb_env.try_n_times(3, 5, cb_env.load_data)
        yield cb_env
        cb_env.try_n_times(3, 5, cb_env.purge_data)
        if request.param == CollectionType.NAMED:
            cb_env.try_n_times_till_exception(5, 3,
                                              cb_env.teardown_named_collections,
                                              raise_if_no_exception=False)

    @pytest.fixture(name="new_kvp")
    def new_key_and_value_with_reset(self, cb_env) -> KVPair:
        key, value = cb_env.get_new_key_value()
        yield KVPair(key, value)
        cb_env.try_n_times_till_exception(10,
                                          1,
                                          cb_env.collection.remove,
                                          key,
                                          expected_exceptions=(DocumentNotFoundException,),
                                          reset_on_timeout=True,
                                          reset_num_times=3)

    @pytest.fixture(name="default_kvp_and_reset")
    def default_key_and_value_with_reset(self, cb_env) -> KVPair:
        key, value = cb_env.default_durable_key_value()
        yield KVPair(key, value)
        cb_env.try_n_times(5, 3, cb_env.collection.upsert, key, value)

    @pytest.fixture(scope="class")
    def check_sync_durability_supported(self, cb_env):
        cb_env.check_if_feature_supported('sync_durability')

    @pytest.fixture(scope="class")
    def num_nodes(self, cb_env):
        return len(cb_env.cluster._cluster_info.nodes)

    @pytest.fixture(scope="class")
    def check_multi_node(self, num_nodes):
        if num_nodes == 1:
            pytest.skip("Test only for clusters with more than a single node.")

    @pytest.fixture(scope="class")
    def check_single_node(self, num_nodes):
        if num_nodes != 1:
            pytest.skip("Test only for clusters with a single node.")

    @pytest.fixture(scope="class")
    def num_replicas(self, cb_env):
        bucket_settings = cb_env.try_n_times(10, 1, cb_env.bm.get_bucket, cb_env.bucket.name)
        num_replicas = bucket_settings.get("num_replicas")
        return num_replicas

    @pytest.fixture(scope="class")
    def check_has_replicas(self, num_replicas):
        if num_replicas == 0:
            pytest.skip("No replicas to test durability.")

    @pytest.mark.usefixtures("check_sync_durability_supported")
    @pytest.mark.usefixtures("check_multi_node")
    @pytest.mark.usefixtures("check_has_replicas")
    def test_server_durable_upsert(self, cb_env, default_kvp_and_reset):
        cb = cb_env.collection
        key = default_kvp_and_reset.key
        value = default_kvp_and_reset.value

        durability = ServerDurability(level=DurabilityLevel.PERSIST_TO_MAJORITY)

        cb.upsert(key, value, UpsertOptions(durability=durability))
        result = cb.get(key)
        assert value == result.content_as[dict]

    @pytest.mark.usefixtures("check_sync_durability_supported")
    @pytest.mark.usefixtures("check_single_node")
    @pytest.mark.usefixtures("check_has_replicas")
    def test_server_durable_upsert_single_node(self, cb_env, default_kvp_and_reset):
        cb = cb_env.collection
        key = default_kvp_and_reset.key
        value = default_kvp_and_reset.value

        durability = ServerDurability(level=DurabilityLevel.PERSIST_TO_MAJORITY)
        with pytest.raises(DurabilityImpossibleException):
            cb.upsert(key, value, UpsertOptions(durability=durability))

    @pytest.mark.usefixtures("check_sync_durability_supported")
    @pytest.mark.usefixtures("check_multi_node")
    @pytest.mark.usefixtures("check_has_replicas")
    def test_server_durable_insert(self, cb_env, new_kvp):
        cb = cb_env.collection
        key = new_kvp.key
        value = new_kvp.value

        durability = ServerDurability(level=DurabilityLevel.PERSIST_TO_MAJORITY)
        cb.insert(key, value, InsertOptions(durability=durability))
        result = cb.get(key)
        assert value == result.content_as[dict]

    @pytest.mark.usefixtures("check_sync_durability_supported")
    @pytest.mark.usefixtures("check_single_node")
    @pytest.mark.usefixtures("check_has_replicas")
    def test_server_durable_insert_single_node(self, cb_env, new_kvp):
        cb = cb_env.collection
        key = new_kvp.key
        value = new_kvp.value

        durability = ServerDurability(level=DurabilityLevel.PERSIST_TO_MAJORITY)
        with pytest.raises(DurabilityImpossibleException):
            cb.insert(key, value, InsertOptions(durability=durability))

    @pytest.mark.usefixtures("check_sync_durability_supported")
    @pytest.mark.usefixtures("check_multi_node")
    @pytest.mark.usefixtures("check_has_replicas")
    def test_server_durable_replace(self, cb_env, default_kvp_and_reset):
        cb = cb_env.collection
        key = default_kvp_and_reset.key
        value = default_kvp_and_reset.value

        durability = ServerDurability(level=DurabilityLevel.PERSIST_TO_MAJORITY)
        cb.replace(key, value, ReplaceOptions(durability=durability))
        result = cb.get(key)
        assert value == result.content_as[dict]

    @pytest.mark.usefixtures("check_sync_durability_supported")
    @pytest.mark.usefixtures("check_single_node")
    @pytest.mark.usefixtures("check_has_replicas")
    def test_server_durable_replace_single_node(self, cb_env, default_kvp_and_reset):
        cb = cb_env.collection
        key = default_kvp_and_reset.key
        value = default_kvp_and_reset.value

        durability = ServerDurability(level=DurabilityLevel.PERSIST_TO_MAJORITY)
        with pytest.raises(DurabilityImpossibleException):
            cb.replace(key, value, ReplaceOptions(durability=durability))

    @pytest.mark.usefixtures("check_sync_durability_supported")
    @pytest.mark.usefixtures("check_multi_node")
    @pytest.mark.usefixtures("check_has_replicas")
    def test_server_durable_remove(self, cb_env, default_kvp_and_reset):
        cb = cb_env.collection
        key = default_kvp_and_reset.key

        durability = ServerDurability(level=DurabilityLevel.PERSIST_TO_MAJORITY)
        cb.remove(key, RemoveOptions(durability=durability))
        with pytest.raises(DocumentNotFoundException):
            cb.get(key)

    @pytest.mark.usefixtures("check_sync_durability_supported")
    @pytest.mark.usefixtures("check_single_node")
    @pytest.mark.usefixtures("check_has_replicas")
    def test_server_durable_remove_single_node(self, cb_env, default_kvp_and_reset):
        cb = cb_env.collection
        key = default_kvp_and_reset.key

        durability = ServerDurability(level=DurabilityLevel.PERSIST_TO_MAJORITY)
        with pytest.raises(DurabilityImpossibleException):
            cb.remove(key, RemoveOptions(durability=durability))

    @pytest.mark.usefixtures("check_multi_node")
    @pytest.mark.usefixtures("check_has_replicas")
    def test_client_durable_upsert(self, cb_env, default_kvp_and_reset, num_replicas):
        cb = cb_env.collection
        key = default_kvp_and_reset.key
        value = default_kvp_and_reset.value

        durability = ClientDurability(
            persist_to=PersistTo.ONE, replicate_to=ReplicateTo(num_replicas))

        cb.upsert(key, value,
                  UpsertOptions(durability=durability), timeout=timedelta(seconds=3))
        result = cb.get(key)
        assert value == result.content_as[dict]

    @pytest.mark.usefixtures("check_multi_node")
    @pytest.mark.usefixtures("check_has_replicas")
    def test_client_durable_upsert_fail(self, cb_env, default_kvp_and_reset, num_replicas):
        if num_replicas > 2:
            pytest.skip("Too many replicas enabled.")

        cb = cb_env.collection
        key = default_kvp_and_reset.key
        value = default_kvp_and_reset.value

        durability = ClientDurability(
            persist_to=PersistToExtended.FOUR, replicate_to=ReplicateTo(num_replicas))
        with pytest.raises(DurabilityImpossibleException):
            cb.upsert(key, value, UpsertOptions(durability=durability))

    @pytest.mark.usefixtures("check_single_node")
    @pytest.mark.usefixtures("check_has_replicas")
    def test_client_durable_upsert_single_node(self, cb_env, default_kvp_and_reset, num_replicas):
        cb = cb_env.collection
        key = default_kvp_and_reset.key
        value = default_kvp_and_reset.value

        durability = ClientDurability(
            persist_to=PersistToExtended.FOUR, replicate_to=ReplicateTo(num_replicas))
        with pytest.raises(DurabilityImpossibleException):
            cb.upsert(key, value, UpsertOptions(durability=durability))

    @pytest.mark.usefixtures("check_multi_node")
    @pytest.mark.usefixtures("check_has_replicas")
    def test_client_durable_insert(self, cb_env, new_kvp, num_replicas):
        cb = cb_env.collection
        key = new_kvp.key
        value = new_kvp.value

        durability = ClientDurability(
            persist_to=PersistTo.ONE, replicate_to=ReplicateTo(num_replicas))

        cb.insert(key, value, InsertOptions(durability=durability))
        result = cb.get(key)
        assert value == result.content_as[dict]

    @pytest.mark.usefixtures("check_multi_node")
    @pytest.mark.usefixtures("check_has_replicas")
    def test_client_durable_insert_fail(self, cb_env, new_kvp, num_replicas):
        if num_replicas > 2:
            pytest.skip("Too many replicas enabled.")

        cb = cb_env.collection
        key = new_kvp.key
        value = new_kvp.value

        durability = ClientDurability(
            persist_to=PersistToExtended.FOUR, replicate_to=ReplicateTo(num_replicas))
        with pytest.raises(DurabilityImpossibleException):
            cb.insert(key, value, InsertOptions(durability=durability))

    # @TODO: why DurabilityImpossibleException not raised?
    # @pytest.mark.usefixtures("check_single_node")
    # @pytest.mark.usefixtures("check_has_replicas")
    # def test_client_durable_insert_single_node(self, cb_env, new_kvp, num_replicas):
    #     cb = cb_env.collection
    #     key = new_kvp.key
    #     value = new_kvp.value

    #     durability = ClientDurability(
    #         persist_to=PersistToExtended.FOUR, replicate_to=ReplicateTo(num_replicas))

    #     with pytest.raises(DurabilityImpossibleException):
    #         cb.insert(key, value, InsertOptions(durability=durability))

    @pytest.mark.usefixtures("check_multi_node")
    @pytest.mark.usefixtures("check_has_replicas")
    def test_client_durable_replace(self, cb_env, default_kvp_and_reset, num_replicas):
        cb = cb_env.collection
        key = default_kvp_and_reset.key
        value = default_kvp_and_reset.value

        durability = ClientDurability(
            persist_to=PersistTo.ONE, replicate_to=ReplicateTo(num_replicas))

        cb.replace(key, value, ReplaceOptions(durability=durability))
        result = cb.get(key)
        assert value == result.content_as[dict]

    @pytest.mark.usefixtures("check_multi_node")
    @pytest.mark.usefixtures("check_has_replicas")
    def test_client_durable_replace_fail(self, cb_env, default_kvp_and_reset, num_replicas):
        if num_replicas > 2:
            pytest.skip("Too many replicas enabled.")

        cb = cb_env.collection
        key = default_kvp_and_reset.key
        value = default_kvp_and_reset.value

        durability = ClientDurability(
            persist_to=PersistToExtended.FOUR, replicate_to=ReplicateTo(num_replicas))
        with pytest.raises(DurabilityImpossibleException):
            cb.replace(key, value, ReplaceOptions(durability=durability))

    # @TODO: why DurabilityImpossibleException not raised?
    # @pytest.mark.usefixtures("check_single_node")
    # @pytest.mark.usefixtures("check_has_replicas")
    # def test_client_durable_replace_single_node(self, cb_env, default_kvp_and_reset, num_replicas):
    #     cb = cb_env.collection
    #     key = default_kvp_and_reset.key
    #     value = default_kvp_and_reset.value

    #     durability = ClientDurability(
    #         persist_to=PersistToExtended.FOUR, replicate_to=ReplicateTo(num_replicas))

    #     with pytest.raises(DurabilityImpossibleException):
    #         cb.replace(key, value, ReplaceOptions(durability=durability))

    @pytest.mark.usefixtures("check_multi_node")
    @pytest.mark.usefixtures("check_has_replicas")
    def test_client_durable_remove(self, cb_env, default_kvp_and_reset, num_replicas):
        cb = cb_env.collection
        key = default_kvp_and_reset.key

        durability = ClientDurability(persist_to=PersistTo.ONE, replicate_to=ReplicateTo(num_replicas))

        cb.remove(key, RemoveOptions(durability=durability))
        with pytest.raises(DocumentNotFoundException):
            cb.get(key)

    @pytest.mark.usefixtures("check_multi_node")
    @pytest.mark.usefixtures("check_has_replicas")
    def test_client_durable_remove_fail(self, cb_env, default_kvp_and_reset, num_replicas):
        if num_replicas > 2:
            pytest.skip("Too many replicas enabled.")

        cb = cb_env.collection
        key = default_kvp_and_reset.key

        durability = ClientDurability(
            persist_to=PersistToExtended.FOUR, replicate_to=ReplicateTo(num_replicas))
        with pytest.raises(DurabilityImpossibleException):
            cb.remove(key, RemoveOptions(durability=durability))

    # @TODO: why DurabilityImpossibleException not raised?
    # @pytest.mark.usefixtures("check_single_node")
    # @pytest.mark.usefixtures("check_has_replicas")
    # def test_client_durable_remove_single_node(self, cb_env, default_kvp_and_reset, num_replicas):
    #     cb = cb_env.collection
    #     key = default_kvp_and_reset.key

    #     durability = ClientDurability(
    #         persist_to=PersistToExtended.FOUR, replicate_to=ReplicateTo(num_replicas))

    #     with pytest.raises(DurabilityImpossibleException):
    #         cb.remove(key, RemoveOptions(durability=durability))

    @pytest.mark.usefixtures("check_multi_node")
    @pytest.mark.usefixtures("check_has_replicas")
    @pytest.mark.parametrize("persist_to", [PersistToExtended.NONE, PersistToExtended.ACTIVE, PersistToExtended.ONE])
    def test_client_persist_to_extended(self, cb_env, default_kvp_and_reset, persist_to):
        cb = cb_env.collection
        key = default_kvp_and_reset.key
        value = default_kvp_and_reset.value

        durability = ClientDurability(
            persist_to=persist_to, replicate_to=ReplicateTo.ONE)

        cb.upsert(key, value, UpsertOptions(durability=durability))
        result = cb.get(key)
        assert value == result.content_as[dict]

    # Sub-document durable operations

    @pytest.mark.usefixtures("check_sync_durability_supported")
    @pytest.mark.usefixtures("check_multi_node")
    @pytest.mark.usefixtures("check_has_replicas")
    def test_server_durable_mutate_in(self, cb_env, default_kvp_and_reset):
        if cb_env.is_mock_server:
            pytest.skip("Mock will not return expiry in the xaddrs.")

        cb = cb_env.collection
        key = default_kvp_and_reset.key
        value = default_kvp_and_reset.value
        value['city'] = 'New City'
        value['faa'] = 'CTY'

        durability = ServerDurability(level=DurabilityLevel.PERSIST_TO_MAJORITY)
        cb.mutate_in(key,
                     (SD.upsert('city', 'New City'), SD.replace('faa', 'CTY')),
                     MutateInOptions(durability=durability))
        result = cb.get(key)
        assert value == result.content_as[dict]

    @pytest.mark.usefixtures("check_sync_durability_supported")
    @pytest.mark.usefixtures("check_single_node")
    @pytest.mark.usefixtures("check_has_replicas")
    def test_server_durable_mutate_in_single_node(self, cb_env, default_kvp_and_reset):
        cb = cb_env.collection
        key = default_kvp_and_reset.key

        durability = ServerDurability(level=DurabilityLevel.PERSIST_TO_MAJORITY)
        with pytest.raises(DurabilityImpossibleException):
            cb.mutate_in(key, (SD.upsert('city', 'New City'),), MutateInOptions(durability=durability))

    @pytest.mark.usefixtures("check_multi_node")
    @pytest.mark.usefixtures("check_has_replicas")
    def test_client_durable_mutate_in(self, cb_env, default_kvp_and_reset, num_replicas):
        cb = cb_env.collection
        key = default_kvp_and_reset.key
        value = default_kvp_and_reset.value
        value['city'] = 'New City'
        value['faa'] = 'CTY'

        durability = ClientDurability(
            persist_to=PersistTo.ONE, replicate_to=ReplicateTo(num_replicas))

        cb.mutate_in(key,
                     (SD.upsert('city', 'New City'), SD.replace('faa', 'CTY')),
                     MutateInOptions(durability=durability))
        result = cb.get(key)
        assert value == result.content_as[dict]

    @pytest.mark.usefixtures("check_multi_node")
    @pytest.mark.usefixtures("check_has_replicas")
    def test_client_durable_mutate_in_fail(self, cb_env, default_kvp_and_reset, num_replicas):
        if num_replicas > 2:
            pytest.skip("Too many replicas enabled.")

        cb = cb_env.collection
        key = default_kvp_and_reset.key

        durability = ClientDurability(
            persist_to=PersistToExtended.FOUR, replicate_to=ReplicateTo(num_replicas))
        with pytest.raises(DurabilityImpossibleException):
            cb.mutate_in(key, (SD.upsert('city', 'New City'),), MutateInOptions(durability=durability))
