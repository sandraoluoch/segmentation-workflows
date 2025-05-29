//PARAMETERS
SOURCE = "//allen/aics/assay-dev/users/Sandi/nuc-morph-analysis/speckle-analysis/seg/seg-overlay/"
OUTPUT_DIR = "//allen/aics/assay-dev/users/Sandi/nuc-morph-analysis/speckle-analysis/seg/max-overlay/";
Dataset = "overlay_seg_"
Tini = 0;
Tend = 531;

// ============

t = Tini;


for (t=Tini; t<=Tend; t++) {
	
	//open(SOURCE+Dataset+"_T="+t+".tiff");
	//run("Bio-Formats Importer", "open="+SOURCE+Dataset+"_T="+t+".tiff");
	open(SOURCE+Dataset+"T="+t+".tiff");
	selectImage(Dataset+"T="+t+".tiff");
	run("RGB Color");
	saveAs("Tiff", OUTPUT_DIR+"MAX_"+Dataset+"T="+t+".tiff");
	run("Close All");
//
}
