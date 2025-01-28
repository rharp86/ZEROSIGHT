import re
import socket
from typing import Union
from ipaddress import ip_address, IPv4Address, IPv6Address

class TargetValidator:
    @staticmethod
    def is_valid_domain(domain: str) -> bool:
        """Validate domain name format"""
        domain_pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        return bool(re.match(domain_pattern, domain))
    
    @staticmethod
    def is_valid_ip(ip: str) -> bool:
        """Validate IP address format"""
        try:
            ip_obj = ip_address(ip)
            return isinstance(ip_obj, (IPv4Address, IPv6Address))
        except ValueError:
            return False
    
    @staticmethod
    def can_resolve(target: str) -> bool:
        """Check if target can be resolved"""
        try:
            socket.gethostbyname(target)
            return True
        except socket.gaierror:
            return False

def validate_target(target: str) -> bool:
    """Validate a target (domain or IP)"""
    validator = TargetValidator()
    return (validator.is_valid_domain(target) or 
            validator.is_valid_ip(target))