#!/bin/bash

# every TCGA MAF script should start with these lines:
: ${TCGAMAF_ROOT_DIR:?" environment variable must be set and non-empty; defines the path to the TCGA MAF directory"}
source ${TCGAMAF_ROOT_DIR}/../../gidget/util/gidget_util.sh


#using UCSC known genes
echo
echo map transcipt id to uniprot id
knownGene=$TCGAMAF_REFERENCES_DIR/HumanDB/hg18_kgXref.txt
cut -d'	' -f1,3 $knownGene | awk '{if($2 != "") {print $0}}' > $TCGAMAF_REFERENCES_DIR/knowngene_to_protein
knownGene=$TCGAMAF_REFERENCES_DIR/HumanDB/hg19_kgXref.txt
cut -d'	' -f1,3 $knownGene | awk '{if($2 != "") {print $0}}' >> $TCGAMAF_REFERENCES_DIR/knowngene_to_protein

echo map transcript id to gene id
knownGene=$TCGAMAF_REFERENCES_DIR/HumanDB/hg18_kgXref.txt
cut -d'	' -f1,5 $knownGene | awk '{if($2 != "") {print $0}}' > $TCGAMAF_REFERENCES_DIR/knowntranscript_to_gene
knownGene=$TCGAMAF_REFERENCES_DIR/HumanDB/hg19_kgXref.txt
cut -d'	' -f1,5 $knownGene | awk '{if($2 != "") {print $0}}' >> $TCGAMAF_REFERENCES_DIR/knowntranscript_to_gene