#!/usr/bin/env python3
"""Report duplicate scalar addresses from an explicitly supplied XDF JSON export."""
import argparse
import json
from collections import Counter
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('json', type=Path)
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.json.read_text(encoding='utf-8-sig'))
        scalars = data['scalars']
        if not isinstance(scalars, list) or any(not isinstance(s, dict) for s in scalars):
            raise ValueError('scalars must be a list of objects')
        addresses = [s['address'] for s in scalars if s.get('address')]
        if any(not isinstance(a, (str, int)) for a in addresses):
            raise ValueError('scalar addresses must be strings or integers')
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.error(str(exc))
    duplicates = sorted((str(a), count) for a, count in Counter(addresses).items() if count > 1)
    print(f'Duplicate scalar addresses: {len(duplicates)}')
    for addr, count in duplicates[:5]:
        print(f'  {addr}: {count} entries')
        for item in scalars:
            if str(item.get('address')) == addr:
                print(f"    - {str(item.get('title', ''))[:60]} = {item.get('value', '')} {item.get('unit', '')}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
