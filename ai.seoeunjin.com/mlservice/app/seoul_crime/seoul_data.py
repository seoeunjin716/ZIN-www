from dataclasses import dataclass
from pathlib import Path
import pandas as pd

@dataclass
class SeoulData(object): 

    _fname: str = '' # file name
    _dname: str = str(Path(__file__).parent / "data") # data path (절대 경로)
    _sname: str = str(Path(__file__).parent / "save") # save path (절대 경로)
    _cctv: pd.DataFrame = None
    _crime: pd.DataFrame = None
    _pop: pd.DataFrame = None
    
    def __post_init__(self):
        """데이터 로드"""
        # CCTV 데이터 로드
        cctv_path = Path(self._dname) / "cctv.csv"
        if cctv_path.exists():
            self._cctv = pd.read_csv(cctv_path)
        
        # Crime 데이터 로드
        crime_path = Path(self._dname) / "crime.csv"
        if crime_path.exists():
            self._crime = pd.read_csv(crime_path)
        
        # Population 데이터 로드
        pop_path = Path(self._dname) / "pop.xls"
        if pop_path.exists():
            self._pop = pd.read_excel(pop_path)

    @property
    def fname(self) -> str: return self._fname

    @fname.setter
    def fname(self, fname): self._fname = fname

    @property
    def dname(self) -> str: return self._dname

    @dname.setter
    def dname(self, dname): self._dname = dname

    @property
    def sname(self) -> str: return self._sname

    @sname.setter
    def sname(self, sname): self._sname = sname

    @property
    def cctv(self) -> pd.DataFrame: return self._cctv

    @cctv.setter
    def cctv(self, cctv): self._cctv = cctv

    @property
    def crime(self) -> pd.DataFrame: return self._crime

    @crime.setter
    def crime(self, crime): self._crime = crime

    @property
    def pop(self) -> pd.DataFrame: return self._pop

    @pop.setter
    def pop(self, pop): self._pop = pop

