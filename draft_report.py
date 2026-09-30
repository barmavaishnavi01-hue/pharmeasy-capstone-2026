def draft_report_v1(flagged_regions,metrics):
   report=[]
   for region in flagged_regions:
    region_metrics=metrics[region]
   april_sales=region_metrics["april_sales"]
   may_sales=region_metrics["may_sales"]
   june_sales=region_metrics["june_sales"]
   april_to_may=region_metrics["april_to_may_growth"]
   may_to_june=region_metrics["may_to_june_growth"]
   block=f"""
   Context:{region}" recorded sales of {april_sales:.2f}% in April,
          {may_sales:.2f}% in May,{june_sales:.2f}% in June 2026.

   Insight:Month-on-Month sales growth was {april_sales:.2f}% from April to May,
          {may_sales:.2f}% from May to June.

   Implication:The Month-on-Month movement for {region} is worth a human review 
               to understand the underlying order and sales changes."""
   report.append(block.strip())
   return "\n".join(report)
