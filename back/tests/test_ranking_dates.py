import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mypjt.settings')
django.setup()

from performances.models import BoxOfficeRanking
from collections import Counter

# Check distinct ranking dates and count
dates = BoxOfficeRanking.objects.values_list('ranking_date', flat=True).distinct()
print(f"Distinct ranking dates: {list(dates)}")

# For each genre_code, show distinct genrenm values
for code in ['AAAA', 'BBBC', 'CCCA', 'CCCD', 'GGGA']:
    genrenms = BoxOfficeRanking.objects.filter(genre_code=code).values_list('performance__genrenm', flat=True)
    counts = Counter(genrenms)
    print(f"\n{code}:")
    for genrenm, count in counts.most_common():
        print(f"  {genrenm}: {count}건")
