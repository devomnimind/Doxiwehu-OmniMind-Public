# Hardware Benchmark Report — OmniMind

Data: 2025-11-19T04:17:21.489882

## Resumo Executivo

- **CPU:** None phys / None log cores
- **Memória:** 0.0 GB total
- **GPU:** N/A
- **Disco:** N/A

## Resultados de Benchmark
| Teste | Resultado | Unidade |
| --- | --- | --- |
| Loop 1M iterações | 71.71 | ms |
| Operações matemáticas | 46.00 | ms |
| SHA-256 (hash) | 286.74 | ms |
| Compressão (zlib) | 43.49 | ms |
| Memory throughput | 16698.51 | MB/s |
| Disk seq. write | 939.99 | MB/s |
| Disk seq. read | 6535.28 | MB/s |
| Disk random | 607.55 | MB/s |

## Recomendações

- GPU está subutilizada ou indisponível; priorizar mais workloads CUDA caso seja confirmada a sustentabilidade.
- CPU com headroom: considerar paralelizar loops críticos e usar vectores em numpy/torch.
- Memória em nível alto; usar caches em RAM para evitar re-loads.
- Disco pode ser gargalo; cache parcial em memória e monitorar latência por I/O random.

## Detalhes
{
  "system_info": {
    "system_info": {
      "timestamp": "2025-11-19T04:16:50.511885",
      "os": {
        "system": "Linux",
        "node": "kali",
        "release": "6.16.8+kali-amd64",
        "version": "#1 SMP PREEMPT_DYNAMIC Kali 6.16.8-1kali1 (2025-09-24)",
        "machine": "x86_64",
        "processor": ""
      },
      "cpu": {
        "physical_cores": 4,
        "logical_cores": 8,
        "frequency": {
          "current_mhz": 2499.9975,
          "min_mhz": 800.0,
          "max_mhz": 2500.0
        },
        "architecture": "x86_64"
      },
      "memory": {
        "total": 24931749888,
        "available": 17102729216,
        "used": 7829020672,
        "percent": 31.4
      },
      "swap": {
        "total": 25492975616,
        "used": 12288,
        "percent": 0.0
      },
      "disk": [
        {
          "device": "/dev/mapper/kali--vg-root",
          "mountpoint": "/",
          "fstype": "ext4",
          "total": 956184760320,
          "used": 148694827008,
          "free": 758842929152,
          "percent": 16.4
        },
        {
          "device": "/dev/nvme0n1p2",
          "mountpoint": "/boot",
          "fstype": "ext4",
          "total": 989052928,
          "used": 385970176,
          "free": 535085056,
          "percent": 41.9
        },
        {
          "device": "/dev/nvme0n1p1",
          "mountpoint": "/boot/efi",
          "fstype": "vfat",
          "total": 1021394944,
          "used": 311296,
          "free": 1021083648,
          "percent": 0.0
        }
      ],
      "network": {
        "lo": {
          "isup": true,
          "speed": 0,
          "mtu": 65536,
          "addresses": [
            {
              "family": "AF_INET",
              "address": "127.0.0.1"
            },
            {
              "family": "AF_INET6",
              "address": "::1"
            },
            {
              "family": "AF_PACKET",
              "address": "00:00:00:00:00:00"
            }
          ]
        },
        "eth0": {
          "isup": true,
          "speed": 1000,
          "mtu": 1500,
          "addresses": [
            {
              "family": "AF_INET",
              "address": "192.168.15.2"
            },
            {
              "family": "AF_INET6",
              "address": "2804:7f0:9482:4cc5:4cb:eccb:b37a:e896"
            },
            {
              "family": "AF_INET6",
              "address": "2804:7f0:9482:4cc5:661c:67ff:fef3:8460"
            },
            {
              "family": "AF_INET6",
              "address": "fe80::661c:67ff:fef3:8460%eth0"
            },
            {
              "family": "AF_PACKET",
              "address": "64:1c:67:f3:84:60"
            }
          ]
        },
        "docker0": {
          "isup": false,
          "speed": 0,
          "mtu": 1500,
          "addresses": [
            {
              "family": "AF_INET",
              "address": "172.17.0.1"
            },
            {
              "family": "AF_PACKET",
              "address": "02:42:0e:15:e0:56"
            }
          ]
        },
        "wlan0": {
          "isup": false,
          "speed": 0,
          "mtu": 1500,
          "addresses": [
            {
              "family": "AF_PACKET",
              "address": "8e:a4:65:43:63:db"
            }
          ]
        }
      },
      "uptime": "2025-11-19T00:27:54"
    }
  },
  "cpu": {
    "loop_ms": 71.70636233331606,
    "math_ms": 46.003471666760255,
    "hash_ms": 286.73677666665753,
    "compression_ms": 43.485132999952235,
    "timestamp": 1763525817.6316276
  },
  "gpu": {
    "status": "N/A",
    "reason": "torch.cuda unavailable or torch not installed"
  },
  "memory": {
    "memory_total": 24931749888,
    "memory_throughput_mb_s": [
      16698.50793853115,
      16158.783783896306
    ],
    "timestamp": 1763525823.645532
  },
  "disk": {
    "write_throughput_mb_s": 939.9865581892917,
    "read_throughput_mb_s": 6535.282651331439,
    "random_access_mb_s": 607.5486746688151,
    "timestamp": 1763525830.4471664
  }
}