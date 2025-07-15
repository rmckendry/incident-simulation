import simpy
import random
import statistics

incidents = []

class OperationsCenter:
    def __init__(self, env, num_teams):
        self.env = env
        self.team = simpy.Resource(env, num_teams)

    def resolve_outage(self, incident):
        yield self.env.timeout(random.randint(5, 15))

def simulate_incident(env, incident_id, ops_center):
    arrival = env.now
    with ops_center.team.request() as req:
        yield req
        yield env.process(ops_center.resolve_outage(incident_id))
    duration = env.now - arrival
    incidents.append(duration)
    print(f"Incident {incident_id} resolved in {duration} min")

def run_simulation(env, num_teams):
    ops_center = OperationsCenter(env, num_teams)
    incident_id = 0
    while True:
        yield env.timeout(random.expovariate(1/10))
        incident_id += 1
        env.process(simulate_incident(env, incident_id, ops_center))

env = simpy.Environment()
env.process(run_simulation(env, num_teams=2))
env.run(until=60)
print(f"Avg outage resolution: {statistics.mean(incidents)} min")