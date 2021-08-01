
import csv
import subprocess
import os
from subprocess import call
import sys

# File I/O

BedFileOpen = open('bedfile_example.csv')  # Opening BED File CSV
BedFileRead = csv.reader(BedFileOpen)

AccessFileOpen = open('SRA_example.csv')  # Opening SRA Accession CSV
AccessFileRead = csv.reader(AccessFileOpen)

range = 10000

# Ref and Beds
bedFile = 'snpBedFile_example'
ref = 'GRCh37.fa'

# Commands
samDump = 'sam-dump'
samDumpFlag = '--aligned-region'
samtoolsView = 'samtools view -b >'
bamFileType = 'bam'
samtoolsMerge = 'samtools merge'
flag = '-b'
bamList = 'ls $search_path > bamlist.txt'

# Paths
sraToolPath = '/.../.../.../.../.../.../sratoolkit.2.9.6-centos_linux64/bin/' # Path for sraToolKit software
GenoCallerIndentPath = '/.../.../.../.../.../.../GenoCaller_indent.py' # Path for GenoCaller Indent Script
refPath = '/.../.../GRCh37' # Path to reference genome
mergeVCFPath = '/.../.../.../.../.../.../merge_vcf.py' # Path to mergeVCF script
markDuplicatesPath = '/.../.../.../MarkDuplicates.jar' # Path to MarkDuplicates

# Dictionaries
d = {}
e = {}


#subprocess.call("%s %s" % ('mkdir', "bams"), shell=True)
#subprocess.call("%s %s" % ('cd ' , 'bams'), shell=True)
#subprocess.call("%s" % ('mkdir emit_all_vcfs'))
#subprocess.call("%s %s" % ('mkdir', "merged_bams"))


AccessFileOpen.seek(0)


for AccessFileRead_row in AccessFileRead:
    if AccessFileRead_row[0] not in d:
        d[AccessFileRead_row[0]] = 1
    else:
        d[AccessFileRead_row[0]] = d[AccessFileRead_row[0]] + 1

    subprocess.call("%s %s_%s" % ('mkdir', AccessFileRead_row[0], d[AccessFileRead_row[0]]), shell=True)
    subprocess.call("%s_%s" % (AccessFileRead_row[0], d[AccessFileRead_row[0]]), shell=True)

    BedFileOpen.seek(0)
    for BedFileReadRow in BedFileRead:
        chromNum = BedFileReadRow[0]
        low = int(BedFileReadRow[1]) - range
        high = int(BedFileReadRow[2]) + range
        SRAAccessNum = AccessFileRead_row[1]
        alias = AccessFileRead_row[0]
        access = AccessFileRead_row[2]
        refSNP = BedFileReadRow[3]
        repeat = d[AccessFileRead_row[0]]

        subprocess.call("%s%s %s %s:%d-%d %s | %s %s_%s_%s_%s_%s.%s" %
                        (sraToolPath, samDump, samDumpFlag, chromNum, low, high, SRAAccessNum, samtoolsView, alias,
                         repeat,access, chromNum, refSNP, bamFileType),
                        shell=True)

    subprocess.call("%s" % bamList,
                    shell=True)

    subprocess.call("%s %s_%s_%s_%s.%s *.%s" %
                    (samtoolsMerge, alias, repeat, access, 'merged', bamFileType, bamFileType),
                    shell=True)

    subprocess.call("%s %s %s_%s_%s_%s.%s %s %s_%s_%s_%s_%s.%s %s %s " %
                    ('samtools', 'sort', alias, repeat, access, 'merged', bamFileType, '-o', alias, repeat, access,
                     'merged', 'sort', bamFileType, '-O', 'bam'),
                    shell=True)

    subprocess.call('%s %s %s %s%s_%s_%s_%s_%s.%s %s%s_%s_%s_%s_%s.%s.%s %s%s %s%s_%s_%s_%s_%s.%s %s%s %s%s' %
                    ('java', '-jar', markDuplicatesPath, 'I=', alias,repeat, access, 'merged', 'sort', bamFileType,
                     'O=',alias, repeat, access, 'merged','sort','Mkdup', bamFileType, 'AS=', 'TRUE', 'M=',alias,
                     repeat, access, 'merged', 'sort', bamFileType, 'REMOVE_DUPLICATES=', 'TRUE',
                     'VALIDATION_STRINGENCY=', 'LENIENT'),
                    shell=True)
  
    subprocess.call('%s %s %s_%s_%s_%s_%s.%s.%s' %
                    ('samtools', 'index', alias, repeat, access, 'merged', 'sort', 'Mkdup', bamFileType),
                    shell=True)

    subprocess.call("%s %s_%s_%s_%s_%s.%s.%s %s" %
                    ('mv', alias, repeat, access, 'merged', 'sort', 'Mkdup', bamFileType, '../merged_bams'),
                    shell=True)

    subprocess.call("%s %s_%s_%s_%s_%s.%s.%s.%s %s" %
                    ('mv', alias, repeat, access, 'merged', 'sort', 'Mkdup', bamFileType,'bai', '../merged_bams'),
                    shell=True)

    os.chdir('../merged_bams')

    subprocess.call("%s %s %s_%s_%s_%s_%s.%s.%s %s%s %s/%s %s" %
                    ('python', GenoCallerIndentPath, alias, repeat, access, 'merged', 'sort', 'Mkdup', bamFileType,
                     bedFile,'.bed', refPath, ref, '5'),
                    shell=True)

    print('%s_%s' % (alias, repeat))

    subprocess.call('%s %s_%s_%s_%s_%s.%s.%s.%s.%s.%s.%s > %s_%s_%s_%s_%s.%s.%s.%s.%s.%s.%s.%s' %
                    ('vcf-sort', alias, repeat, access, 'merged', 'sort','Mkdup', bedFile, 'bed', 'indent5', 'emit_all',
                     'vcf', alias, repeat, access, 'merged', 'sort','Mkdup', bedFile, 'bed', 'indent5', 'emit_all',
                     'sort', 'vcf'),
                    shell=True)

    subprocess.call("%s %s_%s_%s_%s_%s.%s.%s.%s.%s.%s.%s.%s %s " %
                    ('mv', alias, repeat, access, 'merged', 'sort', 'Mkdup', bedFile, 'bed', 'indent5', 'emit_all',
                     'sort', 'vcf', '../emit_all_vcfs'),
                    shell=True)

    e["/%s/%s/%s/%s/%s/%s/%s/%s_%s_%s_%s_%s.%s.%s.%s.%s.%s.%s.%s" %
      ('vault', 'veeramah', 'people', 'Bertino', 'general', 'surc','emit_all_vcfs_new_rev', alias, repeat, access,
       'merged', 'sort','Mkdup', bedFile, 'bed', 'indent5', 'emit_all', 'sort', 'vcf')] = ('%s' % alias)
  
    os.chdir('../')

os.chdir('emit_all_vcfs')

emit_all_list= ('%s_%s' % (access, bedFile))

with open(emit_all_list, 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter='\t')
    for key, value in e.items():
        writer.writerow([key, value])
       
subprocess.call("%s %s '%s' %s > %s_%s" %
                ('sed', '-e', 's/\r//g', emit_all_list, emit_all_list, 'sed'),
                shell=True)


subprocess.call("%s %s %s.%s %s_%s %s/%s" %
                ('python', mergeVCFPath, bedFile, "bed", emit_all_list, 'sed', refPath, ref),
                shell=True)

os.chdir('../')

os.chdir('../')

os.chdir('../')
