use std::fs;

pub fn log_alert(ip: &str, requests: u64) {
    let timestamp = chrono::Local::now().format("%Y-%m-%d %H:%M:%S").to_string();
    let log_entry = format!(
        "[{}] ALERT: High traffic from {} (requests: {})\n",
        timestamp, ip, requests
    );

    fs::write("/var/log/dds_alerts.log", log_entry).unwrap_or_default();
}
