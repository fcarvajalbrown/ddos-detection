use std::sync::{Arc, Mutex};
use tokio::net::TcpStream;
use super::IpStats;

pub async fn process_request(
    ip_stats: &Arc<Mutex<IpStats>>,
    stream: &TcpStream,
) {
    let ip = stream.peer_addr().unwrap().ip().to_string();
    let mut stats = ip_stats.lock().unwrap();

    // Increment request count for this IP
    *stats.entry(ip.clone()).or_insert(0) += 1;

    // Check if threshold exceeded (simplified)
    if *stats.get(&ip).unwrap() > 5 { // Example: 5 requests → alert
        log!("High traffic from {}: {}", ip, stats.get(&ip).unwrap());
    }
}
