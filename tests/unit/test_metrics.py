"""Unit tests for performance metrics."""

import pandas as pd
import pytest

from har_analyzer.core.metrics import PerformanceMetrics
from har_analyzer.config import PerformanceThresholds


class TestPerformanceMetrics:
    """Test cases for PerformanceMetrics class."""
    
    @pytest.fixture
    def metrics(self):
        """Create metrics calculator with default thresholds."""
        thresholds = PerformanceThresholds()
        return PerformanceMetrics(thresholds)
    
    def test_calculate_summary_by_type(self, metrics: PerformanceMetrics, sample_dataframe: pd.DataFrame):
        """Test summary calculation by resource type."""
        summary = metrics.calculate_summary_by_type(sample_dataframe)
        
        assert len(summary) == 2  # JS and CSS
        assert 'type' in summary.columns
        assert 'requests_count' in summary.columns
        assert 'avg_response_time_ms' in summary.columns
        
        # Check JS row
        js_row = summary[summary['type'] == 'JS'].iloc[0]
        assert js_row['requests_count'] == 1
        assert js_row['avg_response_time_ms'] == 150
        assert js_row['total_size_kb'] == 1.0
        
        # Check CSS row  
        css_row = summary[summary['type'] == 'CSS'].iloc[0]
        assert css_row['requests_count'] == 1
        assert css_row['avg_response_time_ms'] == 100
        assert css_row['total_size_kb'] == 0.5
    
    def test_calculate_percentiles(self, metrics: PerformanceMetrics, sample_dataframe: pd.DataFrame):
        """Test percentile calculation."""
        percentiles = metrics.calculate_percentiles(sample_dataframe)
        
        expected_keys = ['p50', 'p75', 'p90', 'p95', 'p99']
        assert all(key in percentiles for key in expected_keys)
        
        # With 2 data points (100, 150), median should be 125
        assert percentiles['p50'] == 125.0
    
    def test_get_top_resources(self, metrics: PerformanceMetrics, sample_dataframe: pd.DataFrame):
        """Test top resources extraction."""
        top_slow = metrics.get_top_resources(sample_dataframe, 'response_time_ms', 1)
        
        assert 'JS' in top_slow
        assert 'CSS' in top_slow
        
        # JS should be the slowest
        js_top = top_slow['JS']
        assert len(js_top) == 1
        assert js_top.iloc[0]['response_time_ms'] == 150
    
    def test_calculate_performance_grade_excellent(self, sample_dataframe: pd.DataFrame):
        """Test performance grade calculation for excellent performance."""
        # Set very high thresholds to ensure A+ grade
        thresholds = PerformanceThresholds(a_plus=300, p95_a_plus=1000)
        metrics = PerformanceMetrics(thresholds)
        
        grade, emoji, explanation = metrics.calculate_performance_grade(sample_dataframe)
        
        assert "A+" in grade
        assert emoji == "🟢"
        assert "Outstanding" in explanation
    
    def test_calculate_performance_grade_poor(self, sample_dataframe: pd.DataFrame):
        """Test performance grade calculation for poor performance."""
        # Set very low thresholds to ensure D grade
        thresholds = PerformanceThresholds(a_plus=50, b=75, c=100)
        metrics = PerformanceMetrics(thresholds)
        
        grade, emoji, explanation = metrics.calculate_performance_grade(sample_dataframe)
        
        assert "D" in grade
        assert emoji == "🔴"
        assert "Poor" in explanation
    
    def test_calculate_core_web_vitals(self, metrics: PerformanceMetrics, sample_dataframe: pd.DataFrame):
        """Test Core Web Vitals calculation."""
        cwv = metrics.calculate_core_web_vitals(sample_dataframe)
        
        assert 'fcp_approximation_ms' in cwv
        assert 'lcp_approximation_ms' in cwv
        assert 'cls_approximation' in cwv
        assert 'note' in cwv
        
        # No HTML in sample data, so FCP should be 0
        assert cwv['fcp_approximation_ms'] == 0
    
    def test_analyze_timing_breakdown(self, metrics: PerformanceMetrics, sample_dataframe: pd.DataFrame):
        """Test timing breakdown analysis."""
        timing = metrics.analyze_timing_breakdown(sample_dataframe)
        
        assert 'averages' in timing
        assert 'medians' in timing
        assert 'p95' in timing
        assert 'totals' in timing
        
        # Check specific timing values
        assert timing['averages']['timing_wait'] == 80.0  # (75 + 85) / 2
        assert timing['totals']['timing_dns'] == 20.0     # 20 + 0
    
    def test_detect_performance_issues(self, metrics: PerformanceMetrics, sample_dataframe: pd.DataFrame):
        """Test performance issue detection."""
        issues = metrics.detect_performance_issues(sample_dataframe)
        
        # With sample data, should not detect major issues
        assert isinstance(issues, list)
        
        # Test with problematic data
        bad_data = sample_dataframe.copy()
        bad_data.loc[0, 'response_time_ms'] = 5000  # Very slow
        bad_data.loc[1, 'size_kb'] = 2000          # Very large
        
        issues = metrics.detect_performance_issues(bad_data)
        assert len(issues) > 0
        
        # Should detect slow resources
        slow_issue = next((i for i in issues if i['type'] == 'slow_resources'), None)
        assert slow_issue is not None
        assert slow_issue['severity'] == 'high'
