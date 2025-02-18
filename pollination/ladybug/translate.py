from dataclasses import dataclass
from pollination_dsl.function import Inputs, Outputs, Function, command


@dataclass
class EpwToWea(Function):
    """Translate an .epw file to a .wea file."""

    epw = Inputs.file(
        description='Weather file.', path='weather.epw', extensions=['epw']
    )

    period = Inputs.str(
        description='An AnalysisPeriod string to filter the datetimes in the resulting '
        'Wea (eg. "6/21 to 9/21 between 8 and 16 @1"). Note that the timestep '
        'of the analysis period should match the input timestep and a * must be at '
        'the end of the string if the input epw is for a leap year. If None, '
        'the Wea will be annual.', default=''
    )

    timestep = Inputs.int(
        description='An integer to set the number of time steps per hour. Default is 1 '
        'for one value per hour. Note that this input will only do a linear '
        'interpolation over the data in the epw file.', default=1
    )

    @command
    def epw_to_wea(self):
        return 'ladybug translate epw-to-wea weather.epw ' \
            '--analysis-period "{{self.period}}" --timestep {{self.timestep}} ' \
            '--output-file weather.wea'

    wea = Outputs.file(
        description='A wea file generated from the input epw.',
        path='weather.wea'
    )


@dataclass
class EpwToDdy(Function):
    """Translate an .epw file to a .ddy file."""

    epw = Inputs.file(
        description='Weather file.', path='weather.epw', extensions=['epw']
    )

    percentile = Inputs.float(
        description='A number between 0 and 50 for the percentile difference from '
        'the most extreme conditions within the EPW to be used for the design day. '
        'Typical values are 0.4 and 1.0.', default=0.4
    )

    @command
    def epw_to_ddy(self):
        return 'ladybug translate epw-to-ddy weather.epw ' \
            '--percentile {{self.percentile}} --output-file weather.ddy'

    ddy = Outputs.file(
        description='A ddy file generated from the input epw.',
        path='weather.ddy'
    )


@dataclass
class WeaToConstant(Function):
    """Convert a Wea file to have a constant value for each datetime.

    This is useful in workflows where hourly irradiance values are inconsequential
    to the analysis and one is only using the Wea as a format to pass location
    and datetime information (eg. for direct sun hours).
    """

    wea = Inputs.file(
        description='Wea file with irradiance values to be set to constant.',
        path='weather.wea', extensions=['wea']
    )

    value = Inputs.int(
        description='The direct and diffuse irradiance value that will be written '
        'in for all datetimes of the Wea.', default=1000
    )

    @command
    def wea_to_constant(self):
        return 'ladybug translate wea-to-constant weather.wea ' \
            '--value {{self.value}} --output-file constant.wea'

    constant_wea = Outputs.file(
        description='A wea file with constant irradiance values for each datetime.',
        path='constant.wea'
    )
