
class ServiceDB:
    def __init__(self, db):
        self.db = db

    def add(self, sid, unit_id, service_name):
        services = self.db.get('services')

        obj = {'sid': sid, 'unit_id': unit_id, 'service': service_name}
        services.append(obj)
        self.db.set('services', services)

    def remove(self, sid, unit_id):
        services = self.db.get('services')
        services = [item
                    for item in services
                    if item['sid'] != sid and item['unit_id'] != unit_id]
        self.db.set('services', services)

    def condition(self, item, sid=None, unit_id=None, service_name=None):

        if sid and item['sid'] != sid:
            return False

        if unit_id and item['unit_id'] != unit_id:
            return False

        if service_name and item['service'] != service_name:
            return False

        return True

    def find(self, sid=None, unit_id=None, service_name=None):
        if sid is None and unit_id is None and service_name is None:
            return None

        return filter(lambda service:
                      self.condition(service, sid, unit_id, service_name),
                      self.db.get('services'))
