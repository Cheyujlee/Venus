import argparse
import os
import sys

### Currently, the indices are un-changeable; but may be user-supplied in future ###
# This is the current path to the default human genome index directory
human_indexDir = "/srv/disk00/cheyul1/excessSTAR-2.7.8a/indices/human.genomeDir/"
# This is the current path to the default mega virus index directory
virus_indexDir = "/srv/disk00/cheyul1/excessSTAR-2.7.8a/indices/HIV.genomeDir/"


### Creates the Argument Parser object ###
parser = argparse.ArgumentParser(description="VENUS, a subtractive analysis software: " + \
                                             "Virus dEtecting in humaN bUlk and Single cell rna sequencing")


### Specifies the argument for bulk RNA-seq ###
parser.add_argument("--read1", type=str, required=True,
                    help="read1 of RNA-seq (barcode if single-cell)")
parser.add_argument("--read2", type=str, required=False,
                    help="read2 of RNA-seq (cDNA if single-cell)")
# parser.add_argument("--indexDir", type=str, required=False, default=human_indexDir, 
#                     help="user-specified genome index directory")
parser.add_argument("--outDir", type=str, required=False, default=os.getcwd(), 
                    help="directory to store output")
parser.add_argument("--singleCBstart", type=int, required=False, 
                    help="cell barcode's start position")
parser.add_argument("--singleCBlen", type=int, required=False,
                    help="cell barcode's length")
parser.add_argument("--singleUMIstart", type=int, required=False, 
                    help="UMI's start position")
parser.add_argument("--singleUMIlen", type=int, required=False, 
                    help="UMI's length")
parser.add_argument("--singleWhitelist", type=str, required=False, 
                    help="single-cell barcode whitelist")
args = parser.parse_args()


### Creates a python output file ###


### Organizes the output directories for human then virus mappings ###
try:
    os.chdir(args.outDir)
    sys.stdout = open("venus.log", "x")
    print("Current working directory: {0}".format(os.getcwd()))
except:
    print("An error has occured while changing into '{0}' directory".format(args.outDir))
    sys.exit()

try:
    human_outDir = os.getcwd() + "/human/" 
    os.mkdir(human_outDir)
    virus_outDir = os.getcwd() + "/virus/" 
    os.mkdir(virus_outDir)
except:
    print("An error has occured while making directories in '{0}' directory".format(args.outDir))
    sys.exit()



### Firstly maps the RNA-seq reads to the human genome ###

if args.singleCBstart:  # Single-Cell RNA-seq
    cmd="STAR " + \
        "--runThreadN 16 " + \
        "--outFileNamePrefix " + human_outDir + " " \
        "--genomeDir " + human_indexDir + " " \
        "--readFilesIn " + args.read2 + " " + args.read1 + " " \
        "--outReadsUnmapped Fastx " + \
        "--outSAMtype None" + " " \
        "--soloType CB_UMI_Simple" + " " \
        "--soloCBwhitelist " + str(args.singleWhitelist) + " " \
        "--soloCBstart " + str(args.singleCBstart) + " " \
        "--soloCBlen " + str(args.singleCBlen) + " " \
        "--soloUMIstart " + str(args.singleUMIstart) + " " \
        "--soloUMIlen " + str(args.singleUMIlen) + " " \
        "--soloBarcodeReadLength 0"

elif args.read2:  # Bulk Paired-end RNA-seq
        cmd="STAR " + \
            "--runThreadN 16 " + \
            "--outFileNamePrefix " + human_outDir + " " \
            "--genomeDir " + human_indexDir + " " \
            "--readFilesIn " + args.read1 + " " + args.read2 + " " \
            "--outReadsUnmapped Fastx " + \
            "--outSAMtype None"
else:   # Bulk Single-end RNA-seq
    cmd="STAR " + \
        "--runThreadN 16 " + \
        "--outFileNamePrefix " + human_outDir + " " \
        "--genomeDir " + human_indexDir + " " \
        "--readFilesIn " + args.read1 + " " \
        "--outReadsUnmapped Fastx " + \
        "--outSAMtype None"

os.system(cmd)  # Command run
print("Running " + cmd)




### Secondly maps the leftover reads to the viral genome ###

### Appropriately renames the read1 & read2 for the virus mapping ###
args.read1=human_outDir + "Unmapped.out.mate1.fastq"
os.rename(human_outDir + "Unmapped.out.mate1", args.read1)
if args.read2:
    args.read2=human_outDir + "Unmapped.out.mate2.fastq"
    os.rename(human_outDir + "Unmapped.out.mate2", args.read2)

if args.singleCBstart:  # Single-Cell RNA-seq
    cmd="STAR " + \
        "--runThreadN 16 " + \
        "--outFileNamePrefix " + virus_outDir + " " \
        "--genomeDir " + virus_indexDir + " " \
        "--readFilesIn " + args.read1 + " " + args.read2 + " " \
        "--outFilterMultimapNmax 1" + " " \
        "--soloType CB_UMI_Simple" + " " \
        "--soloCBwhitelist " + str(args.singleWhitelist) + " " \
        "--soloCBstart " + str(args.singleCBstart) + " " \
        "--soloCBlen " + str(args.singleCBlen) + " " \
        "--soloUMIstart " + str(args.singleUMIstart) + " " \
        "--soloUMIlen " + str(args.singleUMIlen) + " " \
        "--soloBarcodeReadLength 0"

elif args.read2:  # Bulk Paired-end RNA-seq
        cmd="STAR " + \
            "--runThreadN 16 " + \
            "--outFileNamePrefix " + virus_outDir + " " \
            "--genomeDir " + virus_indexDir + " " \
            "--readFilesIn " + args.read1 + " " + args.read2 + " " \
            "--outFilterMultimapNmax 1"

else:   # Bulk Single-end RNA seq
    cmd="STAR " + \
        "--runThreadN 16 " + \
        "--outFileNamePrefix " + virus_outDir + " " \
        "--genomeDir " + virus_indexDir + " " \
        "--readFilesIn " + args.read1 + " " \
        "--outFilterMultimapNmax 1"
os.system(cmd)  # Command run
print("Running " + cmd)

sys.stdout.close()

# ### Counts & Output the mapping to the mega-virus index ###
# os.chdir(args.outDir)
# unique_virus = open("unique.txt", "x")


### local tests ###
# print("{} is read1 and {} is read2; {} is the genomeDir".format(args.read1, args.read2, args.genomeDir))
