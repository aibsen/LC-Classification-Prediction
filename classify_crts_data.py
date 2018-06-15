import luigi
from pipeline_utils import utils_dir, data_dir
from transient_url_extraction import transient_url_extraction
from transient_lc_extraction import transient_lc_extraction
from transient_metadata_extraction import transient_metadata_extraction
from tag_merge_metadata import tag_merge_metadata
from fats_feature_extraction import fats_feature_extraction
from fats_features_preprocessing import fats_features_preprocessing
from first_stage_classification import first_stage_classification
from first_stage_classificationDMDT import first_stage_classificationDMDT
from second_stage_classification import second_stage_classification
from second_stage_classificationDMDT import second_stage_classificationDMDT
from dmdt_mappings import dmdt_mappings
import csv

class TransientURLExtraction(luigi.Task):

    def requires(self):
        return []

    def output(self):
        return luigi.LocalTarget(utils_dir+"transient_lc_urls.csv")
    
    def run(self):
        url_list = transient_url_extraction()
        with self.output().open('w') as f:
            wr = csv.writer(f,lineterminator='\n')
            for url in url_list:
                wr.writerow([url])

class TransientLCExtraction(luigi.Task):
 
    def requires(self):
        return [TransientURLExtraction()]
 
    def output(self):
        return luigi.LocalTarget(data_dir+"/raw/transients/")
 
    def run(self):
        with self.input()[0].open() as fin:
            transient_lc_extraction(fin)


class TransientMetaDataExtraction(luigi.Task):

    def requires(self):
        return [TransientURLExtraction(), TransientLCExtraction()]

    def output(self):
        return luigi.LocalTarget(data_dir+"metadata/transient_lc_metadata.csv")

    def run(self):
        metadata_list = transient_metadata_extraction()
        with self.output().open('w') as f:
            wr = csv.writer(f,lineterminator='\n')
            fieldnames = ['CRTS ID', 'RA (J2000)', 'Dec (J2000)', 'UT Date', 'Mag', 'CSS images', 'SDSS', 'Others', 'Followed', 'Last', 'LC', 'FC', 'Classification','SubClassification']
            wr.writerow(fieldnames)
            wr.writerows(metadata_list)

class VariableMetaDataExtraction(luigi.ExternalTask):
    def output(self):
        return luigi.LocalTarget(data_dir+'metadata/variables_lc_metadata.dat')
 

class TagMergeMetadata(luigi.Task):
    def requires(self):
        return [TransientMetaDataExtraction(),VariableMetaDataExtraction()]
    def output(self):
        return luigi.LocalTarget(data_dir+"metadata/lc_metadata.pkl")
    def run(self):
        tag_merge_metadata(data_dir+"metadata/lc_metadata.pkl")

class FatsFeatureExtraction(luigi.Task):
    def requires(self):
        return [TagMergeMetadata()]
    def output(self):
        return luigi.LocalTarget(data_dir+"features/fats_features/tagged_features.pkl")
    def run(self):
        filename =data_dir+"features/fats_features/tagged_features.pkl"
        errorFilename=data_dir+"features/fats_features/errors.pkl"
        fats_feature_extraction(filename,errorFilename)

class DMDTMappings(luigi.Task):
    def requires(self):
        return [TagMergeMetadata()]
    def output(self):
        return luigi.LocalTarget(data_dir+"features/dmdt_mappings/tagged_features1.pkl")
    def run(self):
        outputFile = data_dir+"features/dmdt_mappings/tagged_features"
        inputFile = data_dir+"metadata/lc_metadata.pkl"
        dmdt_mappings(inputFile,outputFile)

class FatsFeaturesPreprocessing(luigi.Task):
    def requires(self):
        return [FatsFeatureExtraction()]
    def output(self):
        return luigi.LocalTarget(data_dir+"features/fats_features/clean_tagged_features.pkl")
    def run(self):
        outputFile =data_dir+"features/fats_features/clean_tagged_features.pkl"
        inputFile = data_dir+"features/fats_features/tagged_features.pkl"
        fats_features_preprocessing(outputFile, inputFile)

class FirstStageClassification(luigi.Task):
    def requires(self):
        return [FatsFeaturesPreprocessing()]
    def output(self):
        return luigi.LocalTarget(data_dir+"results/fats_features/first_stage_scores.txt")
    def run(self):
        outputFile = data_dir+"results/fats_features/first_stage_scores.txt"
        inputFile = data_dir+"features/fats_features/clean_tagged_features.pkl"
        first_stage_classification(inputFile, outputFile)

class SecondStageClassification(luigi.Task):
    def requires(self):
        return [FatsFeaturesPreprocessing()]
    def output(self):
        return luigi.LocalTarget(data_dir+"results/fats_features/second_stage_scores.txt")
    def run(self):
        outputFile = data_dir+"results/fats_features/second_stage_scores.txt"
        inputFile = data_dir+"features/fats_features/clean_tagged_features.pkl"
        second_stage_classification(inputFile, outputFile)

class FirstStageClassificationDMDT(luigi.Task):
    def requires(self):
        return [DMDTMappings()]
    def output(self):
        return luigi.LocalTarget(data_dir+"results/dmdt_mappings/first_stage_scores.txt")
    def run(self):
        outputFile = data_dir+"results/dmdt_mappings/first_stage_scores.txt"
        inputFile = data_dir+"features/dmdt_mappings/tagged_features"
        first_stage_classificationDMDT(inputFile, outputFile)

class SecondStageClassificationDMDT(luigi.Task):
    def requires(self):
        return [DMDTMappings()]
    def output(self):
        return luigi.LocalTarget(data_dir+"results/tagged_features/second_stage_scores.txt")
    def run(self):
        outputFile = data_dir+"results/dmdt_mappings/second_stage_scores.txt"
        inputFile = data_dir+"features/dmdt_mappings/tagged_features"
        second_stage_classificationDMDT(inputFile, outputFile)

if __name__ == '__main__':
    luigi.run()