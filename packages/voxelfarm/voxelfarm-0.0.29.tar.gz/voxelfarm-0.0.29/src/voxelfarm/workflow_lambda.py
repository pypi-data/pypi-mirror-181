import voxelfarm
import os
import os.path
import pandas as pd

class workflow_lambda_framework:

    def __init__(self):  
        pass

    def log(self, message):
        pass

    def get_entity(self, id = None):
        return None

    def download_entity_file(self, filename, id = None):
        return ""

class workflow_lambda_host:

    def __init__(self, framework = None):  
        if framework:
            self.lambda_framework = framework
        else:
            if voxelfarm.voxelfarm_framework:
                self.lambda_framework = voxelfarm.voxelfarm_framework
            else:
                self.lambda_framework = workflow_lambda_framework()

    def get_product_property(self, product_id, property):
        entity = self.lambda_framework.get_entity()
        if entity and entity.ContainsKey('project'):
            project_id = entity['project']
            project = self.lambda_framework.get_entity(project_id)
            if project and project.ContainsKey('workflow_folder_' + product_id):
                product_folder_id = project['workflow_folder_' + product_id]
                product_entity = self.lambda_framework.get_entity(product_folder_id)
                if product_entity and product_entity.ContainsKey('version_active'):
                    active_version_id = product_entity['version_active']
                    active_version = self.lambda_framework.get_entity(active_version_id)
                    extended_prop = 'version_' + property
                    if active_version and active_version.ContainsKey(extended_prop):
                        return active_version[extended_prop]
                    else:
                        self.lambda_framework.log('Problem with entity active_version ' + active_version_id)
                else:
                    self.lambda_framework.log('Problem with entity product_entity ' + product_folder_id)
            else:
                self.lambda_framework.log('Problem with entity project ' + project_id)
        else:
            self.lambda_framework.log('Problem with entity.')

        return None

    def get_parameter_dataframe(self, product_id):
        attribute_product = self.get_product_property(product_id, 'report_entity')
        if attribute_product:
            attribute_file = self.lambda_framework.download_entity_file('report.csv', attribute_product)
            if os.path.isfile(attribute_file):
                return pd.read_csv(attribute_file)
            else:
                self.lambda_framework.log('Parameter file not found.')
        else:
            self.lambda_framework.log('Attribute product not found.')

        return pd.DataFrame()
