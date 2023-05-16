with stock as (
	select i.id, i.name, sum(ji.qty) as qty_total, i.unit
	from journal_item ji 
	left join ingredient i on ji.ingredient_id = i.id
	group by i.id, i.name, i.unit
)

select i.id, i.name, s.qty_total, i.cost, i.unit, s.qty_total * i.cost as total_cost
from stock s
left join ingredient i on s.id = i.id;