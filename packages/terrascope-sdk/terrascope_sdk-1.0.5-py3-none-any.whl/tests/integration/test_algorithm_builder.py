import pytest

from terrascope.sdk.builder.algorithm import AlgorithmManifest, InterfaceType, DataType


class TestAlgorithmManifest:
    @pytest.mark.asyncio
    async def test_algorithm_manifest(self):
        manifest = AlgorithmManifest()
        manifest.metadata_required(description="Testing algo manifest builder",
                                   version="0.1.0")
        manifest.interface_required(interface_type=InterfaceType.FILESYSTEM_TASK_WORKER)
        manifest.inputs_add_data_type(data_type_name=DataType.PINGS,
                                      min_count=2)

        manifest.container_parameters_required(image="orbitalinsight/raw_foottraffic:84c76f7f",
                                               command=["python",
                                                        "/orbital/base/algorithms/"
                                                        "raw_foottraffic/src/py/raw_foottraffic/simple_foottraffic.py"])
        manifest.outputs_add_data_types(output_data_types=["device_visits"],
                                        observation_value_columns=["unique_device_count"])

        manifest_struct = manifest.get()
        print(manifest_struct)
