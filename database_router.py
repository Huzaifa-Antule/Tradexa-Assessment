class MultiDBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ['users', 'products', 'orders']:
            return model._meta.app_label
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in ['users', 'products', 'orders']:
            return model._meta.app_label
        return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in ['users', 'products', 'orders']:
            return db == app_label
        return db == 'default'
