from flask import Flask
from flask import jsonify
from ..common.schedule_center import ScheduleCenter

app = Flask(__name__)

schedule_center = ScheduleCenter()


@app.route('/')
def index():
    response = {
        'slave_queue_bindings': {k: v.qsize() for k, v in schedule_center._slave_queue_bindings.items()},
        'key_slave_mappings': len(schedule_center._key_slave_mappings),
        'slave_keys_mappings': {k: len(v) for k, v in schedule_center._slave_keys_mappings.items()},
        'slave_kpi_mappings': schedule_center._slave_kpi_mappings,
        'secret_key_store': schedule_center._secret_key_store,
        'checksum_store': schedule_center._checksum_store,
        'slave_heartbeats': schedule_center._slave_heartbeats,
        'reallocate_keys': len(schedule_center._reallocate_keys),
    }
    return jsonify(response)


@app.route('/schedule/<schedule_key>')
def get(schedule_key):
    response = {
        'hello': 'world'
    }
    return jsonify(response)
