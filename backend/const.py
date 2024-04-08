query: str = """
query {
  health
  meta {
    versionString
    hostname
  }
  hostMetrics {
    memory {
      totalBytes
      freeBytes
      usedBytes
      buffersBytes
    }
    swap {
      freeBytes
      totalBytes
      usedBytes
      swappedInBytesTotal
      swappedOutBytesTotal
    }
    cpu {
      cpuSecondsTotal
    }
    loadAverage {
      load1
      load5
      load15
    }
    network {
      receiveBytesTotal
      receiveErrsTotal
      receivePacketsTotal
      transmitErrsTotal
      transmitBytesTotal
      transmitPacketsTotal
      transmitPacketsDropTotal
    }
    filesystem {
      freeBytes
      totalBytes
      usedBytes
    }
    disk {
      readBytesTotal
      readsCompletedTotal
      writtenBytesTotal
      writesCompletedTotal
    }
  }
  sources(first: 10) {
    # See https: //relay.dev/graphql/connections.htm
    edges {
      node {
        componentId
        componentType
        outputs {
          outputId
          sentEventsTotal {
            timestamp
            sentEventsTotal
          }
        }
        metrics {
          # Total events that the source has received.

          sentEventsTotal {
            timestamp
            sentEventsTotal
          }
          receivedEventsTotal {
            timestamp
            receivedEventsTotal
          }
          receivedBytesTotal {
            timestamp
            receivedBytesTotal
          }
        }
      }
    }
  }

  transforms(first: 10) {
    edges {
      node {
        componentId
        sources {
          componentId
          componentType
        }
        metrics {
          # Total events that the transform has sent out.
          sentEventsTotal {
            timestamp
            sentEventsTotal
          }
          receivedEventsTotal {
            timestamp
            receivedEventsTotal
          }
        }
      }
    }
  }

  # Get the last 3 sinks.
  sinks(first: 10) {
    edges {
      node {
        componentId
        transforms {
          componentId
          componentType
        }
        metrics {
          # Total bytes sent by this sink.
          sentBytesTotal {
            timestamp
            sentBytesTotal
          }
          receivedEventsTotal {
            timestamp
            receivedEventsTotal
          }
        }
      }
    }
  }
}

"""
