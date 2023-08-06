
from diagrams import Diagram, Cluster

from diagrams.aws.management import Organizations, OrganizationsAccount, OrganizationsOrganizationalUnit
from diagrams.aws.general import Users, User

with Diagram("SSO-State", show=False, direction="TB"):
    gg = Users("Group")
    uu= User("User")

    with Cluster('Groups'):

        gg_0= Users("AWSLogArchiveVie\nwers")

        gg_1= Users("AWSServiceCatalo\ngAdmins")

        gg_2= Users("AWSSecurityAudit\nors")

        with Cluster("AWSAccountFactory"):

                gg_3= [User("velez94@protonma\nil.com"),]

        gg_4= Users("AWSAuditAccountA\ndmins")

        with Cluster("SecOps_Adms"):

                gg_5= [User("w.alejovl+secops\n-labs@gmail.com"),]

        gg_6= Users("AWSLogArchiveAdm\nins")

        with Cluster("DevSecOps_Admins"):

                gg_7= [User("DevSecOpsAdm"),]

        gg_8= Users("AWSSecurityAudit\nPowerUsers")

        with Cluster("AWSControlTowerAdmins"):

                gg_9= [User("velez94@protonma\nil.com"),]
