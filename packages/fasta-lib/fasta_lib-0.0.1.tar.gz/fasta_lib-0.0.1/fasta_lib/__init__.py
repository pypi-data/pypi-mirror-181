# generator for reading fasta files
# returns header and seq

def fasta_generator(filename):
	with open(filename, 'r') as f:
		lines = f.readlines()
		header = ''
		seq = ''
		for line in lines:
			if line.startswith('>') or line == lines[-1]:
				yield header, seq
				header = line
				seq = ''

			else:				
				seq += line.strip('/n')
				
				
