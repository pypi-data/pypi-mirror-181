import aio_pika
import numpy as np
import simplejson as json
from aio_pika import connect, Message, DeliveryMode, ExchangeType

from coinlib import helper, Registrar
from coinlib.BasicJobSessionStorage import BasicJobSessionStorage, LastSignalValue
from coinlib.WorkerJobProcess import WorkerJobProcess
from coinlib.data.DataTable import DataTable, LastEntry
from coinlib.helper import serializeDTO, to_trendline, trendline
from coinlib.feature.FeatureDTO import RabbitInfo
import pandas as pd
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import datetime
from operator import is_not
from functools import partial
from enum import Enum

class CrossMode(Enum):
    up=1
    down=2
    both=3


class BasicJob:
    def __init__(self, table: DataTable, inputs, storageManager = None):
        self.table = table
        if storageManager is None:
            storageManager = BasicJobSessionStorage()
        self._df = self.table.getDf()
        self.df = self.table.getDf()
        self.registrar = Registrar()
        self._storageManager = storageManager
        self._storageManager.setCurrentIndex(self.closeDate())
        self.inputs = inputs
        self.uniqueName = ""
        self._sessionInfo = self._storageManager.getStorage()
        self.features = self

        ## gets a signal data

    def getStub(self) -> stats.DataWorkerStub:
        pass

    def getWorker(self) -> WorkerJobProcess:
        pass

    def set(self, name, data, index=None):

        return self.table.setColumn(name, data, index)

    def getOutputCol(self):
        return "result"

    def result(self, resultList, colname=None, fillType="front", type=np.float):

        #if isinstance(resultList, np.ndarray):
        #    resultList = np.pad(resultList, (self.df.shape[0] - len(resultList), 0), 'constant', constant_values=(np.nan))

        #self.df[self.getOutputCol()] = resultList
        self.table.setColumn(self.getOutputCol(), resultList, pad=True, type=type)

        return self.table.column(self.getOutputCol())

    ## This method adds a signal
    def wasSignal(self, name, maxSecondsDistance=0, minSecondsDistance=0, logicId=None):
        lastValue = self._storageManager.getLastSignal(logicId if logicId is not None else self.getUniqueName(), name)

        if lastValue.found is True:
            if minSecondsDistance > 0:
                if lastValue.distanceSeconds > minSecondsDistance:
                    return True
            if maxSecondsDistance > 0:
                if lastValue.distanceSeconds < maxSecondsDistance:
                    return True

        return False

    ## This method adds a signal
    def lastSignal(self, name, logicId=None) -> LastSignalValue:

        return self._storageManager.getLastSignal(logicId if logicId is not None else self.getUniqueName(), name)

    ## This method adds a signal
    def signal(self, name, data=None, index=-1, logicId=None) -> LastSignalValue:

        if data is not None:
            return self._storageManager.setSignal(logicId if logicId is not None else self.getUniqueName(), name, data)

        return self._storageManager.getSignal(logicId if logicId is not None else self.getUniqueName(), name)

    def getInputValue(self, input):

        if isinstance(input, dict):
            if "value" in input:
                return input["value"]

        return input


    def getNow(self, name):
        return self.current(name)

    def getCurrent(self, name):
        return self.current(name)

    def logger(self):
        return self.registrar.logger

    def functions(self):
        worker = self.getWorker()

        return worker.getIndicators()

    def isOfflineMode(self):
        worker = self.getWorker()

        return worker.isOfflineWorker()

    def getTrendlines(self, name, history_in_sec=None):
        """
        This method returns you all the trendlines that are currently "in your time" (So the
        trendlines that are going minimum to current position - history_in_sec)
        """
        trendlines = self.get(name)

        if trendlines is not None:

            trendlines = trendlines[trendlines != np.array(None)]
            trendlines = [to_trendline(x) for x in trendlines]

            if len(trendlines) > 0:
                date = self.date()

                if history_in_sec is not None:
                    date = date - datetime.timedelta(seconds=history_in_sec)

                found_lines = []
                for t in trendlines:

                    if t["x1"] > date:
                        found_lines.append(t)


                return found_lines

        return []

    def cross_up_stable(self, line1, line2, index):
        return self.cross_stable(line1, line2, mode=CrossMode.up, index=index)
    def cross_down_stable(self, line1, line2, index):
        return self.cross_stable(line1, line2, mode=CrossMode.down, index=index)
    def cross_stable(self, line1, line2, index, mode=CrossMode):
        return self.cross(line1, line2, mode=mode, index=index, keptStable=True)
    def cross_down(self, line1, line2, index=-1):
        return self.cross(line1, line2, mode=CrossMode.down, index=index)
    def cross_up(self, line1, line2, index=-1):
        return self.cross(line1, line2, mode=CrossMode.up, index=index)
    def cross(self, line1, line2, mode=CrossMode, index=-1, keptStable=False):
        """
        This method calculates a cross between 2 lines.  (line1 X line2).

        mode = Mode can be up, down, both
        index = How far away from now should we search - default is "-1" than the cross is straight here
        keptStable = Checks if there was a cross and the data kept stable on that side
        """
        crossFound = None
        wasStable = 0
        i = index
        while i < 0:

            d1 = self.get(line1, -1+i)
            d2 = self.get(line2, -1+i)
            d1_1 = self.get(line1, -2+i)
            d2_2 = self.get(line2, -2+i)

            if crossFound is None or keptStable is False:
                if mode == CrossMode.up or mode == CrossMode.both:
                    if d1_1 < d2_2 and d1 > d2:
                        crossFound = i
                        wasStable = 0
                        direction = CrossMode.up
                        if keptStable is False:
                            return direction
                        continue
                if mode == CrossMode.down or mode == CrossMode.both:
                    if d1_1 > d2_2 and d1 < d2:
                        crossFound = i
                        wasStable = 0
                        direction = CrossMode.down
                        if keptStable is False:
                            return direction
                        continue

            if crossFound is not None and keptStable is True:
                if direction == CrossMode.down:
                    if d1 > d2:
                        crossFound = None
                        i = i - 1
                        wasStable = 0
                    else:
                        wasStable = wasStable + 1
                if direction == CrossMode.up:
                    if d1 < d2:
                        wasStable = 0
                        i = i - 1
                        crossFound = None
                    else:
                        wasStable = wasStable + 1


            i = i + 1

        if keptStable is False:
            if crossFound is not None:
                return direction
        else:
            if crossFound is not None and wasStable >= (-index-1):
                return direction

        return False

    def get(self, name, index=None, limit=None, filterNone = False, replaceNone=None):

        data = None
        try:
                maybe_col_name = name
                if ":" in maybe_col_name:
                    maybe_col_name = maybe_col_name.split(":")[0]

                # if its a key of inputs - lets export the right column
                if maybe_col_name in self.inputs:
                    if isinstance(self.inputs[maybe_col_name], str):
                        return self.get(self.getInputValue(self.inputs[maybe_col_name]), index, filterNone, replaceNone, limit)
                    if self.inputs[maybe_col_name]["type"] == "dataInput":
                        return self.get(self.getInputValue(self.inputs[maybe_col_name]["value"]), index, filterNone, replaceNone, limit)

                data = None
                if maybe_col_name + ":y" in self.table.columns:
                    data = self.table.column(maybe_col_name + ":y", index, limit=limit)
                if maybe_col_name + ":marker" in self.table.columns:
                    data = self.table.column(maybe_col_name + ":marker", index, limit=limit)
                elif "additionalData."+maybe_col_name in self.table.columns:
                    data = self.table.column("additionalData."+maybe_col_name, index, limit=limit)
                elif maybe_col_name + ":close" in self.table.columns:
                    data = self.table.column(maybe_col_name + ":close", index, limit=limit)
                elif name in self.table.columns:
                    data = self.table.column(name, index, limit=limit)
                elif "stats."+maybe_col_name in self.table.columns:
                    data = self.table.column("stats."+maybe_col_name, index, limit=limit)
                elif "stats." + name in self.table.columns:
                    data = self.table.column("stats." + name, index, limit=limit)
                elif maybe_col_name in self.inputs:
                    data = self.inputs[name]
        except Exception as e:
            self.logger().error(e)

        if data is not None and (filterNone or replaceNone):
            if isinstance(data, list) or isinstance(data, (np.ndarray, np.generic)):
                if len(data) > 1:
                    data = [i if i is not None and (((type(i) != str and not np.isnan(i)) or
                                  (type(i) == str and len(i) > 0))) else None for i in data]
                    if filterNone is True:
                        data = [i for i in data if i is not None]
                    if replaceNone is not None:
                        data = [0 if i is None else i for i in data]
                else:
                    return data[0]
            else:
                if np.isnan(data):
                    data = None


        return data

    def getAsCandle(self, name, index=None) -> {"open": [], "high": [], "low": [], "close": [], "volume": []}:

        data = {
            "open": self.getAsArray(name+":open", index),
            "high": self.getAsArray(name+":high", index),
            "low": self.getAsArray(name+":low", index),
            "close": self.getAsArray(name+":close", index),
            "volume": self.getAsArray(name+":volume", index),
        }

        return data

    def getAsArray(self, name, index=None, type=float):

        data = self.get(name, index=index)

        # filter data and remove nans in the beginning

        if data is not None and len(data) > 0:
            if data[0] is None or np.isnan(data[0]):
                index = 0
                for f in data:
                    if f is None or np.isnan(f):
                        index = index + 1
                    else:
                        break
                data = data[index:]
        float_data = np.array(data, dtype=float)
        return float_data

    ## This method combines all params and combine as a dataframe
    def df(self):
        return self.df

    def columns(self):
        return self.table.columns

    def getColumns(self):
        return self.table.columns

    def last(self, name, maxDistance=100, filterNone=False, replaceNone=None) -> LastEntry:

        data = None
        try:
            maybe_col_name = name
            if ":" in maybe_col_name:
                maybe_col_name = maybe_col_name.split(":")[0]

            # if its a key of inputs - lets export the right column
            if maybe_col_name in self.inputs:
                if isinstance(self.inputs[maybe_col_name], str):
                    return self.last(self.getInputValue(self.inputs[maybe_col_name]))
                if self.inputs[maybe_col_name]["type"] == "dataInput":
                    return self.last(self.getInputValue(self.inputs[maybe_col_name]["value"]))

            data = None
            if maybe_col_name + ":y" in self.table.columns:
                data = self.table.getLastEntry(maybe_col_name + ":y")
            elif name in self.table.columns:
                data = self.table.getLastEntry(name, maxLength=maxDistance)
            elif "additionalData." + maybe_col_name in self.table.columns:
                data = self.table.getLastEntry("additionalData." + maybe_col_name, maxLength=maxDistance)
            elif maybe_col_name + ":close" in self.table.columns:
                data = self.table.getLastEntry(maybe_col_name + ":close", maxLength=maxDistance)
            elif "stats." + maybe_col_name in self.table.columns:
                data = self.table.getLastEntry("stats." + maybe_col_name, maxLength=maxDistance)
            elif "stats." + name in self.table.columns:
                data = self.table.getLastEntry("stats." + name, maxLength=maxDistance)

        except Exception as e:
            self.logger().error(e)

        if data is not None:
            return data

        return data

    def getNow_date(self):
        dt = self.table.getLast("datetime")
        return dt

    def current(self, name):
        return self.get(name, index=-1)

    def statistic(self, name="r_master"):

        return self.current("stats."+name)

    def lastStatistic(self, name="r_master"):

        return self.last("stats."+name)

    def setVar(self, name, data, logicId=None):

        return self.var(name, data, logicId=logicId)

    def setUniqueName(self, name):
        self.uniqueName = name
        return name

    def getUniqueName(self):
        return self.uniqueName

    def price(self, chart="chart1"):
        return self.table.getLast(chart+".main:close")

    def isNaN(self, num):
        return num != num

    def additional(self, name):

        index = -1

        if "additionalData." + name in self.table.columns:
            data = self.table.lastElement("additionalData." + name)
            if self.isNaN(data):
                return None
            return data

        return None

    def date(self):
        date = pd.to_datetime(self.table.index[-1])
        return date

    def closeDate(self):
        if len(self.table.index) > 0:
            date = pd.to_datetime(self.table.index[-1])
            return date
        return None

    def time(self):
        if len(self.table.index) > 0:
            date = pd.to_datetime(self.table.index[-1])
            return date
        return None

    ## This method adds a signal
    def var(self, name, data=None, logicId=None):

        if data is not None:
            return self._storageManager.setVar(logicId if logicId is not None else self.getUniqueName(), name, data)

        return self._storageManager.getVar(logicId if logicId is not None else self.getUniqueName(), name)

    def destroy(self):

        pass