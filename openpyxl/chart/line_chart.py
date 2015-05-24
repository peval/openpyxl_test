from __future__ import absolute_import
#Autogenerated schema
from openpyxl.descriptors.serialisable import Serialisable
from openpyxl.descriptors import (
    Typed,
    Sequence,
    Alias,
    )
from openpyxl.descriptors.excel import ExtensionList
from openpyxl.descriptors.nested import (
    NestedSet,
    NestedBool,
    NestedMinMax,
)

from ._chart import ChartBase
from .updown_bars import UpDownBars
from .descriptors import NestedGapAmount
from .axis import CatAx, ValAx, SerAx, ChartLines, _BaseAxis
from .label import DataLabels
from .series import Series


class _LineChartBase(ChartBase):

    grouping = NestedSet(values=(['percentStacked', 'standard', 'stacked']))
    varyColors = NestedBool(allow_none=True)
    ser = Sequence(expected_type=Series, allow_none=True)
    dLbls = Typed(expected_type=DataLabels, allow_none=True)
    dataLabels = Alias("dLbls")
    dropLines = Typed(expected_type=ChartLines, allow_none=True)

    _series_type = "line"

    __elements__ = ('grouping', 'varyColors', 'ser', 'dLbls', 'dropLines')

    def __init__(self,
                 grouping="standard",
                 varyColors=None,
                 ser=[],
                 dLbls=None,
                 dropLines=None,
                ):
        self.grouping = grouping
        self.varyColors = varyColors
        self.ser = ser
        self.dLbls = dLbls
        self.dropLines = dropLines
        super(_LineChartBase, self).__init__()


class LineChart(_LineChartBase):

    tagname = "lineChart"

    grouping = _LineChartBase.grouping
    varyColors = _LineChartBase.varyColors
    ser = _LineChartBase.ser
    dLbls = _LineChartBase.dLbls
    dropLines =_LineChartBase.dropLines

    hiLowLines = Typed(expected_type=ChartLines, allow_none=True)
    upDownBars = Typed(expected_type=UpDownBars, allow_none=True)
    marker = NestedBool(allow_none=True)
    smooth = NestedBool(allow_none=True)
    extLst = Typed(expected_type=ExtensionList, allow_none=True)

    x_axis = Typed(expected_type=_BaseAxis)
    y_axis = Typed(expected_type=ValAx)

    __elements__ = _LineChartBase.__elements__ + ('hiLowLines', 'upDownBars', 'marker', 'smooth', 'axId')

    def __init__(self,
                 hiLowLines=None,
                 upDownBars=None,
                 marker=None,
                 smooth=None,
                 axId=None,
                 extLst=None,
                 **kw
                ):
        self.hiLowLines = hiLowLines
        self.upDownBars = upDownBars
        self.marker = marker
        self.smooth = smooth
        self.x_axis = CatAx()
        self.y_axis = ValAx()

        super(LineChart, self).__init__(**kw)


class LineChart3D(_LineChartBase):

    tagname = "line3DChart"

    grouping = _LineChartBase.grouping
    varyColors = _LineChartBase.varyColors
    ser = _LineChartBase.ser
    dLbls = _LineChartBase.dLbls
    dropLines =_LineChartBase.dropLines

    gapDepth = NestedGapAmount()
    hiLowLines = Typed(expected_type=ChartLines, allow_none=True)
    upDownBars = Typed(expected_type=UpDownBars, allow_none=True)
    marker = NestedBool(allow_none=True)
    smooth = NestedBool(allow_none=True)
    extLst = Typed(expected_type=ExtensionList, allow_none=True)

    x_axis = Typed(expected_type=CatAx)
    y_axis = Typed(expected_type=ValAx)
    z_axis = Typed(expected_type=SerAx)

    __elements__ = _LineChartBase.__elements__ + ('gapDepth', 'hiLowLines',
                                                  'upDownBars', 'marker', 'smooth', 'axId')

    def __init__(self,
                 gapDepth=None,
                 hiLowLines=None,
                 upDownBars=None,
                 marker=None,
                 smooth=None,
                 axId=None,
                 **kw
                ):
        self.gapDepth = gapDepth
        self.hiLowLines = hiLowLines
        self.upDownBars = upDownBars
        self.marker = marker
        self.smooth = smooth
        self.x_axis = CatAx()
        self.y_axis = ValAx()
        self.z_axis = SerAx()
        super(LineChart3D, self).__init__(**kw)
