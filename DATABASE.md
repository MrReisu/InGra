# InGra – Datenbankkonzept

Dieses Dokument wurde mit KI-Unterstützung (Anthropic Claude Sonnet 4.6 Mittel) erstellt und manuell überprüft.

## Struktur

Das Datenbankschema ist in drei Bereiche aufgeteilt:

- **Core** – Kategorien, Subkategorien und Produkte
- **Preise** – Shops und Preisverlauf
- **Specs** – Produktspezifische Tabellen je Kategorie

---

## ER-Diagramm

```mermaid
erDiagram

    %% ==================
    %% CORE
    %% ==================

    category {
        int id PK
        varchar name
        varchar slug
    }

    subcategory {
        int id PK
        int category_id FK
        varchar name
        varchar slug
    }

    product {
        int id PK
        int category_id FK
        int subcategory_id FK
        varchar name
        varchar manufacturer
        varchar model
        varchar image_url
        varchar product_url
        datetime created_at
        datetime updated_at
    }

    %% ==================
    %% PREISE
    %% ==================

    shop {
        int id PK
        varchar name
        varchar base_url
    }

    price {
        int id PK
        int product_id FK
        int shop_id FK
        float price
        datetime scraped_at
    }

    %% ==================
    %% SPECS
    %% ==================

    gpu_specs {
        int id PK
        int product_id FK
        %% Grafikspeicher in GB
        int vram_gb
        %% Grafikspeichertyp
        varchar vram_type
        %% Grafikspeicher Frequenz
        int vram_freq
        %% Grafikspeicher Bandbreite
        int vram_bandwidth
        %% Speicheranbindung
        int memory_bus
        %% GPU Basistakt
        int base_clock
        %% GPU Boosttakt
        int boost_clock
        %% Stromverbrauch in Watt
        int tdp_watt
        %% Schnittstelle
        varchar pcie_version
        %% Stromanschlüsse
        varchar connectors
        %% Displayanschlüsse
        varchar ports
        %% Maße der Karte (Länge x Breite x Höhe)
        varchar abmessung
        %% Anzahl der genutzten Slots
        int slots
    }

    cpu_specs {
        int id PK
        int product_id FK
        varchar socket
        int cores
        int threads
        float base_clock_ghz
        float boost_clock_ghz
        int tdp_watt
        int l3_cache_mb
        varchar memory_type
        boolean integrated_graphics
        boolean includes_cooler
    }

    mainboard_specs {
        int id PK
        int product_id FK
        varchar socket
        varchar chipset
        varchar form_factor
        int memory_slots
        varchar memory_type
        int max_memory_gb
        int pcie5_slots
        int m2_slots
        boolean usb_c_rear
        boolean wifi
        boolean bluetooth
    }

    psu_specs {
        int id PK
        int product_id FK
        int watt
        varchar efficiency_rating
        varchar modular
        varchar form_factor
        boolean atx3
        int pcie16_connectors
    }

    ram_specs {
        int id PK
        int product_id FK
        varchar memory_type
        int capacity_gb
        int kit_count
        int speed_mhz
        int cl_latency
        float voltage
        boolean rgb
    }

    storage_specs {
        int id PK
        int product_id FK
        int capacity_gb
        varchar interface
        varchar form_factor
        int read_mbps
        int write_mbps
        int tbw
        boolean dram_cache
    }

    air_cooler_specs {
        int id PK
        int product_id FK
        int height_mm
        int tdp_watt
        int fan_count
        int fan_size_mm
        varchar socket_support
        boolean rgb
    }

    case_fan_specs {
        int id PK
        int product_id FK
        int size_mm
        int max_rpm
        float max_airflow_cfm
        float static_pressure
        varchar connector
        boolean rgb
    }

    watercooling_cpu_specs {
        int id PK
        int product_id FK
        varchar socket_support
        int pump_speed_rpm
        boolean rgb
    }

    aio_specs {
        int id PK
        int product_id FK
        int radiator_size_mm
        int fan_count
        int fan_size_mm
        varchar socket_support
        int tubing_length_mm
        boolean rgb
    }

    radiator_specs {
        int id PK
        int product_id FK
        int size_mm
        int thickness_mm
        int fan_slots
        int fan_size_mm
        varchar material
    }

    gpu_watercooling_specs {
        int id PK
        int product_id FK
        varchar compatible_gpus
        varchar material
        boolean rgb
    }

    fitting_specs {
        int id PK
        int product_id FK
        varchar type
        varchar thread
        varchar material
        varchar color
    }

    tubing_specs {
        int id PK
        int product_id FK
        varchar type
        float inner_diameter_mm
        float outer_diameter_mm
        varchar material
        float length_m
        varchar color
    }

    %% ==================
    %% RELATIONEN
    %% ==================

    category ||--o{ subcategory : "hat"
    category ||--o{ product : "hat"
    subcategory ||--o{ product : "hat"

    product ||--o| gpu_specs : "hat"
    product ||--o| cpu_specs : "hat"
    product ||--o| mainboard_specs : "hat"
    product ||--o| psu_specs : "hat"
    product ||--o| ram_specs : "hat"
    product ||--o| storage_specs : "hat"
    product ||--o| air_cooler_specs : "hat"
    product ||--o| case_fan_specs : "hat"
    product ||--o| watercooling_cpu_specs : "hat"
    product ||--o| aio_specs : "hat"
    product ||--o| radiator_specs : "hat"
    product ||--o| gpu_watercooling_specs : "hat"
    product ||--o| fitting_specs : "hat"
    product ||--o| tubing_specs : "hat"

    product ||--o{ price : "hat"
    shop ||--o{ price : "hat"
```

---

## Kategorien & Subkategorien

| Kategorie | Subkategorien | Spec-Tabelle |
|---|---|---|
| GPU | – | `gpu_specs` |
| CPU | – | `cpu_specs` |
| Mainboard | – | `mainboard_specs` |
| Netzteil | – | `psu_specs` |
| RAM | – | `ram_specs` |
| Festplatten | SSD, NVMe | `storage_specs` |
| Kühlung | CPU Luftkühler | `air_cooler_specs` |
| Kühlung | Gehäuselüfter | `case_fan_specs` |
| Kühlung | CPU Wasserkühlung | `watercooling_cpu_specs` |
| Kühlung | AIO | `aio_specs` |
| Kühlung | Radiator | `radiator_specs` |
| Kühlung | GPU Wasserkühlung | `gpu_watercooling_specs` |
| Kühlung | Fittings | `fitting_specs` |
| Kühlung | Rohre & Schläuche | `tubing_specs` |
