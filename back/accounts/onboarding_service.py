import numpy as np
from django.db.models import Q, Count
from django.utils import timezone
from .models import User, UserPreference, UserPerformanceSignal
from performances.models import Performance, PerformanceEmbedding


def get_onboarding_candidates(count=16, strategy='balanced', exclude_ids=None):
    """
    Select performances for onboarding screen

    Strategy:
    - 'balanced': Mix of recent, popular, and diverse genres
    - 'popular': Top ranked performances
    - 'recent': Recently started performances

    Args:
        count: Number of performances to return
        strategy: Selection strategy
        exclude_ids: List of mt20id to exclude (for refresh functionality)

    Returns: QuerySet of Performance objects with embeddings
    """
    # Filter: Only performances with embeddings
    performances = Performance.objects.filter(
        embedding__isnull=False
    ).select_related('embedding')

    # Exclude specified IDs
    if exclude_ids:
        performances = performances.exclude(mt20id__in=exclude_ids)

    if strategy == 'popular':
        # Use PerformanceMetric.score_popularity
        performances = performances.filter(
            metric__isnull=False
        ).order_by('-metric__score_popularity')

    elif strategy == 'recent':
        # Recent start dates
        performances = performances.order_by('-prfpdfrom')

    else:  # balanced (default)
        # Mix of: 8 popular + 4 recent + 4 diverse genres
        popular = performances.filter(
            metric__isnull=False
        ).order_by('-metric__score_popularity')[:8]

        recent = performances.order_by('-prfpdfrom')[:4]

        # Diverse: Pick 1 from each major genre
        diverse = performances.values('genrenm').annotate(
            cnt=Count('mt20id')
        ).order_by('-cnt')[:4]

        genre_samples = []
        for genre_data in diverse:
            sample = performances.filter(
                genrenm=genre_data['genrenm']
            ).order_by('?').first()
            if sample:
                genre_samples.append(sample.mt20id)

        # Combine
        combined_ids = list(popular.values_list('mt20id', flat=True)) + \
                      list(recent.values_list('mt20id', flat=True)) + \
                      genre_samples

        performances = Performance.objects.filter(
            mt20id__in=combined_ids[:count]
        ).select_related('embedding')

    return performances[:count]


def save_user_signals(user, signals_data):
    """
    Save user reactions from onboarding

    Args:
        user: User instance
        signals_data: List of dicts [{"performance_id": "PF123", "signal": 1.5}, ...]

    Returns:
        Number of signals saved
    """
    signals = []
    for item in signals_data:
        perf_id = item.get('performance_id')
        signal_value = item.get('signal')

        try:
            performance = Performance.objects.get(mt20id=perf_id)
            signal_obj = UserPerformanceSignal(
                user=user,
                performance=performance,
                signal=signal_value
            )
            signals.append(signal_obj)
        except Performance.DoesNotExist:
            continue

    # Bulk create
    UserPerformanceSignal.objects.bulk_create(
        signals,
        ignore_conflicts=True  # Skip duplicates
    )

    return len(signals)


def calculate_preference_vector(user):
    """
    Calculate user preference vector from signals

    Algorithm:
    1. Get all user signals
    2. For each signal, get performance embedding vector
    3. Weighted sum: sum(signal_weight * embedding_vector)
    4. L2 normalize result

    Returns:
        1536-dim list of floats (normalized vector)
    """
    # Get user signals with embeddings
    signals = UserPerformanceSignal.objects.filter(
        user=user,
        performance__embedding__isnull=False
    ).select_related('performance__embedding')

    if signals.count() == 0:
        # No signals: return zero vector
        return [0.0] * 1536

    # Initialize accumulator
    weighted_sum = np.zeros(1536, dtype=np.float32)

    for signal_obj in signals:
        embedding_vector = np.array(
            signal_obj.performance.embedding.vector,
            dtype=np.float32
        )

        weight = signal_obj.signal
        weighted_sum += weight * embedding_vector

    # L2 normalization
    norm = np.linalg.norm(weighted_sum)
    if norm > 0:
        normalized = weighted_sum / norm
    else:
        normalized = weighted_sum  # All zeros

    return normalized.tolist()


def complete_onboarding(user):
    """
    Finalize onboarding process

    Steps:
    1. Calculate preference vector from signals
    2. Create/update UserPreference
    3. Mark user.has_onboarded = True
    4. Set user.onboarded_at timestamp

    Returns:
        UserPreference instance
    """
    # Calculate vector
    preference_vector = calculate_preference_vector(user)
    signal_count = UserPerformanceSignal.objects.filter(user=user).count()

    # Save preference
    preference, created = UserPreference.objects.update_or_create(
        user=user,
        defaults={
            'preference_vector': preference_vector,
            'signal_count': signal_count
        }
    )

    # Update user
    user.has_onboarded = True
    user.onboarded_at = timezone.now()
    user.save(update_fields=['has_onboarded', 'onboarded_at'])

    return preference
