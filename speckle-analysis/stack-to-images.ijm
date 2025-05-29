//PARAMETERS
SOURCE = "//allen/aics/assay-dev/users/Sandi/nuc-morph-analysis/speckle-analysis/examples/example2_MAX_SEGfinalspeckle_all.tiff"
OUTPUT_DIR = "//allen/aics/assay-dev/users/Sandi/nuc-morph-analysis/speckle-analysis/examples/example-1-max-projections/";
Tini = 0;
Tend = 531;

// ============

t = Tini;

open("//allen/aics/assay-dev/users/Sandi/nuc-morph-analysis/speckle-analysis/examples/example1_MAX_SEGfinalspeckle_all.tiff");
selectImage("example1_MAX_SEGfinalspeckle_all.tiff");
run("Stack to Images");	

for (t=Tini; t<=Tend; t++) {
	
	//open(SOURCE+Dataset+"_T="+t+".tiff");
	//run("Bio-Formats Importer", "open="+SOURCE);
	
	selectImage("MAX_SEGfinalspeckle_T="+t+".tiff");
	saveAs("Tiff", OUTPUT_DIR+"MAX_SEGfinalspeckle_T="+t+".tiff");
	close();
	//run("Close All");

}
