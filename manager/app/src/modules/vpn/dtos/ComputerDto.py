class ComputerDto:
    def __init__(self, name: str, dns: str, path: str, ip: str) -> None:
        """Constructor"""
        self.name = name
        self.dns = dns
        self.path = path
        self.ip = ip

    def __repr__(self) -> str:
        return f"ComputerDto(name={self.name})"
