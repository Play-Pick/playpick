import time
import requests
import xml.etree.ElementTree as ET
from typing import Dict, Optional, List, Callable
from datetime import datetime
from dateutil.relativedelta import relativedelta

class KopisAPIClient:
    """KOPIS API 클라이언트"""

    BASE_URL = "http://www.kopis.or.kr/openApi/restful/pblprfr"
    BOXOFFICE_URL = "http://kopis.or.kr/openApi/restful/boxoffice"  # 예매상황판 API (www 없음)
    RATE_LIMIT_DELAY = 0.15  # 초 (1초당 6.67회 = 10회 미만)
    MAX_ROWS = 100
    TIMEOUT = 10
    MAX_RETRIES = 3

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.last_request_time = 0

    def _wait_for_rate_limit(self):
        """Rate limit 준수를 위한 대기"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request < self.RATE_LIMIT_DELAY:
            sleep_time = self.RATE_LIMIT_DELAY - time_since_last_request
            time.sleep(sleep_time)

        self.last_request_time = time.time()

    def fetch_performances(
        self,
        start_date: str,
        end_date: str,
        page: int = 1,
        prfstate: Optional[str] = None
    ) -> Dict:
        """
        공연 정보 조회

        Args:
            start_date: 시작일 (YYYYMMDD)
            end_date: 종료일 (YYYYMMDD)
            page: 페이지 번호
            prfstate: 공연 상태 코드 (선택)

        Returns:
            {
                'total': int,           # 전체 건수
                'performances': List,   # 공연 리스트
                'has_more': bool        # 다음 페이지 존재 여부
            }
        """
        # Rate limit 체크
        self._wait_for_rate_limit()

        # API 파라미터 구성
        params = {
            'service': self.api_key,
            'stdate': start_date,
            'eddate': end_date,
            'cpage': page,
            'rows': self.MAX_ROWS,
        }

        if prfstate:
            params['prfstate'] = prfstate

        # 재시도 로직을 포함한 요청
        return self._retry_request(self._make_request, params)

    def _make_request(self, params: Dict) -> Dict:
        """실제 API 요청 수행"""
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=self.TIMEOUT)
            response.raise_for_status()

            # XML 파싱
            return self._parse_xml_response(response.content)

        except requests.RequestException as e:
            raise Exception(f"API 호출 실패: {str(e)}")
        except ET.ParseError as e:
            raise Exception(f"XML 파싱 실패: {str(e)}")

    def _parse_xml_response(self, xml_content: bytes) -> Dict:
        """XML 응답 파싱"""
        root = ET.fromstring(xml_content)

        # 전체 건수 추출
        total_element = root.find('.//db')
        total = 0
        performances = []

        # 모든 <db> 요소 파싱
        for db in root.findall('db'):
            perf_data = {}
            for child in db:
                perf_data[child.tag] = child.text
            performances.append(perf_data)
            total += 1

        # 다음 페이지 존재 여부 확인
        has_more = len(performances) >= self.MAX_ROWS

        return {
            'total': total,
            'performances': performances,
            'has_more': has_more
        }

    def fetch_all_performances(
        self,
        start_date: str,
        end_date: str,
        callback: Optional[Callable[[int, int, int], None]] = None
    ) -> List[Dict]:
        """
        특정 기간의 모든 공연 정보 조회 (페이지네이션 자동 처리)

        Args:
            start_date: 시작일 (YYYYMMDD)
            end_date: 종료일 (YYYYMMDD)
            callback: 진행 상황 콜백 함수(page, total_pages, performances_count)

        Returns:
            모든 공연 정보 리스트
        """
        all_performances = []
        page = 1
        total_pages = 1  # 초기값

        while True:
            result = self.fetch_performances(start_date, end_date, page)
            performances = result['performances']

            if not performances:
                break

            all_performances.extend(performances)

            # 첫 페이지에서 total_pages 계산
            if page == 1 and result['total'] > 0:
                total_pages = (result['total'] + self.MAX_ROWS - 1) // self.MAX_ROWS

            # 콜백 호출
            if callback:
                callback(page, total_pages, len(all_performances))

            # 다음 페이지가 없으면 종료
            if not result['has_more']:
                break

            page += 1

        return all_performances

    def _retry_request(self, func: Callable, *args, **kwargs) -> Dict:
        """재시도 로직"""
        last_exception = None

        for attempt in range(self.MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < self.MAX_RETRIES - 1:
                    # 지수 백오프: 1초, 2초, 4초
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                else:
                    # 마지막 시도에서도 실패하면 예외 발생
                    raise last_exception

        raise last_exception

    def fetch_boxoffice(
        self,
        date: str,  # YYYYMMDD
        genre_code: str,  # AAAA, BBBC 등
        period_type: str = 'week',  # day, week, month
    ) -> Dict:
        """
        예매상황판 데이터 조회

        Args:
            date: 조회 종료일 (YYYYMMDD) - 박스오피스 기준일
            genre_code: 장르 코드 (AAAA, BBBC, CCCA, GGGA, CCCD 등)
            period_type: 기간 유형 (day/week/month)

        Returns:
            {
                'boxoffice_list': List[Dict],  # 박스오피스 목록
                'base_date': str,  # 기준일
            }
        """
        self._wait_for_rate_limit()

        # 박스오피스는 과거 데이터이므로 stdate를 eddate보다 1개월 전으로 설정
        dt = datetime.strptime(date, "%Y%m%d")
        st_dt = dt - relativedelta(months=1)
        stdate = st_dt.strftime("%Y%m%d")


        params = {
            'service': self.api_key,
            'ststype': period_type,
            'stdate': stdate,
            'eddate': date,
            'catecode': genre_code,
        }

        return self._retry_request(self._make_boxoffice_request, params)

    def _make_boxoffice_request(self, params: Dict) -> Dict:
        """박스오피스 API 요청"""
        try:
            response = requests.get(
                self.BOXOFFICE_URL,
                params=params,
                timeout=self.TIMEOUT
            )
            response.raise_for_status()

            return self._parse_boxoffice_xml(response.content)

        except requests.RequestException as e:
            raise Exception(f"박스오피스 API 호출 실패: {str(e)}")
        except ET.ParseError as e:
            raise Exception(f"XML 파싱 실패: {str(e)}")

    def _parse_boxoffice_xml(self, xml_content: bytes) -> Dict:
        """박스오피스 XML 응답 파싱"""
        root = ET.fromstring(xml_content)

        base_date = None
        boxoffice_list = []

        # basedate 추출 (기준일)
        basedate_elem = root.find('.//basedate')
        if basedate_elem is not None and basedate_elem.text:
            base_date = basedate_elem.text

        # boxof 목록 파싱
        for boxof in root.findall('.//boxof'):
            item = {}
            for child in boxof:
                item[child.tag] = child.text
            boxoffice_list.append(item)

        return {
            'boxoffice_list': boxoffice_list,
            'base_date': base_date,
        }

    def fetch_performance_detail(self, mt20id: str) -> Dict:
        """
        공연 상세 정보 조회

        Args:
            mt20id: 공연 ID (예: "PF279020")

        Returns:
            {
                'mt20id': str,
                'prfnm': str,
                'prfcast': str,
                'prfcrew': str,
                'prfruntime': str,
                'prfage': str,
                'entrpsnm': str,
                'pcseguidance': str,
                'poster': str,
                'sty': str,
                'dtguidance': str,
                'genrenm': str,
                'prfpdfrom': str,
                'prfpdto': str,
                'fcltynm': str,
                'relates': List[Dict],  # 예매처 목록
                'styurls': List[str],   # 소개이미지 URL 목록
                # ... 기타 필드
            }
        """
        self._wait_for_rate_limit()

        url = f"{self.BASE_URL}/{mt20id}"
        params = {'service': self.api_key}

        return self._retry_request(self._make_detail_request, url, params)

    def _make_detail_request(self, url: str, params: Dict) -> Dict:
        """공연 상세 API 요청"""
        try:
            response = requests.get(url, params=params, timeout=self.TIMEOUT)
            response.raise_for_status()

            return self._parse_detail_xml(response.content)

        except requests.RequestException as e:
            raise Exception(f"공연 상세 API 호출 실패: {str(e)}")
        except ET.ParseError as e:
            raise Exception(f"XML 파싱 실패: {str(e)}")

    def _parse_detail_xml(self, xml_content: bytes) -> Dict:
        """공연 상세 XML 응답 파싱"""
        root = ET.fromstring(xml_content)
        db = root.find('db')

        if db is None:
            raise Exception("공연 정보를 찾을 수 없습니다")

        detail_data = {}

        # 기본 필드 파싱
        for child in db:
            if child.tag == 'relates':
                # 예매처 목록 파싱
                relates_list = []
                for relate in child.findall('relate'):
                    relate_data = {}
                    for field in relate:
                        relate_data[field.tag] = field.text
                    relates_list.append(relate_data)
                detail_data['relates'] = relates_list

            elif child.tag == 'styurls':
                # 소개이미지 URL 목록 파싱
                styurls_list = []
                for styurl in child.findall('styurl'):
                    if styurl.text:
                        styurls_list.append(styurl.text)
                detail_data['styurls'] = styurls_list

            else:
                detail_data[child.tag] = child.text

        return detail_data
