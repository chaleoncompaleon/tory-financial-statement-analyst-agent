**TORY - Financial Statement Analyst Agent**

This agent processes financial statement data (such as revenue, fees, user metrics, and valuations) by sending it to an AI model and returning bullish/bearish insights.

The agent receives a message that includes:
- `uuid`: Unique identifier (string)
- `timestamp`: When the request was made (integer)
- `token`: A **stringified array** of financial metric objects (JSON format)

It passes this data to an AI API which returns a **single-line JSON summary** containing:
- `bullishThoughts`: array of bullish insights
- `bearishThoughts`: array of bearish insights


### Example Request (`FinancialsRequest`)
```json
{
  "uuid": "123e4567-e89b-12d3-a456-426614174000",
  "timestamp": 1712428800,
  "token": "{\"date\":\"4/1/2025\",\"name\":\"active_developers\",\"val\":4,\"chg\":-0.16},{\"date\":\"4/1/2025\",\"name\":\"code_commits\",\"val\":1,\"chg\":-0.98}, ..."
}
```

### Example Response (FinancialsResponse):
```json
{
  "uuid": "123e4567-e89b-12d3-a456-426614174000",
  "timestamp": 1712428800,
  "summary": "{\"bullishThoughts\":[\"P/F Circulating ratio increased by 7% to 435.41\", ...],\"bearishThoughts\":[\"Active developers decreased by 16% to 4,...\", ...]}"
} 
```