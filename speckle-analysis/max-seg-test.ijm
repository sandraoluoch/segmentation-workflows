//PARAMETERS
SOURCE = "//allen/aics/assay-dev/users/Sandi/nuc-morph-analysis/speckle-analysis/seg/seg_finalspeckle/"
OUTPUT_DIR = "//allen/aics/assay-dev/users/Sandi/nuc-morph-analysis/speckle-analysis/seg/max-seg/";
Dataset = "SEGfinalspeckle"
Tini = 0;
Tend = 531;

// ============

t = Tini;


for (t=Tini; t<=Tend; t++) {
	
	//open(SOURCE+Dataset+"_T="+t+".tiff");
	run("Bio-Formats Importer", "open="+SOURCE+Dataset+"_T="+t+".tiff");
	selectImage("SEGfinalspeckle_T=0.tiff");
	run("Z Project...", "projection=[Max Intensity]");
	saveAs("Tiff", OUTPUT_DIR+"MAX_"+Dataset+"_T="+t+".tiff");
	run("Close All");
//
}