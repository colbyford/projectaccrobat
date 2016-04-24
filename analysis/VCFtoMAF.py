#!/usr/bin/python3

def vcftomaf(file):
	with open(file) as rawfile, open(file+'_outputtemp.vcf', 'a') as vcffile:	
		for line in rawfile.readlines():
			if line.startswith('Hugo_Symbol'):
				continue
			line = line.rstrip()
			columns = line.split("\t")
			chromo = ['chr'+columns[4]]
			start = [columns[5]]
			ID = [columns[13]]
			QUAL = ['.']
			Filter = ['.']
			ref = [columns[10]]
			alt = [columns[12]]
			INFO = [columns[15]]
			vcf = chromo+start+ID+ref+alt+QUAL+Filter+INFO
			vcff = "\t".join(vcf)
			if columns[8] == 'Missense_Mutation':
				vcffile.write(vcff+'\n')
		vcffile.close()
	return(vcffile)

file = 'sampledata.maf'
print(vcftomaf(file))