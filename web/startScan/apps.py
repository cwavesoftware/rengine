from django.apps import AppConfig
import logging
from reNgine import definitions

class StartscanConfig(AppConfig):
    name = 'startScan'

    def ready(self):
        '''
        Any Scans that were incomplete in the last scan, we will mark them Aborted after
        server restarted
        This does not include pending_scans, pending_scans are taken care by celery
        '''
        logging.info('Aborting all the ongoing scans')
        ScanHistory = self.get_model('ScanHistory')
        ScanHistory.objects.filter(scan_status=definitions.SCAN_STATUS_IN_PROGRESS).update(scan_status=definitions.SCAN_STATUS_ABORTED)
