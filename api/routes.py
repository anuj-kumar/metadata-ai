from flask import Blueprint, request, jsonify
from core.query_resolution import resolve_query
from core.context_gathering import gather_context
from core.llm_client import call_llm
from core.agent_actions import take_action


api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/query', methods=['POST'])
def handle_query():
    data = request.json
    user_query = data.get('query')
    intent = resolve_query(user_query)
    context = gather_context(intent)
    llm_response = call_llm(user_query, context)
    return jsonify({'response': llm_response})

@api_blueprint.route('/action', methods=['POST'])
def handle_action():
    data = request.json
    action = data.get('action')
    result = take_action(action)
    return jsonify({'result': result})

@api_blueprint.route('/track', methods=['POST'])
def handle_track():
    data = request.json
    # track_interaction(data)
    return jsonify({'status': 'tracked'})

