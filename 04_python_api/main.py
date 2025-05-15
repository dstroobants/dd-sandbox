# Import necessary modules
from datadog import api, initialize
import time

options = {
    'api_key': '',
    'application_key': '',
}
initialize(**options)


# --- Define the query parameters ---
# Use Unix timestamps (in seconds) for start and end times
# 2025-05-14 22:00:00 UTC corresponds to timestamp 1747260000
# 2025-05-15 00:00:00 UTC corresponds to timestamp 1747267200
start_time_ts = 1747260000
end_time_ts = 1747267200

metric_query = "sum:api.router.client_request.requests_finished{env:prod} by {api.engine_id}.rollup(sum, 3600).as_count()"

# --- Execute the metric query ---
try:
    results = api.Metric.query(
        start=start_time_ts,
        end=end_time_ts,
        query=metric_query
    )

    # --- Print the results ---
    print("Datadog Metric Query Results:")
    print(f"Query: {metric_query}")
    print(f"Start Time (Timestamp): {start_time_ts} ({time.ctime(start_time_ts)})")
    print(f"End Time (Timestamp): {end_time_ts} ({time.ctime(end_time_ts)})")
    print("-" * 30)

    if results and results.get('series'):
        for series in results['series']:
            print(f"Metric: {series.get('metric')}")
            print(f"Scope: {series.get('scope')}")
            print(f"Tags: {series.get('tag_set')}")
            print(f"Expression: {series.get('expression')}")
            print("Points:")
            # Points are typically [timestamp, value] pairs
            if series.get('pointlist'):
                 # Point timestamps are in milliseconds, convert to seconds for ctime
                 for point in series['pointlist']:
                      point_time = time.ctime(point[0] / 1000)
                      print(f"  - Time: {point_time}, Value: {point[1]}")
            else:
                 print("  No data points for this series.")
            print("-" * 15)
    elif results and results.get('errors'):
        print("Error querying metric:")
        print(results['errors'])
    else:
        print("No data returned for the query or time range.")

except Exception as e:
    print(f"An error occurred: {e}")