import logging
import time
import uuid
from datetime import datetime

import pytest
from terrascope_api.models.common_models_pb2 import Pagination


from terrascope.sdk.api.aoi import AOIInputBuilder
from terrascope.sdk.builder.toi import TOIRuleBuilder, TOIBuilder, Frequency
from terrascope.sdk.builder.algorithm import AlgorithmManifest, InterfaceType, DataType, DataSource, \
    AlgorithmConfiguration
from terrascope.sdk.builder.analysis import AnalysisManifest, AnalysisConfiguration
from terrascope.sdk.terrascope_sdk import TerraScopeSDK


class TestAnalysis:
    @pytest.mark.asyncio
    async def test_create(self):
        sdk = TerraScopeSDK()
        name = "integration-test-{}".format(datetime.now())
        author = "terrascope-sdk"
        analysis = await sdk.analysis.create(name=name,
                                             author=author)
        assert analysis.id is not None
        assert analysis.name == name
        assert analysis.author == author

    @pytest.mark.asyncio
    async def test_update(self):
        pass

    @pytest.mark.asyncio
    @pytest.mark.parametrize("analysis_id_count", [
        1,
        10,
        25,
        45
    ])
    async def test_get(self, analysis_id_count: int):
        sdk = TerraScopeSDK()
        analysis_ids = []
        for i in range(analysis_id_count):
            analysis = await sdk.analysis.create(name="analysis_get_element_{}".format(uuid.uuid4()),
                                                 author="terrascope-sdk-pytest")
            analysis_ids.append(analysis.id)
        assert len(analysis_ids) == analysis_id_count
        analyses = await sdk.analysis.get(ids=analysis_ids,
                                          pagination=Pagination(page_size=5))
        assert len(analyses) == analysis_id_count

    @pytest.mark.asyncio
    @pytest.mark.parametrize("analysis_count", [
        10,
        20
    ])
    async def test_list(self, analysis_count):
        sdk = TerraScopeSDK()
        start = datetime.utcnow()
        halfway = None
        search_text = uuid.uuid4()
        for i in range(analysis_count):
            await sdk.analysis.create(name="sdk-search-me-{}-{}".format(i, search_text),
                                      author="terrascope-sdk-list-integration")
            if i + 1 == analysis_count / 2:
                time.sleep(10)
                halfway = datetime.utcnow()

        results = await sdk.analysis.list(search_text=str(search_text),
                                          pagination=Pagination(page_size=5))
        assert len(results) == analysis_count

        search_results = await sdk.analysis.list(min_created_on=start, max_created_on=halfway)
        assert len(search_results) == analysis_count / 2



