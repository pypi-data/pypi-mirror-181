import copyreg
import pathlib
import tempfile
from typing import Dict, Any

import numpy as np
import vtk
from PySide2.QtCore import *
from PySide2.QtGui import *

import vmat

vtkget_ignore = ('GetDebug', 'GetGlobalReleaseDataFlag', 'GetGlobalWarningDisplay', 'GetReferenceCount',
                 'GetAAFrames', 'GetFDFrames', 'GetSubFrames', 'GetUseConstantFDOffsets', 'GetStereoCapableWindow',
                 'GetForceCompileOnly', 'GetGlobalImmediateModeRendering', 'GetImmediateModeRendering',
                 'GetScalarMaterialMode', 'GetReleaseDataFlag')


def vtkInstance_gets(instance) -> Dict[str, Any]:
    """
    返回vtk类型实例的所有Set/Get状态值

    :param instance: vtk类型实例
    :return: 状态值{'GetXXX': Any}
    """
    gets = {}
    for get_name in dir(instance):
        if get_name.startswith('Get'):
            set_name = get_name.replace('Get', 'Set', 1)
            if hasattr(instance, set_name) and get_name not in vtkget_ignore:
                try:
                    a = getattr(instance, get_name)()
                    if 'vtk' not in str(type(a)):
                        gets[get_name] = a
                except TypeError:
                    pass
    return gets


def vtkInstance_sets(instance, gets) -> None:
    """
    设置vtk类型实例的所有Set/Get状态值
    :param instance: vtk类型实例
    :param gets: 状态值{'GetXXX': Any}
    :return: None
    """
    for get_name in gets:
        set_name = get_name.replace('Get', 'Set', 1)
        try:
            getattr(instance, set_name)(gets[get_name])
        except TypeError:
            pass


def pickle_vtkImageData(instance: vtk.vtkImageData):
    gets = vtkInstance_gets(instance)
    if instance.GetNumberOfPoints() == 0:
        data = bytes()
    else:
        with tempfile.TemporaryDirectory() as p:
            p = pathlib.Path(p) / '.vti'
            vmat.imSaveFile_XML(instance, str(p))
            data = p.read_bytes()
    return unpickle_vtkImageData, (gets, data,)


def unpickle_vtkImageData(gets, data):
    if len(data) == 0:
        instance = vtk.vtkImageData()
    else:
        with tempfile.TemporaryDirectory() as p:
            p = pathlib.Path(p) / '.vti'
            p.write_bytes(data)
            instance = vmat.imOpenFile_XML(str(p))
    vtkInstance_sets(instance, gets)
    return instance


def pickle_vtkLookupTable(instance: vtk.vtkLookupTable):
    gets = vtkInstance_gets(instance)
    data = []
    for i in range(instance.GetNumberOfTableValues()):
        data.append(instance.GetTableValue(i))
    return unpickle_vtkLookupTable, (gets, data,)


def unpickle_vtkLookupTable(gets, data):
    instance = vtk.vtkLookupTable()
    vtkInstance_sets(instance, gets)
    instance.SetNumberOfTableValues(len(data))
    for i in range(len(data)):
        instance.SetTableValue(i, data[i])
    instance.Build()
    return instance


def pickle_vtkMatrix4x4(instance: vtk.vtkMatrix4x4):
    gets = vtkInstance_gets(instance)
    data = np.zeros((4, 4))
    for j in range(4):
        for i in range(4):
            data[i, j] = instance.GetElement(j, i)
    return unpickle_vtkMatrix4x4, (gets, data,)


def unpickle_vtkMatrix4x4(gets, data):
    instance = vtk.vtkMatrix4x4()
    vtkInstance_sets(instance, gets)
    for j in range(4):
        for i in range(4):
            instance.SetElement(j, i, data[i, j])
    return instance


def pickle_vtkPolyData(instance: vtk.vtkPolyData):
    gets = vtkInstance_gets(instance)
    if instance.GetNumberOfPoints() == 0:
        data = bytes()
    else:
        with tempfile.TemporaryDirectory() as p:
            p = pathlib.Path(p) / '.vtp'
            vmat.pdSaveFile_XML(instance, str(p))
            data = p.read_bytes()
    return unpickle_vtkPolyData, (gets, data,)


def unpickle_vtkPolyData(gets, data):
    if len(data) == 0:
        instance = vtk.vtkPolyData()
    else:
        with tempfile.TemporaryDirectory() as p:
            p = pathlib.Path(p) / '.vtp'
            p.write_bytes(data)
            instance = vmat.pdOpenFile_XML(str(p))
    vtkInstance_sets(instance, gets)
    return instance


def pickle_vtkFollower(instance: vtk.vtkFollower):
    gets = vtkInstance_gets(instance)
    data = []
    return unpickle_vtkFollower, (gets, data,)


def unpickle_vtkFollower(gets, data):
    instance = vtk.vtkFollower()
    vtkInstance_sets(instance, gets)
    return instance


def pickle_vtkScalarBarActor(instance: vtk.vtkScalarBarActor):
    gets = vtkInstance_gets(instance)
    data = []
    return unpickle_vtkScalarBarActor, (gets, data,)


def unpickle_vtkScalarBarActor(gets, data):
    instance = vtk.vtkScalarBarActor()
    vtkInstance_sets(instance, gets)
    return instance


def pickle_QImage(instance: QImage):
    ba = QByteArray()
    buffer = QBuffer(ba)
    buffer.open(QIODevice.WriteOnly)
    instance.save(buffer, 'PNG')
    return unpickle_QImage, (ba.data(), instance.format().name.decode())


def unpickle_QImage(data, format):
    ba = QByteArray(data)
    instance = QImage.fromData(ba, format)
    return instance


copyreg.pickle(vtk.vtkImageData, pickle_vtkImageData)
copyreg.pickle(vtk.vtkLookupTable, pickle_vtkLookupTable)
copyreg.pickle(vtk.vtkMatrix4x4, pickle_vtkMatrix4x4)
copyreg.pickle(vtk.vtkPolyData, pickle_vtkPolyData)
copyreg.pickle(vtk.vtkFollower, pickle_vtkFollower)
copyreg.pickle(vtk.vtkScalarBarActor, pickle_vtkScalarBarActor)
copyreg.pickle(QImage, pickle_QImage)


def contains_zh_CN(text) -> bool:
    """判断字符串是否包含中文"""
    return text.encode() != text.encode('cp936')

