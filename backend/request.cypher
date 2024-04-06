query {
  
  sources(first: 5) {
    # See https: //relay.dev/graphql/connections.htm
    edges {
      node {
        componentId
        metrics {
          # Total events that the source has received.
          receivedEventsTotal {
            receivedEventsTotal
          }
        }
      }
    }
  }
  
  # Get transforms (defaults to the first 10 WHEN a
LIMIT isn't specified)
  transforms {
    edges {
      node {
        componentId
        metrics {
          # Total events that the transform has sent out.
          sentEventsTotal {
            sentEventsTotal
          }
        }
      }
    }
  }
  
  # Get the last 3 sinks.
  sinks(last: 3) {
    edges {
      node {
        componentId
        metrics {
          # Total bytes sent by this sink.
          sentBytesTotal {
            sentBytesTotal
          }
        }
      }
    }
  }
}