class TestAnalysisVersion:
    @pytest.mark.asyncio
    async def test_create(self):
        sdk = TerraScopeSDK()
        algorithm_versions = []
        algo_name = "device-visits-sdk-integration-test-{}".format(uuid.uuid4())
        algo_display_name = "Device Visits SDK Integration"
        algo_author = "terrascope.sdk.integration@orbitalinsight.com"

        algorithm = await sdk.algorithm.create(name=algo_name,
                                               display_name=algo_display_name,
                                               author=algo_author)
        assert algorithm.id is not None
        assert algorithm.name == algo_name
        assert algorithm.display_name == algo_display_name
        assert algorithm.author == algo_author

        for i in range(3):
            manifest = AlgorithmManifest()
            manifest.metadata_required(
                                       description="Testing algo manifest builder",
                                       version="0.0.{}".format(i + 1))
            manifest.interface_required(interface_type=InterfaceType.FILESYSTEM_TASK_WORKER)
            manifest.inputs_add_data_type(data_type_name=DataType.PINGS,
                                          min_count=2,
                                          max_count=2)

            manifest.container_parameters_required(image="orbitalinsight/raw_foottraffic:84c76f7f",
                                                   command=["python",
                                                            "/orbital/base/algorithms/"
                                                            "raw_foottraffic/src/py/raw_foottraffic/simple_foottraffic.py"])
            manifest.outputs_add_data_types(output_data_types=["device_visits"],
                                            observation_value_columns=["unique_device_count"])

            algorithm_version = await sdk.algorithm_version.create(algorithm_id=algorithm.id,
                                                                   algorithm_manifest=manifest)
            algorithm_versions.append(algorithm_version.id)

        name = "analysis-version-create-test-{}".format(uuid.uuid4())
        author = "terrascope-sdk"
        analysis = await sdk.analysis.create(name=name,
                                             author=author)
        assert analysis.id is not None
        assert analysis.name == name
        assert analysis.author == author

        print(analysis.id)
        manifest = AnalysisManifest()
        manifest_version = "0.1.0"
        description = "Test description for the greatest manifest in the world."
        version = "0.1.0"
        manifest.metadata(description=description,
                          version=version,
                          tags=["sdk-test", "cap-sdk"])
        manifest.add_node(name="fake_name_1",
                          algorithm_version_id=algorithm_versions[0])
        manifest.add_node(name="fake_name_child_2",
                          algorithm_version_id=algorithm_versions[1])
        manifest.add_node(name="fake_name_child_3",
                          algorithm_version_id=algorithm_versions[2])

        manifest.add_node_edge(0, 1)
        manifest.add_node_edge(1, 2)
        analysis_version = await sdk.analysis_version.create(analysis_id=analysis.id,
                                                             analysis_manifest=manifest)
        assert analysis_version.id is not None

    @pytest.mark.asyncio
    @pytest.mark.parametrize("analysis_version_id_count", [
        1,
        10,
        25,
        45
    ])
    async def test_get(self, analysis_version_id_count):
        sdk = TerraScopeSDK()
        algorithm_versions = []
        algo_name = "device-visits-sdk-integration-test-{}".format(uuid.uuid4())
        algo_display_name = "Device Visits SDK Integration"
        algo_author = "terrascope.sdk.integration@orbitalinsight.com"

        algorithm = await sdk.algorithm.create(name=algo_name,
                                               display_name=algo_display_name,
                                               author=algo_author)
        assert algorithm.id is not None
        assert algorithm.name == algo_name
        assert algorithm.display_name == algo_display_name
        assert algorithm.author == algo_author
        for i in range(3):
            manifest = AlgorithmManifest()
            manifest.metadata_required(
                                       description="Testing algo manifest builder",
                                       version="0.0.{}".format(i + 1))
            manifest.interface_required(interface_type=InterfaceType.FILESYSTEM_TASK_WORKER)
            manifest.inputs_add_data_type(data_type_name=DataType.PINGS,
                                          min_count=2,
                                          max_count=2)

            manifest.container_parameters_required(image="orbitalinsight/raw_foottraffic:84c76f7f",
                                                   command=["python",
                                                            "/orbital/base/algorithms/"
                                                            "raw_foottraffic/src/py/raw_foottraffic/simple_foottraffic.py"])
            manifest.outputs_add_data_types(output_data_types=["device_visits"],
                                            observation_value_columns=["unique_device_count"])

            algorithm_version = await sdk.algorithm_version.create(algorithm_id=algorithm.id,
                                                                   algorithm_manifest=manifest)
            algorithm_versions.append(algorithm_version.id)

        name = "analysis-version-get-test-{}".format(datetime.now())
        author = "terrascope-sdk"
        analysis = await sdk.analysis.create(name=name,
                                             author=author)
        assert analysis.id is not None
        assert analysis.name == name
        assert analysis.author == author
        analysis_version_ids = []
        for i in range(analysis_version_id_count):
            manifest = AnalysisManifest()
            description = "Test description for the greatest manifest in the world."
            version = "0.{}.0".format(i)
            manifest.metadata(
                              description=description,
                              version=version,
                              tags=["sdk-test", "cap-sdk"])
            manifest.add_node(name="fake_name_1",
                              algorithm_version_id=algorithm_versions[0])
            manifest.add_node(name="fake_name_child_2",
                              algorithm_version_id=algorithm_versions[1])
            manifest.add_node(name="fake_name_child_3",
                              algorithm_version_id=algorithm_versions[2])

            manifest.add_node_edge(0, 1)
            manifest.add_node_edge(1, 2)

            analysis_version = await sdk.analysis_version.create(analysis_id=analysis.id,
                                                                 analysis_manifest=manifest)
            analysis_version_ids.append(analysis_version.id)
        assert len(analysis_version_ids) == analysis_version_id_count

        # Algo details should fail since fake algo
        analysis_versions = await sdk.analysis_version.get(ids=analysis_version_ids,
                                                           include_manifest=True,
                                                           pagination=Pagination(page_size=5))

        assert len(analysis_versions) == analysis_version_id_count

    @pytest.mark.asyncio
    @pytest.mark.parametrize("analysis_version_id_count", [
        10,
        20
    ])
    async def test_list(self, analysis_version_id_count: int):
        sdk = TerraScopeSDK()

        algorithm_versions = []
        algo_name = "device-visits-sdk-integration-test-{}".format(uuid.uuid4())
        algo_display_name = "Device Visits SDK Integration"
        algo_author = "terrascope.sdk.integration@orbitalinsight.com"

        algorithm = await sdk.algorithm.create(name=algo_name,
                                               display_name=algo_display_name,
                                               author=algo_author)
        assert algorithm.id is not None
        assert algorithm.name == algo_name
        assert algorithm.display_name == algo_display_name
        assert algorithm.author == algo_author
        for i in range(3):
            manifest = AlgorithmManifest()
            manifest.metadata_required(
                                       description="Testing algo manifest builder",
                                       version="0.0.{}".format(i + 1))
            manifest.interface_required(interface_type=InterfaceType.FILESYSTEM_TASK_WORKER)
            manifest.inputs_add_data_type(data_type_name=DataType.PINGS,
                                          min_count=2,
                                          max_count=2)

            manifest.container_parameters_required(image="orbitalinsight/raw_foottraffic:84c76f7f",
                                                   command=["python",
                                                            "/orbital/base/algorithms/"
                                                            "raw_foottraffic/src/py/raw_foottraffic/simple_foottraffic.py"])
            manifest.outputs_add_data_types(output_data_types=["device_visits"],
                                            observation_value_columns=["unique_device_count"])

            algorithm_version = await sdk.algorithm_version.create(algorithm_id=algorithm.id,
                                                                   algorithm_manifest=manifest)
            algorithm_versions.append(algorithm_version.id)

        name = "analysis-version-get-test-{}".format(datetime.now())
        author = "terrascope-sdk"
        analysis = await sdk.analysis.create(name=name,
                                             author=author)

        assert analysis.id is not None
        assert analysis.name == name
        assert analysis.author == author

        min_created_on = datetime.utcnow()
        max_created_on = None
        analysis_version_ids = []
        for i in range(analysis_version_id_count):
            manifest = AnalysisManifest()
            manifest_version = "0.1.{}".format(i)
            description = "Test description for the greatest manifest in the world."
            version = "0.{}.0".format(i)
            manifest.metadata(
                              description=description,
                              version=version,
                              tags=["sdk-test", "cap-sdk"])
            manifest.add_node(name="fake_name_1",
                              algorithm_version_id=algorithm_versions[0])
            manifest.add_node(name="fake_name_child_2",
                              algorithm_version_id=algorithm_versions[1])
            manifest.add_node(name="fake_name_child_3",
                              algorithm_version_id=algorithm_versions[2])

            manifest.add_node_edge(0, 1)
            manifest.add_node_edge(1, 2)

            analysis_version = await sdk.analysis_version.create(analysis_id=analysis.id,
                                                                 analysis_manifest=manifest)

            if i == (analysis_version_id_count / 2) - 1:
                time.sleep(10)
                max_created_on = datetime.utcnow()

            analysis_version_ids.append(analysis_version.id)

        analysis_versions = await sdk.analysis_version.list(analysis_id=analysis.id, include_all_versions=False)

        assert len(analysis_versions) == 1

        analysis_versions = await sdk.analysis_version.list(analysis_id=analysis.id,
                                                            include_all_versions=True)
        assert len(analysis_versions) == len(analysis_version_ids)
        for version in analysis_versions:
            assert version.analysis_id == analysis.id

        analysis_versions = await sdk.analysis_version.list(min_created_on=min_created_on,
                                                            max_created_on=max_created_on,
                                                            include_all_versions=True,
                                                            pagination=Pagination(page_size=5))
        assert len(analysis_versions) == analysis_version_id_count / 2

    @pytest.mark.asyncio
    async def test_deprecate(self):
        pass

    @pytest.mark.asyncio
    async def test_deactivate(self):
        pass


