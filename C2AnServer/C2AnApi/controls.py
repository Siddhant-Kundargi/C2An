from flask import blueprints
from auth import token_required
contorls = blueprints.Blueprint('controls', __name__)

@token_required
@contorls.route('catalog/', methods=['POST'])
def return_catalog():
    pass