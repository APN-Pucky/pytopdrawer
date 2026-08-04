import glob
import os

import pandas as pd


def mcfm_txt_file_to_yoda(txtdir: str, output: str = "mcfm.yoda", weight=None) -> None:
    if os.path.exists(output):
        os.remove(output)
    for txtfile in glob.glob(txtdir + "/*.txt"):
        if "TeV_" not in txtfile:
            # raise ValueError("Input file must contain 'TeV_' in its name")
            continue

        basename = os.path.basename(txtfile).replace(".txt", "")
        group = basename.split("TeV_")[0]
        type = basename.split("TeV_")[-1]
        wt = ""
        if weight is not None:
            wt = f"[{weight}]"

        underflow = 0.0
        overflow = 0.0
        total = 0.0
        with open(txtfile) as handle:
            for line in handle:
                stripped = line.strip()
                if stripped.startswith("# underflow"):
                    parts = stripped.split()
                    if len(parts) >= 3:
                        underflow = float(parts[-2])
                elif stripped.startswith("# overflow"):
                    parts = stripped.split()
                    if len(parts) >= 3:
                        overflow = float(parts[-2])
                elif stripped.startswith("# sum"):
                    parts = stripped.split()
                    if len(parts) >= 3:
                        total = float(parts[-2])

        df = pd.read_csv(txtfile, sep=r"\s+", skiprows=5, header=None)
        df.columns = ["xlow", "xhigh", "sumw", "sumw2sq"]
        # 1000 to pb and divide by bin width
        df["sumw"] = df["sumw"] / 1000
        df["sumw2sq"] = df["sumw2sq"] / 1000
        df["sumw2"] = df["sumw2sq"] ** 2
        df["sumwx"] = 0.0
        df["sumwx2"] = 0.0
        df["nentries"] = 1.0

        with open(output, "a") as f:
            f.write(
                f"BEGIN YODA_HISTO1D_V2 /{group}/"
                + type
                + wt
                + f"\nPath: /{group}/"
                + type
                + "\nTitle: \n"
                + 'Type: "Histo1D"\n---\n'
            )

        with open(output, "a") as f:
            f.write(
                "# ID     ID      sumw    sumw2   sumwx   sumwx2  numEntries\n"
                + f"Total           Total           {total:.6e}    {total:.6e}    0.000000e+00    0.000000e+00    {total:.6e}\n"
                + f"Underflow       Underflow       {underflow:.6e}    {underflow:.6e}    0.000000e+00    0.000000e+00    {underflow:.6e}\n"
                + f"Overflow        Overflow        {overflow:.6e}    {overflow:.6e}    0.000000e+00    0.000000e+00    {overflow:.6e}\n"
                + "# xlow   xhigh   sumw    sumw2   sumwx   sumwx2  numEntries\n"
            )

        df.astype(float).round(7).to_csv(
            output,
            sep=" ",
            mode="a",
            header=False,
            index=False,
            columns=["xlow", "xhigh", "sumw", "sumw2", "sumwx", "sumwx2", "nentries"],
        )

        with open(output, "a") as f:
            f.write("END YODA_HISTO1D_V2\n\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert MCFM txt files to YODA format"
    )
    parser.add_argument("txtdir", type=str, help="Directory containing MCFM txt files")
    parser.add_argument(
        "--output",
        type=str,
        default="mcfm.yoda",
        help="Output YODA file name (default: mcfm.yoda)",
    )
    parser.add_argument(
        "--weight",
        type=str,
        default=None,
        help="Weight to append to the type in the YODA file (default: None)",
    )
    args = parser.parse_args()

    mcfm_txt_file_to_yoda(args.txtdir, args.output, weight=args.weight)
