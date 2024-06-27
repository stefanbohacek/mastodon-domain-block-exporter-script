import argparse
import urllib.request
import json
from csv import DictWriter

parser = argparse.ArgumentParser("script.py")
parser.add_argument("domain", help="Name of the domain from which to import the domain blocks, eg mastodon.social.", type=str)
parser.add_argument("reject_media", help="Should media attachments be rejected? true/false", type=str)
parser.add_argument("reject_reports", help="Should reports from this domain be rejected? true/false", type=str)
parser.add_argument("obfuscate", help="Should the domain name be partially censored when shown publicly? true/false", type=str)
args = parser.parse_args()

if (args.domain):
    print(f"downloading domain blocks from {args.domain}...")

    with urllib.request.urlopen(f"http://{args.domain}/api/v1/instance/domain_blocks") as url:

        data = json.load(url)
        domain_blocks = []
        # print(json_data)
        print("processing...")

        for item in data:
            domain_blocks.append({
                "#domain": item["domain"],
                "#severity": item["severity"],
                "#reject_media": args.reject_media,
                "#reject_reports": args.reject_reports,
                "#public_comment": item["comment"],
                "#obfuscate": args.obfuscate
            })


        file_name = f"{args.domain}-domain-blocks.csv"
        print(f"saving to {file_name}...")

        export_file = open(file_name, "w")
        writer = DictWriter(export_file, domain_blocks[0].keys())
        writer.writeheader()
        writer.writerows(domain_blocks)
        export_file.close()
        print("done!")
