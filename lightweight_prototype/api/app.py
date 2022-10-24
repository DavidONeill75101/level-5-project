from xmlrpc.client import APPLICATION_ERROR
from flask import Flask, request
from flask_cors import CORS, cross_origin
from data import Data
import json

application = Flask(__name__)
cors = CORS(application)
application.config["CORS_HEADERS"] = "Content-Type"

current_data = Data()


@application.route('/', methods=["GET"])
@cross_origin()
def root():
    instructions = {'get_collated': 'parameters - gene, cancer, drug, evidence_type, variant',
                    'get_sentences': 'parameter - matching_id',
                    'get_unfiltered': 'no parameters currently'}

    return "Enpoints: " + json.dumps(instructions)


@application.route('/get_collated', methods=["GET"])
@cross_origin()
def get_collated():

    collated = current_data.collated_pd

    if request.args.get('matching_id'):
        collated = collated[collated['matching_id']
                            == request.args.get('matching_id')]

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

    if request.args.get('start') and request.args.get('end'):
        collated = collated.iloc[int(request.args.get(
            'start')):int(request.args.get('end'))]

    collated = collated.fillna(" ")

    return json.dumps(collated.to_dict("records"))


@application.route('/get_sentences', methods=["GET"])
@cross_origin()
def get_sentences():

    parameters = request.args
    if len(parameters) == 0:
        return 'Need to Specify Matching ID'
    else:
        matching_id = request.args.get("matching_id")
        sentences = current_data.sentences_pd[current_data.sentences_pd['matching_id'] == matching_id]

        if request.args.get('start') and request.args.get('end'):
            sentences = sentences.iloc[int(request.args.get(
                'start')):int(request.args.get('end'))]

        sentences = sentences.fillna(" ")
        return json.dumps(sentences.to_dict("records"))


@application.route('/get_unfiltered', methods=["GET"])
@cross_origin()
def get_unfiltered():
    return json.dumps(current_data.unfiltered_pd.to_dict("records"))


@application.route('/upvote_sentence', methods=['GET'])
@cross_origin()
def upvote_sentence():

    if request.args.get("id"):
        ids = [int(request.args.get("id"))]
        current_data.sentences_pd.loc[current_data.sentences_pd.id.isin(
            ids), 'upvotes'] += 1

        return "Upvoted"

    else:
        return "Need to specify sentence id"


@application.route('/downvote_sentence', methods=['GET'])
@cross_origin()
def downvote_sentence():

    if request.args.get("id"):
        ids = [int(request.args.get("id"))]
        current_data.sentences_pd.loc[current_data.sentences_pd.id.isin(
            ids), 'downvotes'] += 1

        return "Downvoted"

    else:
        return "Need to specify sentence id"


@application.route('/get_genes', methods=['GET'])
@cross_origin()
def get_genes():
    lowercase_genes = sorted(
        current_data.collated_pd['gene_normalized'].str.lower().unique())
    uppercase_genes = [
        l.upper() if 'mir' not in l else l for l in lowercase_genes]
    return uppercase_genes


@application.route('/get_cancers', methods=['GET'])
@cross_origin()
def get_cancers():
    return sorted(current_data.collated_pd['cancer_normalized'].str.lower().unique())


@application.route('/get_drugs', methods=['GET'])
@cross_origin()
def get_drugs():
    return sorted(current_data.collated_pd['drug_normalized'].dropna().unique(), key=lambda x: x.lower())


@application.route('/get_evidence_types', methods=['GET'])
@cross_origin()
def get_evidence_types():
    return sorted(current_data.collated_pd['evidencetype'].unique())


@application.route('/get_variants', methods=['GET'])
@cross_origin()
def get_variants():
    return sorted(current_data.collated_pd['variant_group'].dropna().unique())


if __name__ == "__main__":
    application.run(debug=True)
