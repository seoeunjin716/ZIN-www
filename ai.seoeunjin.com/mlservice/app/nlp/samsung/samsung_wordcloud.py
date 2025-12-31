from __future__ import annotations

import pathlib
from typing import Iterable, List, Optional

import nltk
from nltk import FreqDist
from nltk.tag import pos_tag
from nltk.tokenize import RegexpTokenizer
from wordcloud import WordCloud
from konlpy.tag import Okt
from pathlib import Path
import re
import pandas as pd
from icecream import ic
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize


class SamsungWordCloud:
    """
    Generate a word cloud from the Gutenberg "Emma" corpus.

    The class downloads required NLTK resources on first use and
    produces a word cloud image file based on proper nouns frequency.
    """

    def __init__(self, quiet: bool = True):
        """
        초기화 메서드
        
        Args:
            quiet: NLTK 다운로드 시 출력 여부 (기본값: True)
        """
        # JAVA_HOME 환경 변수 설정 (konlpy가 Java를 필요로 함)
        import os
        import subprocess
        import winreg
        
        # JAVA_HOME이 설정되지 않았거나 잘못된 경우
        java_home = os.environ.get('JAVA_HOME', '')
        if not java_home or not os.path.exists(os.path.join(java_home, 'bin', 'java.exe')):
            # Java 경로 자동 탐지
            try:
                # 1. 레지스트리에서 Java 경로 찾기
                java_paths = []
                try:
                    # JavaSoft 레지스트리 키 확인
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\JavaSoft\Java Runtime Environment")
                    try:
                        current_version = winreg.QueryValueEx(key, "CurrentVersion")[0]
                        version_key = winreg.OpenKey(key, current_version)
                        java_home_reg = winreg.QueryValueEx(version_key, "JavaHome")[0]
                        if os.path.exists(java_home_reg):
                            java_paths.append(java_home_reg)
                        winreg.CloseKey(version_key)
                    except:
                        pass
                    winreg.CloseKey(key)
                except:
                    pass
                
                # 2. where 명령으로 java.exe 경로 찾기
                result = subprocess.run(['where', 'java'], capture_output=True, text=True, shell=True)
                if result.returncode == 0:
                    java_path = result.stdout.strip().split('\n')[0]
                    
                    # 일반적인 JDK 경로들 확인 (우선순위 순)
                    if 'javapath' in java_path:
                        # Oracle Java의 경우 - 일반 경로 확인
                        possible_paths = [
                            r'C:\Program Files\Java\jdk-21',
                            r'C:\Program Files\Java\jdk-17',
                            r'C:\Program Files\Java\jdk-11',
                            r'C:\Program Files\Eclipse Adoptium\jdk-21.0.8-hotspot',
                            r'C:\Program Files\Eclipse Adoptium\jdk-21',
                            r'C:\Program Files\Eclipse Adoptium\jdk-17',
                            r'C:\Program Files\Microsoft\jdk-21',
                            r'C:\Program Files\Microsoft\jdk-17',
                        ]
                        java_paths.extend(possible_paths)
                    else:
                        # 직접 경로에서 추출
                        jdk_root = os.path.dirname(os.path.dirname(java_path))
                        java_paths.insert(0, jdk_root)
                
                # 경로 확인 및 설정
                for path in java_paths:
                    if os.path.exists(path):
                        # jvm.dll 확인 (server 또는 client)
                        jvm_dll_server = os.path.join(path, 'bin', 'server', 'jvm.dll')
                        jvm_dll_client = os.path.join(path, 'bin', 'client', 'jvm.dll')
                        if os.path.exists(jvm_dll_server) or os.path.exists(jvm_dll_client):
                            os.environ['JAVA_HOME'] = path
                            break
                        # jvm.dll이 없는 경우 java.exe만 확인
                        elif os.path.exists(os.path.join(path, 'bin', 'java.exe')):
                            os.environ['JAVA_HOME'] = path
                            break
            except Exception as e:
                import warnings
                warnings.warn(f"JAVA_HOME 자동 설정 실패: {e}. JAVA_HOME 환경 변수를 수동으로 설정해주세요.")
        
        # NLTK 데이터 다운로드 (word_tokenize 사용을 위해 필요)
        try:
            nltk.download('punkt', quiet=quiet)
            nltk.download('punkt_tab', quiet=quiet)  # 최신 NLTK 버전에서 필요
            nltk.download('stopwords', quiet=quiet)
        except Exception as e:
            # 다운로드 실패 시 경고만 출력하고 계속 진행
            import warnings
            warnings.warn(f"NLTK 리소스 다운로드 중 오류 발생: {e}")
        
        # Konlpy Okt 초기화 (에러 처리 추가)
        try:
            self.okt = Okt()
        except Exception as e:
            import warnings
            warnings.warn(f"Konlpy Okt 초기화 중 오류 발생: {e}")
            raise

    def text_process(self, save: bool = True, output_path: str = None):
        """
        전체 텍스트 처리 파이프라인을 실행합니다.
        
        Args:
            save: 워드클라우드 저장 여부 (기본값: True)
            output_path: 저장할 파일 경로 (기본값: None, 기본 경로 사용)
        
        Returns:
            dict: 처리 결과
        """
        freq_txt = self.find_freq()
        
        if save:
            # 워드클라우드 저장
            saved_path = self.save_wordcloud(output_path=output_path)
            return {
                '전처리 결과': '완료',
                'freq_txt': freq_txt,
                'wordcloud_saved': True,
                'file_path': saved_path
            }
        else:
            # 워드클라우드만 표시
            self.draw_wordcloud()
            return {
                '전처리 결과': '완료',
                'freq_txt': freq_txt
            }
    
    def read_file(self):
        try:
            self.okt.pos("삼성전자 글로벌센터 전자사업부", stem=True)
        except:
            pass  # 초기화 확인용, 실패해도 계속 진행
        # 상대 경로를 절대 경로로 변환
        base_dir = Path(__file__).parent.parent
        fname = base_dir / 'data' / 'kr-Report_2018.txt'
        if not fname.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {fname}")
        with open(fname, 'r', encoding='utf-8') as f:
            self.text = f.read()
        return self.text

    def extract_hangeul(self, text: str):
        temp = text.replace('\n', ' ')
        tokenizer = re.compile('[^ ㄱ-ㅣ가-힣]+')
        return tokenizer.sub('',temp)

    def change_token(self, texts):
        return word_tokenize(texts)

    def extract_noun(self):
        # 삼성전자의 스마트폰은 -> 삼성전자 스마트폰
        noun_tokens = []
        tokens = self.change_token(self.extract_hangeul(self.read_file()))
        for i in tokens:
            pos = self.okt.pos(i)
            temp = [j[0] for j in pos if j[1] == 'Noun']
            if len(''.join(temp)) > 1 :
                noun_tokens.append(''.join(temp))
        texts = ' '.join(noun_tokens)
        ic(texts[:100])
        return texts
    def read_stopword(self):
        try:
            self.okt.pos("삼성전자 글로벌센터 전자사업부", stem=True)
        except:
            pass  # 초기화 확인용, 실패해도 계속 진행
        # 상대 경로를 절대 경로로 변환
        base_dir = Path(__file__).parent.parent
        fname = base_dir / 'data' / 'stopwords.txt'
        if not fname.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {fname}")
        with open(fname, 'r', encoding='utf-8') as f:
            stopwords = f.read()
        return stopwords

    def remove_stopword(self):
        texts = self.extract_noun()
        tokens = self.change_token(texts)
        # print('------- 1 명사 -------')
        # print(texts[:30])
        stopwords_text = self.read_stopword()
        # stopwords를 줄바꿈으로 분리하여 리스트로 변환
        stopwords = set(stopwords_text.strip().split('\n'))
        # print('------- 2 스톱 -------')
        # print(stopwords[:30])
        # print('------- 3 필터 -------')
        texts = [text for text in tokens
                 if text not in stopwords]
        # print(texts[:30])
        return texts
    def find_freq(self):
        texts = self.remove_stopword()
        freqtxt = pd.Series(dict(FreqDist(texts))).sort_values(ascending=False)
        ic(freqtxt[:30])
        return freqtxt
    def draw_wordcloud(self):
        texts = self.remove_stopword()
        wcloud = WordCloud('./data/D2Coding.ttf', relative_scaling=0.2,
                           background_color='white').generate(" ".join(texts))
        plt.figure(figsize=(12, 12))
        plt.imshow(wcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()
    
    def save_wordcloud(self, output_path: str = None):
        """
        워드클라우드를 생성하고 지정된 경로에 저장합니다.
        
        Args:
            output_path: 저장할 파일 경로 (기본값: app/nlp/save/samsung_wordcloud.png)
        
        Returns:
            Path: 저장된 파일의 경로
        """
        texts = self.remove_stopword()
        
        # 상대 경로를 절대 경로로 변환
        base_dir = Path(__file__).parent.parent
        font_path = base_dir / 'data' / 'D2Coding.ttf'
        
        # 폰트 파일 존재 확인
        if not font_path.exists():
            raise FileNotFoundError(f"폰트 파일을 찾을 수 없습니다: {font_path}")
        
        # output_path가 제공되지 않으면 기본 경로 사용
        if output_path is None:
            # app/nlp/save 경로로 저장
            save_dir = base_dir / 'save'
            save_dir.mkdir(parents=True, exist_ok=True)
            save_path = save_dir / 'samsung_wordcloud.png'
            # 저장 경로 로깅
            import logging
            logging.info(f"워드클라우드 저장 경로: {save_path}")
        else:
            save_path = Path(output_path)
            # 부모 디렉토리가 없으면 생성
            save_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 텍스트가 비어있는지 확인
        if not texts or len(texts) == 0:
            raise ValueError("워드클라우드를 생성할 텍스트가 없습니다.")
        
        # 워드클라우드 생성
        try:
            wcloud = WordCloud(
                font_path=str(font_path),
                relative_scaling=0.2,
                background_color='white',
                width=1200,
                height=1200
            ).generate(" ".join(texts))
        except Exception as e:
            raise RuntimeError(f"워드클라우드 생성 중 오류 발생: {str(e)}")
        
        # 워드클라우드 저장
        try:
            wcloud.to_file(str(save_path))
        except Exception as e:
            raise RuntimeError(f"워드클라우드 저장 중 오류 발생: {str(e)}")
        
        return save_path