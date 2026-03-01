use log::{info, error};

pub fn setup_logger() {
    env_logger::init();
}

#[macro_export]
macro_rules! log {
    ($($t:tt)*) => {{
        if let Ok(level) = std::env::var("LOG_LEVEL") {
            if level == "error" {
                error!($($t)*);
            } else {
                info!($($t)*);
            }
        } else {
            info!($($t)*);
        }
    }}
}
