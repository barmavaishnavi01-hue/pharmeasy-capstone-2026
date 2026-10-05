# Presentation Storyline & Stakeholder Pushback Q&A

##Audience Reframing (Presentation Storyline)

### 1. Executive Reframing: Situation-Complication-Resolution (SCR)
* **Situation:** Across the April-June 2026 quarter, PharmEasy maintained a baseline performance generating ₹58,63,412.18 in revenue and ₹8,77,210.45 in net profit across 2,100 distinct verified orders.
* **Complication:** Guntur experienced an extreme, unsustained sales spike of **+122.19% Month-on-Month** in May 2026 (rising from ₹62,442.27 in April to ₹1,38,738.93 in May), before retracting by -28.11% in June (₹99,745.18). Basing future regional inventory budgets on May's peak revenue risks severe capital tie-up and over-stocking.
* **Resolution:** We recommend setting Guntur's Q2 inventory allocation against an adjusted baseline derived from its April-June average (~₹1,00,308.79) rather than May's peak. Operations leads will re-evaluate order velocity at the end of July 2026 to confirm whether demand stabilizes at steady-state levels.

---

### 2. Regional Manager Reframing: Overview-Category-Detail (OCD)
* **Overview:** Guntur recorded the highest single Month-on-Month sales surge in the network, jumping **+122.19%** between April (₹62,442.27) and May 2026 (₹1,38,738.93), totaling 190 regional orders across the quarter.
* **Category:** The surge was primarily concentrated in the **OTC Medicines** and **Prescription Medicines** product lines, which collectively drove over 60% of the net volume growth during the May peak.
* **Detail:** Data verified from `pharmeasy.db` confirms zero duplicate `order_id` values and consistent row counts across `INNER JOIN` and `LEFT JOIN` queries between `orders_clean` and `regions_master`. May's revenue increase was driven by a simultaneous rise in order count and average basket size, followed by a natural demand cooling in June (-28.11%).

---

## Anticipated Pushback Q&A

### Category 1: "Why should I believe this number?"
* **Question:** How do we know Guntur's +122.19% May spike wasn't caused by duplicate order ingestion or database join errors during pipeline execution?
* **3-Step Response:**
  1. **Direct Acknowledgement:** That is a crucial validation concern—data duplication or flawed SQL join logic frequently creates false revenue expansion spikes.
  2. **Verified vs. Unverified Status:** **Verified:** Primary key audits confirm exactly zero duplicate `order_id` records in `orders_clean`. Additionally, SQL verification checks confirm identical row counts between `LEFT JOIN` and `INNER JOIN` operations on `regions_master`, confirming zero orphaned or duplicated records in the Guntur aggregate. **Unverified:** The raw API payload logs at the upstream network gateway level have not been audited.
  3. **Resolution & Timeline:** A complete line-by-line ingestion log audit will be cross-referenced with regional warehouse dispatch manifests by July 15, 2026, to guarantee 100% physical order reconciliation.

---

### Category 2: "What if an alternative explanation is driving this?"
* **Question:** Could Guntur's May revenue jump simply be an artifact of local price inflation or product re-categorization rather than actual demand growth?
* **3-Step Response:**
  1. **Direct Acknowledgement:** That is a valid alternative hypothesis—price restructuring or category remapping can inflate top-line figures without any real change in unit volume.
  2. **Verified vs. Unverified Status:** **Verified:** The underlying order data confirms that physical item quantities ordered in Guntur increased alongside gross INR sales in May. **Unverified:** Whether temporary promotional discounts or localized price adjustments were active during May 2026 has not been verified, as promotional campaign tags are not stored in the core database schema.
  3. **Resolution & Timeline:** We will ingest the regional marketing and promotion log data from the commercial team by July 20, 2026, to isolate organic volume growth from promo-driven purchasing.
