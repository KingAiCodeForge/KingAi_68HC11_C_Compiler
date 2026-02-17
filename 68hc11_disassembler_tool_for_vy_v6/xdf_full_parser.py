"""
Comprehensive XDF Parser - Extract ALL addresses by category
Parses Enhanced v1.2 XDF to map every table/constant/flag/patch
"""
import xml.etree.ElementTree as ET
import html
import json
from pathlib import Path
from collections import defaultdict

def decode_html(text):
    """Decode HTML entities like &#013;&#010; (CRLF)"""
    if not text:
        return ""
    return html.unescape(text).replace('\r\n', ' ').replace('\n', ' ').strip()

def parse_xdf(xdf_path):
    """Parse XDF and extract all addresses organized by category"""
    tree = ET.parse(xdf_path)
    root = tree.getroot()
    
    # Get category names
    categories = {}
    for cat in root.findall('.//XDFCATEGORY'):
        cat_id = cat.get('id')
        name_elem = cat.find('XDFCATEGORYNAME')
        if cat_id and name_elem is not None:
            categories[cat_id] = decode_html(name_elem.text)
    
    # Storage for all elements
    data = {
        'categories': categories,
        'tables': defaultdict(list),
        'constants': defaultdict(list),
        'flags': defaultdict(list),
        'patches': defaultdict(list),
        'addresses': {}  # addr -> element info
    }
    
    # Parse Tables
    for table in root.findall('.//XDFTABLE'):
        cat_mem = table.find('CATEGORYMEM')
        cat_id = cat_mem.get('category', '0') if cat_mem is not None else '0'
        cat_name = categories.get(cat_id, 'Uncategorized')
        
        title_elem = table.find('title')
        title = decode_html(title_elem.text) if title_elem is not None else 'NO TITLE'
        
        # Get address from X-axis or Y-axis
        addresses = []
        for axis in table.findall('.//XDFAXIS'):
            emb = axis.find('EMBEDDEDDATA')
            if emb is not None:
                addr = emb.get('mmedaddress', '')
                if addr:
                    addresses.append(addr)
        
        if addresses:
            addr = addresses[0]  # Primary address
            entry = {
                'address': addr,
                'title': title,
                'category': cat_name,
                'type': 'TABLE',
                'all_addresses': addresses
            }
            data['tables'][cat_name].append(entry)
            data['addresses'][addr.upper()] = entry
    
    # Parse Constants
    for const in root.findall('.//XDFCONSTANT'):
        cat_mem = const.find('CATEGORYMEM')
        cat_id = cat_mem.get('category', '0') if cat_mem is not None else '0'
        cat_name = categories.get(cat_id, 'Uncategorized')
        
        title_elem = const.find('title')
        title = decode_html(title_elem.text) if title_elem is not None else 'NO TITLE'
        
        emb = const.find('EMBEDDEDDATA')
        if emb is not None:
            addr = emb.get('mmedaddress', '')
            if addr:
                entry = {
                    'address': addr,
                    'title': title,
                    'category': cat_name,
                    'type': 'CONSTANT'
                }
                data['constants'][cat_name].append(entry)
                data['addresses'][addr.upper()] = entry
    
    # Parse Flags
    for flag in root.findall('.//XDFFLAG'):
        cat_mem = flag.find('CATEGORYMEM')
        cat_id = cat_mem.get('category', '0') if cat_mem is not None else '0'
        cat_name = categories.get(cat_id, 'Uncategorized')
        
        title_elem = flag.find('title')
        title = decode_html(title_elem.text) if title_elem is not None else 'NO TITLE'
        
        emb = flag.find('EMBEDDEDDATA')
        if emb is not None:
            addr = emb.get('mmedaddress', '')
            mask = emb.get('mmedtypeflags', '')
            if addr:
                entry = {
                    'address': addr,
                    'title': title,
                    'category': cat_name,
                    'type': 'FLAG',
                    'mask': mask
                }
                data['flags'][cat_name].append(entry)
                data['addresses'][addr.upper()] = entry
    
    # Parse Patches
    for patch in root.findall('.//XDFPATCH'):
        cat_mem = patch.find('CATEGORYMEM')
        cat_id = cat_mem.get('category', '0') if cat_mem is not None else '0'
        cat_name = categories.get(cat_id, 'Uncategorized')
        
        title_elem = patch.find('title')
        title = decode_html(title_elem.text) if title_elem is not None else 'NO TITLE'
        
        # Patches can have multiple data entries
        addresses = []
        for data_elem in patch.findall('.//XDFPATCHDATA'):
            addr = data_elem.get('mmedaddress', '')
            if addr:
                addresses.append(addr)
        
        if addresses:
            entry = {
                'addresses': addresses,
                'title': title,
                'category': cat_name,
                'type': 'PATCH'
            }
            data['patches'][cat_name].append(entry)
            for addr in addresses:
                data['addresses'][addr.upper()] = entry
    
    return data

