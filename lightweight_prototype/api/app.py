from flask import Flask, request
from data import Data
import json

application = Flask(__name__)

current_data = Data()


@application.route('/', methods=["GET"])
def root():
    instructions = {'get_collated': 'parameters - gene, cancer, drug, evidence_type, variant',
                    'get_sentences': 'parameter - matching_id',
                    'get_unfiltered': 'no parameters currently'}

    return "Enpoints: " + json.dumps(instructions)


@application.route('/get_collated', methods=["GET"])
def get_collated():

    collated = current_data.collated_pd

    if request.args.get('gene'):
        collated = collated[collated['gene_normalized'] == request.args.get(
            'gene').upper()]

    if request.args.get('cancer'):
        collated = collated[collated['cancer_normalized'] == request.args.get(
            'cancer').lower()]

    if request.args.get('drug'):
        collated = collated[collated['drug_normalized'] == request.args.get(
            'drug').lower()]

    if request.args.get('evidence_type'):
        collated = collated[collated['evidencetype']
                            == request.args.get('evidence_type').capitalize()]

    if request.args.get('variant'):
        collated = collated[collated['variant_group']
                            == request.args.get('variant').lower()]

    return json.dumps(collated.to_dict("records"))


@application.route('/get_sentences', methods=["GET"])
def get_sentences():

    parameters = request.args
    if len(parameters) == 0:
        return 'Need to Specify Matching ID'
    else:
        matching_id = request.args.get("matching_id")
        sentences = current_data.sentences_pd[current_data.sentences_pd['matching_id'] == matching_id]
        return json.dumps(sentences.to_dict("records"))


@application.route('/get_unfiltered', methods=["GET"])
def get_unfiltered():
    return json.dumps(current_data.unfiltered_pd.to_dict("records"))
