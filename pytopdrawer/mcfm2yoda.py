import glob

import pandas as pd

def mcfm_txt_file_to_yoda(txtdir: str, output: str = "mcfm.yoda") -> None:
    if
    for txtfile in glob.glob(txtdir + '/*.txt'):
        if not "TeV_" in txtfile:
            #raise ValueError("Input file must contain 'TeV_' in its name")
            continue;

        group = txtfile.replace('.txt','').split('TeV_')[0]
        type = txtfile.replace('.txt','').split('TeV_')[-1]

        df = pd.read_csv(txtfile,sep=r'\s+',skiprows=5,header=None)
        df.columns = ['xlow','xhigh','sumw','sumw2sq']
        # 1000 to pb and divide by bin width
        df["sumw"] = df["sumw"]/1000
        df["sumw2sq"] = df["sumw2sq"]/1000
        df["sumw2"] = df["sumw2sq"]**2

        with open(output, "a") as f:
            f.write(f"BEGIN YODA_HISTO1D_V2 /{group}/" + type + f"\nPath: /{group}/" + type + "\nTitle: \nType: \"Histo1D\"\n---\n")

        df.astype(float).round(7).to_csv("mcfm.yoda",sep=' ',mode='a',header=False,index=False,columns=['xlow','xhigh','sumw','sumw2'])

        with open(output, "a") as f:
            f.write("END YODA_HISTO1D_V2\n\n")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Convert MCFM txt files to YODA format")
    parser.add_argument("txtdir", type=str, help="Directory containing MCFM txt files")
    parser.add_argument("--output", type=str, default="mcfm.yoda", help="Output YODA file name (default: mcfm.yoda)")
    args = parser.parse_args()

    mcfm_txt_file_to_yoda(args.txtdir, args.output)
