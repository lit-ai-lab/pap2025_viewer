import os
import re
from typing import Dict

def clean_text(text: str) -> str:
    """
    텍스트 전처리 함수 - 공백, 특수문자 등 정리
    """
    text = text.replace("\n", " ").replace("\r", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def parse_hwp_to_text(file_path: str) -> str:
    """
    .hwp 파일을 텍스트로 변환 (hwp5txt 사용 가정)
    예: hwp5txt 또는 pyhwp 설치 필요
    """
    try:
        import subprocess
        result = subprocess.run(['hwp5txt', file_path], capture_output=True, text=True)
        return clean_text(result.stdout)
    except Exception as e:
        raise RuntimeError(f"HWP parsing failed: {e}")

def extract_analysis_info(text: str) -> Dict[str, str]:
    """
    분석 정보 추출 - 간단한 패턴 기반
    """
    result = {}

    # 예시: 특정 키워드 기반으로 분석 추출
    if "위반" in text:
        result["위반사항"] = "위반사항이 발견되었습니다."
    if "조치" in text:
        result["조치사항"] = "조치 내용이 존재합니다."

    # 더 많은 키워드 또는 패턴 기반 분석이 가능
    return result

def analyze_viewer_text(text: str) -> Dict[str, str]:
    """
    전체 분석 처리: 원문 -> 정제 -> 분석정보 반환
    """
    cleaned = clean_text(text)
    return extract_analysis_info(cleaned)
