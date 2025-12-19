from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_safe
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Performance, BoxOfficeRanking, GENRE_CODE_MAPPING, GENRE_DISPLAY_ORDER
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


# Create your views here.
@require_safe
def index(request):
    # 페이지네이션 적용 (한 페이지에 50개씩)
    performances_list = Performance.objects.all().order_by('-prfpdfrom')  # 최신순 정렬
    paginator = Paginator(performances_list, 50)  # 50개씩 페이지 분할

    page_number = request.GET.get('page', 1)
    performances = paginator.get_page(page_number)

    # 모든 장르 목록 가져오기 (중복 제거)
    genres = Performance.objects.values_list('genrenm', flat=True).distinct().order_by('genrenm')

    # 카카오맵 API 키 전달
    kakao_api_key = os.getenv('KAKAO_MAP_API_KEY', '')

    context = {
        'performances': performances,
        'genres': genres,
        'kakao_api_key': kakao_api_key,
    }
    return render(request, 'performance/index.html', context)


def filter_genre(request):
    genre = request.GET.get('genre')
    search_query = request.GET.get('search', '')

    # 기본 쿼리셋
    performances = Performance.objects.all()

    # 장르 필터링
    if genre:
        performances = performances.filter(genrenm=genre)

    # 검색어 필터링 (공연명 또는 장소명에 포함)
    if search_query:
        performances = performances.filter(
            Q(prfnm__icontains=search_query) |
            Q(fcltynm__icontains=search_query)
        )

    # JSON 형태로 데이터 반환
    performances_data = []
    for performance in performances:
        performances_data.append({
            'mt20id': performance.mt20id,
            'prfnm': performance.prfnm,
            'prfpdfrom': str(performance.prfpdfrom) if performance.prfpdfrom else None,
            'prfpdto': str(performance.prfpdto) if performance.prfpdto else None,
            'fcltynm': performance.fcltynm,
            'poster': performance.poster,
            'area': performance.area,
            'genrenm': performance.genrenm,
            'prfstate': performance.prfstate,
        })

    return JsonResponse({'performances': performances_data})


@require_safe
def recommended(request):
    return render(request, 'performance/recommended.html')


@require_safe
def landing(request):
    """랜딩 페이지 - 박스오피스 랭킹"""

    # 가장 최근 랭킹 데이터의 날짜 조회
    latest_ranking = BoxOfficeRanking.objects.order_by('-ranking_date').first()

    if latest_ranking:
        latest_date = latest_ranking.ranking_date
    else:
        latest_date = timezone.now().date()

    # 장르 정보 구성
    genres = []
    for genre_code in GENRE_DISPLAY_ORDER:
        genres.append({
            'code': genre_code,
            'name': GENRE_CODE_MAPPING.get(genre_code, genre_code),
        })

    context = {
        'genres': genres,
        'latest_date': latest_date,
    }

    return render(request, 'performance/landing.html', context)


@require_safe
def boxoffice_genre(request):
    """장르별 박스오피스 데이터 조회 (AJAX)"""

    genre_code = request.GET.get('genre', 'BBBC')  # 기본값: 뮤지컬
    print(genre_code)
    # 가장 최근 데이터 조회
    rankings = BoxOfficeRanking.objects.filter(
        genre_code=genre_code
    ).select_related('performance').order_by(
        '-ranking_date', 'rank'
    )[:20]  # 상위 20개

    # 공연 종료 필터링
    today = timezone.now().date()
    active_rankings = []

    for ranking in rankings:
        perf = ranking.performance

        # 공연 종료일 확인
        if perf.prfpdto:
            # openrun이 'Y'이거나 종료일이 오늘 이후인 경우만
            if perf.openrun == 'Y' or perf.prfpdto >= today:
                active_rankings.append(ranking)
        else:
            # 종료일 정보 없으면 포함
            active_rankings.append(ranking)

    # JSON 데이터 구성
    data = []
    for ranking in active_rankings:
        perf = ranking.performance
        data.append({
            'rank': ranking.rank,
            'mt20id': perf.mt20id,
            'prfnm': perf.prfnm,
            'poster': perf.poster or 'https://via.placeholder.com/200x280?text=No+Poster',
            'fcltynm': perf.fcltynm or '',
            'prfpdfrom': str(perf.prfpdfrom) if perf.prfpdfrom else '',
            'prfpdto': str(perf.prfpdto) if perf.prfpdto else '',
            'area': ranking.area or perf.area or '',
            'genrenm': perf.genrenm or '',
        })

    return JsonResponse({
        'success': True,
        'genre': GENRE_CODE_MAPPING.get(genre_code, genre_code),
        'data': data,
        'total': len(data),
    })


@require_safe
def performance_detail(request, mt20id):
    """공연 상세 페이지"""
    # 쿼리 최적화: select_related, prefetch_related 사용
    performance = get_object_or_404(
        Performance.objects.select_related('detail').prefetch_related('intro_images'),
        mt20id=mt20id
    )

    # 상세 정보 조회 (없을 수도 있음)
    detail = performance.get_detail()

    # 소개 이미지 조회
    intro_images = performance.intro_images.all()

    # 카카오맵 API 키
    kakao_api_key = os.getenv('KAKAO_MAP_API_KEY', '')

    context = {
        'performance': performance,
        'detail': detail,
        'intro_images': intro_images,
        'has_detail': performance.has_detail,
        'kakao_api_key': kakao_api_key,
    }

    return render(request, 'performance/detail.html', context)
