# Rebuilding in Public: A 30-Day Cloud Engineer Lab, Days 1 to 4 (LinkedIn post)

Published on LinkedIn, November 21, 2026: https://www.linkedin.com/posts/derekowusubekoe_aws-cloudengineering-iam-share-7529911379764633600-tAjQ
Share link: https://lnkd.in/p/gPRCWz77
Medium article: https://medium.com/@dowusubekoe/rebuilding-in-public-a-30-day-cloud-engineer-lab-days-1-to-4-a0dedb2cd20e

Copied from the live LinkedIn post on November 21, 2026 (read at 9:47 AM EST). Links appear below as LinkedIn displays them (lnkd.in wrapped). The original draft is kept in 00-blog-repository/02-drafts/.

---

I am rebuilding in public: a 30-day cloud lab, with every claim backed by code, logs, and screenshots.

Week 1, Days 1 to 4, is complete and verified. Day 5, the security stack, is in progress, not complete: GuardDuty, AWS Config, Inspector, and Security Hub are enabled and verified, the NAT gateway came out on November 19 to cut cost, and still open are the GuardDuty sample findings, the Security Hub starting score, and removing a deliberately bad security group and a throwaway public bucket I created on purpose to catch.

Day 1: a least-privilege IAM policy written by hand, scoped to one bucket and one prefix, plus a permission boundary and an SCP template. A ceiling as well as a policy.

Day 2: a three-tier VPC, 10.20.0.0/16, six subnets across two zones. The data tier accepts traffic only from the app tier, and has no route in from the internet.

Day 3: an ALB in front of an Auto Scaling group, both targets healthy, one per zone. IAM roles on the instances, no access keys on any box, and no SSH port open at all.

Day 4: PostgreSQL Multi-AZ in the private data tier. I forced a failover and timed it: about 50 seconds. Then I tested a snapshot restore, recorded about 7 minutes, and deleted the databases the same week.

That last part matters. The drill ran about $1.30 a day against a $10 monthly budget, so the evidence stays and the billable infrastructure goes.

Full write-up on Medium: https://lnkd.in/gqBvuMia

Lab notes, scripts, and screenshots on GitHub: https://lnkd.in/gJ8mthTA

Next week: Day 2 in depth, the VPC design, why the data tier stays private, and the one NAT gateway tradeoff in full.

Engineers: how do you prove failover in your own environments, timed test or trust the design?

#AWS #CloudEngineering #IAM #VPC #DevOps
