# AWS Cost Optimization & Billing Runbook
**Account:** cloud-sec101 (`[AWS-ACCOUNT-ID-REDACTED]`)  
**Owner:** Derek O.  
**Email:** [EMAIL-REDACTED]  
**Last Updated:** July 2026  

---

## Table of Contents

1. [Incident Summary](#1-incident-summary)
2. [Root Cause Analysis](#2-root-cause-analysis)
3. [Billing Breakdown](#3-billing-breakdown)
4. [Cleanup Actions Taken](#4-cleanup-actions-taken)
5. [Preventive Controls](#5-preventive-controls)
6. [Daily Session Checklist](#6-daily-session-checklist)
7. [Cost Anomaly Detection Setup](#7-cost-anomaly-detection-setup)
8. [Billing Alarm Reference](#8-billing-alarm-reference)
9. [AWS Support Dispute Template](#9-aws-support-dispute-template)
10. [Approved Running Resources](#10-approved-running-resources)
11. [Monthly Cost Target](#11-monthly-cost-target)

---

## 1. Incident Summary

| Field | Detail |
|-------|--------|
| **Date Detected** | July 2026 |
| **Account Blocked** | Yes — due to unpaid charges |
| **Root Cause** | Team microservices project left ECR + supporting resources running continuously for 3+ days |
| **Charges Disputed** | ~$23.04 (June 2026) |
| **Charges Stopped** | July charges reduced from ~$5.04/month to ~$0.64/month after cleanup |
| **Resolution** | All unused resources deleted · AWS Support dispute filed · Cost Anomaly Detection enabled |

---

## 2. Root Cause Analysis

### Primary Cause
A shared team project deploying a microservices application on AWS left the following
resources running continuously without a shutdown plan:

- Amazon ECR repository with active image pulls
- EC2 instances supporting the microservices workload
- Elastic IPs allocated but not released after project end
- NAT Gateway running in VPC (high cost — $0.045/hr + data transfer)
- Secrets Manager secrets left active after project teardown
- Route 53 hosted zones not deleted after DNS was no longer needed

### Contributing Factors
- No billing alerts configured on the account
- No SCP blocking expensive services in the Workloads OU
- No team agreement on resource cleanup after project completion
- AWS Free Tier limits not monitored

### Lessons Learned
- Always set a billing alarm **before** starting any project
- NAT Gateways and Elastic IPs incur charges even when idle
- Resources created in a team context must have a designated owner responsible for teardown
- Stopped EC2 instances still incur EBS storage charges

---

## 3. Billing Breakdown

### June 2026 — Disputed (~$23.04)

| Service | Cost | Notes |
|---------|------|-------|
| Amazon EC2 - Compute | $8.36 | Team project instances left running |
| Amazon VPC | $7.21 | NAT Gateway + idle Elastic IPs |
| EC2 - Other (EBS, NAT GW, Data Transfer) | $4.94 | Volumes + NAT data transfer |
| Amazon Route 53 | $1.51 | 3 hosted zones unused |
| AWS Secrets Manager | $0.80 | Team project secrets not deleted |
| Amazon ECR | $0.14 | Container image storage |
| Amazon RDS | $0.08 | Backup storage overage |
| **Total** | **$23.04** | **Dispute filed with AWS Support** |

### July 2026 — Before Cleanup (~$5.04 projected)

| Service | Cost | Status |
|---------|------|--------|
| Amazon Route 53 | $1.50 | ✅ Deleted — $0 going forward |
| Amazon EC2 - Compute | $1.44 | ✅ No new instances running |
| Amazon VPC | $1.26 | ✅ Elastic IPs released — $0 going forward |
| EC2 - Other (EBS) | $0.79 | ✅ Unused volumes deleted |
| AWS Secrets Manager | $0.14 | ✅ Deleted — $0 going forward |
| Amazon ECR | $0.02 | ✅ Cleaned up |
| Amazon RDS | $0.01 | ✅ Backup storage resolved |
| **Total** | **$5.04** | **Reduced to ~$0.64/month after cleanup** |

### Post-Cleanup — Approved Ongoing Costs (~$0.64/month)

| Resource | Cost | Reason Kept |
|----------|------|-------------|
| CTF Lab EBS volume (8GB gp2) | ~$0.64/month | Active Linux training course |
| **Total** | **~$0.64/month** | |

---

## 4. Cleanup Actions Taken

### Route 53 — Deleted All 3 Hosted Zones

```bash
# List hosted zones
aws route53 list-hosted-zones \
  --query 'HostedZones[*].{ID:Id,Name:Name}' \
  --output table \
  --profile cloud-eng-iac

# Delete all non-NS/SOA records first (required before zone deletion)
python3 << 'PYEOF'
import boto3

session = boto3.Session(profile_name='cloud-eng-iac')
client = session.client('route53')

ZONE_ID = 'YOUR_ZONE_ID'

response = client.list_resource_record_sets(HostedZoneId=ZONE_ID)
records = response['ResourceRecordSets']
deletable = [r for r in records if r['Type'] not in ['NS', 'SOA']]

if deletable:
    changes = [{"Action": "DELETE", "ResourceRecordSet": r} for r in deletable]
    client.change_resource_record_sets(
        HostedZoneId=ZONE_ID,
        ChangeBatch={"Changes": changes}
    )
    print(f"Deleted {len(deletable)} records")
PYEOF

# Delete the zone
aws route53 delete-hosted-zone \
  --id ZONE_ID \
  --profile cloud-eng-iac
```

**Result:** $1.50/month saved. Output blank — all zones confirmed deleted.

---

### Secrets Manager — Deleted 2 Team Project Secrets

```bash
# Delete two-tier-app/db-credentials
aws secretsmanager delete-secret \
  --secret-id arn:aws:secretsmanager:us-east-1:[AWS-ACCOUNT-ID-REDACTED]:secret:[SECRET-NAME-REDACTED] \
  --force-delete-without-recovery \
  --profile cloud-eng-iac \
  --region us-east-1

# Delete spc-stg-ue1-app-secret-01
aws secretsmanager delete-secret \
  --secret-id arn:aws:secretsmanager:us-east-1:[AWS-ACCOUNT-ID-REDACTED]:secret:[SECRET-NAME-REDACTED] \
  --force-delete-without-recovery \
  --profile cloud-eng-iac \
  --region us-east-1
```

**Result:** $0.40/month saved. Both secrets confirmed deleted.

---

### EC2 — Verified No Unused Instances

```bash
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running,stopped" \
  --query 'Reservations[*].Instances[*].{ID:InstanceId,Name:Tags[?Key==`Name`].Value|[0],State:State.Name,Type:InstanceType}' \
  --output table \
  --profile cloud-eng-iac \
  --region us-east-1
```

**Result:** Only CTF Lab Instance (`[INSTANCE-ID-REDACTED]`) found — kept intentionally (stopped).

---

### Elastic IPs — None Found

```bash
aws ec2 describe-addresses \
  --query 'Addresses[*].{IP:PublicIp,AllocationId:AllocationId,Instance:InstanceId}' \
  --output table \
  --profile cloud-eng-iac \
  --region us-east-1
```

**Result:** No Elastic IPs found. $0 charge confirmed.

---

### EBS Volumes — Only CTF Lab Volume Retained

```bash
aws ec2 describe-volumes \
  --filters "Name=status,Values=available" \
  --query 'Volumes[*].{ID:VolumeId,Size:Size,State:State}' \
  --output table \
  --profile cloud-eng-iac \
  --region us-east-1
```

**Result:** No available (unattached) volumes found. CTF Lab volume (`[VOLUME-ID-REDACTED]`, 8GB gp2, in-use) retained intentionally.

---

## 5. Preventive Controls

### SCP — Deny Expensive Services in Workloads OU

Save as `/scps/deny-expensive-services.json` and attach to the Workloads OU:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyExpensiveEC2",
      "Effect": "Deny",
      "Action": "ec2:RunInstances",
      "Resource": "arn:aws:ec2:*:*:instance/*",
      "Condition": {
        "StringNotLike": {
          "ec2:InstanceType": ["t2.*", "t3.*", "t3a.*"]
        }
      }
    },
    {
      "Sid": "DenyNATGateway",
      "Effect": "Deny",
      "Action": "ec2:CreateNatGateway",
      "Resource": "*"
    },
    {
      "Sid": "DenyNonApprovedRegions",
      "Effect": "Deny",
      "NotAction": [
        "iam:*", "organizations:*", "account:*",
        "sts:*", "support:*", "route53:*"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": ["us-east-1", "us-west-2"]
        }
      }
    }
  ]
}
```

```bash
# Create and attach the SCP
aws organizations create-policy \
  --name "DenyExpensiveServices" \
  --description "Blocks expensive EC2 types, NAT Gateways, and non-approved regions" \
  --type SERVICE_CONTROL_POLICY \
  --content file://scps/deny-expensive-services.json \
  --profile cloud-eng-iac

# Attach to Workloads OU (replace OU_ID)
aws organizations attach-policy \
  --policy-id POLICY_ID \
  --target-id OU_ID \
  --profile cloud-eng-iac
```

---
.01
### Billing Alerts — CloudWatch Alarms

```bash
# Enable billing alerts (run once)
aws ce create-anomaly-monitor \
  --anomaly-monitor '{
    "MonitorName": "AccountSpendMonitor",
    "MonitorType": "DIMENSIONAL",
    "MonitorDimension": "SERVICE"
  }' \
  --profile cloud-eng-iac \
  --region us-east-1

# Create daily email alert at $10 threshold
aws ce create-anomaly-subscription \
  --anomaly-subscription '{
    "SubscriptionName": "SpendAlert10",
    "MonitorArnList": ["arn:aws:ce::[AWS-ACCOUNT-ID-REDACTED]:anomalymonitor/[MONITOR-ID-REDACTED]"],
    "Subscribers": [{
      "Address": "[EMAIL-REDACTED]",
      "Type": "EMAIL"
    }],
    "Threshold": 10,
    "Frequency": "DAILY"
  }' \
  --profile cloud-eng-iac \
  --region us-east-1
```
> **Note:** `IMMEDIATE` frequency only supports SNS topic subscribers.
> Use `DAILY` or `WEEKLY` for direct email alerts.

---

## 6. Daily Session Checklist

Run this **every time before closing your laptop**:

```bash
# Check for any running instances
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[*].Instances[*].{ID:InstanceId,Name:Tags[?Key==`Name`].Value|[0],Type:InstanceType}' \
  --output table \
  --profile cloud-eng-iac \
  --region us-east-1
```

| Output | Meaning | Action |
|--------|---------|--------|
| Blank table | Nothing running | ✅ Safe to close |
| CTF Lab only | Expected | ✅ Safe — stop it if done for the day |
| Any other instance | Unexpected | ⚠️ Investigate and terminate |

### Stop CTF Lab When Not in Use

```bash
# Stop (not terminate — preserves your data)
aws ec2 stop-instances \
  --instance-ids [INSTANCE-ID-REDACTED] \
  --profile cloud-eng-iac \
  --region us-east-1

# Start again when needed
aws ec2 start-instances \
  --instance-ids [INSTANCE-ID-REDACTED] \
  --profile cloud-eng-iac \
  --region us-east-1
```

---

## 7. Cost Anomaly Detection Setup

Cost Anomaly Detection was enabled on the account following the July 2026 incident.

| Setting | Value |
|---------|-------|
| Monitor Name | AccountSpendMonitor |
| Monitor Type | DIMENSIONAL (per service) |
| Monitor ARN | `arn:aws:ce::[AWS-ACCOUNT-ID-REDACTED]:anomalymonitor/[MONITOR-ID-REDACTED]` |
| Alert Threshold | $10 |
| Frequency | DAILY |
| Subscriber | [EMAIL-REDACTED] |

---

## 8. Billing Alarm Reference

### Free Services (No Charge)
- AWS Organizations — free
- AWS IAM — free
- AWS CloudTrail (first trail) — free
- AWS Config (first rules) — nearly free
- VPCs — free (public IPv4 addresses are NOT free as of Feb 2024)

### Common Cost Traps to Avoid

| Service | Trap | Cost |
|---------|------|------|
| NAT Gateway | Runs 24/7 even with no traffic | $0.045/hr = $32/month |
| Elastic IP | Idle (unassociated) address | $0.005/hr = $3.60/month |
| EC2 (stopped) | EBS volume still bills | $0.08/GB/month |
| Secrets Manager | Per secret per month | $0.40/secret/month |
| Route 53 | Per hosted zone | $0.50/zone/month |
| RDS (stopped) | Stops for 7 days then auto-restarts | $0.00 → resumes billing |
| ECR | Image storage | $0.10/GB/month |
| S3 | Requests + storage | Varies |

---

## 9. AWS Support Dispute Template

Use this template when filing a billing dispute:

```
Subject: Request for billing adjustment — accidental charges from team project

I am a cloud engineering student using AWS Free Tier for personal
learning projects. During a shared team microservices project, several
resources were left running continuously without my knowledge, resulting
in unexpected charges.

I have since:
- Deleted all 3 unused Route 53 hosted zones
- Deleted 2 unused Secrets Manager secrets
- Verified no unused EC2 instances are running
- Confirmed no idle Elastic IPs exist
- Deleted all unused EBS volumes
- Enabled Cost Anomaly Detection with a $10 alert threshold

This is my first billing incident on this account. I am requesting a
one-time courtesy credit for the charges incurred.

Account ID: [AWS-ACCOUNT-ID-REDACTED]
Disputed period: June 2026
Disputed amount: ~$23.04
```

---

## 10. Approved Running Resources

The following resources are intentionally kept and their costs accepted:

| Resource | ID | Purpose | Monthly Cost |
|----------|----|---------|-------------|
| CTF Lab Instance (stopped) | `[INSTANCE-ID-REDACTED]` | Linux hands-on training | $0 compute (stopped) |
| CTF Lab EBS Volume (8GB gp2) | `[VOLUME-ID-REDACTED]` | CTF Lab root volume | ~$0.64 |
| **Total approved spend** | | | **~$0.64/month** |

> Any resource not listed above should be investigated and terminated.

---

## 11. Monthly Cost Target

| Threshold | Action |
|-----------|--------|
| < $1 | ✅ On target — CTF Lab EBS only |
| $1 — $10 | ⚠️ Investigate — something may have been left running |
| > $10 | 🚨 Cost anomaly alert fires — immediate investigation required |

```bash
# Check current month spend at any time
aws ce get-cost-and-usage \
  --time-period Start=2026-07-01,End=2026-07-31 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --query 'ResultsByTime[*].Total.BlendedCost' \
  --profile cloud-eng-iac \
  --region us-east-1
```

---

# AWS Cost Optimization & Billing Runbook
**Account:** cloud-sec101 (`[AWS-ACCOUNT-ID-REDACTED]`)  
**Owner:** Derek O.  
**Email:** [EMAIL-REDACTED]  
**Last Updated:** July 7, 2026  

---

## Table of Contents

1. [Incident Summary](#1-incident-summary)
2. [Root Cause Analysis](#2-root-cause-analysis)
3. [Complete Billing Breakdown](#3-complete-billing-breakdown)
4. [Full Cleanup Actions Taken](#4-full-cleanup-actions-taken)
5. [Troubleshooting Log](#5-troubleshooting-log)
6. [Preventive Controls](#6-preventive-controls)
7. [Daily Session Checklist](#7-daily-session-checklist)
8. [Cost Anomaly Detection Setup](#8-cost-anomaly-detection-setup)
9. [AWS Support Dispute — Full Timeline](#9-aws-support-dispute--full-timeline)
10. [Approved Running Resources](#10-approved-running-resources)
11. [Monthly Cost Target](#11-monthly-cost-target)
12. [Key Lessons Learned](#12-key-lessons-learned)

---

## 1. Incident Summary

| Field | Detail |
|-------|--------|
| **Date Detected** | July 6, 2026 |
| **Account Blocked** | Yes — outstanding balance blocked root password recovery on all member accounts |
| **Initial Estimated Charge** | ~$23.04 (June 2026 only — incomplete view) |
| **Actual Total Outstanding** | $223.31 across April–July 2026 |
| **Root Cause** | Team microservices project left EKS cluster, RDS, NAT Gateway, EC2, and supporting resources running across multiple months |
| **Primary Month** | May 2026 — $222.35 (EKS cluster alone: $153.65) |
| **Payment Made** | $23.04 paid on July 7, 2026 |
| **Remaining Balance** | ~$200.27 — AWS Support credit request filed |
| **Resolution Status** | Pending AWS Support credit approval (Case: [AWS-CASE-ID-REDACTED]) |
| **Account Status After Cleanup** | Clean — ~$0.64/month ongoing (CTF Lab EBS only) |

---

## 2. Root Cause Analysis

### Primary Cause
A shared team project deploying a **petclinic microservices application** on AWS left the following resources running continuously across April, May, and June 2026 without a shutdown plan:

| Resource | Impact |
|----------|--------|
| **EKS Cluster** | $153.65 in May alone ($0.10/hr control plane + worker nodes) |
| **RDS Database** | $10.84 in April, $7.18 in May |
| **NAT Gateway** | ~$32/month when running continuously |
| **Application Load Balancer** | $7.95 in May |
| **Multiple EC2 instances** | Running across April–June |
| **Elastic IPs** | Idle IPs charged at $0.005/hr each |
| **EBS Volumes** | petclinic PVCs in us-east-2 (2x 10GB) |
| **EBS Snapshots** | AMI-backed snapshots in us-east-1 (2x 8GB) |
| **CloudWatch** | $4.91 in May from EKS logging |
| **ECR** | Container image storage |
| **Secrets Manager** | Team project secrets not cleaned up |
| **Route 53** | 3 hosted zones not deleted |

### Contributing Factors
- No billing alerts configured on the account
- No SCP blocking expensive services in Workloads OU
- No team agreement on resource cleanup after project completion
- AWS Free Tier limits not monitored
- Resources spread across multiple regions (us-east-1, us-east-2) making discovery harder
- AMI-backed snapshots not visible without `--owner-ids self` flag
- EKS charges not immediately obvious — control plane fee is separate from worker node EC2 costs

### Why the Initial Estimate Was Wrong
AWS Support's first response showed only ~$5.04 for July 1–6. This was a **partial view** of current period charges only. The full outstanding balance of $223.31 included unpaid charges from April, May, and June that had been accumulating.

---

## 3. Complete Billing Breakdown

### Monthly Breakdown by Service

| Service | Apr 2026 | May 2026 | Jun 2026 | Jul 2026 | **Total** |
|---------|----------|----------|----------|----------|-----------|
| **Amazon EKS** | $0 | **$153.65** | $0 | $0 | **$153.65** |
| EC2 - Other (NAT GW/EBS/Transfer) | $12.50 | $21.70 | $4.94 | $0.84 | **$39.98** |
| Amazon EC2 Compute | $7.46 | $13.69 | $8.36 | $1.54 | **$31.05** |
| Amazon VPC (NAT GW + Elastic IPs) | $7.41 | $10.78 | $7.21 | $1.35 | **$26.75** |
| Amazon RDS | $10.84 | $7.18 | $0.08 | $0.01 | **$18.11** |
| Elastic Load Balancing | $0 | $7.95 | $0 | $0 | **$7.95** |
| Amazon Route 53 | $0 | $2.51 | $1.51 | $1.50 | **$5.52** |
| AmazonCloudWatch | $0 | $4.91 | $0 | $0 | **$4.91** |
| AWS Secrets Manager | $0.40 | $0.79 | $0.80 | $0.15 | **$2.14** |
| Amazon ECR | $0 | $0.14 | $0.14 | $0.03 | **$0.31** |
| S3 / DynamoDB / Other | ~$0 | ~$0 | ~$0 | ~$0 | **~$0** |
| **Monthly Total** | **$38.61** | **$222.35** | **$23.04** | **$5.47** | **~$289.47** |

> **Note:** $223.31 outstanding = total accumulated minus partial payments.
> $23.04 paid on July 7, 2026. Remaining: ~$200.27 (pending credit).

### Key Cost Driver — EKS in May 2026

EKS is the single largest charge at **$153.65 in one month**. Breakdown:
- EKS control plane: $0.10/hr × 744hrs = **$74.40**
- Worker node EC2 instances: included in EC2 Compute charges
- NAT Gateway for pod traffic: included in VPC charges
- CloudWatch Container Insights logging: $4.91
- Load Balancer for ingress: $7.95

---

## 4. Full Cleanup Actions Taken

### 4.1 Route 53 — Deleted All 3 Hosted Zones

**Issue encountered:** `HostedZoneNotEmpty` error — zones contained DNS records that had to be deleted first.

**Solution:** Delete all non-NS/SOA records before deleting the zone.

```bash
# List hosted zones
aws route53 list-hosted-zones \
  --query 'HostedZones[*].{ID:Id,Name:Name}' \
  --output table \
  --profile cloud-eng-iac

# Delete all non-NS/SOA records using Python
python3 << 'PYEOF'
import boto3

session = boto3.Session(profile_name='cloud-eng-iac')
client = session.client('route53')

ZONE_ID = 'YOUR_ZONE_ID'

response = client.list_resource_record_sets(HostedZoneId=ZONE_ID)
records = response['ResourceRecordSets']
deletable = [r for r in records if r['Type'] not in ['NS', 'SOA']]

if deletable:
    changes = [{"Action": "DELETE", "ResourceRecordSet": r} for r in deletable]
    client.change_resource_record_sets(
        HostedZoneId=ZONE_ID,
        ChangeBatch={"Changes": changes}
    )
    print(f"Deleted {len(deletable)} records")
else:
    print("No deletable records — zone ready to delete")
PYEOF

# Delete the zone
aws route53 delete-hosted-zone \
  --id ZONE_ID \
  --profile cloud-eng-iac
```

**Result:** All 3 zones deleted. $1.50/month saved.

---

### 4.2 Secrets Manager — Deleted 2 Team Project Secrets

```bash
aws secretsmanager delete-secret \
  --secret-id arn:aws:secretsmanager:us-east-1:[AWS-ACCOUNT-ID-REDACTED]:secret:[SECRET-NAME-REDACTED] \
  --force-delete-without-recovery \
  --profile cloud-eng-iac \
  --region us-east-1

aws secretsmanager delete-secret \
  --secret-id arn:aws:secretsmanager:us-east-1:[AWS-ACCOUNT-ID-REDACTED]:secret:[SECRET-NAME-REDACTED] \
  --force-delete-without-recovery \
  --profile cloud-eng-iac \
  --region us-east-1
```

**Result:** Both secrets deleted. $0.40/month saved.

---

### 4.3 RDS Snapshot — Deleted Team Project Snapshot

```bash
aws rds delete-db-snapshot \
  --db-snapshot-identifier spc-staging-ue1-rds-db-snapshot \
  --profile cloud-eng-iac \
  --region us-east-1
```

**Result:** 30GB RDS snapshot deleted.

---

### 4.4 EBS Snapshots — Deregistered AMIs First (us-east-1)

**Issue encountered:** `InvalidSnapshot.InUse` error — snapshots were backing AMIs and could not be deleted directly.

**Root Cause:** Two AMIs created from EC2 instances during the team project still existed, locking the snapshots.

**Solution:** Deregister the AMIs first, then delete the snapshots.

```bash
# Step 1 — Deregister both AMIs
aws ec2 deregister-image \
  --image-id [AMI-ID-REDACTED] \
  --profile cloud-eng-iac \
  --region us-east-1

aws ec2 deregister-image \
  --image-id [AMI-ID-REDACTED] \
  --profile cloud-eng-iac \
  --region us-east-1

# Step 2 — Delete the now-unlocked snapshots
aws ec2 delete-snapshot \
  --snapshot-id [SNAPSHOT-ID-REDACTED] \
  --profile cloud-eng-iac \
  --region us-east-1

aws ec2 delete-snapshot \
  --snapshot-id [SNAPSHOT-ID-REDACTED] \
  --profile cloud-eng-iac \
  --region us-east-1
```

**Result:** Both AMIs deregistered, both snapshots deleted.

---

### 4.5 EBS Volumes — Deleted petclinic PVCs (us-east-2)

**Discovery:** AWS Support identified an additional EBS volume in us-east-2 not
found in initial cleanup because the scan was limited to us-east-1.

**Lesson:** Always scan all regions, not just us-east-1.

```bash
aws ec2 delete-volume \
  --volume-id [VOLUME-ID-REDACTED] \
  --profile cloud-eng-iac \
  --region us-east-2

aws ec2 delete-volume \
  --volume-id [VOLUME-ID-REDACTED] \
  --profile cloud-eng-iac \
  --region us-east-2
```

**Result:** Both 10GB petclinic Kubernetes PVC volumes deleted.

---

### 4.6 EC2 — CTF Lab Retained (Intentional)

| Instance | ID | Decision |
|----------|----|----------|
| CTF Lab Instance | `[INSTANCE-ID-REDACTED]` | ✅ Kept — active Linux training |

CTF Lab is stopped (not running) — only the attached 8GB EBS volume
incurs charges at ~$0.64/month.

---

### 4.7 Final Multi-Region Verification

```bash
# Scan all regions for remaining volumes
for region in us-east-1 us-east-2 us-west-1 us-west-2 eu-west-1; do
  echo "=== $region ==="
  aws ec2 describe-volumes \
    --filters "Name=status,Values=available" \
    --profile cloud-eng-iac \
    --region $region \
    --query 'Volumes[*].{ID:VolumeId,Size:Size,State:State}' \
    --output table
done

# Scan all regions for snapshots
for region in us-east-1 us-east-2 us-west-1 us-west-2 eu-west-1; do
  echo "=== $region ==="
  aws ec2 describe-snapshots \
    --owner-ids self \
    --profile cloud-eng-iac \
    --region $region \
    --query 'Snapshots[*].{ID:SnapshotId,Size:VolumeSize}' \
    --output table
done
```

**Result:** All blank — confirmed clean across all regions.

---

## 5. Troubleshooting Log

### Error 1 — AccessDeniedException on list-accounts

```
Error: An error occurred (AccessDeniedException) when calling the
ListAccounts operation: You don't have permissions to access this resource.
```

**Cause:** CLI was using wrong profile or an IAM user without Organizations permissions.

**Fix:**
```bash
# Verify correct profile is being used
aws sts get-caller-identity --profile cloud-eng-iac
aws organizations list-accounts --profile cloud-eng-iac
```

---

### Error 2 — ConstraintViolationException on leave-organization

```
Error: ConstraintViolationException: The member account is missing one or
more prerequisites — MEMBER_ACCOUNT_PAYMENT_INSTRUMENT_REQUIRED
```

**Cause:** Member accounts created via Organizations never had standalone
billing set up. AWS requires a payment method before allowing
`leave-organization`.

**Fix:** Skip `leave-organization` entirely. Use `close-account` directly
from the Management account — different API call, no payment method required.

```bash
aws organizations close-account \
  --account-id ACCOUNT_ID \
  --profile cloud-eng-iac
```

---

### Error 3 — Password Recovery Disabled on Member Accounts

```
Password recovery failed
Password recovery is disabled for your AWS account.
```

**Cause:** Outstanding bill caused AWS to block root password recovery
on all member accounts at the platform level.

**Fix:** Resolve the outstanding balance first. Use Switch Role
(`OrganizationAccountAccessRole`) to access member accounts without
root password in the meantime.

```
Console → Management Account → Switch Role
Account ID:    MEMBER_ACCOUNT_ID
Role Name:     OrganizationAccountAccessRole
```

---

### Error 4 — HostedZoneNotEmpty on delete-hosted-zone

```
Error: HostedZoneNotEmpty: The specified hosted zone contains
non-required resource record sets and so cannot be deleted.
```

**Cause:** DNS records inside the zone must be deleted before the
zone itself can be removed. NS and SOA records are required and
cannot be deleted — all others must be removed first.

**Fix:** Use the Python script in Section 4.1 to delete all
deletable records, then delete the zone.

---

### Error 5 — InvalidSnapshot.InUse on delete-snapshot

```
Error: InvalidSnapshot.InUse: The snapshot snap-XXXXXXXXX is
currently in use by ami-XXXXXXXXX
```

**Cause:** Snapshots were created as part of AMI (machine image)
creation. The AMI holds a lock on the snapshot until the AMI
is deregistered.

**Fix:** Deregister the AMI first, then delete the snapshot.

```bash
aws ec2 deregister-image --image-id ami-XXXXXXXXX --profile cloud-eng-iac --region us-east-1
aws ec2 delete-snapshot --snapshot-id snap-XXXXXXXXX --profile cloud-eng-iac --region us-east-1
```

---

### Error 6 — ValidationException on create-anomaly-subscription

```
Error: ValidationException: Immediate frequencies only support
SNSTopic subscriptions
```

**Cause:** `IMMEDIATE` frequency for Cost Anomaly Detection only
works with SNS topics, not direct email subscribers.

**Fix:** Use `DAILY` or `WEEKLY` for email subscriptions.

```bash
# Correct — use DAILY for email
"Frequency": "DAILY"

# Only valid with SNS ARN as subscriber
"Frequency": "IMMEDIATE"
```

---

### Error 7 — Unknown options on describe-db-snapshots

```
Error: Unknown options: --owner-type, self
```

**Cause:** `--owner-type` is not a valid flag for `describe-db-snapshots`.

**Fix:** Use `--snapshot-type manual` instead.

```bash
aws rds describe-db-snapshots \
  --snapshot-type manual \
  --profile cloud-eng-iac \
  --region us-east-1
```

---

### Error 8 — ValidationError on DeleteStackInstances (account-level)

```
Error: ValidationError: StackSets with SERVICE_MANAGED permission
model can only have OrganizationalUnit as target
```

**Cause:** Control Tower uses SERVICE_MANAGED StackSets which operate
at the OU level, not individual account level. Cannot target
specific accounts directly.

**Fix:** Target the OU ID instead of the account ID.

```bash
aws cloudformation delete-stack-instances \
  --stack-set-name AWSControlTowerExecutionRole \
  --deployment-targets OrganizationalUnitIds=ou-9skp-tbjk46xu \
  --regions us-east-1 \
  --no-retain-stacks \
  --profile cloud-eng-iac \
  --region us-east-1
```

---

### Error 9 — Control Tower AWSControlTowerExecution Role Failure

```
Error: AWS Control Tower cannot create the required role
AWSControlTowerExecution because some stack instances of the stack
set AWSControlTowerExecutionRole could not be deployed.
```

**Cause:** Suspended accounts in the Workloads OU caused CloudFormation
StackSet deployment to fail. Suspended accounts reject all
CloudFormation operations with `OptInRequired` (403).

**Fix:**
1. Identify failed stack instances
2. Delete stack instances targeting the affected OU
3. Ensure all active member accounts have accepted AWS terms
4. Retry Control Tower setup

```bash
# Identify failed instances
aws cloudformation list-stack-instances \
  --stack-set-name AWSControlTowerExecutionRole \
  --profile cloud-eng-iac \
  --region us-east-1 \
  --query 'Summaries[*].{Account:Account,Status:Status,Reason:StatusReason}' \
  --output table

# Delete failed instances by OU
aws cloudformation delete-stack-instances \
  --stack-set-name AWSControlTowerExecutionRole \
  --deployment-targets OrganizationalUnitIds=ou-9skp-tbjk46xu \
  --regions us-east-1 \
  --no-retain-stacks \
  --profile cloud-eng-iac \
  --region us-east-1
```

---

## 6. Preventive Controls

### SCP — Deny Expensive Services in Workloads OU

Save as `/scps/deny-expensive-services.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyExpensiveEC2",
      "Effect": "Deny",
      "Action": "ec2:RunInstances",
      "Resource": "arn:aws:ec2:*:*:instance/*",
      "Condition": {
        "StringNotLike": {
          "ec2:InstanceType": ["t2.*", "t3.*", "t3a.*"]
        }
      }
    },
    {
      "Sid": "DenyNATGateway",
      "Effect": "Deny",
      "Action": "ec2:CreateNatGateway",
      "Resource": "*"
    },
    {
      "Sid": "DenyEKS",
      "Effect": "Deny",
      "Action": "eks:CreateCluster",
      "Resource": "*"
    },
    {
      "Sid": "DenyRDS",
      "Effect": "Deny",
      "Action": "rds:CreateDBInstance",
      "Resource": "*"
    },
    {
      "Sid": "DenyNonApprovedRegions",
      "Effect": "Deny",
      "NotAction": [
        "iam:*", "organizations:*", "account:*",
        "sts:*", "support:*", "route53:*"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": ["us-east-1", "us-west-2"]
        }
      }
    }
  ]
}
```

```bash
# Create and attach SCP
aws organizations create-policy \
  --name "DenyExpensiveServices" \
  --description "Blocks EKS, RDS, NAT Gateways, expensive EC2, non-approved regions" \
  --type SERVICE_CONTROL_POLICY \
  --content file://scps/deny-expensive-services.json \
  --profile cloud-eng-iac

# Attach to Workloads OU
aws organizations attach-policy \
  --policy-id POLICY_ID \
  --target-id ou-9skp-tbjk46xu \
  --profile cloud-eng-iac
```

---

### Cost Anomaly Detection

```bash
# Create monitor
aws ce create-anomaly-monitor \
  --anomaly-monitor '{
    "MonitorName": "AccountSpendMonitor",
    "MonitorType": "DIMENSIONAL",
    "MonitorDimension": "SERVICE"
  }' \
  --profile cloud-eng-iac \
  --region us-east-1

