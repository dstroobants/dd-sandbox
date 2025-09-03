# Create new spans_metric resource
resource "datadog_spans_metric" "testing_spans_metric" {
  name = "rails_test.requests"
  compute {
    aggregation_type    = "distribution"
    include_percentiles = false
    path                = "@duration"
  }
  filter {
    query = "service:rails-app"
  }
  group_by {
    path     = "resource_name"
    tag_name = "resource_name"
  }
}
