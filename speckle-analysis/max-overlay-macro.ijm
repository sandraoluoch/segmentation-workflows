SOURCE_1 = "//allen/aics/assay-dev/users/Sandi/nuc-morph-analysis/speckle-analysis/raw/max-raw/"
SOURCE_2 = "//allen/aics/assay-dev/users/Sandi/nuc-morph-analysis/speckle-analysis/seg/max-seg/"
OUTPUT_DIR = "//allen/aics/assay-dev/users/Sandi/nuc-morph-analysis/speckle-analysis/seg/max-overlay/"

DATASET_1 = "MAX_20230425_L02-01_processed_C=0"
DATASET_2 = "MAX_SEGfinalspeckle"

Tini = 0;
Tend = 530;

// ============

t = Tini;

c4=DATASET_1+"_T="+t+".tiff"
c6=DATASET_2+"_T="+t+".tiff"


for (t=Tini; t<=Tend; t++) {
	open(SOURCE_1+DATASET_1+"_T="+t+".tiff");
	selectImage(DATASET_1+"_T="+t+".tiff");
	
	open(SOURCE_2+DATASET_2+"_T="+t+".tiff");
	selectImage(DATASET_2+"_T="+t+".tiff");
	
	run("Merge Channels...", "c4=MAX_20230425_L02-01_processed_C=0_T="+t+".tiff c6=MAX_SEGfinalspeckle_T="+t+".tiff create");
//	run("Merge Channels...", "c4=MAX_20230425_L02-01_processed_C=0_T=4.tiff c6=MAX_SEGfinalspeckle_T=4.tiff create");
	saveAs("Tiff", OUTPUT_DIR+"overlay_seg"+"_T="+t+".tiff" );
	run("Close All");
}
