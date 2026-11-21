# Rebuilding in Public: A 30-Day Cloud Engineer Lab, Days 1 to 4

Published on Medium, November 21, 2026: https://medium.com/@dowusubekoe/rebuilding-in-public-a-30-day-cloud-engineer-lab-days-1-to-4-a0dedb2cd20e

Copied from the live Medium post on November 21, 2026 (read at 9:47 AM EST, after the author's post-publish edits). The original draft is kept in 00-blog-repository/02-drafts/.

---

Four days, one three-tier AWS architecture, and a rule that matters more than the build: if it is not verified live, it does not count.

[IMAGE: cover image, no caption]

## Day 1: IAM, with a ceiling as well as a policy

Day 1 hardened the account first: MFA on the root user, a named admin profile for daily work, and a $10 monthly budget with an alert at 80 percent, set before anything billable was built.

The core work was a least-privilege policy written by hand, app-data-access. It allows reading and writing objects in one S3 bucket, under one prefix only, app/, and listing that bucket only within that prefix. Nothing else.

Two templates complete the day, and the distinction is the point. A permission boundary is a ceiling for one user or role: it grants nothing, and a principal can never exceed it, even if a broader policy is attached by mistake. An SCP is a ceiling for every account in an organization, and the right place to deny actions nobody should ever take, such as stopping CloudTrail or turning off encryption.

[IMAGE: The app-data-access policy document. Object access scoped to one bucket and one prefix.]

## Day 2: A VPC where the data tier has no way in

Day 2 built lab-vpc, 10.20.0.0/16 in us-east-1, with six subnets across two availability zones: public, app, and data tiers, each in both zones. Flow logs capture all traffic to CloudWatch, verified ACTIVE.

Only the public tier has a route to the internet gateway. The app tier accepts 443 only from the public tier security group. The data tier accepts database traffic, ports 5432 and 3306, only from the app tier security group. The rules reference groups, not IP addresses, so they stay correct when instances are replaced or scaled. Nothing on the internet can initiate a connection to the app or data tiers.

One tradeoff is documented rather than hidden. The lab uses a single NAT gateway, about $32 a month at full rate, instead of one per zone at double the cost. The accepted risk is precise: if us-east-1a fails, private subnets in us-east-1b lose internet egress too. For a training build on a $10 budget, that is the right call. In production, I would pay for one per zone. Naming the failure you accepted, and what it costs to remove it, is the work.

[IMAGE: The data tier security group. Database ports accepted only from the app tier group.]

## Day 3: Compute with no keys on the box

Day 3 put compute behind an application load balancer, w1-alb. An Auto Scaling group, app-asg, runs two instances across the two app subnets, minimum 2, maximum 4, with target tracking at 50 percent average CPU. Both targets were verified healthy, one in each zone.

Two decisions carry the day. The instances get their AWS permissions from an IAM role, ec2-app-role, through an instance profile. There are no access keys stored on any server, and the console evidence shows the role attached and no key pair on the instances. And there is no SSH rule at all. Administration uses AWS Systems Manager Session Manager, which works through the role. If you can administer a server without opening a port, do that.

The day states its own simplification honestly. The lab load balancer listens on HTTP because a training build has no domain or TLS certificate. In production it would use a certificate, listen on 443, redirect 80 to 443, and the port 80 rules would come off.

[IMAGE: Both app targets healthy behind w1-alb, one per availability zone. This is the Day 3 test result.]

## Day 4: A database failover, timed

Day 4 placed PostgreSQL in the data tier only. The primary, app-db, ran PostgreSQL 15.19 on a db.t3.micro, Multi-AZ, storage encrypted, no public access, automated backups retained for 7 days. A read replica, app-db-rr, sat alongside it.

The day’s notes make a distinction many designs get wrong. A read replica is not a backup, and it is not automatic failover. Multi-AZ is the failover mechanism. Backups are the recovery mechanism. A replica is for read scaling and can be promoted by hand. Three tools, three different jobs.

Then both mechanisms were tested, not assumed. A forced Multi-AZ failover started at 08:00:49 EST and completed at 08:01:39 EST, about 50 seconds, taken from the RDS events and verified on November 17. A snapshot restore test followed: the snapshot was restored as a test instance, reached available in about 7 minutes, and was then deleted.

The cost decision closed the day. Multi-AZ plus a replica ran about $1.30 a day against a $10 monthly budget, so once the tests were recorded, the primary and replica were deleted and verified gone, with zero RDS instances remaining. The manual snapshot stays, at pennies, as both the proof and a recovery point. A drill is not a deployment, and it should not bill like one.

## What is still open, stated honestly

Day 5, the security stack, is in progress, not complete. GuardDuty, AWS Config, Inspector, and Security Hub are enabled and verified on the services side, and the NAT gateway was removed on November 19, cutting the running lab to the load balancer and pennies a day. Still open: working the GuardDuty sample findings, recording the Security Hub starting score, and removing a deliberately bad security group and a throwaway public bucket created on purpose to catch. Week 4 of this series will cover Day 5 in full.

## What I would carry into production

- Set the billing alert before the first resource, not after the first surprise bill.
- Write the narrow policy first, then add the ceiling. A permission boundary turns a mistaken broad attachment into a non-event.
- Chain security groups by reference, tier to tier, and give the data tier no route in from the internet.
- Test failover and test restores, with timings. An untested backup is a hope, not a control.
- Delete drill infrastructure the day the evidence is captured, and keep only the cheap artifact that proves it happened.

## Code and full lab notes

Every command, script, note, and screenshot for Days 1 to 4 is in the public repository, organized by day:
https://github.com/dowusubekoe-dev/cloud-engineer-30-day-program

Next week: Day 2 in depth, the VPC design, why the data tier stays private, and the one NAT gateway tradeoff in full.

#AWS #Cloud Engineering #IAM #VPC #DevOps
