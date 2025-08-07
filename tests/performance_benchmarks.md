# Test performance data for benchmarking

## Test Case 1: Small Website (< 50 requests)
- Expected Grade: A+ or B
- Response Time: < 300ms average
- Total Size: < 1MB

## Test Case 2: Medium Website (50-200 requests) 
- Expected Grade: B or C
- Response Time: 300-800ms average
- Total Size: 1-5MB

## Test Case 3: Large Website (> 200 requests)
- Expected Grade: C or D
- Response Time: > 800ms average
- Total Size: > 5MB

## Performance Benchmarks

### Memory Usage Limits
- Small HAR files (< 1MB): < 100MB RAM
- Medium HAR files (1-10MB): < 500MB RAM  
- Large HAR files (> 10MB): < 1GB RAM

### Processing Time Limits
- Small files: < 5 seconds
- Medium files: < 30 seconds
- Large files: < 2 minutes

### Accuracy Targets
- Parsing success rate: > 99%
- Report generation success: > 99.5%
- Performance grade consistency: > 95%
