"""Read-only public Trident showcase with synthetic, non-routable examples."""

from __future__ import annotations

import streamlit as st


st.set_page_config(
    page_title="Trident SOC demo",
    page_icon=":material/security:",
    layout="wide",
)


# These records are intentionally self-contained. This public app never imports
# the local SOC backend, opens a database, or reads environment secrets.
ALERTS = [
    {
        "id": "TR-DEMO-1042",
        "severity": "Critical",
        "title": "Unusual login followed by admin role activation",
        "asset": "acct-demo-01",
        "source": "203.0.113.42",
        "destination": "idp.example.test",
        "age": "8 min",
        "events": 18,
        "evidence": [
            "Successful sign-in from a documentation-only address range.",
            "Privileged role activation followed the sign-in by 3 minutes.",
            "No matching change window appears in this synthetic scenario.",
        ],
        "next_step": "Validate the sign-in and role activation with the account owner.",
    },
    {
        "id": "TR-DEMO-1041",
        "severity": "High",
        "title": "Encoded script started from a demo workstation",
        "asset": "host-demo-07",
        "source": "192.0.2.17",
        "destination": "files.example.test",
        "age": "21 min",
        "events": 12,
        "evidence": [
            "A script interpreter started with an encoded command-line argument.",
            "The process attempted to contact a documentation-only destination.",
            "This example contains no real endpoint or telemetry data.",
        ],
        "next_step": "Review the parent process and compare the command with an approved change.",
    },
    {
        "id": "TR-DEMO-1038",
        "severity": "Medium",
        "title": "Repeated authentication failures for a service identity",
        "asset": "service-demo-02",
        "source": "198.51.100.23",
        "destination": "directory.example.test",
        "age": "44 min",
        "events": 41,
        "evidence": [
            "Authentication failures repeated across two synthetic hosts.",
            "The event rate increased above the example baseline.",
            "No successful authentication is present in the sample window.",
        ],
        "next_step": "Check the service schedule and confirm whether a credential rotation is underway.",
    },
    {
        "id": "TR-DEMO-1031",
        "severity": "Low",
        "title": "Outbound DNS request to a newly observed test domain",
        "asset": "host-demo-12",
        "source": "198.51.100.44",
        "destination": "updates.example.test",
        "age": "2 hr",
        "events": 6,
        "evidence": [
            "A new test domain appeared in the synthetic DNS sample.",
            "The example host made six lookups in the review window.",
            "No payload transfer or execution is represented here.",
        ],
        "next_step": "Confirm whether the domain belongs to an approved software test.",
    },
]

SEVERITIES = ["Critical", "High", "Medium", "Low"]


st.title(":material/security: Trident SOC workspace")
st.caption("Analyst workflow preview · public demonstration")
st.info(
    "**Synthetic demo only.** Every alert and identifier on this page is fictional. "
    "This public showcase has no QRadar connection, sign-in, persistent storage, "
    "or write actions. Do not enter real incident data.",
    icon=":material/info:",
)

with st.sidebar:
    st.subheader("Explore the sample")
    severity_filter = st.multiselect(
        "Severity",
        SEVERITIES,
        default=SEVERITIES,
        help="Filters the static synthetic examples shown on this page.",
    )
    search = st.text_input(
        "Search examples",
        placeholder="Alert, asset, or destination",
    ).strip().casefold()
    st.divider()
    st.caption("Read-only showcase · no account or production data")

visible_alerts = [
    alert
    for alert in ALERTS
    if alert["severity"] in severity_filter
    and search
    in " ".join(
        [
            alert["id"],
            alert["severity"],
            alert["title"],
            alert["asset"],
            alert["source"],
            alert["destination"],
        ]
    ).casefold()
]

critical_count = sum(alert["severity"] == "Critical" for alert in visible_alerts)
high_count = sum(alert["severity"] == "High" for alert in visible_alerts)
event_count = sum(alert["events"] for alert in visible_alerts)

metric_columns = st.columns(3)
metric_columns[0].metric("Sample alerts", len(visible_alerts))
metric_columns[1].metric("Critical / high", f"{critical_count} / {high_count}")
metric_columns[2].metric("Example events", event_count)

st.subheader("Offense queue")
if not visible_alerts:
    st.warning("No synthetic alerts match these filters.")
else:
    st.dataframe(
        [
            {
                "Alert": alert["id"],
                "Severity": alert["severity"],
                "Summary": alert["title"],
                "Asset": alert["asset"],
                "Source": alert["source"],
                "Destination": alert["destination"],
                "Age": alert["age"],
                "Events": alert["events"],
            }
            for alert in visible_alerts
        ],
        hide_index=True,
    )

    st.subheader("Investigation preview")
    selected_id = st.selectbox(
        "Choose a synthetic alert",
        [alert["id"] for alert in visible_alerts],
        format_func=lambda alert_id: next(
            f"{alert_id} · {alert['title']}"
            for alert in visible_alerts
            if alert["id"] == alert_id
        ),
    )
    selected = next(alert for alert in visible_alerts if alert["id"] == selected_id)

    with st.container(border=True):
        st.markdown(f"**{selected['severity']} · {selected['title']}**")
        st.caption(
            f"{selected['id']} · {selected['asset']} · {selected['age']} ago · "
            f"{selected['events']} synthetic events"
        )
        st.markdown("**Evidence summary**")
        for item in selected["evidence"]:
            st.write(f"• {item}")
        st.markdown("**Suggested analyst follow-up**")
        st.write(selected["next_step"])

st.divider()
st.caption(
    "Trident is a workflow preview, not a live SIEM. This page uses static synthetic "
    "examples only; it has no connector calls, case-note submission, or write actions."
)
