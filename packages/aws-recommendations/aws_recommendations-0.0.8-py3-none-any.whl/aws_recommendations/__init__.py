from aws_recommendations import ec2 as fn
from boto3 import session

__author__ = "Dheeraj Banodha"
__version__ = '0.0.8'

class aws_client:
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        self.session = session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    from .recommendation import get_recommendations

    from .ec2 import delete_or_downsize_instance_recommendation, purge_unattached_vol_recommendation, purge_8_weeks_older_snapshots, reserved_instance_lease_expiration, unassociated_elastic_ip_addresses

    from .rds import downsize_underutilized_rds_recommendation, rds_idle_db_instances

    from .cost_estimations import estimated_savings



