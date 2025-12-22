"""
추천 시스템 엔진 (Recommendation Engine)
하이브리드 추천 알고리즘 구현: 6개 점수 함수의 가중 합산
"""
from django.utils import timezone
from django.db.models import Q, Count
from datetime import timedelta
import math


class RecommendationEngine:
    """
    공연 추천 엔진
    사용자 로그, 취향, 위치 등 다양한 요소를 종합하여 개인화된 추천 제공
    """

    # 가중치 설정 (총합 = 1.0)
    WEIGHTS = {
        'f1_click': 0.20,         # 클릭/관심 로그 기반 (감소)
        'f2_preference': 0.15,    # 취향 매칭 (감소)
        'f3_location': 0.10,      # 위치 근접성 (감소)
        'f4_popularity': 0.15,    # 대중성
        'f5_recency': 0.10,       # 최신성
        'f6_collaborative': 0.10, # 협업 필터링 (감소)
        'f7_embedding': 0.20      # 임베딩 유사도 (NEW)
    }

    # 행동 유형별 점수 (f1 계산용)
    ACTION_SCORES = {
        'view': 1,
        'like': 3,
        'search': 2
    }

    # Time Decay 계수 (f1, f5 계산용)
    DECAY_LAMBDA = 0.95

    def __init__(self, user):
        """
        Args:
            user: 추천 대상 User 객체
        """
        self.user = user

    def get_recommendations(self, top_n=10):
        """
        사용자를 위한 Top-N 추천 목록 생성

        Returns:
            list: [
                {
                    'mt20id': 'PF123',
                    'score': 0.85,
                    'reason': 'location',  # 가장 높은 점수를 기록한 요인
                    'reason_text': '🏠 강남구 근처에서 공연해요!'
                },
                ...
            ]
        """
        from performances.models import Performance

        # 1. 후보군 필터링 (현재 공연 중이거나 예정인 공연)
        candidates = Performance.objects.filter(
            Q(prfstate='공연중') | Q(prfstate='공연예정')
        ).select_related('metric', 'embedding')

        # 2. 각 공연에 대해 점수 계산
        scored_performances = []
        for performance in candidates[:300]:  # 성능을 위해 최대 300개로 제한
            score_breakdown = self._calculate_score(performance)
            total_score = score_breakdown['total']

            if total_score > 0:
                scored_performances.append({
                    'performance': performance,
                    'score': total_score,
                    'breakdown': score_breakdown
                })

        # 3. 점수 기준 정렬
        scored_performances.sort(key=lambda x: x['score'], reverse=True)

        # 4. Top-N 추출 및 추천 사유 추가
        recommendations = []
        for item in scored_performances[:top_n]:
            performance = item['performance']
            breakdown = item['breakdown']

            # 가장 높은 점수를 기록한 요인 찾기
            reason, reason_text = self._get_top_reason(breakdown, performance)

            recommendations.append({
                'mt20id': performance.mt20id,
                'score': round(item['score'], 2),
                'reason': reason,
                'reason_text': reason_text
            })

        return recommendations

    def _calculate_score(self, performance):
        """
        개별 공연에 대한 종합 점수 계산

        Returns:
            dict: {
                'total': 0.85,
                'f1': 0.20,
                'f2': 0.15,
                ...
            }
        """
        f1 = self._f1_click_score(performance)
        f2 = self._f2_preference_score(performance)
        f3 = self._f3_location_score(performance)
        f4 = self._f4_popularity_score(performance)
        f5 = self._f5_recency_score(performance)
        f6 = self._f6_collaborative_score(performance)
        f7 = self._f7_embedding_score(performance)

        total = (
            self.WEIGHTS['f1_click'] * f1 +
            self.WEIGHTS['f2_preference'] * f2 +
            self.WEIGHTS['f3_location'] * f3 +
            self.WEIGHTS['f4_popularity'] * f4 +
            self.WEIGHTS['f5_recency'] * f5 +
            self.WEIGHTS['f6_collaborative'] * f6 +
            self.WEIGHTS['f7_embedding'] * f7
        )

        return {
            'total': total,
            'f1': f1,
            'f2': f2,
            'f3': f3,
            'f4': f4,
            'f5': f5,
            'f6': f6,
            'f7': f7
        }

    def _f1_click_score(self, performance):
        """
        [f1] 클릭/관심 로그 기반 점수 (Time Decay 적용)
        사용자가 과거에 본 공연과 유사한 장르/배우가 있으면 점수 부여
        """
        from ..models import UserLog

        # 최근 30일간의 로그만 고려
        recent_date = timezone.now() - timedelta(days=30)
        logs = UserLog.objects.filter(
            user=self.user,
            timestamp__gte=recent_date
        ).select_related('performance')

        if not logs.exists():
            return 0.0

        score = 0.0
        for log in logs:
            # 장르 일치 여부
            if log.performance.genrenm == performance.genrenm:
                # 행동 유형에 따른 기본 점수
                base_score = self.ACTION_SCORES.get(log.action_type, 1)

                # Time Decay 적용 (최근일수록 높은 점수)
                days_ago = (timezone.now() - log.timestamp).days
                decayed_score = base_score * (self.DECAY_LAMBDA ** days_ago)

                score += decayed_score

        # 0~1 사이로 정규화 (최대 10점으로 가정)
        return min(score / 10.0, 1.0)

    def _f2_preference_score(self, performance):
        """
        [f2] 취향 매칭 점수
        User의 preference_tags, favorite_actors와 공연 정보 매칭
        """
        score = 0.0

        # 1. 장르 태그 매칭 (60%)
        if self.user.preference_tags and performance.genrenm:
            # preference_tags는 JSON 리스트: ["뮤지컬", "로맨틱"]
            for tag in self.user.preference_tags:
                if tag in performance.genrenm:
                    score += 0.6
                    break

        # 2. 배우 매칭 (40%)
        if self.user.favorite_actors and performance.cast_search_text:
            # favorite_actors는 JSON 리스트: ["조승우", "옥주현"]
            for actor in self.user.favorite_actors:
                if actor in performance.cast_search_text:
                    score += 0.4
                    break

        return min(score, 1.0)

    def _f3_location_score(self, performance):
        """
        [f3] 위치 근접성 점수 (광역시/도 단위 매칭)
        User의 region과 Performance의 area 비교
        """
        if not self.user.region or not performance.area:
            return 0.5  # 정보 없으면 중립 점수

        # 광역시/도 완전 일치 -> 최고 점수
        if self.user.region == performance.area:
            return 1.0

        # 부분 일치 (예: "서울" in "서울특별시")
        if self.user.region in performance.area or performance.area in self.user.region:
            return 0.8

        return 0.0

    def _f4_popularity_score(self, performance):
        """
        [f4] 대중성 점수
        PerformanceMetric의 score_popularity 활용
        """
        try:
            if hasattr(performance, 'metric') and performance.metric:
                return performance.metric.score_popularity
        except:
            pass

        # Metric이 없으면 BoxOffice 랭킹으로 대체 계산
        if hasattr(performance, 'box_office_rankings'):
            rankings = performance.box_office_rankings.all()
            if rankings.exists():
                # 랭킹이 높을수록 점수 높음 (1위 = 1.0, 10위 = 0.1)
                best_rank = min([r.rank for r in rankings])
                return max(0, 1 - (best_rank - 1) / 10)

        return 0.3  # 기본 점수

    def _f5_recency_score(self, performance):
        """
        [f5] 최신성 점수
        공연 시작일이 가까울수록 높은 점수 (마감 임박 효과)
        """
        try:
            if hasattr(performance, 'metric') and performance.metric:
                return performance.metric.score_recency
        except:
            pass

        # Metric이 없으면 직접 계산
        if not performance.prfpdfrom:
            return 0.5

        today = timezone.now().date()
        days_until_start = (performance.prfpdfrom - today).days

        # 시작일이 임박할수록 점수 높음 (시그모이드 함수)
        # 0~30일: 높은 점수, 30일 이후: 점수 감소
        if days_until_start < 0:
            # 이미 시작한 공연
            return 0.7
        else:
            # 시작 예정 공연
            return 1 / (1 + math.exp(0.1 * (days_until_start - 15)))

    def _f6_collaborative_score(self, performance):
        """
        [f6] 협업 필터링 점수
        사용자가 좋아한 공연과 유사한 공연 추천
        """
        from ..models import UserLog

        # 사용자가 'like'한 공연들 조회
        liked_performances = UserLog.objects.filter(
            user=self.user,
            action_type='like'
        ).values_list('performance_id', flat=True)[:10]

        if not liked_performances:
            return 0.5

        # PerformanceMetric의 similar_performances 활용
        try:
            if hasattr(performance, 'metric') and performance.metric:
                similar_list = performance.metric.similar_performances
                if similar_list:
                    # 좋아한 공연 중 유사 목록에 포함되어 있는지 확인
                    overlap_count = sum(1 for pid in liked_performances if pid in similar_list)
                    return min(overlap_count / 3.0, 1.0)  # 최대 3개 일치 시 만점
        except:
            pass

        # Metric이 없으면 장르 유사도로 대체
        for liked_id in liked_performances:
            try:
                from performances.models import Performance
                liked_perf = Performance.objects.get(mt20id=liked_id)
                if liked_perf.genrenm == performance.genrenm:
                    return 0.7
            except:
                continue

        return 0.3

    def _f7_embedding_score(self, performance):
        """
        [f7] 임베딩 유사도 점수
        사용자 선호도 벡터와 공연 임베딩 벡터 간의 코사인 유사도 계산
        """
        # 사용자가 온보딩을 완료하지 않았으면 중립 점수 반환
        try:
            user_preference = self.user.preference
            if not user_preference or not user_preference.preference_vector:
                return 0.5
        except:
            return 0.5

        # 공연에 임베딩이 없으면 중립 점수 반환
        try:
            if not hasattr(performance, 'embedding') or not performance.embedding:
                return 0.5

            performance_vector = performance.embedding.vector
            if not performance_vector:
                return 0.5
        except:
            return 0.5

        # 코사인 유사도 계산
        try:
            import numpy as np

            user_vec = np.array(user_preference.preference_vector, dtype=np.float32)
            perf_vec = np.array(performance_vector, dtype=np.float32)

            # 벡터 정규화 확인
            user_norm = np.linalg.norm(user_vec)
            perf_norm = np.linalg.norm(perf_vec)

            if user_norm == 0 or perf_norm == 0:
                return 0.5

            # 코사인 유사도 계산
            similarity = np.dot(user_vec, perf_vec) / (user_norm * perf_norm)

            # -1~1 범위를 0~1 범위로 변환
            score = (similarity + 1) / 2

            return float(score)

        except Exception as e:
            # 에러 발생 시 중립 점수 반환
            return 0.5

    def _get_top_reason(self, breakdown, performance):
        """
        추천 사유 결정 (가장 높은 점수를 기록한 요인)

        Returns:
            tuple: (reason_code, reason_text)
        """
        # f1~f7 중 가장 높은 점수 찾기
        scores = {
            'click': breakdown['f1'],
            'preference': breakdown['f2'],
            'location': breakdown['f3'],
            'popularity': breakdown['f4'],
            'recency': breakdown['f5'],
            'collaborative': breakdown['f6'],
            'embedding': breakdown['f7']
        }

        top_reason = max(scores, key=scores.get)

        # 사유별 메시지 생성
        reason_messages = {
            'click': f"👁️ 최근 {performance.genrenm} 장르를 자주 보셨어요!",
            'preference': "❤️ 취향 저격 공연이에요!",
            'location': f"🏠 {self.user.region}에서 공연해요!",
            'popularity': "🔥 지금 가장 핫한 공연이에요!",
            'recency': "⏰ 곧 시작하는 공연이에요!",
            'collaborative': "👥 비슷한 취향의 사람들이 좋아해요!",
            'embedding': "✨ AI가 선택한 당신의 완벽한 공연!"
        }

        return top_reason, reason_messages.get(top_reason, "추천 공연입니다!")
