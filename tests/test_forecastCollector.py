import unittest

from forecastCollector import forecastCollector

def test_rowOfData():
    row = ("201812151700,20181216,1,56.0,31.1,0.25,0")
    data = forecastCollector.getWeatherData()
    assert row == data

