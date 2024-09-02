class EventRouter:
    event_db = 'event-db'

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'mass':  # Assuming 'mass' is the app label
            return self.event_db
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'mass':
            return self.event_db
        return None

    def allow_migration(self, db, app_label, model_name=None, **hints):
        if app_label == 'mass':
            return db == self.event_db
        return None
