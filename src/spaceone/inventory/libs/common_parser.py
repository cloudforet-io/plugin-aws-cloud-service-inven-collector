import ipaddress
import logging
import re

IP_PATTERN = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

AWS_SUBNET_MIN_BIT_MASK = 16
AWS_SUBNET_MAX_BIT_MASK = 28

_LOGGER = logging.getLogger(__name__)


def get_name_from_tags(tags: list):
    if not isinstance(tags, list):
        return None

    name = None
    for tag in tags:
        if tag.get('Key') == 'Name':
            name = tag.get('Value')
            break
    return name


def _check_cidr_format(cidr):
    if not isinstance(cidr, str):
        return None, None

    split_cidr = cidr.split('/')
    if len(split_cidr) != 2:
        return None, None

    ip = split_cidr[0]
    bit = split_cidr[1]
    if not is_ip_format(split_cidr[0]):
        return None, None

    if not is_subnet_bit_mask(split_cidr[1]):
        return None, None

    return ip, bit


def calculate_ip_ranges_from_cidr(cidr, start_shift=0, end_shift=0):
    ip, bit = parse_ip_and_bit_from_cidr(cidr)
    if is_ip_format(ip) and is_subnet_bit_mask(bit):
        net = ipaddress.ip_network(cidr)
        start_at = 0 + start_shift
        end_at = 0 - 1 - end_shift
        return str(net[start_at]), str(net[end_at])
    return None, None


def get_nth_ip_from_cidr(cidr, n):
    ip, bit = parse_ip_and_bit_from_cidr(cidr)
    if is_ip_format(ip) and is_subnet_bit_mask(bit):
        net = ipaddress.ip_network(cidr)
        return net[n]
    return None


def parse_ip_and_bit_from_cidr(cidr):
    ip, bit = _check_cidr_format(cidr)
    if ip and bit:
        return ip, bit
    return None, None


def is_ip_format(ip):
    if not ip or not IP_PATTERN.match(ip):
        return False

    blocks = ip.split('.')
    for block in blocks:
        if not 0 <= int(block) <= 255:
            return False

    return True


def is_subnet_bit_mask(bit):
    result = False
    try:
        if bit and isinstance(bit, str):
            bit = int(bit)
            if AWS_SUBNET_MIN_BIT_MASK <= bit <= AWS_SUBNET_MAX_BIT_MASK:
                result = True
    except Exception:
        _LOGGER.error('Error parse cidr_bit string to int')

    return result
