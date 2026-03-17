#!/usr/bin/env python3
"""
USAID Impact Tracker — Data Pipeline for CloudPublica

Polls real data sources to track the impact of USAID defunding on global health.
Outputs a static JSON file consumable by the CloudPublica tracker page.

Data sources:
1. USAspending.gov — actual USAID disbursement data (agency code 7200)
2. WHO GHO API — mortality data by country/disease/year
3. Lancet projections — baseline from Cavalcanti et al. 2025 (SSRN 5239038)
4. GDELT — news coverage of health crises in USAID-recipient countries

Output: ~/usaid-tracker/data/tracker-data.json
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone, date

DELAY = 3  # seconds between API calls
DATA_DIR = os.path.expanduser("~/usaid-tracker/data")
LOG_DIR = os.path.expanduser("~/usaid-tracker/logs")

def fetch_json(url, headers=None, data=None, timeout=30):
    req = urllib.request.Request(url, data=data, headers=headers or {
        "User-Agent": "GD-Research-Bot/1.0 (CloudPublica USAID tracker; contact bee@justnice.us)"
    })
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}", file=sys.stderr)
        return None


# ── LANCET BASELINE PROJECTIONS ──────────────────────────────────
# From Cavalcanti et al., Lancet 2025 (SSRN 5239038)
# 133 countries, 2001-2021 retrospective + 2025-2030 projection
# These are the PROJECTED deaths under 83% USAID funding cut scenario

LANCET_PROJECTIONS = {
    "total_prevented_2001_2021": 91_000_000,
    "children_prevented_2001_2021": 30_000_000,
    "projected_additional_deaths_by_2030": 14_000_000,
    "projected_child_deaths_by_2030": 4_500_000,
    "child_deaths_per_year": 700_000,
    "funding_cut_percent": 83,
    "disease_reduction_lost": {
        "hiv_aids": {"reduction_percent": 74, "label": "HIV/AIDS"},
        "malaria": {"reduction_percent": 53, "label": "Malaria"},
        "tropical_diseases": {"reduction_percent": 51, "label": "Tropical Diseases"},
        "tuberculosis": {"reduction_percent": None, "label": "Tuberculosis"},
        "maternal_perinatal": {"reduction_percent": None, "label": "Maternal/Perinatal"},
    },
    "source": "Cavalcanti et al., Lancet 2025, SSRN 5239038",
    "source_url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5239038",
    "lancet_url": "https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(25)01186-9/fulltext",
    "n_countries": 133,
}

# Linear interpolation parameters (same as usaidcounter.github.io)
# Start: 757,314 on 2026-01-01, End: 14,000,000 on 2030-01-01
COUNTER_START_DATE = date(2026, 1, 1)
COUNTER_END_DATE = date(2030, 1, 1)
COUNTER_START_VALUE = 757_314
COUNTER_END_VALUE = 14_000_000


def compute_projected_deaths_today():
    """Linear interpolation of Lancet projection for current date."""
    today = date.today()
    if today <= COUNTER_START_DATE:
        return COUNTER_START_VALUE
    if today >= COUNTER_END_DATE:
        return COUNTER_END_VALUE
    total_days = (COUNTER_END_DATE - COUNTER_START_DATE).days
    elapsed_days = (today - COUNTER_START_DATE).days
    fraction = elapsed_days / total_days
    return int(COUNTER_START_VALUE + fraction * (COUNTER_END_VALUE - COUNTER_START_VALUE))


# ── USASPENDING POLLER ───────────────────────────────────────────

def poll_usaid_spending():
    """Pull USAID agency spending data from USAspending.gov API v2."""
    print("[USAspending] Polling USAID agency spending...")

    results = {}

    # USAID toptier agency code is "072", name is "Agency for International Development"
    for fy in [2024, 2025, 2026]:
        time.sleep(DELAY)
        url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
        payload = json.dumps({
            "filters": {
                "agencies": [{"type": "funding", "tier": "toptier", "name": "Agency for International Development"}],
                "time_period": [{"start_date": f"{fy}-10-01", "end_date": f"{fy+1}-09-30"}],
                "award_type_codes": ["A", "B", "C", "D"]
            },
            "fields": ["Award ID", "Recipient Name", "Award Amount",
                        "Awarding Agency", "Funding Agency", "Start Date",
                        "Description"],
            "page": 1, "limit": 5, "sort": "Award Amount", "order": "desc"
        }).encode()

        data = fetch_json(url, data=payload)
        if data and "results" in data and len(data["results"]) > 0:
            # Note: page_metadata.total is often 0 even when results exist (API bug)
            actual_count = len(data["results"])
            total_amount = sum(r.get("Award Amount", 0) or 0 for r in data["results"])
            results[f"FY{fy}"] = {
                "total_awards": actual_count,
                "reported_total": data.get("page_metadata", {}).get("total", 0),
                "top_awards_amount": total_amount,
                "sample_awards": [
                    {
                        "recipient": r.get("Recipient Name", ""),
                        "amount": r.get("Award Amount", 0),
                        "description": (r.get("Description") or "")[:200],
                        "start_date": r.get("Start Date", ""),
                    }
                    for r in data["results"][:5]
                ]
            }
            print(f"  FY{fy}: {actual_count} awards returned, top amount: ${total_amount:,.0f}")
        else:
            print(f"  FY{fy}: no data or error")
            results[f"FY{fy}"] = {"total_awards": 0, "error": "API returned no results"}

    # Try the agency obligations endpoint (different format)
    time.sleep(DELAY)
    obligations_url = "https://api.usaspending.gov/api/v2/agency/toptier_code/072/obligations/"
    obligations_data = fetch_json(obligations_url)
    if obligations_data:
        results["obligations"] = obligations_data
        print(f"  Agency obligations data retrieved")
    else:
        # Fallback: try agency overview
        time.sleep(DELAY)
        overview_url = "https://api.usaspending.gov/api/v2/agency/072/"
        overview_data = fetch_json(overview_url)
        if overview_data:
            results["agency_overview"] = overview_data
            print(f"  Agency overview retrieved")

    return results


# ── WHO GHO POLLER ───────────────────────────────────────────────

WHO_INDICATORS = {
    "under5_mortality": {
        "code": "MDG_0000000001",  # Under-five mortality rate (per 1000 live births)
        "label": "Under-5 Mortality Rate",
    },
    "neonatal_mortality": {
        "code": "MDG_0000000003",  # Neonatal mortality rate
        "label": "Neonatal Mortality Rate",
    },
    "maternal_mortality": {
        "code": "MDG_0000000026",  # Maternal mortality ratio
        "label": "Maternal Mortality Ratio",
    },
    "hiv_incidence": {
        "code": "HIV_0000000026",  # New HIV infections per 1000
        "label": "New HIV Infections (per 1000)",
    },
    "tb_incidence": {
        "code": "MDG_0000000020",  # TB incidence per 100k
        "label": "TB Incidence (per 100k)",
    },
    "malaria_incidence": {
        "code": "MALARIA_EST_INCIDENCE",  # Malaria incidence per 1000
        "label": "Malaria Incidence (per 1000 at risk)",
    },
}

# High-impact USAID recipient countries (top 20 by USAID spending)
PRIORITY_COUNTRIES = [
    "AFG", "ETH", "NGA", "COD", "KEN", "UGA", "TZA", "MOZ", "ZMB", "MWI",
    "ZWE", "HTI", "BGD", "PAK", "IND", "GHA", "SSD", "SOM", "MLI", "NER"
]


def poll_who_gho():
    """Pull mortality indicators from WHO Global Health Observatory OData API."""
    print("[WHO GHO] Polling health indicators...")

    results = {}
    for key, indicator in WHO_INDICATORS.items():
        time.sleep(DELAY)
        code = indicator["code"]
        # WHO GHO OData API — URL-encode spaces in OData filter
        filter_str = urllib.request.quote("TimeDim ge 2020 and TimeDim le 2026")
        select_str = urllib.request.quote("SpatialDim,TimeDim,NumericValue,Dim1")
        orderby_str = urllib.request.quote("TimeDim desc")
        url = (
            f"https://ghoapi.azureedge.net/api/{code}"
            f"?$filter={filter_str}"
            f"&$select={select_str}"
            f"&$orderby={orderby_str}"
            f"&$top=500"
        )
        data = fetch_json(url)
        if data and "value" in data:
            records = data["value"]
            # Filter to priority countries
            priority_records = [r for r in records if r.get("SpatialDim") in PRIORITY_COUNTRIES]
            all_records_count = len(records)

            # Aggregate by year
            by_year = {}
            for r in priority_records:
                yr = r.get("TimeDim")
                val = r.get("NumericValue")
                if yr and val is not None:
                    if yr not in by_year:
                        by_year[yr] = []
                    by_year[yr].append({"country": r["SpatialDim"], "value": val})

            results[key] = {
                "label": indicator["label"],
                "indicator_code": code,
                "total_records": all_records_count,
                "priority_country_records": len(priority_records),
                "by_year": {yr: {
                    "n_countries": len(vals),
                    "mean": sum(v["value"] for v in vals) / len(vals) if vals else 0,
                    "values": vals[:5]  # sample
                } for yr, vals in sorted(by_year.items(), reverse=True)},
                "latest_year": max(by_year.keys()) if by_year else None,
            }
            print(f"  {key}: {len(priority_records)} records from priority countries, latest={results[key]['latest_year']}")
        else:
            print(f"  {key}: no data")
            results[key] = {"label": indicator["label"], "error": "no data from API"}

    return results


# ── GDELT NEWS MONITOR ───────────────────────────────────────────

def poll_gdelt_usaid():
    """Track USAID-related health crisis coverage via GDELT."""
    print("[GDELT] Polling USAID health news...")

    queries = [
        ("USAID defunding health", "usaid_defunding"),
        ("PEPFAR funding cuts HIV", "pepfar_cuts"),
        ("malaria aid cuts Africa", "malaria_cuts"),
        ("maternal mortality aid cuts", "maternal_cuts"),
    ]

    results = {}
    for query, key in queries:
        time.sleep(DELAY)
        encoded = urllib.request.quote(query)
        url = f"https://api.gdeltproject.org/api/v2/doc/doc?query={encoded}&mode=ArtList&maxrecords=10&format=json&sort=DateDesc&timespan=30d"
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "GD-Research-Bot/1.0 (CloudPublica USAID tracker; contact bee@justnice.us)"
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                text = resp.read().decode()
            data = json.loads(text)
            articles = data.get("articles", [])
            results[key] = {
                "query": query,
                "count": len(articles),
                "articles": [{"title": a.get("title", ""), "url": a.get("url", ""),
                              "date": a.get("seendate", ""), "domain": a.get("domain", "")}
                             for a in articles[:10]]
            }
            print(f"  {key}: {len(articles)} articles (30d)")
        except Exception as e:
            print(f"  {key}: error — {e}")
            results[key] = {"query": query, "count": 0, "error": str(e)}

    return results


# ── MAIN PIPELINE ────────────────────────────────────────────────

def run_pipeline():
    """Run all pollers and assemble tracker data."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    timestamp = datetime.now(timezone.utc).isoformat()
    print(f"\n{'='*60}")
    print(f"USAID Impact Tracker Pipeline — {timestamp}")
    print(f"{'='*60}\n")

    # 1. Compute projected deaths
    projected = compute_projected_deaths_today()
    print(f"Lancet projection for today: {projected:,} deaths\n")

    # 2. Poll data sources
    usaspending_data = poll_usaid_spending()
    print()
    who_data = poll_who_gho()
    print()
    gdelt_data = poll_gdelt_usaid()
    print()

    # 3. Assemble tracker data
    tracker = {
        "metadata": {
            "generated_at": timestamp,
            "generated_by": "CloudPublica USAID Impact Tracker Pipeline v1",
            "update_frequency": "every 6 hours",
            "methodology": "Lancet projections (Cavalcanti et al. 2025) + real-time data from USAspending, WHO GHO, GDELT",
        },
        "counter": {
            "projected_deaths_today": projected,
            "projected_deaths_2030": LANCET_PROJECTIONS["projected_additional_deaths_by_2030"],
            "projected_child_deaths_2030": LANCET_PROJECTIONS["projected_child_deaths_by_2030"],
            "deaths_prevented_2001_2021": LANCET_PROJECTIONS["total_prevented_2001_2021"],
            "funding_cut_percent": LANCET_PROJECTIONS["funding_cut_percent"],
            "methodology_note": "Linear interpolation of Lancet projection. Actual impact may differ.",
        },
        "lancet": LANCET_PROJECTIONS,
        "funding": {
            "source": "USAspending.gov API v2",
            "agency": "Agency for International Development (USAID)",
            "data": usaspending_data,
        },
        "health_indicators": {
            "source": "WHO Global Health Observatory OData API",
            "priority_countries": PRIORITY_COUNTRIES,
            "indicators": who_data,
        },
        "news_coverage": {
            "source": "GDELT Project API",
            "timespan": "30 days",
            "data": gdelt_data,
        },
        "sources": [
            {"name": "Lancet Study", "url": LANCET_PROJECTIONS["lancet_url"], "description": "Cavalcanti et al. 2025 — 14M projected deaths by 2030"},
            {"name": "UCLA Press Release", "url": "https://ph.ucla.edu/news-events/news/research-finds-more-14-million-preventable-deaths-2030-if-usaid-defunding"},
            {"name": "USAspending.gov", "url": "https://www.usaspending.gov/agency/agency-for-international-development", "description": "Federal spending transparency"},
            {"name": "WHO GHO", "url": "https://www.who.int/data/gho", "description": "Global health indicators"},
            {"name": "GDELT Project", "url": "https://www.gdeltproject.org/", "description": "Global news monitoring"},
        ],
    }

    # 4. Save
    output_path = os.path.join(DATA_DIR, "tracker-data.json")
    with open(output_path, "w") as f:
        json.dump(tracker, f, indent=2)
    print(f"\nTracker data saved to {output_path}")

    # Also save timestamped snapshot
    snapshot_path = os.path.join(LOG_DIR, f"snapshot-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}.json")
    with open(snapshot_path, "w") as f:
        json.dump(tracker, f, indent=2)
    print(f"Snapshot saved to {snapshot_path}")

    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"  Projected deaths today: {projected:,}")
    print(f"  USAspending: {sum(1 for v in usaspending_data.values() if isinstance(v, dict) and 'total_awards' in v and v['total_awards'] > 0)} fiscal years with data")
    print(f"  WHO indicators: {sum(1 for v in who_data.values() if isinstance(v, dict) and 'error' not in v)} of {len(WHO_INDICATORS)} reporting")
    print(f"  GDELT articles: {sum(v.get('count', 0) for v in gdelt_data.values())} in last 30 days")
    print(f"{'='*60}")

    return tracker


if __name__ == "__main__":
    run_pipeline()
