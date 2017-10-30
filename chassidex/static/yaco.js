function read_fasta(fasta){
/*function to read a fasta file and remove the header line
  for each protein sequence
*/
	if (!fasta)
		return false;

	//to remove white spaces
	fasta = fasta.trim()

	// split on newlines...
	var lines = fasta.split('\n');

	// check for header
	if (fasta[0] == '>') {
		// remove one line, starting at the first position
		lines.splice(0, 1);
	}

	// join the array back into a single string without newlines and
	// trailing or leading spaces
	fasta = lines.join('').trim();
	return fasta;
}

function percent_gc(nucleotide){
/* function to calculate and return the percent
   GC content of given nucleotide sequence
*/
	gc = 0;
	length = nucleotide.length;
	i=0;

	for(i=0; i<length; i++){
		if (nucleotide[i] == "G")
			gc++;
		if (nucleotide[i] == "C")
			gc++;
	}
	return (gc/length)*100
}

function parseUsageTable(json){
/* function to parse a JSON file into
	an object and return usage_table
*/
	var usage_table = JSON.parse(json);
	return usage_table
}

function optimize(prot,usage_table){
/*function to convert optimise the protein sequence

*/  dna = []
    for(i=0; i<prot.length; i++){
		dict = usage_table[prot[i]];
		maxVal = 0;
        maxCodon = ''
        codons = Object.keys(dict)
        k = 0;
        for(j=0;j<codons.length;j++){
            if (dict[codons[j]] > maxVal){
            	maxVal = dict[codons[j]];
            	maxCodon = codons[j];
                k = j;
            }
    	}
        dna.push([prot[i],maxCodon]);
    }

	//adding stop codon
	maxval = 0
	dict=usage_table["Stop"]
	for(i in dict){
	    if (parseFloat(dict[i]) > maxval){
	        maxval = parseFloat(dict[i]);
	        codon = i;
        }
    }

	dna.push(["Stop",codon]);
	return dna
}

function rna2protein(rna){
/*function to convert an rna sequence to protein
sequence
*/
    dna = ''
    for(i=0;i<rna.length;i++){
        if(rna[i]=='U'){
            dna = dna + 'T';
        }
        else{
            dna = dna + rna[i]; 
        }

    }
    proteinsequence=dna2protein(dna);
	return proteinsequence;
}

function dna2protein(dna){
/* function that converts a nucleotide sequence to
a protein sequence after comparing it with a
given table
*/
    codontable = {"TTT": "F","CTT": "L","ATT": "I","GTT": "V","TTC": "F","CTC": "L","ATC": "I","GTC": "V","TTA": "L","CTA": "L","ATA": "I","GTA": "V","TTG": "L","CTG": "L","ATG": "M","GTG": "V","TCT": "S","CCT": "P","ACT": "T","GCT": "A","TCC": "S","CCC": "P","ACC": "T","GCC": "A","TCA": "S","CCA": "P","ACA": "T","GCA": "A","TCG": "S","CCG": "P","ACG": "T","GCG": "A","TAT": "Y","CAT": "H","AAT": "N","GAT": "D","TAC": "Y","CAC": "H","AAC": "N","GAC": "D","TAA": "Stop","CAA": "Q","AAA": "K","GAA": "E","TAG": "Stop","CAG": "Q","AAG": "K","GAG": "E","TGT": "C","CGT": "R","AGT": "S","GGT": "G","TGC": "C","CGC": "R","AGC": "S","GGC": "G","TGA": "Stop","CGA": "R","AGA": "R","GGA": "G","TGG": "W","CGG": "R","AGG": "R","GGG": "G"}
    prot = '';
    for(i=0;i<dna.length;i+=3){
        codon = dna.slice(i,i+3);
        if(codontable[codon]=="Stop"){
            break;
        }
        prot = prot + codontable[codon];
    }
    return prot
}
