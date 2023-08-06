from dataclasses import dataclass
from BridgeAccesslib import ExtendedBridge
from MainAccesslib.hearbeat_thread import KillableThread


@dataclass
class Connection:
    ip_addr: str
    sync_port: int
    async_port: int
    lib_absolute_path: str
    sleep_interval: float = 2.5

    def __enter__(self) -> ExtendedBridge:
        self._bridge = ExtendedBridge(self.ip_addr, self.sync_port, self.async_port, self.lib_absolute_path)
        self.heartbeat = KillableThread(self._bridge.update_hb, sleep_interval=2.5)
        self.heartbeat.start()
        return self._bridge

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self._bridge:
            self._bridge.close_communication()
            self.heartbeat.kill()
        return False