# Create daily email alert at $10 threshold
# Note: DAILY required for EMAIL — IMMEDIATE only works with SNS
aws ce create-anomaly-subscription \
  --anomaly-subscription '{
    "SubscriptionName": "SpendAlert10",
    "MonitorArnList": ["arn:aws:ce::[AWS-ACCOUNT-ID-REDACTED]:anomalymonitor/[MONITOR-ID-REDACTED]"],
    "Subscribers": [{
      "Address": "[EMAIL-REDACTED]",
      "Type": "EMAIL"
    }],
    "Threshold": 10,
    "Frequency": "DAILY"
  }' \
  --profile cloud-eng-iac \
  --region us-east-1
```

---

## 7. Daily Session Checklist

Run before closing your laptop every session:

```bash
# Check for running instances across primary regions
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[*].Instances[*].{ID:InstanceId,Name:Tags[?Key==`Name`].Value|[0],Type:InstanceType}' \
  --output table \
  --profile cloud-eng-iac \
  --region us-east-1
```

| Output | Meaning | Action |
|--------|---------|--------|
| Blank | Nothing running | ✅ Safe to close |
| CTF Lab only | Expected if started | Stop it when done |
| Any other instance | Unexpected | ⚠️ Investigate and terminate |

### Stop CTF Lab When Not in Use

```bash
# Stop
aws ec2 stop-instances \
  --instance-ids [INSTANCE-ID-REDACTED] \
  --profile cloud-eng-iac \
  --region us-east-1