class TestAnalysisConfig:
    @pytest.mark.asyncio
    async def test_create(self):
        sdk = TerraScopeSDK()

        algo_name = "device-visits-sdk-integration-test-{}".format(uuid.uuid4())
        algo_display_name = "Device Visits SDK Integration"
        algo_author = "terrascope.sdk.integration@orbitalinsight.com"

        algorithm = await sdk.algorithm.create(name=algo_name,
                                               display_name=algo_display_name,
                                               author=algo_author)

        manifest = AlgorithmManifest()
        manifest.metadata_required(description="Testing algo manifest builder",
                                   version="0.0.1")
        manifest.interface_required(interface_type=InterfaceType.FILESYSTEM_TASK_WORKER)
        manifest.inputs_add_data_type(data_type_name=DataType.PINGS)

        manifest.container_parameters_required(image="orbitalinsight/raw_foottraffic:84c76f7f",
                                               command=["python",
                                                        "/orbital/base/algorithms/"
                                                        "raw_foottraffic/src/py/raw_foottraffic/simple_foottraffic.py"])
        manifest.outputs_add_data_types(output_data_types=["device_visits"],
                                        observation_value_columns=["unique_device_count"])

        algorithm_version = await sdk.algorithm_version.create(algorithm_id=algorithm.id,
                                                               algorithm_manifest=manifest)

        name = "analysis-config-create-test-{}".format(datetime.now())
        author = "terrascope-sdk"
        analysis = await sdk.analysis.create(name=name,
                                             author=author)
        assert analysis.id is not None
        assert analysis.name == name
        assert analysis.author == author

        manifest = AnalysisManifest()
        manifest_version = "0.1.0"
        description = "Test description for the greatest manifest in the world."
        version = "0.1.0"
        manifest.metadata(description=description,
                          version=version,
                          tags=["sdk-test", "cap-sdk", "create-test"])
        manifest.add_node(name="fake_name_1",
                          algorithm_version_id=algorithm_version.id)

        analysis_version = await sdk.analysis_version.create(analysis_id=analysis.id,
                                                             analysis_manifest=manifest)

        algorithm_config_build = AlgorithmConfiguration()
        algorithm_config_build.add_data_source(data_type=DataType.PINGS, data_source=DataSource.WEJO)
        algorithm_config = await sdk.algorithm_config.create(algorithm_version_id=algorithm_version.id,
                                                             algorithm_config=algorithm_config_build,
                                                             name="test_config-{}".format(uuid.uuid4()),
                                                             description="sdk test config")

        config = AnalysisConfiguration(analysis_version.id)
        config.add_config_node(name=manifest.get().algorithm_nodes[0].name,
                               algorithm_config_id=algorithm_config.id)
        analysis_config = await sdk.analysis_config.create(analysis_version_id=analysis_version.id,

                                                           name="analysis_config_test_create_{}".format(uuid.uuid4()),
                                                           description="Integration test for analysis_config.create",
                                                           algorithm_config_nodes=config.get())

        assert analysis_config.id is not None

    @pytest.mark.asyncio
    async def test_update(self):
        pass

    @pytest.mark.asyncio
    @pytest.mark.parametrize("config_count", [
        1,
        10,
        25,
        45
    ])
    async def test_get(self, config_count: int):
        sdk = TerraScopeSDK()
        algo_name = "device-visits-sdk-integration-test-{}".format(uuid.uuid4())
        algo_display_name = "Device Visits SDK Integration"
        algo_author = "terrascope.sdk.integration@orbitalinsight.com"

        algorithm = await sdk.algorithm.create(name=algo_name,
                                               display_name=algo_display_name,
                                               author=algo_author)

        manifest = AlgorithmManifest()
        manifest.metadata_required(description="Testing algo manifest builder",
                                   version="0.0.1")
        manifest.interface_required(interface_type=InterfaceType.FILESYSTEM_TASK_WORKER)
        manifest.inputs_add_data_type(data_type_name=DataType.PINGS)

        manifest.container_parameters_required(image="orbitalinsight/raw_foottraffic:84c76f7f",
                                               command=["python",
                                                        "/orbital/base/algorithms/"
                                                        "raw_foottraffic/src/py/raw_foottraffic/simple_foottraffic.py"])
        manifest.outputs_add_data_types(output_data_types=["device_visits"],
                                        observation_value_columns=["unique_device_count"])

        algorithm_version = await sdk.algorithm_version.create(algorithm_id=algorithm.id,
                                                               algorithm_manifest=manifest)

        name = "analysis-config-create-test-{}".format(datetime.now())
        author = "terrascope-sdk"
        analysis = await sdk.analysis.create(name=name,
                                             author=author)
        assert analysis.id is not None
        assert analysis.name == name
        assert analysis.author == author

        manifest = AnalysisManifest()
        manifest_version = "0.1.0"
        description = "Test description for the greatest manifest in the world."
        version = "0.1.0"
        manifest.metadata(description=description,
                          version=version,
                          tags=["sdk-test", "cap-sdk", "create-test"])
        manifest.add_node(name="fake_name_1",
                          algorithm_version_id=algorithm_version.id)

        analysis_version = await sdk.analysis_version.create(analysis_id=analysis.id,
                                                             analysis_manifest=manifest)

        algorithm_config_build = AlgorithmConfiguration()
        algorithm_config_build.add_data_source(data_type=DataType.PINGS, data_source=DataSource.WEJO)
        algorithm_config = await sdk.algorithm_config.create(algorithm_version_id=algorithm_version.id,
                                                             algorithm_config=algorithm_config_build,
                                                             name="test_config-{}".format(uuid.uuid4()),
                                                             description="sdk test config")

        analysis_config_ids = []
        for i in range(config_count):
            config = AnalysisConfiguration(analysis_version.id)
            config.add_config_node(name=manifest.get().algorithm_nodes[0].name,
                                   algorithm_config_id=algorithm_config.id)
            analysis_config = await sdk.analysis_config.create(analysis_version_id=analysis_version.id,

                                                               name="analysis_config_test_create_{}".format(
                                                                   uuid.uuid4()),
                                                               description="Integration test for analysis_config.create",
                                                               algorithm_config_nodes=config.get())

            assert analysis_config.id is not None
            analysis_config_ids.append(analysis_config.id)

        analysis_configs = await sdk.analysis_config.get(ids=analysis_config_ids,
                                                         include_algorithm_details=False,
                                          pagination=Pagination(page_size=5))

        assert len(analysis_configs) == config_count

    @pytest.mark.asyncio
    @pytest.mark.parametrize("config_count", [
        1,
        10,
        25
    ])
    async def test_list(self, config_count: int):
        sdk = TerraScopeSDK()
        algo_name = "device-visits-sdk-integration-test-{}".format(uuid.uuid4())
        algo_display_name = "Device Visits SDK Integration"
        algo_author = "terrascope.sdk.integration@orbitalinsight.com"

        algorithm = await sdk.algorithm.create(name=algo_name,
                                               display_name=algo_display_name,
                                               author=algo_author)

        manifest = AlgorithmManifest()
        manifest.metadata_required(description="Testing algo manifest builder",
                                   version="0.0.1")
        manifest.interface_required(interface_type=InterfaceType.FILESYSTEM_TASK_WORKER)
        manifest.inputs_add_data_type(data_type_name=DataType.PINGS)

        manifest.container_parameters_required(image="orbitalinsight/raw_foottraffic:84c76f7f",
                                               command=["python",
                                                        "/orbital/base/algorithms/"
                                                        "raw_foottraffic/src/py/raw_foottraffic/simple_foottraffic.py"])
        manifest.outputs_add_data_types(output_data_types=["device_visits"],
                                        observation_value_columns=["unique_device_count"])

        algorithm_version = await sdk.algorithm_version.create(algorithm_id=algorithm.id,
                                                               algorithm_manifest=manifest)

        name = "analysis-config-create-test-{}".format(datetime.now())
        author = "terrascope-sdk"
        analysis = await sdk.analysis.create(name=name,
                                             author=author)
        assert analysis.id is not None
        assert analysis.name == name
        assert analysis.author == author

        manifest = AnalysisManifest()
        manifest_version = "0.1.0"
        description = "Test description for the greatest manifest in the world."
        version = "0.1.0"
        manifest.metadata(description=description,
                          version=version,
                          tags=["sdk-test", "cap-sdk", "create-test"])
        manifest.add_node(name="fake_name_1",
                          algorithm_version_id=algorithm_version.id)

        analysis_version = await sdk.analysis_version.create(analysis_id=analysis.id,
                                                             analysis_manifest=manifest)

        algorithm_config_build = AlgorithmConfiguration()
        algorithm_config_build.add_data_source(data_type=DataType.PINGS, data_source=DataSource.WEJO)
        algorithm_config = await sdk.algorithm_config.create(algorithm_version_id=algorithm_version.id,
                                                             algorithm_config=algorithm_config_build,
                                                             name="test_config-{}".format(uuid.uuid4()),
                                                             description="sdk test config")

        analysis_config_ids = []
        for i in range(config_count):
            config = AnalysisConfiguration(analysis_version.id)
            config.add_config_node(name=manifest.get().algorithm_nodes[0].name,
                                   algorithm_config_id=algorithm_config.id)
            analysis_config = await sdk.analysis_config.create(analysis_version_id=analysis_version.id,

                                                               name="analysis_config_test_create_{}".format(
                                                                   uuid.uuid4()),
                                                               description="Integration test for analysis_config.create",
                                                               algorithm_config_nodes=config.get())

            assert analysis_config.id is not None
            analysis_config_ids.append(analysis_config.id)

        analysis_configs = await sdk.analysis_config.list(analysis_version_id=analysis_version.id,
                                                          pagination=Pagination(page_size=5))
        assert len(analysis_configs) == config_count

    @pytest.mark.asyncio
    async def test_deprecate(self):
        pass

    @pytest.mark.asyncio
    async def test_deactivate(self):
        pass

    @pytest.mark.asyncio
    async def test_delete(self):
        pass


