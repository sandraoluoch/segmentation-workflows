//PARAMETERS
SOURCE = "//allen/aics/assay-dev/users/Benji/DataForOthers/Chantelle/NucMorphLattice/cropped_raw/"
OUTPUT_DIR = "//allen/aics/assay-dev/users/Sandi/nuc-morph-analysis/speckle-analysis/raw/raw-max/";
Dataset = "20230425_L02-01_processed_C=0"
Tini = 34;
Tend = 531;

// ============

t = Tini;


for (t=Tini; t<=Tend; t++) {
	
	//open(SOURCE+Dataset+"_T="+t+".tiff");
	run("Bio-Formats Importer", "open="+SOURCE+Dataset+"_T="+t+".tiff");
	selectImage(Dataset+"_T="+t+".tiff");
	run("Z Project...", "projection=[Max Intensity]");
	setOption("ScaleConversions", true);
	run("8-bit");
	saveAs("Tiff", OUTPUT_DIR+"MAX_"+Dataset+"_T="+t+".tiff");
	run("Close All");

}
