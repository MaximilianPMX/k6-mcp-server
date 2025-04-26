# k6-mcp-server

Recreation of the k6-mcp-server, focusing on its core event-driven and plugin architecture based on the Model Context Protocol (MCP). This project aims to provide a server that can accept and process data from k6 load testing tool, potentially acting as a central coordination point or data aggregation service.

## API Documentation

The server exposes an API endpoint to receive data from k6. This section describes the expected request format and the server's response.

### Endpoint

`POST /data`

### Request

**Headers:**

```
Content-Type: application/json
```

**Body (JSON Example):**

```json
{
  "metric_name": "my_custom_metric",
  "value": 123.45,
  "timestamp": 1678886400,  // Unix timestamp in seconds
  "tags": {
    "environment": "production",
    "region": "us-west-2"
  }
}
```

### Response

**Success (200 OK):**

```json
{
  "status": "success",
  "message": "Data received and processed."
}
```

**Error (400 Bad Request):**

Returned if the request body is invalid or missing required fields.  The response body will provide details about the error.

```json
{
  "status": "error",
  "message": "Invalid request body: Missing 'metric_name' field."
}
```

**Error (500 Internal Server Error):**

Returned if there's an unexpected error during processing.

```json
{
  "status": "error",
  "message": "Internal server error."
}
```

## Configuration

The server's configuration is managed through `config.yaml`.  See the `config.yaml` file for available options.