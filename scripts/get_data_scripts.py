import xml.etree.ElementTree as ET
import csv

NS = {"db": "http://www.drugbank.ca"}

def get_text(x):
    if x is None or x.text is None:
        return None
    return x.text.strip()

def get_primary_id(drug):
    for dbid in drug.findall("db:drugbank-id", NS):
        if dbid.get("primary") == "true":
            return get_text(dbid)
    first = drug.find("db:drugbank-id", NS)
    return get_text(first)

def get_smiles(drug):
    paths = [
        "db:calculated-properties/db:property",
        "db:experimental-properties/db:property"
    ]
    for path in paths:
        for prop in drug.findall(path, NS):
            kind = get_text(prop.find("db:kind", NS))
            if kind and kind.upper() == "SMILES":
                val = get_text(prop.find("db:value", NS))
                if val:
                    return val
    return get_text(drug.find("db:smiles", NS))

def extract_targets(drug):
    block = drug.find("db:targets", NS)
    if block is None:
        return []
    out = []
    for t in block.findall("db:target", NS):
        organism = get_text(t.find("db:organism", NS)) or ""
        polys = t.findall("db:polypeptide", NS)
        for p in polys:
            uniprot = p.get("id")
            seq = get_text(p.find("db:amino-acid-sequence", NS)) or ""
            if uniprot:
                out.append((uniprot, seq, organism))
    return out

def main():
    xml_path = "full_database.xml"
    out_csv = "drugbank_dti_clean.csv"

    tree = ET.parse(xml_path)
    root = tree.getroot()

    with open(out_csv, "w", newline="", encoding="utf8") as f:
        w = csv.writer(f)
        w.writerow([
            "drugbank_id",
            "drug_name",
            "smiles",
            "protein_uniprot_id",
            "protein_sequence",
            "organism",
            "label"
        ])

        total_rows = 0

        for drug in root.findall("db:drug", NS):
            if drug.get("type", "").lower() != "small molecule":
                continue

            did = get_primary_id(drug)
            name = get_text(drug.find("db:name", NS)) or ""
            smiles = get_smiles(drug)
            if not did or not smiles:
                continue

            targets = extract_targets(drug)
            for uni, seq, org in targets:
                w.writerow([did, name, smiles, uni, seq, org, 1])
                total_rows += 1

    print("Done. Total pairs:", total_rows)
    print("Saved to", out_csv)

if __name__ == "__main__":
    main()