# Start
aws ec2 start-instances \
  --instance-ids [INSTANCE-ID-REDACTED] \
  --profile cloud-eng-iac \
  --region us-east-1
```

---

## 8. Cost Anomaly Detection Setup

| Setting | Value |
|---------|-------|
| Monitor Name | AccountSpendMonitor |
| Monitor ARN | `arn:aws:ce::[AWS-ACCOUNT-ID-REDACTED]:anomalymonitor/[MONITOR-ID-REDACTED]` |
| Alert Threshold | $10 |
| Frequency | DAILY (EMAIL requirement) |
| Subscriber | [EMAIL-REDACTED] |
| Status | ✅ Active |

---

## 9. AWS Support Dispute — Full Timeline

### Case Details

| Field | Value |
|-------|-------|
| Case ID | [AWS-CASE-ID-REDACTED] |
| Created | July 6, 2026 18:34:45 |
| Subject | Request for billing adjustment — accidental ECR charges from team project |
| Status | Pending Customer Action → Awaiting credit decision |

### Timeline of Events

| Date | Action |
|------|--------|
| July 6 | Billing case filed — initial estimate ~$23.04 |
| July 7 | Full cost analysis run — actual balance $223.31 |
| July 7 | Deleted Route 53 zones, Secrets Manager secrets |
| July 7 | Discovered and deleted RDS snapshot |
| July 7 | Deregistered AMIs and deleted locked EBS snapshots |
| July 7 | Deleted petclinic EBS volumes in us-east-2 |
| July 7 | Paid $23.04 toward balance |
| July 7 | Updated support case with full cleanup confirmation |
| July 7 | Case set to Pending Customer Action by AWS |

### Final Support Case Reply Sent

```
I have completed all requested cleanup actions and performed
a full sweep across all regions.

