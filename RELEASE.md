# Plugin AWS Cloud Services Inventory Collector Release Notes

## Ver 1.15.3
* [When sorting IAM User's Access Key Age column, sort alphabetically, not numeric](https://github.com/cloudforet-io/plugin-aws-cloud-service-inven-collector/issues/18)

## Ver 1.15.2
* [Cloudtrail icon does not display](https://github.com/cloudforet-io/plugin-aws-cloud-service-inven-collector/issues/23)

## Ver 1.15.1
* [Add custom_asset_url option](https://github.com/cloudforet-io/plugin-aws-cloud-service-inven-collector/pull/21)

## Ver 1.15.0
* [Refactoring Tags](https://github.com/cloudforet-io/plugin-aws-cloud-service-inven-collector/issues/7)
* [Separating Access Key Resource from IAM.User](https://github.com/cloudforet-io/plugin-aws-cloud-service-inven-collector/issues/12)
* [Fix bug: CloudTrailARNInvalidException](https://github.com/cloudforet-io/plugin-aws-cloud-service-inven-collector/issues/11)

## Ver 1.14.2
* Fix bug: Typo (RDS Cluster Tags)

## Ver 1.14.1
* Fix bug: Typo (Lambda)

## Ver 1.14
* Support CloudTrail for monitoring log [#453](https://github.com/cloudforet-io/plugin-aws-cloud-service-inven-collector/issues/453) 
* Restructure CloudWatch metric info 

## Ver 1.13.13
* Update exclude Region list for Collecting a Lightsail and DocumentDB [#446](https://github.com/cloudforet-io/plugin-aws-cloud-service-inven-collector/issues/446) [#447](https://github.com/cloudforet-io/plugin-aws-cloud-service-inven-collector/issues/447)

## Ver 1.13.12
* Add all storage type object size for S3  [#443](https://github.com/cloudforet-io/plugin-aws-cloud-service-inven-collector/issues/443)

## Ver 1.13.11
* Exclude Region for Collecting a Lightsail (ap-east-1) [#440](https://github.com/cloudforet-io/plugin-aws-cloud-service-inven-collector/issues/440)
* Add sleep for avoid API Rate Limitation for collecting a API Gatway resource [#441](https://github.com/cloudforet-io/plugin-aws-cloud-service-inven-collector/issues/441)

## Ver 1.13.10
* Update RDS Filter (add Postgresql Aurora)

## Ver 1.13.9
* (Fix Bug) ECS collecting error when many services or tasks ([#431](https://github.com/cloudforet-io/plugin-aws-cloud-service-inven-collector/issues/431))

## Ver 1.13.8
* Add Lightsail Service ([#414](https://github.com/cloudforet-io/plugin-aws-cloud-service-inven-collector/issues/414))
* update Cloud Service Type (is_primary is True) in CertificateManager.Certificate ([#427](https://github.com/cloudforet-io/plugin-aws-cloud-service-inven-collector/issues/427))

## Ver 1.13.7
* Add feature to convert service_code to what you want using options ([#417](https://github.com/cloudforet-io/plugin-aws-cloud-service-inven-collector/issues/417))

## Ver 1.13.1-6
* Fix some bugs..!

## Ver 1.13
* Add feature to specify the Cloud Service Type and collect it.

## Ver 1.12
* Separated to setting the parameter and collecting resources.
* Fix some bug

## Ver 1.11.10
* Remove region_name filter in secret_data
* Fix some bug

## Ver 1.11.9
* (Fix bug) Modify get bucket location for S3 (set the default region when bucket was located is us-east-1)

## Ver 1.11.7
* Add attached instances information in Security Groups
* Add Target Groups, Instances information in Load Balancer

## Ver 1.11.6
* Add exceptions for S3 collecting logic

## Ver 1.11
* Add is_optional in Cloud Service Type metadata for Dynamic Tables
* (Fix Bug) Modify region_code for EKS Cluster

## Ver 1.10
* Add name field each cloud services for standardization


## Ver 1.9.3
* (Fix Bug) Modify node_count, shard_count in ElastiCache
* (Fix Bug) Modify unexpected region code in EKS Node Group
* (Fix Bug) Modify RDS Filter action
* Add search matched launch template to Auto Scaling Group through mixed instance policy info

## Ver 1.9.2
* Add Load Balancers in Auto Scaling Group
    * Group: Auto Scaling Group
    * Name : LoadBalaners
* Add related Auto Scaling Group ARNs in EKS

## Ver 1.9.1
* Add Node Group in EKS
    * Group: EKS
    * Name : NodeGroup

## Ver 1.9
* Add to supported Cloud Service
    * ElastiCache
        * Memcached
        * Redis
* Add related Launch Template detail data in Auto Scaling Group information
* Add releated ELB ARNs in Auto Scaling Group
* Add lifecycle(Spot or Scheduled) information in Auto Scaling Group's instances
* Fix bug, etc.

## Ver 1.8
* Add to supported Cloud Service
    * Amazon MSK (Managed Streaming for Apache)
        * Cluster
        * Cluster Configuration

    * Kinesis Data Stream
        * Data Stream

    * Kinesis Data Firehose
        * Delivery Stream

    * Amazon Certificate Manager (ACM)
        * Certificate
    
