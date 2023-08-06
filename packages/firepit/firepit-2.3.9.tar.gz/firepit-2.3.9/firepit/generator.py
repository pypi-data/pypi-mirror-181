import argparse
import json
import random
import re

from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date

import pandas as pd
from stix2.v20 import Bundle, Identity

from firepit.timestamp import timefmt
from firepit.woodchipper import dict2observation


def infer_protocols(dst_port):
    '''Try to guess a sensible list of protos based on destination port'''
    tcp = ['ip', 'tcp']
    udp = ['ip', 'udp']
    if dst_port in [80, 3128, 8080]:
        return tcp + ['http']
    if dst_port in [443]:
        return tcp + ['tls']
    if dst_port in [53, 500]:
        return udp
    # Default to tcp
    return tcp


class Generator:
    def __init__(self, ident, start_time, end_time, assets, domains):
        self.ident = ident
        self.start_time = start_time
        self.end_time = end_time
        self.duration = end_time - start_time
        self.assets = assets
        self.domains = domains
        self.conns = []
        self.scos = set()

    def random_timestamp(self):
        secs = random.choice(range(int(self.duration.total_seconds())))
        usecs = random.choice(range(100000))
        offset = timedelta(seconds=secs, microseconds=usecs)
        return self.start_time + offset

    def make_random(self):
        timestamp = self.random_timestamp()
        obj = {
            'first_observed': timefmt(timestamp, 6),
            'last_observed': timefmt(timestamp, 6),
            'number_observed': 1
        }
        # Pick random asset and domain to make a conn
        i = random.choice(range(len(self.assets.index)))
        obj.update(dict(self.assets.loc[i]))
        j = random.choice(range(len(self.domains.index)))
        obj.update(dict(self.domains.loc[j]))
        obj['network-traffic:src_ref'] = 'x-oca-asset:ip_refs[0]'
        obj['network-traffic:src_port'] = random.choice(range(49152, 65536))
        obj['network-traffic:dst_ref'] = 'domain-name:resolves_to_refs[0]'
        dst_port = random.choice([53, 443])
        obj['network-traffic:dst_port'] = dst_port
        obj['network-traffic:protocols'] = infer_protocols(dst_port)
        return dict2observation(self.ident, obj)


def delta(s):
    result = None
    m = re.match(r'([0-9]+)([dhms])', s)
    if m:
        value = int(m.group(1))
        unit = m.group(2)
        if unit == 'd':
            result = timedelta(days=value)
        elif unit == 'h':
            result = timedelta(hours=value)
        elif unit == 'm':
            result = timedelta(minutes=value)
        elif unit == 's':
            result = timedelta(seconds=value)
    return result


def main():
    parser = argparse.ArgumentParser('Generate a bundle of STIX observed-data')
    parser.add_argument('-n', '--num', metavar='N', default=2000, type=int)
    parser.add_argument('-s', '--start-time', metavar='DATETIME')
    parser.add_argument('-e', '--end-time', metavar='DATETIME')
    parser.add_argument('-a', '--assets', metavar='CSVFILE', default=None)
    parser.add_argument('-d', '--domains', metavar='CSVFILE', default=None)
    parser.add_argument('--source-net', metavar='CIDR', default='192.168.1.0/24')
    parser.add_argument('--dest-net', metavar='CIDR', default='10.0.0.0/8')
    parser.add_argument('-u', '--add-user', action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument('-i', '--identity', metavar='NAME', default='bnudle-generator')
    parser.add_argument('--seed', metavar='SEED', type=int)
    args = parser.parse_args()

    if args.seed:
        random.seed(args.seed)

    if args.end_time:
        end_time = parse_date(args.end_time)  # UTC "aware"
    else:
        end_time = datetime.utcnow()
    if args.start_time:
        s = delta(args.start_time)
        if s:
            # Relative
            start_time = end_time - s
        else:
            # Absolute
            start_time = parse_date(args.start_time)  # UTC "aware"
    else:
        start_time = end_time - delta('5m')

    if args.domains:
        domains = pd.read_csv(args.domains)
    else:
        pass  #TODO

    if args.assets:
        assets = pd.read_csv(args.assets)
    else:
        pass  #TODO

    ident = Identity(name='data-generator', identity_class='program')
    dgen = Generator(ident, start_time, end_time, assets, domains)
    objects = [dgen.make_random() for i in range(args.num)]
    bundle = json.loads(str(Bundle(ident, objects=[])))

    # Replace empty objects array with the JSON ones we built above
    bundle['objects'] += sorted(objects, key=lambda i: i['first_observed'])
    print(json.dumps(bundle, indent=4))


if __name__ == '__main__':
    main()
