use serde::Deserialize;
use std::fs;

#[derive(Debug, Deserialize)]
pub struct Config {
    pub rate_limit: u64,  // Requests/sec threshold
}

pub fn load_config() -> Result<Config, toml::de::Error> {
    let config_str = match std::fs::read_to_string("config/thresholds.toml") {
        Ok(s) => s,
        Err(e) => return Err(e),
    };
    toml::from_str(&config_str)
}
