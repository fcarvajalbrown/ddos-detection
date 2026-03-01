use std::collections::VecDeque;
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Debug)]
pub struct RateLimiter {
    tokens: u64,
    max_tokens: u64,
    window_size_secs: u64,
}

impl RateLimiter {
    pub fn new(max_requests_per_sec: u64) -> Self {
        Self {
            tokens: max_requests_per_sec,
            max_tokens: max_requests_per_sec,
            window_size_secs: 1, // 1-second window
        }
    }

    pub fn check(&mut self, ip: &str) -> bool {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();

        // Reset tokens every window
        if now % self.window_size_secs == 0 {
            self.tokens = self.max_tokens;
        }

        // Check if IP is allowed
        if self.tokens > 0 {
            self.tokens -= 1;
            true
        } else {
            false
        }
    }
}
