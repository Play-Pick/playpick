import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mypjt.settings')
django.setup()

from performances.models import BoxOfficeRanking
import json

# Check what genrenm values exist for each genre_code
for code in ['AAAA', 'BBBC', 'CCCA', 'CCCD', 'GGGA']:
    items = BoxOfficeRanking.objects.filter(genre_code=code).select_related('performance')[:5]
    print(f"\n{code}:")
    for item in items:
        print(f"  Rank {item.rank}: {item.performance.prfnm} - genrenm: '{item.performance.genrenm}'")