COMPLETED ACTIONS:

us-east-1:
✅ EBS Snapshots — deregistered backing AMIs first,
   then deleted both snapshots:
   - [AMI-ID-REDACTED] + [SNAPSHOT-ID-REDACTED] (8GB)
   - [AMI-ID-REDACTED] + [SNAPSHOT-ID-REDACTED] (8GB)

us-east-2:
✅ EBS Volumes — deleted both available petclinic
   team project volumes:
   - [VOLUME-ID-REDACTED] (10GB) — petclinic-dev PVC
   - [VOLUME-ID-REDACTED] (10GB) — petclinic-dev PVC
✅ EBS Snapshots — none found in us-east-2

FULL ACCOUNT STATE — July 7, 2026:
• 1 stopped EC2 t3.micro — CTF Lab (intentional)
• 1 EBS volume 8GB gp2 — CTF Lab root volume (~$0.64/month)
• 0 snapshots across all regions
• 0 AMIs across all regions
• 0 NAT Gateways
• 0 Elastic IPs
• 0 RDS instances or snapshots
• 0 EKS clusters
• 0 Load Balancers
• 0 Route 53 hosted zones
• 0 Secrets Manager secrets

Outstanding balance: ~$200.27 (after $23.04 payment)
Account ID: [AWS-ACCOUNT-ID-REDACTED]
Case ID: [AWS-CASE-ID-REDACTED]
```

---

## 10. Approved Running Resources

| Resource | ID | Purpose | Monthly Cost |
|----------|----|---------|-------------|
| CTF Lab EC2 t3.micro (stopped) | `[INSTANCE-ID-REDACTED]` | Linux hands-on training | $0 compute |
| CTF Lab EBS Volume 8GB gp2 | `[VOLUME-ID-REDACTED]` | CTF Lab root volume | ~$0.64 |
| **Total approved spend** | | | **~$0.64/month** |

> Any resource not listed above should be investigated and terminated immediately.

---

## 11. Monthly Cost Target

| Threshold | Status | Action Required |
|-----------|--------|----------------|
| < $1 | ✅ On target | CTF Lab EBS only — expected |
| $1 – $10 | ⚠️ Investigate | Something may be running unexpectedly |
| > $10 | 🚨 Alert fires | Immediate investigation — check all regions |

```bash
# Check current month spend at any time
aws ce get-cost-and-usage \
  --time-period Start=2026-07-01,End=2026-07-31 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=DIMENSION,Key=SERVICE \
  --profile cloud-eng-iac \
  --region us-east-1 \
  --query 'ResultsByTime[*].Groups[?Metrics.BlendedCost.Amount>`"0.01"`].{Service:Keys[0],Cost:Metrics.BlendedCost.Amount}' \
  --output table
