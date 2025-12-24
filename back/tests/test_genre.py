import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mypjt.settings')
django.setup()

from performances.models import BoxOfficeRanking
import json

results = {}
for code in ['AAAA', 'BBBC', 'CCCA', 'CCCD', 'GGGA']:
    items = BoxOfficeRanking.objects.filter(genre_code=code).select_related('performance').order_by('-ranking_date', 'rank')[:3]
    results[code] = [(r.rank, r.performance.mt20id, r.performance.prfnm, r.performance.genrenm) for r in items]

print(json.dumps(results, ensure_ascii=False, indent=2))