class TestAnalysisComputation:
    @pytest.mark.asyncio
    async def test_create(self):
        sdk = TerraScopeSDK()
        # SETUP ALGORITHM
        algo_name = "device-visits-sdk-integration-test-{}".format(uuid.uuid4())
        algo_display_name = "Device Visits SDK Integration"
        algo_author = "terrascope.sdk.integration@orbitalinsight.com"

        algorithm = await sdk.algorithm.create(name=algo_name,
                                               display_name=algo_display_name,
                                               author=algo_author)
        assert algorithm.id is not None
        assert algorithm.name == algo_name
        assert algorithm.display_name == algo_display_name
        assert algorithm.author == algo_author

        manifest = AlgorithmManifest()
        manifest.metadata_required(description="Testing algo manifest builder",
                                   version="0.0.1")
        manifest.interface_required(interface_type=InterfaceType.FILESYSTEM_TASK_WORKER)
        manifest.inputs_add_data_type(data_type_name=DataType.PINGS)

        manifest.container_parameters_required(image="orbitalinsight/raw_foottraffic:84c76f7f",
                                               command=["python",
                                                        "/orbital/base/algorithms/"
                                                        "raw_foottraffic/src/py/raw_foottraffic/simple_foottraffic.py"])
        manifest.outputs_add_data_types(output_data_types=["device_visits"],
                                        observation_value_columns=["unique_device_count"])
        manifest.grouping_frequency(frequency="DAILY", value=1)
        manifest.parameter_add(name="dwell_time",
                               description="define dwell times",
                               type="integer",
                               min=10,
                               max=1440,
                               default=1440)

        algorithm_version = await sdk.algorithm_version.create(algorithm_id=algorithm.id,
                                                               algorithm_manifest=manifest)

        assert algorithm_version.id is not None

        configuration = AlgorithmConfiguration()
        configuration.add_data_source(DataType.PINGS, DataSource.WEJO)

        algorithm_configuration = await sdk.algorithm_config.create(algorithm_version_id=algorithm_version.id,
                                                                    name="device_visit_sdk_test_config",
                                                                    description="A test configuration.",
                                                                    algorithm_config=configuration)

        # SETUP ANALYSIS
        name = "analysis-config-create-test-{}".format(datetime.now())
        name = "analysis-config-create-test-{}".format(datetime.now())
        author = "terrascope-sdk"
        analysis = await sdk.analysis.create(name=name,
                                             author=author)
        assert analysis.id is not None
        assert analysis.name == name
        assert analysis.author == author

        manifest = AnalysisManifest()
        manifest_version = "0.1.0"
        description = "Test description for the greatest manifest in the world."
        version = "0.0.1"
        manifest.metadata(description=description,
                          version=version,
                          tags=["sdk-test", "cap-sdk", "create-test"])
        manifest.add_node(name="device-visits",
                          algorithm_version_id=algorithm_version.id)

        analysis_version = await sdk.analysis_version.create(analysis_id=analysis.id,
                                                             analysis_manifest=manifest)

        config = AnalysisConfiguration(analysis_version.id)
        config.add_config_node(name=manifest.get().algorithm_nodes[0].name,
                               algorithm_config_id=algorithm_configuration.id)
        analysis_config = await sdk.analysis_config.create(analysis_version_id=analysis_version.id,
                                                           name="analysis_config_test_create_{}".format(uuid.uuid4()),
                                                           description="Integration test for analysis_config.create",
                                                           algorithm_config_nodes=config.get())

        assert analysis_config.id is not None

        # SETUP AOI
        aoi_collection = await sdk.aoi_collection.create(aoi_collection_name=name)
        assert aoi_collection.id is not None

        wkt = """POLYGON ((-121.891336 37.345116, -121.882978 37.322622, -121.865618 37.335404, -121.891336 37.345116))
                """
        aoi_builder = AOIInputBuilder()
        aoi = aoi_builder.build(
            geom_wkt=wkt,
            name="aoi-" + name,
            category="industry",
            category_type="LNG",
            tags=["industrial", "LNG", "test"])
        aoi_identifiers = await sdk.aoi.create(aoi_collection_id=aoi_collection.id,
                                               aoi_inputs=[aoi])

        assert aoi_identifiers is not None

        # SETUP TOI

        datetime_format = '%Y-%m-%dT%H:%M:%SZ'
        toi_configuration = TOIBuilder()
        toi_configuration.build_toi(start=datetime.strptime("2019-01-05T01:00:00Z", datetime_format),
                                    finish=datetime.strptime("2019-01-15T01:00:00Z", datetime_format))
        toi_configuration.build_recurrence(TOIRuleBuilder.build_rule(
            frequency=Frequency.DAILY,
            interval=1
        ))
        toi = await sdk.toi.create(toi_configuration.get())
        assert toi.id is not None

        # SETUP ANALYSIS COMPUTATION
        analysis_computation = await sdk.analysis_computation.create(
            analysis_config_id=analysis_config.id,
            toi_id=toi.id,
            aoi_collection_id=aoi_collection.id)
        assert analysis_computation.id is not None

    @pytest.mark.asyncio
    async def test_run(self):
        sdk = TerraScopeSDK()
        # SETUP ALGORITHM
        algo_name = "device-visits-sdk-integration-test-{}".format(uuid.uuid4())
        algo_display_name = "Device Visits SDK Integration"
        algo_author = "terrascope.sdk.integration@orbitalinsight.com"

        algorithm = await sdk.algorithm.create(name=algo_name,
                                               display_name=algo_display_name,
                                               author=algo_author)
        assert algorithm.id is not None
        assert algorithm.name == algo_name
        assert algorithm.display_name == algo_display_name
        assert algorithm.author == algo_author

        manifest = AlgorithmManifest()
        manifest.metadata_required(description="Testing algo manifest builder",
                                   version="0.0.1")
        manifest.interface_required(interface_type=InterfaceType.FILESYSTEM_TASK_WORKER)
        manifest.inputs_add_data_type(data_type_name=DataType.PINGS)

        manifest.container_parameters_required(image="orbitalinsight/raw_foottraffic:40be9a67",
                                               command=["python",
                                                        "/orbital/base/algorithms/"
                                                        "raw_foottraffic/src/py/raw_foottraffic/simple_foottraffic.py"])
        manifest.outputs_add_data_types(output_data_types=["device_visits"],
                                        observation_value_columns=["unique_device_count"])
        manifest.grouping_frequency(frequency="DAILY", value=1)
        manifest.parameter_add(name="min_dwell_time", type="integer", units="minutes", min=0, max=1440, default=0,
                               description="Minimum dwell time in minutes required for a ping to be included "
                                           "in unique device count. Default is 0 (i.e. all pings are included).")
        manifest.parameter_add(name="max_dwell_time", type="integer", units="minutes", min=0, max=1440, default=1440,
                               description="Maximum dwell time in minutes required for a ping to be included in "
                                           "unique device count. Default is None (i.e. all pings are included).")

        algorithm_version = await sdk.algorithm_version.create(algorithm_id=algorithm.id,
                                                               algorithm_manifest=manifest)

        assert algorithm_version.id is not None

        configuration = AlgorithmConfiguration()
        configuration.add_data_source(DataType.PINGS, DataSource.WEJO)

        algorithm_configuration = await sdk.algorithm_config.create(algorithm_version_id=algorithm_version.id,
                                                                    name="device_visit_sdk_test_config",
                                                                    description="A test configuration.",
                                                                    algorithm_config=configuration)

        # SETUP ANALYSIS
        name = "analysis-config-create-test-{}".format(datetime.now())
        author = "terrascope-sdk"
        analysis = await sdk.analysis.create(name=name,
                                             author=author)
        assert analysis.id is not None
        assert analysis.name == name
        assert analysis.author == author

        manifest = AnalysisManifest()
        description = "Test description for the greatest manifest in the world."
        version = "0.0.1"
        manifest.metadata(description=description,
                          version=version,
                          tags=["sdk-test", "cap-sdk", "create-test"])
        manifest.add_node(name="foot_traffic",
                          algorithm_version_id=algorithm_version.id)

        analysis_version = await sdk.analysis_version.create(analysis_id=analysis.id,
                                                             analysis_manifest=manifest)

        config = AnalysisConfiguration(analysis_version.id)
        config.add_config_node(name=manifest.get().algorithm_nodes[0].name,
                               algorithm_config_id=algorithm_configuration.id)
        analysis_config = await sdk.analysis_config.create(analysis_version_id=analysis_version.id,
                                                           name="analysis_config_test_create_{}".format(uuid.uuid4()),
                                                           description="Integration test for analysis_config.create",
                                                           algorithm_config_nodes=config.get())

        assert analysis_config.id is not None

        # SETUP AOI
        aoi_collection = await sdk.aoi_collection.create(aoi_collection_name=name)
        assert aoi_collection.id is not None

        wkt = """POLYGON ((-121.891336 37.345116, -121.882978 37.322622, -121.865618 37.335404, -121.891336 37.345116))
                        """
        aoi_builder = AOIInputBuilder()
        aoi = aoi_builder.build(
            geom_wkt=wkt,
            name="aoi-" + name,
            category="industry",
            type="LNG",
            tags=["industrial", "LNG", "test"]
        )
        aoi_identifiers = await sdk.aoi.create(aoi_collection_id=aoi_collection.id,
                                               aoi_inputs=[aoi])

        assert aoi_identifiers is not None

        # SETUP TOI
        datetime_format = '%Y-%m-%dT%H:%M:%SZ'
        toi_configuration = TOIBuilder()
        toi_configuration.build_toi(start=datetime.strptime("2019-01-05T01:00:00Z", datetime_format),
                                    finish=datetime.strptime("2019-01-06T01:00:00Z", datetime_format))
        toi_configuration.build_recurrence(TOIRuleBuilder.build_rule(
            frequency=Frequency.DAILY,
            interval=1
        ))
        toi = await sdk.toi.create(toi_configuration.get())
        assert toi.id is not None

        # SETUP ANALYSIS COMPUTATION
        analysis_computation = await sdk.analysis_computation.create(analysis_config_id=analysis_config.id,
                                                                     toi_id=toi.id,
                                                                     aoi_collection_id=aoi_collection.id)
        assert analysis_computation.id is not None

        logging.info(analysis_computation)
        # RUN ANALYSIS COMPUTATION
        await sdk.analysis_computation.run([analysis_computation.id])

    @pytest.mark.asyncio
    async def test_get(self):
        sdk = TerraScopeSDK()
        # SETUP ALGORITHM
        algo_name = "device-visits-sdk-integration-test-{}".format(uuid.uuid4())
        algo_display_name = "Device Visits SDK Integration"
        algo_author = "terrascope.sdk.integration@orbitalinsight.com"

        algorithm = await sdk.algorithm.create(name=algo_name,
                                               display_name=algo_display_name,
                                               author=algo_author)
        assert algorithm.id is not None
        assert algorithm.name == algo_name
        assert algorithm.display_name == algo_display_name
        assert algorithm.author == algo_author

        manifest = AlgorithmManifest()
        manifest.metadata_required(description="Testing algo manifest builder",
                                   version="0.0.1")
        manifest.interface_required(interface_type=InterfaceType.FILESYSTEM_TASK_WORKER)
        manifest.inputs_add_data_type(data_type_name=DataType.PINGS)

        manifest.container_parameters_required(image="orbitalinsight/raw_foottraffic:84c76f7f",
                                               command=["python",
                                                        "/orbital/base/algorithms/"
                                                        "raw_foottraffic/src/py/raw_foottraffic/simple_foottraffic.py"])
        manifest.outputs_add_data_types(output_data_types=["device_visits"],
                                        observation_value_columns=["unique_device_count"])
        manifest.grouping_frequency(frequency="DAILY", value=1)
        manifest.parameter_add(name="dwell_time",
                               description="define dwell times",
                               type="integer",
                               min=10,
                               max=1440,
                               default=1440)

        algorithm_version = await sdk.algorithm_version.create(algorithm_id=algorithm.id,
                                                               algorithm_manifest=manifest)

        assert algorithm_version.id is not None

        configuration = AlgorithmConfiguration()
        configuration.add_data_source(DataType.PINGS, DataSource.WEJO)

        algorithm_configuration = await sdk.algorithm_config.create(algorithm_version_id=algorithm_version.id,
                                                                    name="device_visit_sdk_test_config",
                                                                    description="A test configuration.",
                                                                    algorithm_config=configuration)

        # SETUP ANALYSIS
        name = "analysis-config-create-test-{}".format(datetime.now())
        author = "terrascope-sdk"
        analysis = await sdk.analysis.create(name=name,
                                             author=author)
        assert analysis.id is not None
        assert analysis.name == name
        assert analysis.author == author

        manifest = AnalysisManifest()
        manifest_version = "0.1.0"
        description = "Test description for the greatest manifest in the world."
        version = "0.0.1"
        manifest.metadata(description=description,
                          version=version,
                          tags=["sdk-test", "cap-sdk", "create-test"])
        manifest.add_node(name="device-visits",
                          algorithm_version_id=algorithm_version.id)

        analysis_version = await sdk.analysis_version.create(analysis_id=analysis.id,
                                                             analysis_manifest=manifest)

        config = AnalysisConfiguration(analysis_version.id)
        config.add_config_node(name=manifest.get().algorithm_nodes[0].name,
                               algorithm_config_id=algorithm_configuration.id)
        analysis_config = await sdk.analysis_config.create(analysis_version_id=analysis_version.id,
                                                           name="analysis_config_test_create_{}".format(uuid.uuid4()),
                                                           description="Integration test for analysis_config.create",
                                                           algorithm_config_nodes=config.get())

        assert analysis_config.id is not None

        # SETUP AOI
        aoi_collection = await sdk.aoi_collection.create(aoi_collection_name=name)
        assert aoi_collection.id is not None

        wkt = """POLYGON ((-121.891336 37.345116, -121.882978 37.322622, -121.865618 37.335404, -121.891336 37.345116))
                        """
        aoi_identifiers = await sdk.aoi.create(aoi_collection_id=aoi_collection.id,
                                               aoi_inputs=[AOIInputBuilder.build(geom_wkt=wkt,
                                                                                 name="aoi-" + name,
                                                                                 category="industry",
                                                                                 type="LNG",
                                                                                 tags=["industrial", "LNG", "test"])])

        assert aoi_identifiers is not None

        # SETUP TOI
        datetime_format = '%Y-%m-%dT%H:%M:%SZ'
        toi_configuration = TOIBuilder()
        toi_configuration.build_toi(start=datetime.strptime("2019-01-05T01:00:00Z", datetime_format),
                                    finish=datetime.strptime("2019-01-06T01:00:00Z", datetime_format))
        toi_configuration.build_recurrence(TOIRuleBuilder.build_rule(
            frequency=Frequency.DAILY,
            interval=1
        ))
        toi = await sdk.toi.create(toi_configuration.get())
        assert toi.id is not None

        # SETUP ANALYSIS COMPUTATION
        analysis_computation = await sdk.analysis_computation.create(
            analysis_config_id=analysis_config.id,
            toi_id=toi.id,
            aoi_collection_id=aoi_collection.id)
        assert analysis_computation.id is not None

        analysis_computation = await sdk.analysis_computation.get([analysis_computation.id])
        assert analysis_computation is not None

    @pytest.mark.asyncio
    async def test_list(self):
        pass
