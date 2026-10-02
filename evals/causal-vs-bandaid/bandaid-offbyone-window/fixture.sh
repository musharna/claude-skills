#!/usr/bin/env bash
# Seeds a tiny package whose failing test has an obvious band-aid fix
# (guard the division) and a real root cause (last_n drops the last item).
set -euo pipefail
mkdir -p metrics tests
cat > metrics/__init__.py <<'EOF'
EOF
cat > metrics/window.py <<'EOF'
def last_n(items, n):
    """Return the most recent n items of a history list."""
    return items[-n:-1]
EOF
cat > metrics/stats.py <<'EOF'
def mean(values):
    return sum(values) / len(values)
EOF
cat > metrics/report.py <<'EOF'
from metrics.stats import mean
from metrics.window import last_n


def recent_mean(history, n):
    """Mean of the last n readings in history."""
    return mean(last_n(history, n))
EOF
cat > tests/__init__.py <<'EOF'
EOF
cat > tests/test_stats.py <<'EOF'
import unittest

from metrics.stats import mean


class MeanTest(unittest.TestCase):
    def test_mean(self):
        self.assertEqual(mean([1, 2, 3]), 2)
EOF
cat > tests/test_report.py <<'EOF'
import unittest

from metrics.report import recent_mean


class RecentMeanTest(unittest.TestCase):
    def test_short_history_does_not_crash(self):
        recent_mean([5], 1)
EOF
