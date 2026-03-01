mod monitor;
mod limiter;
mod alert;
mod utils;

use tokio::net::{TcpListener, UdpSocket};
use std::sync::Arc;
use std::collections::HashMap;

// Global state for shared data (e.g., IP tracking)
type IpStats = HashMap<String, u64>; // { ip: requests_count }

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize logging
    utils::setup_logger();

    // Load thresholds from config
    let thresholds = match utils::load_config() {
        Ok(cfg) => cfg,
        Err(e) => eprintln!("Failed to load config: {}", e);
    };

    // Shared state for monitoring/limiting
    let ip_stats = Arc::new(IpStats::new());
    let limiter = Arc::new(limiter::RateLimiter::new(thresholds.rate_limit));

    // Start TCP/UDP listeners (example)
    tokio::spawn(async move {
        if let Err(e) = start_tcp_listener(&ip_stats, &limiter).await {
            eprintln!("TCP listener failed: {}", e);
        }
    });

    tokio::spawn(async move {
        if let Err(e) = start_udp_listener(&ip_stats, &limiter).await {
            eprintln!("UDP listener failed: {}", e);
        }
    });

    Ok(())
}

// Helper functions for TCP/UDP listeners (to be implemented)
async fn start_tcp_listener(
    ip_stats: &Arc<IpStats>,
    limiter: &Arc<limiter::RateLimiter>,
) -> Result<(), std::io::Error> {
    let listener = TcpListener::bind("0.0.0.0:8080")?;
    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                tokio::spawn(async move {
                    if limiter.check(&stream.peer_addr().unwrap()) {
                        monitor::process_request(&ip_stats, &stream).await;
                    }
                });
            }
            Err(e) => eprintln!("Connection error: {}", e),
        }
    }
    Ok(())
}

async fn start_udp_listener(
    ip_stats: &Arc<IpStats>,
    limiter: &Arc<limiter::RateLimiter>,
) -> Result<(), std::io::Error> {
    let socket = UdpSocket::bind("0.0.0.0:8081")?;
    loop {
        let mut buf = [0; 1024];
        match socket.recv_from(&mut buf).await? {
            (_, addr) => {
                tokio::spawn(async move {
                    if limiter.check(&addr.ip()) {
                        monitor::process_udp_request(ip_stats, &addr);
                    }
                });
            }
        }
    }
}