def print_category_summary(data, output_file=None):
    """Print summary of all categories and element counts"""
    lines = []
    lines.append('=' * 80)
    lines.append('XDF CATEGORY SUMMARY')
    lines.append('=' * 80)
    
    for cat_id, cat_name in sorted(data['categories'].items(), key=lambda x: int(x[0]) if x[0].isdigit() else 999):
        table_count = len(data['tables'][cat_name])
        const_count = len(data['constants'][cat_name])
        flag_count = len(data['flags'][cat_name])
        patch_count = len(data['patches'][cat_name])
        total = table_count + const_count + flag_count + patch_count
        
        lines.append(f'\n[{cat_id}] {cat_name}')
        lines.append(f'  Tables: {table_count}, Constants: {const_count}, Flags: {flag_count}, Patches: {patch_count}')
        lines.append(f'  Total: {total} elements')
    
    output = '\n'.join(lines)
    print(output)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)

def export_category_addresses(data, category_name, output_file):
    """Export all addresses for a specific category"""
    lines = []
    lines.append('=' * 80)
    lines.append(f'CATEGORY: {category_name}')
    lines.append('=' * 80)
    
    # Tables
    if data['tables'][category_name]:
        lines.append(f'\n--- TABLES ({len(data["tables"][category_name])}) ---')
        for item in sorted(data['tables'][category_name], key=lambda x: x['address']):
            lines.append(f'{item["address"]:10s} {item["title"]}')
    
    # Constants
    if data['constants'][category_name]:
        lines.append(f'\n--- CONSTANTS ({len(data["constants"][category_name])}) ---')
        for item in sorted(data['constants'][category_name], key=lambda x: x['address']):
            lines.append(f'{item["address"]:10s} {item["title"]}')
    
    # Flags
    if data['flags'][category_name]:
        lines.append(f'\n--- FLAGS ({len(data["flags"][category_name])}) ---')
        for item in sorted(data['flags'][category_name], key=lambda x: x['address']):
            lines.append(f'{item["address"]:10s} [{item["mask"]}] {item["title"]}')
    
    # Patches
    if data['patches'][category_name]:
        lines.append(f'\n--- PATCHES ({len(data["patches"][category_name])}) ---')
        for item in data['patches'][category_name]:
            addrs = ', '.join(item['addresses'])
            lines.append(f'{addrs:30s} {item["title"]}')
    
    output = '\n'.join(lines)
    print(output)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)

def search_keywords(data, keywords):
    """Search for keywords across all elements"""
    results = []
    for addr, info in data['addresses'].items():
        title = info.get('title', '')
        if any(kw.lower() in title.lower() for kw in keywords):
            results.append(info)
    return results

if __name__ == '__main__':
    xdf_path = Path(r'C:\Users\jason\OneDrive\Documents\TunerPro Files\VY_V6_$060A_Enhanced_v1.2.xdf')
    output_dir = Path(r'R:\VY_V6_Assembly_Modding\xdf_analysis')
    output_dir.mkdir(exist_ok=True)
    
    print('Parsing XDF file...')
    data = parse_xdf(xdf_path)
    
    # Print summary
    print_category_summary(data, output_dir / 'category_summary.txt')
    
    # Export key categories
    key_categories = [
        'Spark',
        'Fuel',
        'Transmission',
        'RPM',
        'Knock',
        'EGR',
        'Performance'
    ]
    
    for cat_name in key_categories:
        if cat_name in data['categories'].values():
            output_file = output_dir / f'{cat_name.replace(" ", "_")}_addresses.txt'
            export_category_addresses(data, cat_name, output_file)
    
    # Search for spark-related items
    print('\n\n' + '=' * 80)
    print('SPARK/IGNITION KEYWORD SEARCH')
    print('=' * 80)
    spark_results = search_keywords(data, ['spark', 'ignition', 'timing', 'advance', 'EST'])
    for item in spark_results[:30]:
        addr = item.get('address') or item.get('addresses', [''])[0]
        print(f'{addr:10s} [{item["type"]:8s}] {item["title"][:70]}')
    
    # Search for RPM
    print('\n\n' + '=' * 80)
    print('RPM KEYWORD SEARCH')
    print('=' * 80)
    rpm_results = search_keywords(data, ['rpm', 'engine speed'])
    for item in rpm_results[:20]:
        addr = item.get('address') or item.get('addresses', [''])[0]
        print(f'{addr:10s} [{item["type"]:8s}] {item["title"][:70]}')
    
    # Look for 0x17283 specifically
    print('\n\n' + '=' * 80)
    print('SEARCHING FOR 0x17283')
    print('=' * 80)
    if '0X17283' in data['addresses']:
        info = data['addresses']['0X17283']
        print(f'FOUND: {info}')
    else:
        print('0x17283 NOT FOUND in XDF addresses')
    
    # Export full database to JSON
    json_path = output_dir / 'xdf_full_database.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        # Convert defaultdict to dict for JSON serialization
        export_data = {
            'categories': data['categories'],
            'tables': {k: v for k, v in data['tables'].items()},
            'constants': {k: v for k, v in data['constants'].items()},
            'flags': {k: v for k, v in data['flags'].items()},
            'patches': {k: v for k, v in data['patches'].items()},
            'addresses': data['addresses']
        }
        json.dump(export_data, f, indent=2)
    
    print(f'\n\nFull database exported to: {json_path}')
    print(f'Category exports in: {output_dir}')
