import os
import datetime
import csv
from enum import Enum

class GET(Enum):
    ALL = 0
    NAME = 1
    DESCRIPTION = 2
    START_TIME = 3
    END_TIME = 4
    START_TIMER = 5
    END_TIMER = 6

class TSV_Read():
    def __init__(self, file:str):
        extension = os.path.splitext(file)[-1]
        if not(os.path.exists(file)):
            raise ImportError(f"File {file} does not exist!")
        if(extension!=".tsv"):
            raise ImportError("File has to be .tsv")
        currentline = 0
        tsv_file = csv.reader(open(file), delimiter="\t")
        for line in tsv_file:
            currentline = currentline+1
            try: int(line[0])
            except:
                if not(line[0].startswith("-")):
                    raise ValueError(f"Cannot read Line {currentline} of {file}")
        self.file = file

    def _is_today(self, line:str):
        if(line.startswith("-")): #Ignore if Line starts with -
            return False
        if(datetime.datetime.now().weekday()==int(line)):
            return True
        return False
    def _get_info(self, value:GET, line:str):
        match value:
            case GET.ALL:
                return(line)
            case GET.NAME:
                return(line[1])
            case GET.DESCRIPTION:
                return(line[2])
            case GET.START_TIME:
                return datetime.timedelta(days=int(line[0]),hours=int(line[3][0:2]), minutes=int(line[3][2:4]))
            case GET.END_TIME:
                return datetime.timedelta(days=int(line[0]),hours=int(line[4][0:2]), minutes=int(line[4][2:4]))
            case GET.END_TIMER:
                return self._get_info(GET.END_TIME,line)-datetime.timedelta(days=datetime.datetime.now().weekday(),hours=datetime.datetime.now().hour,minutes=datetime.datetime.now().minute, seconds=datetime.datetime.now().second)
            case GET.START_TIMER:
                return self._get_info(GET.START_TIME,line)-datetime.timedelta(days=datetime.datetime.now().weekday(),hours=datetime.datetime.now().hour,minutes=datetime.datetime.now().minute, seconds=datetime.datetime.now().second)

    def all(self, Information:GET=GET.ALL):
        tsv_file = csv.reader(open(self.file), delimiter="\t")
        info_return = []
        for line in tsv_file:
            info_return.append(self._get_info(Information, line))
        return info_return
    def today(self, Information:GET=GET.ALL):
        tsv_file = csv.reader(open(self.file), delimiter="\t")
        info_return = []
        for line in tsv_file:
            if(self._is_today(line[0])):
                info_return.append(self._get_info(Information, line))
        return info_return
    def next(self, Information:GET=GET.ALL, Entire_Week:bool = False):
        tsv_file = csv.reader(open(self.file), delimiter="\t")
        for line in tsv_file:
            if(self._is_today(line[0])):
                currenttime = datetime.datetime.now().strftime("%H%M")
                if(currenttime < line[3]):
                    return self._get_info(Information, line)

        if(Entire_Week):
            tsv_file = csv.reader(open(self.file), delimiter="\t")
            for line in tsv_file:
                if not(line[0].startswith("-")):
                    if(int(line[0])>datetime.datetime.now().weekday()):
                            return self._get_info(Information, line)
        return False
    def current(self, Information:GET=GET.ALL):
        if isinstance(Information, GET):
            tsv_file = csv.reader(open(self.file), delimiter="\t")
            for line in tsv_file:
                if(self._is_today(line[0])):
                    currenttime = datetime.datetime.now().strftime("%H%M")
                    if(line[3] < currenttime and currenttime < line[4]):
                        return self._get_info(Information, line)
            return False
        else:
            raise TypeError("Argument must be of Type tsv_calendar.GET")