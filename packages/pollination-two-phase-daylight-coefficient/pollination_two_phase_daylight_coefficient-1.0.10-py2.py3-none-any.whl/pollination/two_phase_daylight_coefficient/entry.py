from dataclasses import dataclass
from pollination_dsl.dag import Inputs, DAG, task, Outputs
from pollination.honeybee_radiance.multiphase import PrepareMultiphase

# input/output alias
from pollination.alias.inputs.model import hbjson_model_grid_input
from pollination.alias.inputs.wea import wea_input_timestep_check
from pollination.alias.inputs.north import north_input
from pollination.alias.inputs.radiancepar import rad_par_annual_input
from pollination.alias.inputs.grid import grid_filter_input, \
    min_sensor_count_input, cpu_count

from ._prepare_folder import TwoPhasePrepareFolder
from .two_phase.entry import TwoPhaseSimulation


@dataclass
class TwoPhaseDaylightCoefficientEntryPoint(DAG):
    """Annual daylight entry point."""

    # inputs
    north = Inputs.float(
        default=0,
        description='A number for rotation from north.',
        spec={'type': 'number', 'minimum': 0, 'maximum': 360},
        alias=north_input
    )

    cpu_count = Inputs.int(
        default=50,
        description='The maximum number of CPUs for parallel execution. This will be '
        'used to determine the number of sensors run by each worker.',
        spec={'type': 'integer', 'minimum': 1},
        alias=cpu_count
    )

    min_sensor_count = Inputs.int(
        description='The minimum number of sensors in each sensor grid after '
        'redistributing the sensors based on cpu_count. This value takes '
        'precedence over the cpu_count and can be used to ensure that '
        'the parallelization does not result in generating unnecessarily small '
        'sensor grids. The default value is set to 1, which means that the '
        'cpu_count is always respected.', default=500,
        spec={'type': 'integer', 'minimum': 1},
        alias=min_sensor_count_input
    )

    radiance_parameters = Inputs.str(
        description='The radiance parameters for ray tracing.',
        default='-ab 2 -ad 5000 -lw 2e-05 -dr 0',
        alias=rad_par_annual_input
    )

    grid_filter = Inputs.str(
        description='Text for a grid identifier or a pattern to filter the sensor grids '
        'of the model that are simulated. For instance, first_floor_* will simulate '
        'only the sensor grids that have an identifier that starts with '
        'first_floor_. By default, all grids in the model will be simulated.',
        default='*',
        alias=grid_filter_input
    )

    model = Inputs.file(
        description='A Honeybee Model JSON file (HBJSON) or a Model pkl (HBpkl) file. '
        'This can also be a zipped version of a Radiance folder, in which case this '
        'recipe will simply unzip the file and simulate it as-is.',
        extensions=['json', 'hbjson', 'pkl', 'hbpkl', 'zip'],
        alias=hbjson_model_grid_input
    )

    wea = Inputs.file(
        description='Wea file.',
        extensions=['wea'],
        alias=wea_input_timestep_check
    )

    @task(template=TwoPhasePrepareFolder)
    def prepare_folder_annual_daylight(
        self, north=north, grid_filter=grid_filter, model=model, wea=wea
        ):
        return [
            {
                'from': TwoPhasePrepareFolder()._outputs.model_folder,
                'to': 'model'
            },
            {
                'from': TwoPhasePrepareFolder()._outputs.resources,
                'to': 'resources'
            },
            {
                'from': TwoPhasePrepareFolder()._outputs.results,
                'to': 'results'
            }
        ]

    @task(
        template=PrepareMultiphase,
        needs=[prepare_folder_annual_daylight],
        sub_paths={
            'sunpath': 'sunpath.mtx'
        }
    )
    def prepare_multiphase(
        self, model=prepare_folder_annual_daylight._outputs.model_folder,
        sunpath=prepare_folder_annual_daylight._outputs.resources, phase=2,
        cpu_count=cpu_count, cpus_per_grid=3,
        min_sensor_count=min_sensor_count, static='include'
    ):
        return [
            {
                'from': PrepareMultiphase()._outputs.scene_folder,
                'to': 'resources/dynamic/octree'
            },
            {
                'from': PrepareMultiphase()._outputs.grid_folder,
                'to': 'resources/dynamic/grid'
            },
            {
                'from': PrepareMultiphase()._outputs.two_phase_info
            },
            {   'from': PrepareMultiphase()._outputs.grid_states_file,
                'to': 'results/grid_states.json'
            }
        ]

    @task(
        template=TwoPhaseSimulation,
        loop=prepare_multiphase._outputs.two_phase_info,
        needs=[prepare_folder_annual_daylight, prepare_multiphase],
        sub_folder='calcs/2_phase/{{item.identifier}}',
        sub_paths={
            'octree_file': '{{item.octree}}',
            'octree_file_direct': '{{item.octree_direct}}',
            'octree_file_with_suns': '{{item.octree_direct_sun}}',
            'sensor_grids_folder': '{{item.sensor_grids_folder}}',
            'sky_dome': 'sky.dome',
            'total_sky': 'sky.mtx',
            'direct_sky': 'sky_direct.mtx',
            'sun_modifiers': 'suns.mod',
            'bsdf_folder': 'bsdf'
        }
    )
    def calculate_two_phase_matrix(
        self,
        identifier='{{item.identifier}}',
        light_path='{{item.light_path}}',
        radiance_parameters=radiance_parameters,
        sensor_grids_info='{{item.sensor_grids_info}}',
        sensor_grids_folder=prepare_multiphase._outputs.grid_folder,
        octree_file=prepare_multiphase._outputs.scene_folder,
        octree_file_direct=prepare_multiphase._outputs.scene_folder,
        octree_file_with_suns=prepare_multiphase._outputs.scene_folder,
        sky_dome=prepare_folder_annual_daylight._outputs.resources,
        total_sky=prepare_folder_annual_daylight._outputs.resources,
        direct_sky=prepare_folder_annual_daylight._outputs.resources,
        sun_modifiers=prepare_folder_annual_daylight._outputs.resources,
        bsdf_folder=prepare_folder_annual_daylight._outputs.model_folder,
        results_folder='../../../results'
    ):
        pass

    results = Outputs.folder(
        source='results', description='Folder with raw result files (.ill) that '
        'contain illuminance matrices for each sensor at each timestep of the analysis.'
    )