```

---

## 12. Key Lessons Learned

### Before Starting Any Project

```
[ ] Set a $10 billing alarm BEFORE creating any resources
[ ] Enable Cost Anomaly Detection
[ ] Define a resource cleanup plan with the team
[ ] Designate one person as resource owner responsible for teardown
[ ] Apply SCPs blocking EKS, RDS, NAT Gateway in non-production OUs
```

### Common AWS Cost Traps

| Service | Trap | Monthly Cost |
|---------|------|-------------|
| **EKS Cluster** | Control plane fee even with no workloads | $72/month |
| **NAT Gateway** | Runs 24/7 even with zero traffic | $32/month |
| **RDS Instance** | Stopped instances auto-restart after 7 days | $20–100/month |
| **Elastic IP** | Idle (unassociated) address | $3.60/month |
| **ALB** | Hourly charge even with no traffic | $16/month |
| **EC2 (stopped)** | EBS volume still bills when instance is stopped | $0.08/GB/month |
| **Secrets Manager** | Per secret per month | $0.40/secret/month |
| **Route 53** | Per hosted zone per month | $0.50/zone/month |
| **EBS Snapshots** | Storage charge until explicitly deleted | $0.05/GB/month |
| **AMI-backed Snapshots** | Cannot delete without deregistering AMI first | $0.05/GB/month |

### Multi-Region Gotcha
Resources can exist in **any region** — always scan beyond us-east-1.
The team project left petclinic PVC volumes in **us-east-2** that were
missed in the initial cleanup and only discovered via AWS Support review.

```bash
# Always run multi-region scan during cleanup
for region in us-east-1 us-east-2 us-west-1 us-west-2 eu-west-1; do
  echo "=== Checking $region ==="
  aws ec2 describe-instances \
    --filters "Name=instance-state-name,Values=running" \
    --profile cloud-eng-iac --region $region \
    --query 'Reservations[*].Instances[*].{ID:InstanceId,Type:InstanceType}' \
    --output table
  aws ec2 describe-volumes \
    --filters "Name=status,Values=available" \
    --profile cloud-eng-iac --region $region \
    --query 'Volumes[*].{ID:VolumeId,Size:Size}' --output table
  aws ec2 describe-snapshots \
    --owner-ids self \
    --profile cloud-eng-iac --region $region \
    --query 'Snapshots[*].{ID:SnapshotId,Size:VolumeSize}' --output table
done
```

---

*Document maintained in: `aws-landing-zone/docs/cost-optimization.md`*  
*Case reference: [AWS-CASE-ID-REDACTED]*  
*Last action: Full cleanup confirmed July 7, 2026 — awaiting AWS credit decision*
