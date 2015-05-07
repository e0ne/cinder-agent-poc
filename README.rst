============
CINDER AGENT
============

TBD

Run agent:
cinder-agent-poc/cinderagent$ python app.py

Call API:
curl -H "Content-Type: application/json" http://localhost:500/connector -X GET -d '{"protocol":"iscsi"}'
